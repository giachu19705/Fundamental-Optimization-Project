from ortools.linear_solver import pywraplp
import os
def schedule_timetable_ip(N, M, t, g, s, c):
    # Constants
    T = 60
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        return "Solver not available."

    solver.SetTimeLimit(500 * 1000)
    # Variables
    x = {}  # x[i, p, k]: 1 nếu lớp i được xếp vào phòng p và bắt đầu từ tiết k
    for i in range(N):
        for p in range(M):
            for k in range(T - t[i] + 1):
                x[i, p, k] = solver.IntVar(0, 1, f'x_{i}_{p}_{k}')

    # Constraints

    # 1. Mỗi lớp chỉ được xếp nhiều nhất 1 lần
    for i in range(N):
        solver.Add(sum(x[i, p, k] for p in range(M) for k in range(T - t[i] + 1)) <= 1)

    # 2. Phòng phải đủ lớn để chứa
    for i in range(N):
        for p in range(M):
            if s[i] > c[p]:
                for k in range(T - t[i] + 1):
                    solver.Add(x[i, p, k] == 0)

    # 3. Không có hai lớp học trùng thời gian trong cùng một phòng
    for p in range(M):
        for time in range(T):
            solver.Add(sum(x[i, p, k] for i in range(N) for k in range(max(0, time - t[i] + 1), min(time + 1, T - t[i] + 1))) <= 1)

    # 4. Các lớp học có cùng giáo viên không được trùng thời gian
    for teacher in set(g):
        classes = [i for i in range(N) if g[i] == teacher]
        for time in range(T):
            solver.Add(sum(x[i, p, k] for i in classes for p in range(M) for k in range(max(0, time - t[i] + 1), min(time + 1, T - t[i] + 1))) <= 1)

    # 5. Các tiết của một lớp phải nằm trong cùng một ngày & Lớp không được kéo dài qua buổi sáng hoặc chiều
    for i in range(N):
        for p in range(M):
            for k in range(T - t[i] + 1):
                day_start = (k // 12) * 12
                if k + t[i] - 1 >= day_start + 12:
                    solver.Add(x[i, p, k] == 0)
    # Objective: 
    objective = solver.Objective()
    for i in range(N):
        for p in range(M):
            for k in range(T - t[i] + 1):
                objective.SetCoefficient(x[i, p, k], 1)
    objective.SetMaximization()

    status = solver.Solve()
    time = solver.WallTime()/1000
    # Results
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        schedule = []
        for i in range(N):
            for p in range(M):
                for k in range(T - t[i] + 1):
                    if x[i, p, k].solution_value() > 0.5:
                        schedule.append((i + 1, k + 1, p + 1))
        return schedule ,time 
    else:
        return "No feasible solution found."
    
def test_input(inputFile):
    t=[]
    g=[]
    s=[]
    c=[]
    with open(inputFile, "r") as f:
        lines = f.readlines()
        N, M = [int(x) for x in lines[0].split()]
        for i in range(1, N + 1):
            a, b, c = lines[i].split()
            t.append(int(a))
            g.append(int(b))
            s.append(int(c))
        c=list(map(int,lines[N+1].split()))
    return N,M,t,g,s,c

def solve(test_path, index):
    N,M,t,g,s,c = test_input(test_path)
    schedule, time =schedule_timetable_ip(N,M,t,g,s,c)
    if schedule == "No feasible solution found.":
        print ("No feasible solution found.")
        with open(f'./RESULT/IP/result_test{index}.txt', 'w') as f:
                f.write("No feasible solution found.")
    else:
        print (len(schedule))
        for i in schedule: print(*i)
        print(f"Solver run time: {time} seconds")
        with open(f'./RESULT/IP/result_test{index}.txt', 'w') as f:
            f.write(f"Number of classes need to be scheduled: {N}\n")
            f.write(f"Number of tasks scheduled: {len(schedule)}\n")
            f.write(f"Solver run time: {time} seconds\n") 

for i in range(1,25):
    test_path=f'./DATA/test{i}.txt'
    solve(test_path,i)
