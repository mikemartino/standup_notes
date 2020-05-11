# PYTHON_ARGCOMPLETE_OK
import os
import sys
from datetime import date, timedelta
from typing import Callable

import argcomplete
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

    parser.add_argument('--list', help='List all stand-up notes.', action='store_true')
    parser.add_argument('-r', '--read', help='Read stand-up notes',
                        action='store_true')
    parser.add_argument('-c', '--copy', help='Copy stand-up notes', action='store_true')
    parser.add_argument('-e', '--edit', help='Edit stand-up notes', action='store_true')
    parser.add_argument('-d', '--delete', help='Delete stand-up notes from inputted date', action='store', type=int)
    argcomplete.autocomplete(parser)
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
        delete_notes(arguments.delete)

    if arguments.read:
        if arguments.yesterday:
            read_note(last_weekday(date.today()))
        if arguments.today:
            read_note(date.today())
        if arguments.tomorrow:
            read_note(next_weekday(date.today()))

    if arguments.edit:
        if arguments.yesterday:
            edit_note(last_weekday(date.today()))
        if arguments.today:
            edit_note(date.today())
        if arguments.tomorrow:
            edit_note(next_weekday(date.today()))
    if arguments.copy:
        if arguments.yesterday:
            copy_note(last_weekday(date.today()))
        if arguments.today:
            copy_note(date.today())
        if arguments.tomorrow:
            copy_note(next_weekday(date.today()))
    """
    if arguments.read_yesterday:
        read_note(last_weekday(date.today()))

    if arguments.read_today:
        read_note(date.today())

    if arguments.read_tomorrow:
        read_note(next_weekday(date.today()))

    if arguments.edit_yesterday:
        edit_note(last_weekday(date.today()))

    if arguments.edit_today:
        edit_note(date.today())

    if arguments.edit_tomorrow:
        edit_note(next_weekday(date.today()))

    if arguments.copy_yesterday:
        copy_note(last_weekday(date.today()))

    if arguments.copy_today:
        copy_note(date.today())

    if arguments.copy_tomorrow:
        copy_note(next_weekday(date.today()))
    """


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
        # Note: It appears that the file will be saved regardless of what you do in your editor (in my case, vim).
        editor.edit(note, STANDUP_TEMPLATE.read())
        # Note: Date will be inserted after the document has been finished being created
        f = open(note, "r")
        contents = f.readlines()
        f.close()
        date_of_note = "Date: " + day.strftime("%m/%d/%Y") + " \n"
        contents.insert(0, date_of_note)

        f = open(note, "w")
        contents = "".join(contents)
        f.write(contents)
        f.close()


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


def delete_notes(amount):
    file_to_delete = []
    if len(str(amount)) != 8:
        print("Please enter in a valid date")
        return
    for file in os.listdir(STANDUP_NOTES):
        value = int(file.split('.')[0])
        if value < amount:
            file_to_delete.append(file)
    if file_to_delete:
        print("Here are the file to be deleted")
        for file in file_to_delete:
            print(file)
        while True:
            result = input("Are you sure you want to delete these files y/n: ")
            if result.lower() == 'y':
                for file in file_to_delete:
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


if __name__ == '__main__':
    main()
