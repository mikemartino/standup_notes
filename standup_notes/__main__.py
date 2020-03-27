#!/usr/bin/python3

import os
import sys
from argparse import ArgumentParser, Namespace
from datetime import datetime, timedelta

import editor
import pyperclip

EXT = '.standup-notes.txt'
STANDUP_NOTES = os.path.join(os.environ.get("HOME"), 'Desktop/standup-notes')
STANDUP_TEMPLATE = os.path.join(os.path.dirname(__file__), 'standup.template')


def main(arguments: Namespace):
    today = datetime.strftime(datetime.now(), '%Y%m%d')
    today_note = os.path.join(STANDUP_NOTES, today + EXT)
    tomorrow = datetime.strftime(datetime.now() + timedelta(days=1), '%Y%m%d')
    tomorrow_note = os.path.join(STANDUP_NOTES, tomorrow + EXT)

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
        with open(STANDUP_TEMPLATE, 'r') as f:
            editor.edit(note, f.read())


def read_note(note):
    """Print the note if it exists."""
    if os.path.exists(note):
        with open(note, 'r') as f:
            print(f.read())
    else:
        print(note + ' doesn\'t exist yet.')


parser = ArgumentParser()
parser.add_argument('--list', help='List all stand-up notes.', action='store_true')
parser.add_argument('--read-today', help='Read today\'s stand-up notes.', action='store_true')
parser.add_argument('--read-tomorrow', help='Read tomorrow\'s stand-up notes.', action='store_true')
parser.add_argument('--copy-today', help='Copy today\'s stand-up notes to the clipboard.', action='store_true')
parser.add_argument('--copy-tomorrow', help='Copy tomorrow\'s stand-up notes to the clipboard.', action='store_true')
parser.add_argument('--edit-today', help='Edit today\'s stand-up notes.', action='store_true')
parser.add_argument('--edit-tomorrow', help='Edit tomorrow\'s stand-up notes.', action='store_true')
args = parser.parse_args()

# sys.argv includes a list of elements starting with the program name
if len(sys.argv) < 2:
    parser.print_usage()
    sys.exit(1)

main(args)
