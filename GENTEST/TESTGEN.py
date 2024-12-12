import random
import os

def generate_test_case(N, M, filename):
    # Mảng để lưu số lượng sinh viên trong mỗi phòng
    c = [random.randint(30, 300) for _ in range(M)]  # Chỗ ngồi phòng từ 30 đến 300

    # Tạo thông tin cho các lớp
    t = []  # Số tiết của lớp
    g = []  # Giáo viên của lớp
    s = []  # Số sinh viên trong lớp

    for i in range(N):
        t.append(random.randint(1, 4))  # Số tiết của lớp từ 1 đến 4
        g.append(random.randint(1, 100))  # Giáo viên của lớp từ 1 đến 100
        s.append(random.randint(1, 200))  # Số sinh viên của lớp từ 1 đến 200       

    # Ghi vào file input.txt
    with open(filename, 'w') as f:

        f.write(f"{N} {M}\n")

        for i in range(N):
            f.write(f"{t[i]} {g[i]} {s[i]}\n")
        
        # Ghi số chỗ ngồi của mỗi phòng
        f.write(" ".join(map(str, c)) + "\n")

if not os.path.exists("input_data"):
    os.makedirs("input_data")
test_count=1
for n in range (10, 101, 10):
    M = random. randint(1,n)
    filename = f"input_data/test{test_count}.txt"
    test_count+=1
    generate_test_case(n, M, filename)
for n in range (100, 1001, 100):
    M = random. randint(30,100)
    filename = f"input_data/test{test_count}.txt"
    test_count+=1
    generate_test_case(n, M, filename)


        
        