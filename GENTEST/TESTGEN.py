import random
import os

def generate_test_case(N, M, filename):
    # Mảng để lưu số lượng sinh viên trong mỗi phòng
    c = [random.randint(10, 150) for _ in range(M)]  # Chỗ ngồi phòng từ 30 đến 300

    # Tạo thông tin cho các lớp
    t = []  # Số tiết của lớp
    g = []  # Giáo viên của lớp
    s = []  # Số sinh viên trong lớp

    for i in range(N):
        t.append(random.randint(1, 4))  # Số tiết của lớp từ 1 đến 4
        g.append(random.randint(1, 50))  # Giáo viên của lớp từ 1 đến 100
        s.append(random.randint(1, 100))  # Số sinh viên của lớp từ 1 đến 200       

    # Ghi vào file input.txt
    with open(filename, 'w') as f:

        f.write(f"{N} {M}\n")

        for i in range(N):
            f.write(f"{t[i]} {g[i]} {s[i]}\n")

        f.write(" ".join(map(str, c)) + "\n")


#main       
if not os.path.exists("./DATA"):
    os.makedirs("./DATA")
test_count=1
for n in range (10, 101, 5):
    M = random. randint(1,100)
    filename = f"./DATA/test{test_count}.txt"
    test_count+=1
    generate_test_case(n, M, filename)
for n in range (150, 301, 50):
    M = random. randint(1,100)
    filename = f"./DATA/test{test_count}.txt"
    test_count+=1
    generate_test_case(n, M, filename)
for n in range (400, 1001, 200):
    M = random. randint(1,100)
    filename = f"./DATA/test{test_count}.txt"
    test_count+=1
    generate_test_case(n, M, filename)

        
        