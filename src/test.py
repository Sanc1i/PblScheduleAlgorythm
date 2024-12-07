import random
from deap import base, creator, tools

print("hello world")

# Problem setup
time_slots = ["S1", "S2"]
groups = ["G1", "G2"]
teachers = ["T1", "T2", "T3"]
rooms = ["R1", "R2"]

# Chromosome: Random assignments of (teacher, room) for each group and time slot
def random_schedule():
    return [random.choice(teachers) + "-" + random.choice(rooms) for _ in groups * len(time_slots)]

# Fitness function
def fitness(schedule):
    conflicts = sum(schedule.count(assign) > 1 for assign in schedule)
    return 1 / (1 + conflicts)  # Minimize conflicts

# GA setup
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)
toolbox = base.Toolbox()
toolbox.register("individual", tools.initIterate, creator.Individual, random_schedule)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("evaluate", fitness)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.2)
toolbox.register("select", tools.selTournament, tournsize=3)

# Run GA
population = toolbox.population(n=100)
for gen in range(50):
    offspring = tools.selBest(population, len(population) // 2)
    offspring = list(map(toolbox.clone, offspring))
    for child1, child2 in zip(offspring[::2], offspring[1::2]):
        toolbox.mate(child1, child2)
        del child1.fitness.values, child2.fitness.values
    for mutant in offspring:
        if random.random() < 0.2:
            toolbox.mutate(mutant)
            del mutant.fitness.values
    population[:] = tools.selBest(population + offspring, 100)

best_individual = tools.selBest(population, 1)[0]
print("Final Schedule (Best Individual):")
for i, assignment in enumerate(best_individual):
    time_slot = time_slots[i % len(time_slots)]
    group = groups[i // len(time_slots)]
    print(f"Time Slot: {time_slot}, Group: {group}, Assignment: {assignment}")