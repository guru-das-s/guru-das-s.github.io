Title: TIL: Execute current line in vim
Date: 2024-07-29T22:52:04-07:00
url: til/vim-execute-current-line-in-bash/
save_as: til/vim-execute-current-line-in-bash/index.html
tldr: How to easily execute the currently highlighted line in vim
Tags: vim

I write a lot of notes in Markdown on a daily basis as a sort of personal wiki.
Almost all of them contain code snippets - shell commands, mostly. Today I learnt
that there is a much better way to directly execute a shell command listed on its own
in a single line in `vim`.

Two ways, in fact.

# The first

```bash
.w !bash
```
The fullstop character used here has special significance - it refers to the current
line. From `:help cmdline-ranges`:

```
Some Ex commands accept a line range in front of them.  This is noted as
[range].  It consists of one or more line specifiers, separated with ',' or
';'.

...

Line numbers may be specified with:		:range {address}
    {number}        an absolute line number  E1247
    .               the current line			    :.
```

The space between the `w` and the `!` is important here. Without it, the current file
would be saved with filename `bash`, which is not what we want to happen.

From `:help !`:
```
4.1 Filter commands					*filter*

A filter is a program that accepts text at standard input, changes it in some
way, and sends it to standard output.  You can use the commands below to send
some text through a filter, so that it is replaced by the filter output.
Examples of filters are "sort", which sorts lines alphabetically, and
"indent", which formats C program files (you need a version of indent that
works like a filter; not all versions do).  The 'shell' option specifies the
shell Vim uses to execute the filter command (See also the 'shelltype'
option).  You can repeat filter commands with ".".  Vim does not recognize a
comment (starting with '"') after the `:!` command.

							*!*
!{motion}{filter}   Filter {motion} text lines through the external
                    program {filter}.

```
# The second

The second method is also documented a few lines from above:
```
							*!!*
!!{filter}          Filter [count] lines through the external program
                    {filter}.
```
Just need to say `!!bash` (note: no preceding `:`).

But this will overwrite the contents of the current line with the output of the
command in that line.

# Addendum

This same trick can be used to insert a date in a Markdown file: `!!date`
