import openpyxl  # For interacting with Excel files
from .sheet_operations import *
from .constants import *


def fcfs_schedule_with_requirements(file_path, tutors, rooms, subjects, groups, faculty):
    """
    Fill the timetable using FCFS scheduling, ensuring requirements are met for each group within a faculty.
    """
    # Open workbook
    workbook = openpyxl.load_workbook(file_path)
    
    # Convert data into dictionaries for easier access
    subject_keys = [
        'SubjectID', 'SubjectName', 'FacultyID', 'HoursRequired', 
        'RequiresBlackboard', 'RequiresComputers', 'MaxStudents', 'Type'
    ]
    room_keys = ['RoomID', 'RoomName', 'Capacity', 'HasBlackboard', 'HasComputers']
    tutor_keys = ['TutorID', 'Name', 'Surname', 'Subject']
    group_keys = ['GroupID', 'FacultyID', 'GroupNumber', 'NumberOfStudents']

    subjects = [dict(zip(subject_keys, subject)) for subject in subjects]
    rooms = [dict(zip(room_keys, room)) for room in rooms]
    tutors = [dict(zip(tutor_keys + [f'Schedule_{i}' for i in range(len(tutor) - len(tutor_keys))], tutor)) for tutor in tutors]
    groups = [dict(zip(group_keys, group)) for group in groups]

    unassigned_subjects_count = 0  # Counter for unassigned subjects

    for subject in subjects:
        subject_name = subject['SubjectName']
        faculty_id = subject['FacultyID']
        requires_blackboard = subject['RequiresBlackboard']
        requires_computers = subject['RequiresComputers']
        max_students = subject['MaxStudents']
        subject_type = subject['Type']

        # Filter groups that belong to the subject's faculty
        relevant_groups = [group for group in groups if group['FacultyID'] == faculty_id]

        for group in relevant_groups:
            group_number = group['GroupNumber']
            group_size = group['NumberOfStudents']
            group_sheet_name = f"Schedule_Faculty{faculty_id}_Group{group_number}"

            # Ensure group sheet exists
            if group_sheet_name not in workbook.sheetnames:
                workbook.create_sheet(group_sheet_name)
            group_sheet = workbook[group_sheet_name]

            # Filter suitable rooms for the group size
            suitable_rooms = [
                room for room in rooms
                if (not requires_blackboard or room['HasBlackboard']) and
                   (not requires_computers or room['HasComputers']) and
                   room['Capacity'] >= group_size
            ]

            if not suitable_rooms:
                print(f"No suitable rooms found for {subject_name} in Group {group_number}. Skipping.")
                unassigned_subjects_count += 1
                continue

            # Filter suitable tutors for the subject
            suitable_tutors = [tutor for tutor in tutors if tutor['Subject'] == subject_type]

            if not suitable_tutors:
                print(f"No suitable tutors found for {subject_name} in Group {group_number}. Skipping.")
                unassigned_subjects_count += 1
                continue

            scheduled = False

            # Attempt to schedule the subject
            for day_number, day in enumerate(DAYS):
                if scheduled:
                    break
                for time_number, time in enumerate(CLASS_TIMES):
                    if scheduled or time_number >= 11:
                        continue
                    cell = f"{chr(day_number + ord('B'))}{time_number + 2}"
                    cell_secondHour = f"{chr(day_number + ord('B'))}{time_number + 3}"

                    for room in suitable_rooms:
                        room_sheet = workbook[f"Schedule_{room['RoomName']}"]

                        for tutor in suitable_tutors:
                            tutor_sheet = workbook[f"Schedule_{tutor['Name']}_{tutor['Surname']}"]

                            # Check availability
                            if any([
                                is_cell_occupied(sheet, cell) or is_cell_occupied(sheet, cell_secondHour)
                                for sheet in [tutor_sheet, group_sheet, room_sheet]
                            ]):
                                continue

                            # Fill the schedules with group details
                            details = f"{subject_name} (Group {group_number}, Room {room['RoomName']}, Tutor {tutor['Name']} {tutor['Surname']})"
                            fill_cell(group_sheet, cell, details)
                            fill_cell(room_sheet, cell, details)
                            fill_cell(tutor_sheet, cell, details)
                            fill_cell(group_sheet, cell_secondHour, details)
                            fill_cell(room_sheet, cell_secondHour, details)
                            fill_cell(tutor_sheet, cell_secondHour, details)

                            scheduled = True
                            break
                        if scheduled:
                            break
                    if scheduled:
                        break

            if not scheduled:
                print(f"Could not schedule {subject_name} for Group {group_number}. No suitable slot available.")
                unassigned_subjects_count += 1

    workbook.save(file_path)
    print("All schedules updated successfully.")
    print(f"Total unassigned subjects: {unassigned_subjects_count}")



# def fcfs_schedule_with_requirements(file_path, tutors, rooms, subjects, groups, faculty):
#     """
#     Fill the timetable using FCFS scheduling, ensuring requirements are met.
#     """
#     # Open workbook
#     workbook = openpyxl.load_workbook(file_path)
    
#     # Convert subjects from tuples to dictionaries
#     subject_keys = [
#         'SubjectID', 'SubjectName', 'FacultyID', 'HoursRequired', 
#         'RequiresBlackboard', 'RequiresComputers', 'MaxStudents', 'Type'
#     ]
#     room_keys = ['RoomID', 'RoomName', 'Capacity', 'HasBlackboard', 'HasComputers']
#     tutor_keys = ['TutorID', 'Name', 'Surname', 'Subject']

#     subjects = [dict(zip(subject_keys, subject)) for subject in subjects]
#     rooms = [dict(zip(room_keys, room)) for room in rooms]
#     tutors = [dict(zip(tutor_keys + [f'Schedule_{i}' for i in range(len(tutor) - len(tutor_keys))], tutor)) for tutor in tutors]

#     unassigned_subjects_count = 0  # Counter for unassigned subjects

#     for subject in subjects:
#         subject_name = subject['SubjectName']
#         faculty_id = subject['FacultyID']
#         requires_blackboard = subject['RequiresBlackboard']
#         requires_computers = subject['RequiresComputers']
#         max_students = subject['MaxStudents']
#         subject_type = subject['Type']

#         # Filter suitable rooms for the subject
#         suitable_rooms = [
#             room for room in rooms
#             if (not requires_blackboard or room['HasBlackboard']) and
#                (not requires_computers or room['HasComputers']) and
#                room['Capacity'] >= max_students
#         ]

#         if not suitable_rooms:
#             print(f"No suitable rooms found for {subject_name}. Skipping.")
#             unassigned_subjects_count += 1
#             continue

#         # Filter suitable tutors for the subject
#         suitable_tutors = [tutor for tutor in tutors if tutor['Subject'] == subject_type]

#         if not suitable_tutors:
#             print(f"No suitable tutors found for {subject_name}. Skipping.")
#             unassigned_subjects_count += 1
#             continue

#         scheduled = False  # To track if the subject gets scheduled

#         # Try all days and times
#         for day_number, day in enumerate(DAYS):
#             if scheduled:
#                 break
#             for time_number, time in enumerate(CLASS_TIMES):
#                 if scheduled:
#                     break
#                 if time_number >= 11:
#                     continue
#                 cell = f"{chr(day_number + ord('B'))}{time_number + 2}"
#                 cell_secondHour = f"{chr(day_number + ord('B'))}{time_number + 3}"

#                 # Try every combination of room and tutor for this time slot
#                 for room in suitable_rooms:
#                     room_sheet = workbook[f"Schedule_{room['RoomName']}"]

#                     for tutor in suitable_tutors:
#                         tutor_sheet = workbook[f"Schedule_{tutor['Name']}_{tutor['Surname']}"]
#                         faculty_sheet = workbook[f"Schedule_{faculty_id}"]

#                         # Check availability in all three schedules
#                         if is_cell_occupied(tutor_sheet, cell) or \
#                            is_cell_occupied(faculty_sheet, cell) or \
#                            is_cell_occupied(room_sheet, cell) or \
#                            is_cell_occupied(tutor_sheet, cell_secondHour) or \
#                            is_cell_occupied(faculty_sheet, cell_secondHour) or \
#                            is_cell_occupied(room_sheet, cell_secondHour):
#                             continue

#                         # Fill the schedules
#                         fill_cell(tutor_sheet, cell, f"{subject_name} (Faculty {faculty_id}, Room {room['RoomName']})")
#                         fill_cell(faculty_sheet, cell, f"{subject_name} (Tutor {tutor['Name']}_{tutor['Surname']}, Room {room['RoomName']})")
#                         fill_cell(room_sheet, cell, f"{subject_name} (Tutor {tutor['Name']}_{tutor['Surname']}, Faculty {faculty_id})")
#                         fill_cell(tutor_sheet, cell_secondHour, f"{subject_name} (Faculty {faculty_id}, Room {room['RoomName']})")
#                         fill_cell(faculty_sheet, cell_secondHour, f"{subject_name} (Tutor {tutor['Name']}_{tutor['Surname']}, Room {room['RoomName']})")
#                         fill_cell(room_sheet, cell_secondHour, f"{subject_name} (Tutor {tutor['Name']}_{tutor['Surname']}, Faculty {faculty_id})")

#                         # print(f"Scheduled {subject_name} on {day} at {time} in room {room['RoomName']} with tutor {tutor['Name']} {tutor['Surname']}.")
#                         scheduled = True
#                         break  # Break from tutor loop
#                     if scheduled:
#                         break  # Break from room loop
#                 if scheduled:
#                     break  # Break from time loop

#         if not scheduled:
#             print(f"Could not schedule {subject_name}. No suitable time, room, or tutor was available.")
#             unassigned_subjects_count += 1

#     # Save the workbook
#     workbook.save(file_path)
#     print(f"All schedules updated successfully.")
#     print(f"Total unassigned subjects: {unassigned_subjects_count}")
