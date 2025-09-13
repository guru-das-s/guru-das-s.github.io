Title: TIL: Show current C function in vim status line sans plugins
Date: 2024-03-13T00:10:11-07:00
url: til/vim-show-current-c-function/
save_as: til/vim-show-current-c-function/index.html
tldr: A very useful plain vanilla vimscript function to display the function the cursor is currently at, in the vim statusline.
Tags: vim

I primarily work on the Linux kernel (which is written almost entirely in C) and I
frequently find myself needing to know which function I'm currently in while browsing
the codebase. There is, of course, the dictum that functions should be as small as
possible and not more than a screen's length long; this is mostly just a guiding
principle.

There are plugins to do this sort of thing, but I do not want to become overly
dependent on them. I am more partial towards things I can use that are just plain
vanilla vimscript because I can just stick them in my `.vimrc` when setting up a new
workstation or logging into a remote server somewhere.

# The function

Here's the function in all its inscrutable beauty:

```vim
" Show function name on demand, mapped to key ','
fun! ShowFuncName()
	echohl ModeMsg
	echo getline(search("^[^ \t#/]\\{2}.*[^:]\s*$", 'bWn'))
	echohl None
endfun

nmap , :call ShowFuncName()<CR>
```

I couldn't locate the StackOverflow answer I had sourced this from (even though this
post says TIL, I did not learn this *literally* today) so I used [Gemini
AI](https://gemini.google.com/app) to break this down for me.

# The breakdown

`echohl ModeMsg`: Sets the highlighting for the echo output to the mode message
style. This ensures the function name visually stands out.

`getline(search("^[^ \t#/]\\{2}.*[^:]\s*$", 'bWn'))`: This line is the core
logic for finding the function name. Let's break down the search pattern:

- `^[^ \t#/]` - Matches the beginning of the line (`^`) and excludes whitespace (` ` and `\t`), tabs (`/`), and comments (`#`).
- `\\{2}` - Matches exactly two characters (the function name can have at least two characters).
- `.*` - Matches any characters (captures the function name).
- `[^:]` - Excludes the colon (`:`) which might follow the function name.
- `\s*$` - Matches whitespace at the end of the line.
- `bWn` - Flags:
    * `b` - Starts searching backward from the current line.
    * `W` - Considers word boundaries.
    * `n` - Doesn't include the matching pattern in the returned line.

This search essentially finds the line before the current line that starts with
two non-whitespace, non-tab, non-comment characters, followed by any characters
(the function name), excluding the colon and ending with whitespace.

`echo`: Prints the captured line containing the function name.

`echohl None`: Resets the highlighting back to the default.

# The demo

If you were at [this
line](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/drivers/mfd/qcom-pm8008.c?h=v6.8#n178)
in `drivers/mfd/qcom-pm8008.c` (which is a driver I authored) and pressed `,`
to trigger the above command, you would see this in the vim statusline:

```c
static int pm8008_probe(struct i2c_client *client)
```

which is, in my view, a very clean way of doing things.
