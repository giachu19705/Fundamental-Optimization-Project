import random

def generate_test_case(N, M):
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
    with open('input.txt', 'w') as f:
        # Ghi số lượng lớp và phòng học
        f.write(f"{N} {M}\n")
        
        # Ghi thông tin mỗi lớp (t(i), g(i), s(i))
        for i in range(N):
            f.write(f"{t[i]} {g[i]} {s[i]}\n")
        
        # Ghi số chỗ ngồi của mỗi phòng
        f.write(" ".join(map(str, c)) + "\n")

# Sinh test case với N lớp và M phòng
generate_test_case(100, 15)