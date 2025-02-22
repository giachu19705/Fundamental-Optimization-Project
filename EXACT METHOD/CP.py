from ortools.sat.python import cp_model
import os
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

    # Objective: Maximize the number of classes scheduled
    model.Maximize(sum(x[i, p, k] for i in range(N) for p in range(M) for k in range(T - t[i] + 1)))

    # Solve the model
    solver = cp_model.CpSolver()
    

    status = solver.Solve(model)
    solver.parameters.max_time_in_seconds = 500.0

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        schedule = []
        for i in range(N):
            for p in range(M):
                for k in range(T - t[i] + 1):
                    if solver.BooleanValue(x[i, p, k]):
                        schedule.append([i + 1, k + 1, p + 1]) 
        return schedule, solver.WallTime()
    else:
        return "No feasible solution found."
    
def test_input():
    t = []
    g = []
    s = []
    c = []
    N,M = map(int,input().split())
    for i in range (N):
        a, b, c= map(int,input().split())
        t.append(int(a))
        g.append(int(b))
        s.append(int(c))
    c=list(map(int,input().split()))
    return N,M,t,g,s,c

#main
def solve():
    N,M,t,g,s,c = test_input()
    schedule, time =schedule_timetable(N,M,t,g,s,c)
    if schedule == "No feasible solution found.":
        print ("No feasible solution found.")
    else:
        print (len(schedule))
        for i in schedule: print(*i)
        print(f"Solver run time: {time} seconds")
solve()

