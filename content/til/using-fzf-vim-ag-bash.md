Title: TIL: The fzf fuzzy finder is amazing
Date: Sat Dec 14 05:28:27 PM PST 2024
url: til/using-fzf-vim-ag-bash/
save_as: til/using-fzf-vim-ag-bash/index.html
tldr: How I use the fzf fuzzy finder tool in conjunction with bash, vim and the silver searcher ag
Tags: vim, terminal, git

[`fzf`](https://github.com/junegunn/fzf) is a general-purpose fuzzy text matching
tool at its core that takes in a list of newline-separated text and allows the user
to search for something within those lines and select one or more of the lines by
typing just a few character sequences into a search field. It is highly customizable
and the maintainer seems to have a good head on his shoulders. I recently started
using it after a colleague introduced me to it and it has improved my developer
workflow tremendously.

Here are some of the actions and workflows I use `fzf` for, multiple times on a daily
basis.

# Opening files in vim within current directory

From the shell, it is easy to search for a file within the current directory
(recursively) and open it in `vim`. I have this Bash alias that does that for me with
just one keystroke:

```bash
alias f='vim $(fzf)'
```

It is easy to do this from within an open `vim` session as well. For this, I use the
[`fzf.vim` plugin](https://github.com/junegunn/fzf.vim) with these lines in my
`.vimrc`:

```vim
nnoremap <C-f> :GFiles<CR>
let g:fzf_action = {
        \ 'ctrl-l': 'split',
        \ 'ctrl-h': 'vsplit' }
```

The above config allows me to use `Ctrl + F` from within vim to bring up a list of
all the files known to Git in that directory (`GFiles` = Git Files). From the
plugin's documentation, one can remap that key combination to just `:Files` as well
for directories that are not git repositories. I can then search for the file I want
and then open it in a horizontal or vertical split with `Ctrl + L` or `Ctrl + H`.

# ag integration from within vim

I use `ag` (the "silver searcher") instead of `grep`, and the `fzf.vim` plugin
supports this natively. I just had to make [a couple of
customizations](https://github.com/guru-das-s/fzf.vim/commits/master/) for my
convenience:

1. I [renamed][fzf-renamed] the invocation command from `:Ag` to `:A`, thereby saving
   one precious keystroke.
2. The vimscript helper function that fashions the invocation parameters to `ag`
   sets the search query to `'^(?=.)'` by default if a search term is not provided.
   The effect of this is that `ag` will print out every single line of every single
   file in the repo if `:A` is invoked as such without the search parameter, which
   makes no sense.<br>
   So instead, I [changed][fzf-changed] the default search query to
   `expand("<cword>")` in case of an empty search query.  The effect of this is that
   I can just place my cursor on a word and then say `:A` to search for that word,
   which is highly effective.

# Bash alias to add filename in REPL prompt

Adding this line to `~/.bashrc` adds the default fzf bindings for bash:

```bash
[ -f ~/.fzf.bash ] && source ~/.fzf.bash
# Set up fzf key bindings and fuzzy completion
eval "$(fzf --bash)"
```

Now, `Ctrl + T` brings the power of `fzf` to locating deeply-nested build artifact
files and using them in a command you're building on the fly at the REPL shell
prompt.

# Bash alias for git log

The single most frequent use case is browsing git log output with `fzf`. This is how
I've hooked things up - and a warning: it's not that pretty to look at, but gets the
job done, and well.

```bash
export FZF_O_OPTS="--ansi --color=16 --no-mouse --multi --track --tac --disabled --no-print-query --bind j:down,k:up,q:abort"

function do_o() { git log --color=always --oneline --decorate ${2:-} ${1:-} | fzf $FZF_O_OPTS --preview "git show --color=always {1}"; }
function do_O()
{
    local num_commits="${2:-}"
    local path=${1:-}
    local commit=$(do_o "$path" "$num_commits" | awk "{print \$1}")
    if [[ -n $commit ]]; then
        git show --color=always -U10 --stat $commit
    fi
}

function o() { local path=${1:-}; do_O "$path" "-10"; }
function oo() { local path=${1:-}; do_O "$path" "-20"; }
function ooo() { local path=${1:-}; do_O "$path" "-30"; }
function O() { local path=${1:-}; do_O "$path"; }
```

Saying `o` at the terminal thus produces a `fzf` window containing the 10 most recent
commits with the highlighted commit `git-show`n in the preview pane for easy review.
One can easily cycle up and down the commits via the `j` and `k` keys, vim-style.

Since I do not care about searching for a specific commit in this mode, I pass
`--disabled` to the `fzf` invocation options. Instead, I've chosen to make browsing
through the list easier by binding the `j` and `k` keys vim-style, saving on having
to hold `Ctrl` down otherwise.

If there is a specific commit I want to inspect further, I simply finalize the `fzf`
selection via `Enter`, which then prints out the whole commit with `git show -U10
--stat` for full review.

Since I typically make lots of tiny commits as I develop a feature, I end up with
dozens of atomic commits that I later would need to squash together or prune, which
requires reviewing all of them in rapid succession. For this reason, I have the
functions `oo()` and `ooo()` that show me the latest 20 and 30 commits, respectively,
with the same behaviour as above. Finally, there's also `O()` (capital O) that just
lists _all_ the commits of the repo without any limits.

I came across the `fzf` maintainer's [suggested plumbing][plumb] for this same
feature, but I have not tried it out personally as I am quite happy with my own
solution.

[fzf-renamed]: https://github.com/guru-das-s/fzf.vim/commit/07792d18f86aed8853c5bbfa62eb6db871d81551
[fzf-changed]: https://github.com/guru-das-s/fzf.vim/commit/a9f45fe47b10bdfd0b88efbe36ae02175fc6f2cf
[plumb]: https://gist.github.com/junegunn/f4fca918e937e6bf5bad
