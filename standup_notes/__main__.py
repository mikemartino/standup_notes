import os
import sys
from argparse import ArgumentParser, Namespace
from datetime import date, timedelta
from pkg_resources import resource_stream

import editor
import pyperclip

EXT = '.standup-notes.txt'
STANDUP_NOTES = os.path.join(os.environ.get("HOME"), 'Desktop/standup-notes')
STANDUP_TEMPLATE = resource_stream('standup_notes.resources', 'standup.template')

def main():
    parser = ArgumentParser()
    parser.add_argument('--list', help='List all stand-up notes.', action='store_true')
    parser.add_argument('--read-today', help='Read today\'s stand-up notes.', action='store_true')
    parser.add_argument('--read-tomorrow', help='Read tomorrow\'s stand-up notes.', action='store_true')
    parser.add_argument('--copy-today', help='Copy today\'s stand-up notes to the clipboard.', action='store_true')
    parser.add_argument('--copy-tomorrow', help='Copy tomorrow\'s stand-up notes to the clipboard.', action='store_true')
    parser.add_argument('--edit-today', help='Edit today\'s stand-up notes.', action='store_true')
    parser.add_argument('--edit-tomorrow', help='Edit tomorrow\'s stand-up notes.', action='store_true')
    arguments = parser.parse_args()

    # sys.argv includes a list of elements starting with the program name
    if len(sys.argv) < 2:
        parser.print_usage()
        sys.exit(1)

    today = date.strftime(date.today(), '%Y%m%d')
    today_note = os.path.join(STANDUP_NOTES, today + EXT)
    tomorrow = date.strftime(next_weekday(date.today()), '%Y%m%d')
    tomorrow_note = os.path.join(STANDUP_NOTES, tomorrow + EXT)

    if not os.path.exists(STANDUP_NOTES):
        os.mkdir(STANDUP_NOTES)

    if arguments.list:
        for note in os.listdir(STANDUP_NOTES):
            print(os.path.join(STANDUP_NOTES, note))

    if arguments.read_today:
        read_note(today_note)

    if arguments.read_tomorrow:
        read_note(tomorrow_note)

    if arguments.edit_today:
        edit_note(today_note)

    if arguments.edit_tomorrow:
        edit_note(tomorrow_note)

    if arguments.copy_today:
        copy_note(today_note)

    if arguments.copy_tomorrow:
        copy_note(tomorrow_note)


def copy_note(note):
    """Copy the note to the clipboard if it exists."""
    if os.path.exists(note):
        with open(note, 'r') as f:
            pyperclip.copy(f.read())
    else:
        print(note + ' doesn\'t exist yet.')


def edit_note(note):
    """Launches the default $EDITOR or a suitable default. If the note already exists, the editor opens it for editing.
    If the note does not exist, the editor opens a new file using the stand-up template."""
    if os.path.exists(note):
        editor.edit(note)
    else:
        # Note: It appears that the file will be saved regardless of what you do in your editor (in my case, vim).
        editor.edit(note, STANDUP_TEMPLATE.read())


def read_note(note):
    """Print the note if it exists."""
    if os.path.exists(note):
        with open(note, 'r') as f:
            print(f.read())
    else:
        print(note + ' doesn\'t exist yet.')


def next_weekday(day: date) -> date:
    tomorrow = day + timedelta(days=1)
    day_num = tomorrow.weekday()
    # Monday - Friday (0-4), Saturday(5), Sunday(6)
    if day_num < 5:  # Weekday
        return tomorrow
    else:  # Weekend
        return next_weekday(tomorrow)


if __name__ == '__main__':
    main()

