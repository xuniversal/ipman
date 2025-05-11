import requests
import csv
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

def check_proxy(ip_port, api_url_template):
    ip, port = ip_port.split(':')
    api_url = api_url_template.format(ip=ip, port=port)
    try:
        response = requests.get(api_url, timeout=60)
        response.raise_for_status()
        data = response.json()

        status = data.get("proxyip", False)
        delay = data.get('delay', 'N/A')
        country = data.get('country', 'N/A')
        city = data.get('city', 'N/A')
        
        if status:
            print(f"{ip}:{port} is ALIVE | Delay: {delay}ms | Location: {country}-{city}")
            return (ip_port, True)
        else:
            print(f"{ip}:{port} is DEAD")
            return (ip_port, False)
            
    except requests.exceptions.RequestException as e:
        print(f"Error checking {ip}:{port}: {e}")
        return (ip_port, False)
    except ValueError as ve:
        print(f"Error parsing JSON for {ip}:{port}: {ve}")
        return (ip_port, False)

def main():
    input_file = os.getenv('INPUT_FILE', 'rawproxy.txt')
    alive_file = 'alive.txt'
    dead_file = 'dead.txt'
    api_url_template = os.getenv('API_URL', 'https://id1.foolvpn.me/api/v1/check?ip={ip}:{port}')

    alive_proxies = []
    dead_proxies = []

    try:
        with open(input_file, "r") as f:
            proxies = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"File {input_file} not found.")
        return

    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = [executor.submit(check_proxy, proxy, api_url_template) for proxy in proxies if ':' in proxy]

        for future in as_completed(futures):
            proxy, is_alive = future.result()
            if is_alive:
                alive_proxies.append(proxy)
            else:
                dead_proxies.append(proxy)

    # Write alive proxies
    try:
        with open(alive_file, "w") as f:
            f.write("\n".join(alive_proxies) + "\n")
        print(f"Saved {len(alive_proxies)} alive proxies to {alive_file}")
    except Exception as e:
        print(f"Error writing to {alive_file}: {e}")

    # Write dead proxies
    try:
        with open(dead_file, "w") as f:
            f.write("\n".join(dead_proxies) + "\n")
        print(f"Saved {len(dead_proxies)} dead proxies to {dead_file}")
    except Exception as e:
        print(f"Error writing to {dead_file}: {e}")

if __name__ == "__main__":
    main()
