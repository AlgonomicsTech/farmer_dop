def find_and_print_matching_lines(file1_path, file2_path):
    with open(file1_path, 'r') as file1, open(file2_path, 'r') as file2:
        lines_file1 = file1.readlines()
        lines_file2 = file2.readlines()

    for line1 in lines_file1:
        for line2 in lines_file2:
            if line1.strip() in line2.strip():
                print(line2.strip())

# Виклик функції
find_and_print_matching_lines('test.txt', 'ref.txt')


