#/usr/bin/env bash

_standup_completions()
{
    local cur prev opts
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
    first_arg="${COMP_WORDS[1]}"

    opts="-l --list -v --view -c --copy -e --edit -d --delete"
    days="--today --tomorrow --yesterday"

    case "${prev}" in
      -l | --list | -d | --delete | --today | --tomorrow | --yesterday)
        case "${first_arg}" in
          -e | --edit)
          COMPREPLY=($(compgen -W "-c --copy" -- ${cur}))
          return 0
          ;;
        esac
        return 0
        ;;
      -c | --copy| -e | --edit | -v | --view)
      if [ "${#COMP_WORDS[@]}" != "3" ]; then
        return
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