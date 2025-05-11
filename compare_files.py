import difflib

def compare_and_process_files(file1, file2, output_file):
    # Membaca kedua file
    with open(file1, 'r') as f1:
        lines1 = f1.readlines()
    with open(file2, 'r') as f2:
        lines2 = f2.readlines()

    # Memeriksa apakah file mengandung data
    print(f"File 1 ({file1}) contains:")
    print("".join(lines1))  # Menampilkan isi ip.txt
    print(f"File 2 ({file2}) contains:")
    print("".join(lines2))  # Menampilkan isi 2024.txt

    # Membandingkan file
    diff = difflib.unified_diff(lines1, lines2, lineterm='', fromfile=file1, tofile=file2)

    # Menyimpan hasil ke output file
    with open(output_file, 'w') as out:
        print(f"Writing differences to {output_file}")
        for line in diff:
            if line.startswith('+ ') or line.startswith('- '):
                out.write(line[2:] + "\n")  # Menulis hanya baris yang berbeda tanpa tanda "+" atau "-"
    
    print(f"Perbandingan selesai, hasil disalin ke {output_file}")

# Tentukan nama file
compare_and_process_files('ip.txt', '2024.txt', 'output.txt')
