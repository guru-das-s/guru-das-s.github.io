Title: Configuring the Visual Studio Code vim extension
Date: Fri Sep  1

I just installed Visual Studio Code (VS Code) on my Arch Linux machine, and one
of the first things I did was to install the `vim` extension.

I love `vim` and so I needed its keybindings in VS Code. But it was missing a
couple of features I wanted, so I enabled them.

The shortcut to summon the Settings page is `Ctrl + ,`. Search for "vim
key bindings". The nice UI touch is that clicking on the `Vim: Insert Mode Key
bindings` directly opens up the `settings.json` file which you can then edit to
add config options as you please.

My `settings.json` (shortcut: `Ctrl + ,` ) looks like this:

```
{
    "keyboard.dispatch": "keyCode",
    "vim.normalModeKeyBindings": [
        {
            "before": [";"],
            "after": [":"]
        }
    ]
}
```

Explanations:

```
    "keyboard.dispatch": "keyCode",
```

I have remapped `Caps Lock` on my laptop to `Esc`. This is extremely convenient
for me as I can easily enter and exit Insert mode in `vim`. And, frankly, I
don't know how this is not the default - I wonder how people are okay with
reaching allll the way to the top left corner of the keyboard multiple times
per five seconds. Anyway, the above line enables VS Code to respect this
system-wide keymapping of mine. [ref] Source: [FAQ on VS Code Marketplace](https://marketplace.visualstudio.com/items?itemName=vscodevim.vim#-faq:~:text=I%27ve%20swapped%20Escape%20and%20Caps%20Lock)[/ref]

```
    "vim.normalModeKeyBindings": [
        {
            "before": [";"],
            "after": [":"]
        }
    ]
```

This is the equivalent of `nmap ; :` in `.vimrc`. This allows to me avoid the
focus- and productivity-destroying `Shift + ;` to enter Command-line mode from
Normal mode.

With these, I am a happy bunny using VS Code on my laptop!

---
