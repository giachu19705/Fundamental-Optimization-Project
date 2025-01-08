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
        if classes[other_class][1] == g or other_room == room:
            if max(slot, other_slot) < min(slot + t, other_slot + classes[other_class][0]):
                return False
    return True

def initialize_solution(N, M, classes, room_capacities):
    assignments = []
    assigned_slots = [([False] * M) for _ in range(60)]
    sorted_classes = sorted(range(N), key=lambda i: (classes[i][0], -classes[i][2]), reverse=True)

    for i in sorted_classes:
        t, g, s = classes[i]
        added = False
        for start_slot in range(60 - t + 1):
            for room in range(M):
                if all(not assigned_slots[start_slot + k][room] for k in range(t)):
                    if is_valid_assignment(i, start_slot, room, assignments, classes, room_capacities):
                        assignments.append((i, start_slot, room))
                        for k in range(t):
                            assigned_slots[start_slot + k][room] = True
                        added = True
                        break
            if added:
                break

    return assignments

def generate_neighbors(assignments, N, M, classes, room_capacities):
    neighbors = []
    sampled_indices = random.sample(range(len(assignments)), min(50, len(assignments)))
    
    for i in sampled_indices:
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
                    new_assignments = assignments[:i] + [(class_idx, new_slot, new_room)] + assignments[i + 1:]
                    if is_valid_assignment(class_idx, new_slot, new_room, new_assignments, classes, room_capacities):
                        neighbors.append(new_assignments)

    return random.sample(neighbors, min(10, len(neighbors)))

def attempt_to_add_unassigned_classes(current_solution, N, M, classes, room_capacities):
    unassigned_classes = set(range(N)) - set([a[0] for a in current_solution])
    assigned_slots = [([False] * M) for _ in range(60)]
    for _, slot, room in current_solution:
        assigned_slots[slot][room] = True

    for class_idx in unassigned_classes:
        t, g, s = classes[class_idx]
        for start_slot in range(60 - t + 1):
            for room in range(M):
                if all(not assigned_slots[start_slot + k][room] for k in range(t)):
                    if is_valid_assignment(class_idx, start_slot, room, current_solution, classes, room_capacities):
                        current_solution.append((class_idx, start_slot, room))
                        for k in range(t):
                            assigned_slots[start_slot + k][room] = True
                        return current_solution

    return current_solution

def calculate_score(assignments):
    return len(assignments)

def local_search_run(args):
    N, M, classes, room_capacities = args
    current_solution = initialize_solution(N, M, classes, room_capacities)
    current_score = calculate_score(current_solution)

    no_improve_count = 0
    max_iterations = 300
    no_improve_limit = 50
    iterations = 0

    while no_improve_count < no_improve_limit and iterations < max_iterations:
        neighbors = generate_neighbors(current_solution, N, M, classes, room_capacities)
        if neighbors:
            best_neighbor = max(neighbors, key=calculate_score, default=None)
            if best_neighbor and calculate_score(best_neighbor) > current_score:
                current_solution = best_neighbor
                current_score = calculate_score(best_neighbor)
                no_improve_count = 0
            else:
                no_improve_count += 1
        else:
            no_improve_count += 1
        
        current_solution = attempt_to_add_unassigned_classes(current_solution, N, M, classes, room_capacities)
        current_score = calculate_score(current_solution)
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
