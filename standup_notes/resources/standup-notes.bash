#/usr/bin/env bash

_standup_completions()
{
    local cur prev opts base
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"

    opts="-l --list -v --view -c --copy -e --edit -d --delete"
    days="--today --tomorrow --yesterday"

    # echo "${COMP_CWORD}"

    case "${prev}" in
      -l | --list | -d | --delete | --today | --tomorrow | -yesterday)
        return 0
        ;;
      -c | --copy | -e | --edit | -v | --view)
        COMPREPLY=( $(compgen -W "${days}" -- ${cur}))
        return 0
        ;;
      *)
      ;;
    esac

    COMPREPLY=( $(compgen -W "${opts}" -- ${cur}))


}
complete -F _standup_completions standup-notes