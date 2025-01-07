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
    for i in range(len(assignments)):
        class_idx, slot, room = assignments[i]
        t = classes[class_idx][0]

        for new_slot in range(60 - t + 1):
            if new_slot != slot:
                new_assignments = assignments[:i] + [(class_idx, new_slot, room)] + assignments[i + 1:]
                if is_valid_assignment(class_idx, new_slot, room, new_assignments, classes, room_capacities):
                    neighbors.append(new_assignments)

        for new_room in range(M):
            if new_room != room:
                for new_slot in range(60 - t + 1):
                    new_assignments = assignments[:i] + [(class_idx, new_slot, new_room)] + assignments[i+1:]
                    if is_valid_assignment(class_idx, new_slot, new_room, new_assignments, classes, room_capacities):
                        neighbors.append(new_assignments)

    for class_idx in range(N):
        if class_idx not in [assignment[0] for assignment in assignments]:
            t, g, s = classes[class_idx]
            for start_slot in range(60 - t + 1):
                for room in range(M):
                    new_assignments = assignments + [(class_idx, start_slot, room)]
                    if is_valid_assignment(class_idx, start_slot, room, new_assignments, classes, room_capacities):
                        neighbors.append(new_assignments)
    return neighbors

def calculate_score(assignments):
    return len(assignments)

def local_search_run(args):
    N, M, classes, room_capacities = args
    current_solution = initialize_solution(N, M, classes, room_capacities)
    current_score = calculate_score(current_solution)

    no_improve_count = 0
    iterations = 0
    max_iterations = 300
    no_improve_limit = 100

    while no_improve_count < no_improve_limit and iterations < max_iterations:
        neighbors = generate_neighbors(current_solution, N, M, classes, room_capacities)
        if not neighbors:
            break

        best_neighbor = max(neighbors, key=calculate_score, default=None)
        if best_neighbor and calculate_score(best_neighbor) > current_score:
            current_solution = best_neighbor
            current_score = calculate_score(best_neighbor)
            no_improve_count = 0
        else:
            no_improve_count += 1
        iterations += 1

    return current_solution

def local_search(N, M, classes, room_capacities):
    num_runs = 4
    with multiprocessing.Pool(processes=num_runs) as pool:
        results = pool.map(local_search_run, [(N, M, classes, room_capacities)] * num_runs)
    return max(results, key=calculate_score)

if __name__ == "__main__":
    N, M, classes, room_capacities = read_input()
    solution = local_search(N, M, classes, room_capacities)

    print(len(solution))
    for class_idx, slot, room in solution:
        print(class_idx + 1, slot + 1, room + 1)
