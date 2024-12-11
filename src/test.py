# import random
# from deap import base, creator, tools

# print("hello world")

# # Problem setup
# time_slots = ["S1", "S2"]
# groups = ["G1", "G2"]
# teachers = ["T1", "T2", "T3"]
# rooms = ["R1", "R2"]

# # Chromosome: Random assignments of (teacher, room) for each group and time slot
# def random_schedule():
#     return [random.choice(teachers) + "-" + random.choice(rooms) for _ in groups * len(time_slots)]

# # Fitness function
# def fitness(schedule):
#     conflicts = sum(schedule.count(assign) > 1 for assign in schedule)
#     return 1 / (1 + conflicts)  # Minimize conflicts

# # GA setup
# creator.create("FitnessMax", base.Fitness, weights=(1.0,))
# creator.create("Individual", list, fitness=creator.FitnessMax)
# toolbox = base.Toolbox()
# toolbox.register("individual", tools.initIterate, creator.Individual, random_schedule)
# toolbox.register("population", tools.initRepeat, list, toolbox.individual)
# toolbox.register("evaluate", fitness)
# toolbox.register("mate", tools.cxTwoPoint)
# toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.2)
# toolbox.register("select", tools.selTournament, tournsize=3)

# # Run GA
# population = toolbox.population(n=100)
# for gen in range(50):
#     offspring = tools.selBest(population, len(population) // 2)
#     offspring = list(map(toolbox.clone, offspring))
#     for child1, child2 in zip(offspring[::2], offspring[1::2]):
#         toolbox.mate(child1, child2)
#         del child1.fitness.values, child2.fitness.values
#     for mutant in offspring:
#         if random.random() < 0.2:
#             toolbox.mutate(mutant)
#             del mutant.fitness.values
#     population[:] = tools.selBest(population + offspring, 100)

# best_individual = tools.selBest(population, 1)[0]
# print("Final Schedule (Best Individual):")
# for i, assignment in enumerate(best_individual):
#     time_slot = time_slots[i % len(time_slots)]
#     group = groups[i // len(time_slots)]
#     print(f"Time Slot: {time_slot}, Group: {group}, Assignment: {assignment}")
import itertools

class Course:
    def __init__(self, name, lectures=0, exercises=0, labs=0):
        self.name = name
        self.lectures = lectures
        self.exercises = exercises
        self.labs = labs

class Schedule:
    def __init__(self):
        self.days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        self.timeslots = [f"{hour}:15 - {hour+1}:45" for hour in range(10, 17, 2)]  # From 10:15 to 16:45
        self.timetable = {day: {timeslot: None for timeslot in self.timeslots} for day in self.days}

    def add_course(self, course, day, timeslot, room):
        self.timetable[day][timeslot] = (course, room)

    def is_available(self, day, timeslot):
        return self.timetable[day][timeslot] is None

    def print_schedule(self):
        for day, times in self.timetable.items():
            print(f"\n{day}:")
            for timeslot, course in times.items():
                if course:
                    print(f"  {timeslot} -> {course[0].name} in Room {course[1]}")
                else:
                    print(f"  {timeslot} -> Free")

def generate_schedule(courses):
    schedule = Schedule()
    rooms = itertools.cycle(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'])  # Assigning rooms
    day_slots = [(day, slot) for day in schedule.days for slot in schedule.timeslots]

    for course in courses:
        if course.lectures:
            place_component(schedule, course, 'Lecture', rooms, day_slots)
        if course.exercises:
            place_component(schedule, course, 'Exercises', rooms, day_slots)
        if course.labs:
            place_component(schedule, course, 'Labs', rooms, day_slots)

    return schedule

def place_component(schedule, course, component_type, rooms, day_slots):
    for day, slot in day_slots:
        if schedule.is_available(day, slot):
            room = next(rooms)
            schedule.add_course(course, day, slot, room)
            print(f"Scheduled {course.name} ({component_type}) on {day} at {slot} in Room {room}")
            break

# Define courses for each program
bst_courses = [
    Course("Metrology", lectures=1, exercises=1),
    Course("Basic Materials Engineering", lectures=1, labs=1),
    Course("Information Technology 1", exercises=1, labs=1),
    Course("Principles of Management", lectures=1, exercises=1),
    Course("Engineering Drawing", lectures=1, exercises=1),
    Course("Fundamentals of Physics and Chemistry", lectures=1, labs=1),
    Course("Mathematics 1", lectures=1, exercises=1),
    Course("Academic English for Engineers 1", exercises=1)
]

cs_courses = [
    Course("Introduction to Computer Science", lectures=1, exercises=1),
    Course("Electrical and Electronic Engineering", lectures=1, labs=1),
    Course("Scripting Languages", exercises=1, labs=1),
    Course("Introduction to Web Development", exercises=1, labs=1),
    Course("Physics", lectures=1, labs=1, exercises=1),
    Course("Mathematics 1", lectures=1, exercises=1, labs=1),
    Course("Academic English for Engineers 1", exercises=1)
]

mmds_courses = [
    Course("Engineering Drawing", lectures=1, exercises=1),
    Course("Introduction to Logic and Discrete Mathematics", lectures=1, exercises=1),
    Course("Information Technologies I", exercises=1, labs=1),
    Course("Physics", lectures=1, labs=1, exercises=1),
    Course("Linear Algebra in Data Analysis", lectures=1, labs=1),
    Course("Mathematical Analysis I", lectures=1, exercises=1),
    Course("Academic English for Engineers 1", exercises=1)
]

# Generate and print schedules
bst_schedule = generate_schedule(bst_courses.copy())
cs_schedule = generate_schedule(cs_courses.copy())
mmds_schedule = generate_schedule(mmds_courses.copy())

print("BST Schedule:")
bst_schedule.print_schedule()
print("\nCS Schedule:")
cs_schedule.print_schedule()
print("\nMMDS Schedule:")
mmds_schedule.print_schedule()