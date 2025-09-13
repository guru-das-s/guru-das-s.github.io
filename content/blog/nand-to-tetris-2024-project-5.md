Title: Nand2Tetris - Projects 4 to 5
Date: Wed Aug 28 12:03:11 AM PDT 2024
tldr: How I built my own Nand2Tetris Hack computer by creating a CPU, Memory unit and ROM and wiring them all together
Tags: nand2tetris, opensource

Continuing from [where I left off]({filename}nand-to-tetris-2024-project-3.md) in my
[Nand2Tetris](https://www.nand2tetris.org/course) journey, I went ahead and completed
Projects 4 (Machine Language) and Project 5 (Computer Architecture) and I now have
"built" my very own Hack computer from scratch!

Follow my progress on Github here:
[guru-das-s/nand2tetris](https://github.com/guru-das-s/nand2tetris/commits/master/).

# Project 4: Machine Language

This project introduces the Hack instruction set architecture (ISA) and assembly
language corresponding to the Hack computer we're building, and tasks the student
with writing two programs that provide a good understanding and feel for the
platform.

The first program, `Mult.asm` is quite straightforward - to multiply two numbers.

The second program, `Fill.asm` has a particularly satisfying end result - to turn the
screen in the CPU Emulator completely black or white based on keyboard input.

I haven't written a lot of assembly code, so it was very gratifying to reason about a
problem in terms of assembly and write code while conforming to the constraints of
the ISA.

# Project 5: Computer Architecture

This is the first big project in the course according to me, and the most climactic
so far, as we progressively build:

1. a Memory unit from the RAM chips built earlier,
2. a CPU from the ALU built earlier,

and finally wire them both together along with a ROM unit (separate instruction and
data memories), thus creating a full-fledged Hack computer that can load and execute
any arbitrary program!

The textbook chapter says it best:

> _The computer that will emerge from this project will be as simple as possible, but
> not simpler._

It's true - this computer does not have fancy stuff like pipelining, or branch
predictors or caches of any kind. It also implements the Harvard architecture -
separate instruction and data memories instead of the Von Neumann architecture model.

**The Memory unit**

The memory unit consists of a 16K RAM, a memory-mapped screen, and a memory-mapped
keyboard all laid out adjacent to each other with no holes.

**The CPU**

This is the crux of the whole project - decoding an instruction from its bits and
figuring out what action needs to take place for it. To that end, various bits and
bitfields of the instruction encode specific pieces of information, like the type of
ALU operation that needs to take place, where to store the results of the operation,
and what kind of jump is requested.

The challenge in this part of the project is to route various bits and bitfields of
the 16-bit instruction to the A, D and PC registers and implement the
hardware-software contract.

There are a couple of gotchas that make things interesting when testing the code
using the provided tests. I caught [one edge
case](https://github.com/guru-das-s/nand2tetris/commit/582b905ef29b420295ecda1bcef1e9d9e6605ead)
only when running the test for the next part of the project, i.e. building the
Computer.

`DMux8Way` saved my ass in both the Memory and CPU parts of this project. It took me
a while to recognize that the logic for powering the jump detection could easily make
use of this building block - a side effect of not being a hardware guy, I suppose.

**The Computer**

After the rigours of the CPU design part of the project, this turned out to be
relatively straightforward. Just three lines of code wiring the ROM, RAM and CPU
together.

# Looking ahead

The next project, Project 6, is to build an assembler that converts Hack assembly
code into binary. I've not attempted something of this nature before, and am really
excited about this!
