from dataclasses import dataclass, field
import numpy as np

NUMDAYS = 5
NUMLESSONS = 12
Inf = int(1e9 + 7)

@dataclass
class Lecture:
    id: int = 0
    numLesson: int = 0
    teacher: int = 0
    numStudents: int = 0
    idRoom: int = 0
    idLesson: int = 0

@dataclass
class Room:
    id: int = 0
    capacity: int = 0
    status: np.ndarray = field(default_factory=lambda: np.zeros((NUMDAYS + 1, NUMLESSONS + 1), dtype=int))

    def canAssign(self, day, lesson, lecture):
        if lecture.numStudents > self.capacity:
            return False
        if lesson + lecture.numLesson - 1 > NUMLESSONS:
            return False
        for i in range(lesson, lesson + lecture.numLesson):
            if self.status[day, i] > 0:
                return False
        return True

    def assign(self, day, lesson, lecture):
        for i in range(lesson, lesson + lecture.numLesson):
            assert self.status[day, i] == 0, "Room slot already occupied"
            self.status[day, i] = lecture.id

class Teacher(Room):
    def __init__(self, id):
        super().__init__(id=id)
        self.capacity = Inf

def read_input():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    numLectures = int(data[0])
    numRooms = int(data[1])
    index = 2
    lectures = []
    rooms = []
    teachers = {i: Teacher(i) for i in range(1, numLectures + 1)}
    
    for i in range(1, numLectures + 1):
        numLesson, teacher, numStudents = map(int, data[index:index+3])
        lectures.append(Lecture(id=i, numLesson=numLesson, teacher=teacher, numStudents=numStudents))
        index += 3

    for i in range(1, numRooms + 1):
        capacity = int(data[index])
        rooms.append(Room(id=i, capacity=capacity))
        index += 1

    return numLectures, numRooms, lectures, rooms, teachers

def greedy_assignment(lectures, rooms, teachers):
    lectures.sort(key=lambda l: l.numStudents, reverse=True)
    rooms.sort(key=lambda r: r.capacity, reverse=True)
    
    assigned_lectures = []

    for lecture in lectures:
        assigned = False
        for day in range(1, NUMDAYS + 1):
            for lesson in range(1, NUMLESSONS + 1):
                if teachers[lecture.teacher].canAssign(day, lesson, lecture):
                    for room in rooms:
                        if room.canAssign(day, lesson, lecture):
                            room.assign(day, lesson, lecture)
                            teachers[lecture.teacher].assign(day, lesson, lecture)
                            lecture.idRoom = room.id
                            lecture.idLesson = (day - 1) * NUMLESSONS + lesson
                            assigned_lectures.append(lecture)
                            assigned = True
                            break
                    if assigned:
                        break
            if assigned:
                break

    return assigned_lectures

def solve():
    numLectures, numRooms, lectures, rooms, teachers = read_input()
    assigned_lectures = greedy_assignment(lectures, rooms, teachers)

    print(len(assigned_lectures))
    for lecture in assigned_lectures:
        print(f"{lecture.id} {lecture.idLesson} {lecture.idRoom}")

solve()
