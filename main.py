from src import *
import argparse


def generate(args):
    groups = getdata.get_sheet_data_as_tuples("Groups")
    faculty = getdata.get_sheet_data_as_tuples("Faculties")
    subjects = getdata.get_sheet_data_as_tuples("Subjects")
    rooms = getdata.get_sheet_data_as_tuples("Rooms")
    tutors = getdata.get_sheet_data_as_tuples("Tutors")

    names = extract.extract_all(groups, rooms, tutors)
    
    createfile.createFile(args.generate, names)
    absents.mark_tutor_absence(createfile.get_file_path(args.generate), tutors)
    fcfs.fcfs_schedule_with_requirements(createfile.get_file_path(args.generate), tutors, rooms, subjects, groups, faculty)

def main():
    parser = argparse.ArgumentParser(description="Schedule generator")
    parser.add_argument('-g', '--generate', metavar='FILENAME', help="Generates a Schedule with the given filename")
    parser.add_argument('-p', '--print', metavar='FILENAME', help="Prints the Schedule for the given filename")
    args = parser.parse_args()

    if args.generate:
        print("Start Generation")
        generate(args)
        print("End Generation")
    elif args.print:
        printing.print_all_schedules(createfile.get_file_path(args.print))
    else:
        print("No valid arguments provided. Use -h for help")
        

if __name__ == "__main__":
    main()