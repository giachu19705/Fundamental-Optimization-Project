import random
import multiprocessing

def read_input():
    N, M = map(int, input().split())
    classes = []
    for _ in range(N):
        t, g, s = map(int, input().split())
        classes.append((t, g, s))
    room_capacities = list(map(int, input().split()))
    return N, M, classes, room_capacities

def is_valid_assignment(class_idx, slot, room, assignments, classes, room_capacities):
    t, g, s = classes[class_idx]
    if s > room_capacities[room]:
        return False
    for other_class, other_slot, other_room in assignments:
        if classes[other_class][1] == g:
            if max(slot, other_slot) < min(slot + t, other_slot + classes[other_class][0]):
                return False
        if other_room == room and max(slot, other_slot) < min(slot + t, other_slot + classes[other_class][0]):
            return False
    return True

def initialize_solution(N, M, classes, room_capacities):
    assignments = []
    assigned_slots = [([False] * M) for _ in range(60)]
    sorted_classes = sorted(range(N), key=lambda i: classes[i][0], reverse=True)
    for i in sorted_classes:
        t, g, s = classes[i]
        for start_slot in range(60 - t + 1):
            for room in range(M):
                valid = True
                for k in range(t):
                    if assigned_slots[start_slot + k][room] or not is_valid_assignment(i, start_slot + k, room, assignments, classes, room_capacities):
                        valid = False
                        break
                if valid:
                    assignments.append((i, start_slot, room))
                    for k in range(t):
                        assigned_slots[start_slot + k][room] = True
                    break
            if valid:
                break
    return assignments

def generate_neighbors(assignments, N, M, classes, room_capacities):
    neighbors = []
    n_assignments = len(assignments)
    if n_assignments < 2:
        return neighbors
    for i in range(n_assignments):
        class_idx, slot, room = assignments[i]
        t = classes[class_idx][0]

        # Di chuyển trong cùng phòng trước
        for new_slot in range(60 - t + 1):
            if new_slot != slot:
                new_assignments = assignments[:i] + [(class_idx, new_slot, room)] + assignments[i + 1:]
                if is_valid_assignment(class_idx, new_slot, room, new_assignments, classes, room_capacities):
                    neighbors.append(new_assignments)

        # Di chuyển sang phòng khác
        for new_room in range(M):
            if new_room != room:
                for new_slot in range(60 - t + 1):
                    new_assignments = assignments[:i] + [(class_idx, new_slot, new_room)] + assignments[i+1:]
                    if is_valid_assignment(class_idx, new_slot, new_room, new_assignments, classes, room_capacities):
                        neighbors.append(new_assignments)

        # Hoán đổi
        for j in range(i + 1, n_assignments):
            if classes[assignments[i][0]][1] != classes[assignments[j][0]][1]:
                new_assignments = assignments[:]
                new_assignments[i], new_assignments[j] = new_assignments[j], new_assignments[i]
                valid_i = is_valid_assignment(assignments[j][0], new_assignments[i][1], new_assignments[i][2], new_assignments, classes, room_capacities)
                valid_j = is_valid_assignment(assignments[i][0], new_assignments[j][1], new_assignments[j][2], new_assignments, classes, room_capacities)
                if valid_i and valid_j:
                    neighbors.append(new_assignments)
    return neighbors

def calculate_score(assignments):
    return len(assignments)

def local_search_run(args):
    N, M, classes, room_capacities = args
    best_solution = []
    best_score = 0
    max_iterations = 300
    no_improve_limit = 100

    current_solution = initialize_solution(N, M, classes, room_capacities)
    current_score = calculate_score(current_solution)
    no_improve_count = 0
    iterations = 0

    while no_improve_count < no_improve_limit and iterations < max_iterations:
        neighbors = generate_neighbors(current_solution, N, M, classes, room_capacities)
        if not neighbors:
            break
        k_best_neighbors = sorted(neighbors, key=calculate_score, reverse=True)[:min(5, len(neighbors))]
        best_neighbor = random.choice(k_best_neighbors) if k_best_neighbors else None
        if best_neighbor is None:
            break
        neighbor_score = calculate_score(best_neighbor)

        if neighbor_score > current_score:
            current_solution = best_neighbor
            current_score = neighbor_score
            no_improve_count = 0
        else:
            no_improve_count += 1
        iterations += 1

    if current_score > best_score:
        best_score = current_score
        best_solution = current_solution

    return best_solution

def local_search(N, M, classes, room_capacities):
    num_runs = 4  # Number of parallel runs

    with multiprocessing.Pool(processes=num_runs) as pool:
        results = pool.map(local_search_run, [(N, M, classes, room_capacities)] * num_runs)

    best_solution = max(results, key=lambda sol: calculate_score(sol))
    return best_solution

def output_solution(solution):
    print(len(solution))
    for class_idx, slot, room in solution:
        print(class_idx + 1, slot + 1, room + 1)

if __name__ == "__main__":
    N, M, classes, room_capacities = read_input()
    solution = local_search(N, M, classes, room_capacities)
    output_solution(solution)
