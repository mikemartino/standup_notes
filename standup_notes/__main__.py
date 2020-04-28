import os
import sys
from argparse import ArgumentParser, Namespace
from datetime import date, timedelta
from dotenv import load_dotenv
from typing import Callable

from pkg_resources import resource_stream

import editor
import pyperclip

STANDUP_TEMPLATE = resource_stream('standup_notes.resources', 'standup.template')


def main():
    parser = ArgumentParser()
    parser.add_argument('--list', help='List all stand-up notes.', action='store_true')
    parser.add_argument('--read-yesterday', help='Read yesterday\'s stand-up notes.', action='store_true')
    parser.add_argument('--read-today', help='Read today\'s stand-up notes.', action='store_true')
    parser.add_argument('--read-tomorrow', help='Read tomorrow\'s stand-up notes.', action='store_true')
    parser.add_argument('--copy-yesterday', help='Copy yesterday\'s stand-up notes to the clipboard.',
                        action='store_true')
    parser.add_argument('--copy-today', help='Copy today\'s stand-up notes to the clipboard.', action='store_true')
    parser.add_argument('--copy-tomorrow', help='Copy tomorrow\'s stand-up notes to the clipboard.',
                        action='store_true')
    parser.add_argument('--edit-yesterday', help='Edit yesterday\'s stand-up notes.', action='store_true')
    parser.add_argument('--edit-today', help='Edit today\'s stand-up notes.', action='store_true')
    parser.add_argument('--edit-tomorrow', help='Edit tomorrow\'s stand-up notes.', action='store_true')
    arguments = parser.parse_args()
    
    load_dotenv()

    # sys.argv includes a list of elements starting with the program name
    if len(sys.argv) < 2:
        parser.print_usage()
        sys.exit(1)

    standup_notes_dir = os.getenv("STANDUP_NOTES_DIR")

    if not os.path.exists(standup_notes_dir):
        os.mkdir(standup_notes_dir)

    if arguments.list:
        for note in reversed(sorted(os.listdir(standup_notes_dir))):
            print(os.path.join(standup_notes_dir, note))

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


def get_note_name(weekday: date):
    """Map the date to the proper path of the standup-notes file for the day."""
    return os.path.join(os.getenv("STANDUP_NOTES_DIR"), date.strftime(weekday, '%Y%m%d') + os.getenv("STANDUP_NOTES_EXT"))


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


if __name__ == '__main__':
    main()

