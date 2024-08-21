#Enable colors and change prompt:
autoload -U colors && colors
#PS1="%B%{$fg[red]%}[%{$fg[yellow]%}%n%{$fg[blue]%}%~%{$fg[red]%}]%{$reset_color%}$%b "
PS1="%B%{$fg[red]%}%n%{$fg[green]%}%~ %{$reset_color%}%B>%b "
alias ls='ls --color=auto'
alias ..="cd .."
alias e='exit'
alias c='clear'
alias deutsch='setxkbmap -layout "de"'
alias config='/usr/bin/git --git-dir=$HOME/.dotfiles/ --work-tree=$HOME'
alias cd='z'
alias fetch='fastfetch'

# History in cache directory:
HISTSIZE=10000
SAVEHIST=10000
HISTFILE=~/.cache/zsh/history

# Basic auto/tab complete:
autoload -U compinit
zstyle ':completion:*' menu select
zmodload zsh/complist
compinit
_comp_options+=(globdots)        # Include hidden files.

bindkey '^[[H' beginning-of-line
bindkey '^[[F' end-of-line
bindkey '^[[1;5C' forward-word
bindkey '^[[1;5D' backward-word
bindkey '^[[3~' delete-char
bindkey '^H' backward-kill-word

eval "$(zoxide init zsh)"

export PATH=$PATH:/home/benkenobi/.local/bin

if [ -n "$PS1" ] && [ -z "$TMUX" ]; then
  tmux new-session -A -s 0
fi


source ~/.zsh/catppuccin-zsh-syntax-highlighting.zsh
source ~/.zsh/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh
source ~/.zsh/zsh-autosuggestions/zsh-autosuggestions.zsh
