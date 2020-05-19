import os
import sys
from datetime import datetime, date, timedelta
from typing import Callable

import argparse
import editor
import pyperclip
from pkg_resources import resource_stream

EXT = '.standup-notes.txt'
STANDUP_NOTES = os.path.join(os.environ.get("HOME"), 'Desktop/standup-notes')
STANDUP_TEMPLATE = resource_stream('standup_notes.resources', 'standup.template')


def main():
    parser = argparse.ArgumentParser()
    days = parser.add_mutually_exclusive_group()

    days.add_argument("--today", action="store_true")
    days.add_argument("--tomorrow", action="store_true")
    days.add_argument("--yesterday", action="store_true")

    parser.add_argument('-l', '--list', help='List all stand-up notes.', action='store_true')
    parser.add_argument('-r', '--read', help='Read stand-up notes',
                        action='store_true')
    parser.add_argument('-c', '--copy', help='Copy stand-up notes', action='store_true')
    parser.add_argument('-e', '--edit', help='Edit stand-up notes', action='store_true')
    parser.add_argument('-d', '--delete', help='Delete stand-up notes from inputted date', action='store', type=str)
    arguments = parser.parse_args()

    # sys.argv includes a list of elements starting with the program name
    if len(sys.argv) < 2:
        parser.print_usage()
        sys.exit(1)

    if not os.path.exists(STANDUP_NOTES):
        os.mkdir(STANDUP_NOTES)

    if arguments.list:
        for note in reversed(sorted(os.listdir(STANDUP_NOTES))):
            print(os.path.join(STANDUP_NOTES, note))

    if arguments.delete:
        call_func_for_specified_day(delete_notes, arguments)

    if arguments.read:
        call_func_for_specified_day(read_note, arguments)

    if arguments.edit:
        call_func_for_specified_day(edit_note, arguments)

    if arguments.copy:
        call_func_for_specified_day(copy_note, arguments)


def call_func_for_specified_day(func, arguments):
    """Call the proper function to either """
    if arguments.yesterday:
        func(last_weekday(date.today()))
    if arguments.today:
        func(date.today())
    if arguments.tomorrow:
        func(next_weekday(date.today()))
    if arguments.delete:
        func(arguments.delete)


def get_note_name(weekday: date):
    """Map the date to the proper path of the standup-notes file for the day."""
    return os.path.join(STANDUP_NOTES, date.strftime(weekday, '%Y%m%d') + EXT)


def copy_note(day: date):
    """Copy the note to the clipboard if it exists."""
    note = get_note_name(day)
    if os.path.exists(note):
        with open(note, 'r') as f:
            pyperclip.copy(f.read())
    else:
        print(note + ' doesn\'t exist yet.')


def edit_note(day: date):
    """Launches the default $EDITOR or a suitable default. If the note already exists, the editor opens it for editing.
    If the note does not exist, the editor opens a new file using the stand-up template."""
    note = get_note_name(day)
    if os.path.exists(note):
        editor.edit(note)
    else:
        date_of_note = "Date: " + day.strftime("%m/%d/%Y") + " \n"
        editor.edit(note, contents=date_of_note + str(STANDUP_TEMPLATE.read().decode('UTF-8')))


def read_note(day: date):
    """Print the note if it exists."""
    note = get_note_name(day)
    if os.path.exists(note):
        with open(note, 'r') as f:
            print(f.read())
    else:
        print(note + ' doesn\'t exist yet.')


def next_weekday(start_day: date) -> date:
    return iterate_weekday(start_day, lambda input_day: input_day + timedelta(days=1))


def last_weekday(start_day: date) -> date:
    return iterate_weekday(start_day, lambda input_day: input_day - timedelta(days=1))


def iterate_weekday(day: date, func: Callable[[date], date]) -> date:
    next_day = func(day)
    day_num = next_day.weekday()
    # Monday - Friday (0-4), Saturday(5), Sunday(6)
    if day_num < 5:  # Weekday
        return next_day
    else:  # Weekend
        return iterate_weekday(next_day, func)


def delete_notes(date_to_delete):
    files_to_delete = []
    validate(date_to_delete)
    date_in_int = int(date_to_delete.replace('-', ''))
    for file in os.listdir(STANDUP_NOTES):
        value = int(file.split('.')[0])
        if value < date_in_int:
            files_to_delete.append(file)
    if files_to_delete:
        print("Here are the file to be deleted")
        print(*files_to_delete, sep='\n')
        while True:
            result = input("Are you sure you want to delete these files y/n: ")
            if result.lower() == 'y':
                for file in files_to_delete:
                    os.remove(os.path.join(STANDUP_NOTES, file))
                print("Files have been deleted.")
                break
            if result.lower() == 'n':
                print("No files to be deleted")
                break
            else:
                print("Please enter a valid response")
    else:
        print("No files to be deleted")


def validate(date_text):
    try:
        datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD")


if __name__ == '__main__':
    main()
