Title: TIL: How to unify all three of Ubuntu's clipboards
Date: 2024-03-02T18:24:00-08:00
url: til/single-clipboard-ubuntu
save_as: til/single-clipboard-ubuntu.html
tldr: Make Ubuntu share one single clipboard for easy copy-pasting using both mouse as well as standard keyboard shortcuts.

Yes, you read that right - Ubuntu (which uses the X server) has a grand total of
*three* clipboards: As the Inter-Client Communication Conventions Manual (ICCCM)
[explains](https://x.org/releases/X11R7.6/doc/xorg-docs/specs/ICCCM/icccm.html#:~:text=large%20data%20transfers.-,Use%20of%20Selection%20Atoms,-Defining%20a%20new):

> Selection Atoms
>
> There can be an arbitrary number of selections, each named by an atom. To conform
> with the inter-client conventions, however, clients need deal with only these three
> selections:
>
> * PRIMARY
> * SECONDARY
> * CLIPBOARD

Of these, only `PRIMARY` and `CLIPBOARD` are commonly used by applications. As
`freedesktop.org`
[explains](https://specifications.freedesktop.org/clipboards-spec/clipboards-latest.txt):

> There are two historical interpretations of the ICCCM:
>
> a) use PRIMARY for mouse selection, middle mouse button paste, and
>    explicit cut/copy/paste menu items (Qt 2, GNU Emacs 20)

> b) use CLIPBOARD for the Windows-style cut/copy/paste menu items;
>    use PRIMARY for the currently-selected text, even if it isn't
>    explicitly copied, and for middle-mouse-click (Netscape, Mozilla,
>    XEmacs, some GTK+ apps)
>
> No one ever does anything interesting with SECONDARY as far as I can
> tell.

##### What led me to this discovery? <a name="copyways"></a>

There are two main ways to copy and paste stuff from one application to another on
Ubuntu:

1. Select text using mouse, `Ctrl-C`, `Ctrl-V`
2. Select text using mouse, paste using middle click of mouse.

It was when I found myself naturally mixing up these two methods and expecting this
unsupported hybrid scheme to work that I grew frustrated and decided to investigate
why the scheme that occurred to me naturally did not, in fact, work. Allow me to
explain using a couple of scenarios.

##### Terminal &rarr; Terminal

As a heavy terminal and `tmux` user, my workflow involves frequently copying stuff I
use `tmux`, so I need to copy stuff from one tmux pane to another. To achieve this, I
use the second method above.

This is intuitive to me because the two operations occur in the same application and
what the mouse selects, it copies, too. The first method also works, albeit with a twist:
need to use `Ctrl-Shift-C` and `Ctrl-Shift-V`. So this is technically a _third_ way
of copying and pasting on Ubuntu.

##### Non-terminal application &rarr; non-terminal application

Example: copying from one Google Chrome tab to another.

Here, the first method is intuitive to me because it is what has been ingrained in me
from a young age thanks to Windows.

##### Non-terminal application &rarr; Terminal

Example: copying from Google Chrome to the terminal.

Here, too, the first method is intuitive to me, albeit with a twist. The twist is
that you need to paste using `Ctrl-Shift-V` in the terminal. So this is technically a
_fourth_ way of copying and pasting on Ubuntu.

##### Terminal &rarr; non-terminal application

Example: copying from the terminal to Google Chrome.

Here is where my brain crosses out disruptively. What is intuitive to me is copying
by selecting the text using the mouse, and pasting using `Ctrl-V`. This does not
work. This is what is intuitive to me because I used PuTTy on Windows for a long time
for work and this is how it works there.

Really, this was the main use case that frustrated me because I frequently have to
look up a compilation error message, or copy some logs to a chat client. I would
select to copy using the mouse, paste using `Ctrl-V`, fail, then middle-click. I did
this so many times that I found it disruptive to my workflow and had to fix this.

##### The fix: unify both clipboards

Install [autocutsel](https://www.nongnu.org/autocutsel/) and add this to your
`.bashrc`:

```bash
autocutsel -s CLIPBOARD &
autocutsel -s PRIMARY   &
```

Now, Ubuntu behaves as though there is only a single, common clipboard for all
applications - terminal or otherwise. To add to the [above list](#copyways), you now
can:

3. Select text using mouse, `Ctrl-C`, paste using middle click of mouse.
4. Select text using mouse, paste using `Ctrl-V`

You can also go one step further and unify the third clipboard too, but I have not
tried this out personally.

```bash
autocutsel -s SECONDARY &
```

StackOverflow helped me a lot [ref][Merge primary and clipboard X
selections](https://unix.stackexchange.com/questions/628492/merge-primary-and-clipboard-x-selections)
[/ref] [ref] [How can I merge the gnome clipboard and the X
selection?](https://superuser.com/questions/68170/how-can-i-merge-the-gnome-clipboard-and-the-x-selection)
[/ref] while researching this fix and learning more about the underlying architecture.

---
