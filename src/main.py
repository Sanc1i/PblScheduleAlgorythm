from ortools.sat.python import cp_model

def create_schedule(tasks, time_slots, resources, constraints):
    """
    Create a schedule using CSP.

    :param tasks: List of tasks to schedule.
    :param time_slots: List of available time slots.
    :param resources: List of resources available for tasks.
    :param constraints: A dictionary of constraints (e.g., {'task1': {'not_before': 2, 'resource': 'resource1'}}).
    :return: A dictionary with the schedule.
    """
    model = cp_model.CpModel()

    # Create variables
    task_start_times = {}
    task_resources = {}
    for task in tasks:
        task_start_times[task] = model.NewIntVar(0, len(time_slots) - 1, f"start_{task}")
        task_resources[task] = model.NewIntVar(0, len(resources) - 1, f"resource_{task}")

    # Add constraints
    for task, task_constraints in constraints.items():
        if 'not_before' in task_constraints:
            model.Add(task_start_times[task] >= task_constraints['not_before'])
        if 'not_after' in task_constraints:
            model.Add(task_start_times[task] <= task_constraints['not_after'])
        if 'resource' in task_constraints:
            resource_index = resources.index(task_constraints['resource'])
            model.Add(task_resources[task] == resource_index)

    # Ensure no overlap of tasks using the same resource
    for i in range(len(tasks)):
        for j in range(i + 1, len(tasks)):
            # Create a boolean variable indicating if tasks[i] and tasks[j] share the same resource
            same_resource = model.NewBoolVar(f"same_resource_{tasks[i]}_{tasks[j]}")
            model.Add(task_resources[tasks[i]] == task_resources[tasks[j]]).OnlyEnforceIf(same_resource)
            model.Add(task_resources[tasks[i]] != task_resources[tasks[j]]).OnlyEnforceIf(same_resource.Not())

            # Ensure start times are different if tasks share the same resource
            model.Add(task_start_times[tasks[i]] != task_start_times[tasks[j]]).OnlyEnforceIf(same_resource)

    # Solve the model
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        schedule = {}
        for task in tasks:
            schedule[task] = {
                'start_time': solver.Value(task_start_times[task]),
                'resource': resources[solver.Value(task_resources[task])]
            }
        return schedule
    else:
        return None

# Example usage
tasks = ['task1', 'task2', 'task3']
time_slots = [0, 1, 2, 3, 4]  # Time slots available
resources = ['resource1', 'resource2']  # Resources available
constraints = {
    'task1': {'not_before': 1, 'resource': 'resource1'},
    'task2': {'not_after': 3},
    'task3': {'resource': 'resource2'}
}

schedule = create_schedule(tasks, time_slots, resources, constraints)
if schedule:
    print("Schedule:")
    for task, details in schedule.items():
        print(f"{task}: Start at {details['start_time']}, Resource: {details['resource']}")
else:
    print("No feasible schedule found.")