def find_available_teacher(subject, teachers):
    for teacher in teachers:
        if teacher["faculty"] == subject["faculty"]:
            return teacher
    return None

def find_available_room(group, rooms):
    for room in rooms:
        if room["capacity"] >= group["size"]:
            return room
    return None

def schedule_fcfs(subjects, teachers, rooms, student_groups):
    schedule = []
    for subject in subjects:
        teacher = find_available_teacher(subject, teachers)
        if not teacher:
            print(f"No teacher available for subject {subject['name']}")
            continue
        
        group = next((g for g in student_groups if g["faculty"] == subject["faculty"]), None)
        if not group:
            print(f"No group found for faculty {subject['faculty']}")
            continue
        
        room = find_available_room(group, rooms)
        if not room:
            print(f"No room available for group {group['name']}")
            continue
        
        assigned_time = teacher["available_times"][0] if teacher["available_times"] else "No available time"
        
        schedule.append({
            "subject": subject["name"],
            "teacher": teacher["name"],
            "room": room["name"],
            "time": assigned_time,
            "group": group["name"]
        })
        
        # Remove assigned time slot from availability
        teacher["available_times"].remove(assigned_time)
        room["available_times"].remove(assigned_time)
    
    return schedule