from ortools.sat.python import cp_model
import time
def schedule_timetable(N, M, t, g, s, c):
    # Constants
    T = 60
    model = cp_model.CpModel()

    x = {}  # x[i, p, k]: 1 nếu lớp i được xếp vào phòng p bắt đầu từ tiết k
    for i in range(N):
        for p in range(M):
            for k in range(T - t[i] + 1):
                x[i, p, k] = model.NewBoolVar(f'x_{i}_{p}_{k}')

    # Constraints

    # 1. Mỗi lớp chỉ được xếp nhiều nhất 1 lần
    for i in range(N):
        model.Add(sum(x[i, p, k] for p in range(M) for k in range(T - t[i] + 1)) <= 1)

    # 2. Phòng phải đủ lớn để chứa
        for i in range(N):
            for p in range(M):
                if s[i] > c[p]:
                    for k in range(T - t[i] + 1):
                        model.Add(x[i, p, k] == 0)
    # 3. Không có hai lớp học trùng thời gian trong cùng một phòng
    for p in range(M):
        for time in range(T):
            model.Add(sum(x[i, p, k] for i in range(N) for k in range(max(0, time - t[i] + 1), min(time + 1, T - t[i] + 1))) <= 1)

    # 4. Các lớp học có cùng giáo viên không được trùng thời gian
    for teacher in set(g):
        classes = [i for i in range(N) if g[i] == teacher]
        for time in range(T):
            model.Add(sum(x[i, p, k] for i in classes for p in range(M) for k in range(max(0, time - t[i] + 1), min(time + 1, T - t[i] + 1))) <= 1 )

    # 5. Các tiết của một lớp phải nằm trong cùng một ngày & Lớp không được kéo dài qua buổi sáng hoặc chiều
    for i in range(N):
        for p in range(M):
            for k in range(T - t[i] + 1):
                day_start = (k // 12) * 12
                if k + t[i] - 1 >= day_start + 12:
                    model.Add(x[i, p, k] == 0)
                if k % 12 <= 6:  # Sáng
                    shift_end = (k // 12) * 12 + 6
                else:  # Chiều
                    shift_end = (k // 12) * 12 + 12
                if k + t[i] - 1 > shift_end:
                    model.Add(x[i, p, k] == 0)

    # Objective: Maximize the number of classes scheduled
    model.Maximize(sum(x[i, p, k] for i in range(N) for p in range(M) for k in range(T - t[i] + 1)))

    # Solve the model
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 400.0

    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        schedule = []
        for i in range(N):
            for p in range(M):
                for k in range(T - t[i] + 1):
                    if solver.BooleanValue(x[i, p, k]):
                        schedule.append([i + 1, k + 1, p + 1]) 
        print(len(schedule))
        for i in schedule:
            print (*i)
    else:
        print ("No feasible solution found.")
    print (f"Solver run time: {solver.WallTime()} seconds\n")

t=[]
g=[]
s=[]
c=[]
N, M =list(map(int, input().split()))
A=[]
for i in range (N):
    A = list(map(int,input().split()))
    t.append(A[0])
    g.append(A[1])
    s.append(A[2])
c=list(map(int,input().split()))
schedule_timetable(N, M, t, g, s, c)
