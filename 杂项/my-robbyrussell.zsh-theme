local ret_status="%(?:%{$fg_bold[green]%}:%{$fg_bold[red]%})"
local xx="%{$fg_bold[green]%}%n%{$fg[cyan]%}@%{$fg_bold[green]%}%m%{$fg_bold[green]%}%p:"
PROMPT='${xx}${ret_status}%{$fg[cyan]%}%d%{$reset_color%} $(git_prompt_info)$ '
ZSH_THEME_GIT_PROMPT_PREFIX="%{$fg_bold[blue]%}git:(%{$fg[red]%}"
ZSH_THEME_GIT_PROMPT_SUFFIX="%{$reset_color%} "
ZSH_THEME_GIT_PROMPT_DIRTY="%{$fg[blue]%}) %{$fg[yellow]%}✗"
ZSH_THEME_GIT_PROMPT_CLEAN="%{$fg[blue]%})"
