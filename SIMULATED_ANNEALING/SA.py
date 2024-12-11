import sys
import random
import math

def input_data():
    [N, M] = [int(x) for x in sys.stdin.readline().split()]
    t = []
    g = []
    s = []
    for i in range(N):
        [T, G, S] = [int(x) for x in sys.stdin.readline().split()]
        t.append(T)
        g.append(G)
        s.append(S)
    c = [int(x) for x in sys.stdin.readline().split()]
    return N, M, t, g, s, c

def initial_feasible_solution(N, M, t, g, s, c):
    assignments = []
    teacher_slots = {i: [] for i in range(1, 101)}  # Teacher availability tracking
    room_slots = {i: [] for i in range(1, M + 1)}  # Room availability tracking
    
    for class_id in range(1, N + 1):
        # Filter out rooms that can accommodate the class size
        suitable_rooms = [j for j in range(1, M + 1) if c[j - 1] >= s[class_id - 1]]
        if not suitable_rooms:
            # Skip this class if no rooms are suitable
            continue

        # Try to find a slot where this class can be scheduled
        for _ in range(100):  # Attempt multiple times to find a slot
            start_slot = random.randint(1, 61 - t[class_id - 1])
            room_chosen = random.choice(suitable_rooms)

            # Check if the chosen slot and room are available
            if all(start_slot + offset not in teacher_slots[g[class_id - 1]] for offset in range(t[class_id - 1])) and \
               all(start_slot + offset not in room_slots[room_chosen] for offset in range(t[class_id - 1])):
                assignments.append((class_id, start_slot, room_chosen))
                # Mark the slots as taken for both the teacher and the room
                for offset in range(t[class_id - 1]):
                    teacher_slots[g[class_id - 1]].append(start_slot + offset)
                    room_slots[room_chosen].append(start_slot + offset)
                break

    return assignments


def cost_function(assignments):
    # The cost is the number of classes successfully scheduled
    return len(assignments)

def get_neighbor(assignments, N, M, t, g, s, c, teacher_slots, room_slots):
    if not assignments:
        return assignments

    idx = random.randint(0, len(assignments) - 1)
    class_id, slot, room = assignments[idx]

    # Try to find a new feasible slot and room
    for _ in range(10):
        new_slot = random.randint(1, 61 - t[class_id - 1])
        new_room = random.choice([j for j in range(1, M + 1) if c[j - 1] >= s[class_id - 1]])

        if all(new_slot + offset not in teacher_slots[g[class_id - 1]] for offset in range(t[class_id - 1])) and \
           all(new_slot + offset not in room_slots[new_room] for offset in range(t[class_id - 1])):
            # Remove old slots
            for offset in range(t[class_id - 1]):
                teacher_slots[g[class_id - 1]].remove(slot + offset)
                room_slots[room].remove(slot + offset)

            # Update slots
            for offset in range(t[class_id - 1]):
                teacher_slots[g[class_id - 1]].append(new_slot + offset)
                room_slots[new_room].append(new_slot + offset)

            assignments[idx] = (class_id, new_slot, new_room)
            return assignments

    return assignments  # Return old if no feasible neighbor found

def simulated_annealing(N, M, t, g, s, c):
    current_solution = initial_feasible_solution(N, M, t, g, s, c)
    current_cost = cost_function(current_solution)
    temperature = 100.0
    cooling_rate = 0.95
    min_temperature = 0.01

    teacher_slots = {i: [] for i in range(1, 101)}
    room_slots = {i: [] for i in range(1, M + 1)}
    
    # Populate slots from the current solution
    for class_id, slot, room in current_solution:
        for offset in range(t[class_id - 1]):
            teacher_slots[g[class_id - 1]].append(slot + offset)
            room_slots[room].append(slot + offset)

    while temperature > min_temperature:
        new_solution = get_neighbor(current_solution, N, M, t, g, s, c, teacher_slots, room_slots)
        new_cost = cost_function(new_solution)
        if new_cost > current_cost or math.exp((new_cost - current_cost) / temperature) > random.random():
            current_solution = new_solution
            current_cost = new_cost
        temperature *= cooling_rate

    return current_solution

def main():
    N, M, t, g, s, c = input_data()
    final_solution = simulated_annealing(N, M, t, g, s, c)
    print(len(final_solution))
    for solution in final_solution:
        print(f"{solution[0]} {solution[1]} {solution[2]}")

if __name__ == "__main__":
    main()
