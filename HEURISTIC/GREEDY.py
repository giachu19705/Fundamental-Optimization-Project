class Schedule:
    def __init__(self, num_classes, num_rooms, num_days=5, slots_per_day=12):
        self.num_classes = num_classes
        self.num_rooms = num_rooms
        self.num_days = num_days
        self.slots_per_day = slots_per_day
        self.total_slots = num_days * slots_per_day
        self.schedule = [[None for _ in range(self.total_slots)] for _ in range(num_rooms)]

    def can_schedule(self, room, start, duration, teacher, teacher_schedule):
        # Check if the room is available for the given time duration
        for t in range(start, start + duration):
            if t >= self.total_slots or self.schedule[room][t] is not None:
                return False

        # Check if the teacher is available for the given time duration
        for t in range(start, start + duration):
            if teacher_schedule[t] is True:
                return False
        return True

    def assign_schedule(self, room, start, duration, class_id, teacher_schedule):
        # Assign the class to the room and mark the teacher's schedule
        for t in range(start, start + duration):
            self.schedule[room][t] = class_id
            teacher_schedule[t] = True

def greedy_schedule(classes, rooms):
    num_classes = len(classes)
    num_rooms = len(rooms)
    teacher_schedules = {teacher: [False] * 60 for teacher in set(c['teacher'] for c in classes)}

    # Sort classes by priority (e.g., larger duration or student count first)
    classes = sorted(classes, key=lambda c: (-c['duration'], -c['students']))

    schedule = Schedule(num_classes, num_rooms)

    assignments = []

    for class_info in classes:
        class_id = class_info['id']
        duration = class_info['duration']
        teacher = class_info['teacher']
        students = class_info['students']

        # Try to find a suitable room and time slot
        assigned = False
        for room_id, room_capacity in enumerate(rooms):
            if room_capacity < students:
                continue  # Skip room if it doesn't fit the class

            for day in range(schedule.num_days):
                for slot in range(0, schedule.slots_per_day - duration + 1):
                    start = day * schedule.slots_per_day + slot
                    if schedule.can_schedule(room_id, start, duration, teacher, teacher_schedules[teacher]):
                        schedule.assign_schedule(room_id, start, duration, class_id, teacher_schedules[teacher])
                        assignments.append((class_id, start + 1, room_id + 1))  # Adjust for 1-based indexing
                        assigned = True
                        break
                if assigned:
                    break
            if assigned:
                break
    
    assignments.sort(key=lambda x: x[0])
    # Output the result
    print(len(assignments))
    for assignment in assignments:
        print(*assignment)

# Input parsing
N, M = map(int, input().split())  # Number of classes and rooms

# Read classes information
classes = []
for i in range(N):
    t, g, s = map(int, input().split())  
    classes.append({'id': i + 1, 'duration': t, 'teacher': g, 'students': s})

# Read room capacities
rooms = list(map(int, input().split()))  # c(1), c(2), ..., c(M)

# Run the greedy scheduler
greedy_schedule(classes, rooms)
