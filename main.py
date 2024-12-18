from src import *

groups = getdata.get_sheet_data_as_tuples("Groups")
subjects = getdata.get_sheet_data_as_tuples("Subjects")
rooms = getdata.get_sheet_data_as_tuples("Rooms")
tutors = getdata.get_sheet_data_as_tuples("Tutors")

names = randomShit.extract_tutor_names(groups) + randomShit.extract_rest(subjects) +  randomShit.extract_rest(rooms) +  randomShit.extract_tutor_names(tutors)
createfile.createFile("Schedule1", len(groups) + len(rooms) + len(tutors), )