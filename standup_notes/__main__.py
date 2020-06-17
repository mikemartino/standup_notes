#!/usr/bin/env python3
import os
import sys
from datetime import datetime, date, timedelta
from typing import Callable

import argparse
import editor
import pyperclip
import pymsteams
from pkg_resources import resource_stream

EXT = '.standup-notes.txt'
STANDUP_NOTES = os.path.join(os.environ.get("HOME"), 'Desktop/standup-notes')
STANDUP_TEMPLATE = resource_stream('standup_notes.resources', 'standup.template')
STANDUP_TEMPLATE_STRING = str(STANDUP_TEMPLATE.read().decode('UTF-8'))


def main():
    parser = argparse.ArgumentParser()
    days = parser.add_mutually_exclusive_group()

    days.add_argument("--today", help="Flag passed in to do action with today's notes", action="store_true")
    days.add_argument("--tomorrow", help="Flag passed in to do action with tomorrow's notes", action="store_true")
    days.add_argument("--yesterday", help="Flag passed in to do action with tomorrow's notes", action="store_true")

    parser.add_argument('-l', '--list', help='List all stand-up notes.', action='store_true')
    parser.add_argument('-r', '--read', help='Read stand-up notes', action='store_true')
    parser.add_argument('-c', '--copy', help='If combined with the \'edit\' flag, copies the previous days TODO. '
                                             'Otherwise, copies the specified day\'s notes ', action='store_true')
    parser.add_argument('-e', '--edit', help='Edit stand-up notes', action='store_true')
    parser.add_argument('-d', '--delete', help='Delete stand-up notes from inputted date', action='store', type=str)
    parser.add_argument('-p', '--post', help='Function to post notes to msteams chat', action='store_true')
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
        if arguments.copy:
            call_func_for_specified_day(copy_prev, arguments)
        else:
            call_func_for_specified_day(edit_note, arguments)

    if arguments.copy:
        call_func_for_specified_day(copy_note, arguments)

    if arguments.post:
        post_note(date.today())


def call_func_for_specified_day(func, arguments):
    """Makes sure proper day arguments are being passed to their respective functions"""
    if arguments.yesterday:
        func(last_weekday(date.today()))
        return 0
    if arguments.today:
        func(date.today())
        return 0
    if arguments.tomorrow:
        func(next_weekday(date.today()))
        return 0
    if arguments.delete:
        func(arguments.delete)
        return 0
    else:
        print("Make sure to include the proper argument. Type standup-notes -h for more info")


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


def copy_prev(day: date):
    """
    This function will allow the option of copying the previous days "What I'm doing today" into the
    "What I did yesterdays" section of  that days notes
    """
    previous_days_note = get_note_name(last_weekday(day))
    note = get_note_name(day)
    date_of_note = "Date: " + day.strftime("%m/%d/%Y") + " \n"
    beginning_format = str(STANDUP_TEMPLATE_STRING.splitlines()[0]) + '\n'
    end_format = '\n'.join(STANDUP_TEMPLATE_STRING.splitlines()[2:])
    copy_text = False
    lines_to_append = []
    # If the previous days notes exists
    if os.path.exists(previous_days_note):
        result = verify_input("Found yesterdays notes, would you like to insert applicable information into your "
                              "notes y/n: ")
        # If the user wants to copy previous days notes
        if result:
            # Copy's applicable information from previous days notes
            lines_to_append = get_text(previous_days_note, 't')
            # If the note that wants to be edited already exists
            # It will add "lines_to_append" to "What I did yesterdays" section of notes
            if os.path.exists(note):
                with open(note) as f:
                    data = f.readlines()
                data[1] = data[1] + "".join(lines_to_append)
                with open(note, 'w') as file:
                    file.writelines(data)
            else:
                editor.edit(note, contents=date_of_note + beginning_format + "".join(lines_to_append) + end_format)
                return 0
        if not result:
            response = input("Yesterdays notes will not be copied. Press enter to continue")
    # If previous days notes doesn't exist
    else:
        response = input("Yesterdays notes were not found, nothing will be copied. Press enter to continue: ")
    edit_note(day)


def edit_note(day: date):
    """Launches the default $EDITOR or a suitable default. If the note already exists, the editor opens it for editing.
    If the note does not exist, the editor opens a new file using the stand-up template."""
    note = get_note_name(day)
    date_of_note = "Date: " + day.strftime("%m/%d/%Y") + " \n"
    if os.path.exists(note):
        editor.edit(note)
    else:
        editor.edit(note, contents=date_of_note + STANDUP_TEMPLATE_STRING)


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
    """
    Allows the user to delete notes. User inputs a date and will ask the user if they want to delete notes older
    than the date provided
    """
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
        result = verify_input("Are you sure you want to delete these files y/n: ")
        if result:
            for file in files_to_delete:
                os.remove(os.path.join(STANDUP_NOTES, file))
                print("Files have been deleted.")
        else:
            print("No files to be deleted")
    else:
        print("No files to be deleted")


def post_note(day: date):
    print("Posting your note")
    date_of_note = "Date: " + day.strftime("%m/%d/%Y") + " \n"
    link = input("Please put in the connector link: ")
    name = input("Please enter your name: ")
    myTeamsMessage = pymsteams.connectorcard(link)
    myTeamsMessage.text(name+ "'s standup notes for " + date_of_note)
    # Create Section 1
    Section1 = pymsteams.cardsection()
    Section1.activityTitle("What I did yesterday")
    Section1.activityText(get_text(get_note_name(day), 'y'))

    # Create Section 2
    Section2 = pymsteams.cardsection()
    Section2.activityTitle("What I am doing today")
    Section2.activityText(get_text(get_note_name(day), 't'))

    # Create Section 3
    Section3 = pymsteams.cardsection()
    Section3.activityTitle("Blockers")
    Section3.activityText(get_blockers(get_note_name(day)))
    # Add both Sections to the main card object
    myTeamsMessage.addSection(Section1)
    myTeamsMessage.addSection(Section2)
    myTeamsMessage.addSection(Section3)
    myTeamsMessage.send()
    print("Message sent")


def validate(date_text):
    """
    Validate if date input is correct
    """
    try:
        datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD")


def verify_input(log):
    """
    Loop to verify yes or no input.
    Function takes a string which is printed out so the user knows what they are agreeing to
    """
    while True:
        result = input(log)
        if result.lower() == 'y':
            return True
        if result.lower() == 'n':
            return False
        else:
            print("Please enter a valid response")


def get_text(text, day):
    lines_to_append = []
    text_to_use = []
    if day == 't':
        text_to_use = ['Blockers', 'What I\'m doing']
    if day == 'y':
        text_to_use = ['What I\'m doing', 'What I did']
    copy_text = False
    with open(text) as f:
        for line in f:
            if copy_text:
                if text_to_use[0] not in line:
                    lines_to_append.append(line)
            if text_to_use[1] in line:
                copy_text = True
            if text_to_use[0] in line:
                copy_text = False
    return "".join(lines_to_append)


def get_blockers(text):
    lines_to_append = []
    copy_text = False
    with open(text) as f:
        for line in f:
            if copy_text:
                lines_to_append.append(line)
            if 'Blockers' in line:
                copy_text = True
    return "".join(lines_to_append)


if __name__ == '__main__':
    main()
