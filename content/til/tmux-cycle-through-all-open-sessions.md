Title: TIL: Easily cycle through all open tmux sessions
Date: 2024-03-30T08:32:00-07:00
url: til/tmux-cycle-through-all-open-sessions/
save_as: til/tmux-cycle-through-all-open-sessions/index.html
tldr: tmux configuration options and keybindings to easily cycle through all open sessions with very few keystrokes
Tags: tmux

My `tmux` workflow thus far has been strictly windows- and panes-based, meaning I
usually launch only one tmux session and then create named windows and panes
(horizontal and vertical splits) as necessary to deal with the set of projects for
the day. While this works well, things get quickly out of hand when there is some
firefighting to be done and context-switching between the projects is frequent,
involving creating new windows to explore new ideas. 

I draw the line at nine open windows because that's the maximum number of windows I
can quickly jump to with one keystroke using the `prefix + <number>` keyboard
shortcut. I have no interest in dealing with double-digit numbers of windows. But
what if I have, say, three different projects to work on during the day, and I "run
out" of windows? This week, I realized that there is a better way to effect a clean
context switch and also organize my tmux windows better: by using the native sessions
feature.

`man tmux` has this to say about sessions:

>_When tmux is started, it creates a new session with a single window and displays it
on screen.  A status line at the bottom of the screen shows information on the
current session and is used to enter interactive commands._

> _A session is a single collection of pseudo terminals under the management of tmux.
Each session has one or more windows linked to it. [...] and any
number of windows may be present in the same session.  Once all sessions are killed,
tmux exits._

| Command                    | Comment                                             |
|----------------------------|-----------------------------------------------------|
| `tmux`                     | Launch new unnamed `tmux` session                   |
| `<prefix> + $`             | From within `tmux`, rename current session          |
| `tmux new -s <session>`    | Launch new session named `<session>`                |
| `tmux ls`                  | List all open `tmux` sessions                       |
| `<prefix> + s`             | List all open `tmux` sessions from within a session |
| `tmux attach -t <session>` | Attach to an open session named `<session>`         |
| `<prefix> + d`             | From within `tmux`, detach from current session     |

[Adding these
lines](https://github.com/guru-das-s/dotfiles/commit/8fd159707076a5b8a594bf4f6cb1a716042829da)
to my `.tmux.conf` solved my issue:

```bash
# Easily cycle between open tmux sessions
unbind (
bind-key 0 switch-client -p
unbind )
bind-key = switch-client -n
```

Turns out that `<prefix> + (` or `)` enables switching to the previous or next open
session. I find this cumbersome because of the need to use the `Shift` key and so I
remapped them to single keys. Now I can easily cycle through all my open sessions
using `<prefix> + 0` or `<prefix> + =`.

And, since I have this ability, I can happily create as many new sessions as I
need - one per project - without having to fear using the `Shift` key to type in the
paranthesis characters each time I want to switch to another session I created.

You may well wonder how I could access the `0`-th pane if `<prefix> + 0` has been
re-bound as above. I don't, because I don't have a `0`-th pane at all. I number my
panes starting from `1` and not `0` via these lines:

```bash
# Start windows and panes at 1, not 0
set -g base-index 1
setw -g pane-base-index 1
```

And for good measure and clean pane number management:

```bash
# Automatically renumber all windows/panes when one is killed
# e.g. 1 2 [3] 4   .... 3 is killed, results in:
#      1 2 3       .... and not 1 2 4, which would call for a :movew -r
set -g renumber-windows on
```

And I chose `=` to switch to the next session because of its proximity to the
`Backspace` key (easier to reach).

Bottom line: my workflow is now the following.

1. Open terminal, navigate to project directory, launch first `tmux` session
2. Create/kill as many windows and panes I need
3. If I need to switch to a new project, detach from current session
4. Navigate to new project directory, launch new session
5. Cycle through open sessions using `<prefix> + 0` or `<prefix> + =`
    - I mostly end up using only the latter because of its proximity to the Backspace
        key.

The explicit switching from one session to another not only separates one project's
windows from another in `tmux`, making for clean organization, but also helps me
context-switch in my mind more effectively.
