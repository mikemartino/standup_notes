#/usr/bin/env bash

_standup_completions()
{
    local cur opts prev prev2
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
    prev2="${COMP_WORDS[COMP_CWORD-2]}"

    opts="-l --list -r --read -c --copy -e --edit -d --delete -p --post -x --editcopy"
    days="--today --tomorrow --yesterday"

    case "${prev}" in
      -l | --list | -d | --delete | --today | --tomorrow | --yesterday)
        return 0
        ;;
      -c | --copy | -e | --edit | -r | --read | -x | --editcopy | -p | --post)
        if [ "$prev2" = "--yesterday" ] || [ "$prev2" = "--today" ] ||[ "$prev2" = "--tomorrow" ] ; then
          return 0
        fi
        COMPREPLY=( $(compgen -W "${days}" -- ${cur}))
        return 0
        ;;
      *)
      ;;
    esac
    COMPREPLY=( $(compgen -W "${opts}" -- ${cur}))
}
complete -F _standup_completions standup-notes