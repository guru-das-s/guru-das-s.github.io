Title: Nand2Tetris - Projects 1 to 3
Date: 2024-04-13T11:53:34-07:00
tldr: My account of taking the NAND2Tetris course in 2024, up until Project 3: Sequential logic and memory
Tags: nand2tetris, opensource

[Nand2Tetris](https://www.nand2tetris.org/) is a very interesting "learning by doing"
free and open-source course that enables one to learn how a computer is designed from the
ground up, and also how it is programmed from the very lowest of levels. It is a
fantastic course offered in two parts (first building the hardware for the computer,
and then the software) and is very rewarding to those who finish it. I started
working on it this year after having discovered it via [Hacker
News](https://news.ycombinator.com/item?id=38735066) and have completed Projects 1 to
3 of 12 projects in total. You may follow my progress on Github here:
[guru-das-s/nand2tetris](https://github.com/guru-das-s/nand2tetris/commits/master/).

The [projects](https://www.nand2tetris.org/course) in this course start from
designing various boolean gates using NAND gates as a building block and slowly build
upon each other to create a full-fledged computer, complete with its own corresponding
assembler, compiler and operating system, thus allowing for running rich and
complex full-featured programs such as
[Tetris](https://en.wikipedia.org/wiki/Tetris).

My motivation for starting and committing to this project is to fill in any gaps in
my understanding of how computing systems work, from the application layer down to
the individual components. Modern-day computer architectures such as x86 and ARM have
many layers of optimization and complexity to achieve industrial levels of
performance. This course pares away all inessential elements during the design
process, retaining only clean and simple elements for illustrating the basic
concepts. Most of all, I *love* the 100% hands-on approach because I learn better by
*doing*.

Here are some thoughts and observations on each of the projects I've completed so
far:

# Project 1: Boolean logic

1. This project is about creating gates such as OR, NOT, and MUX along with their
   16-bit versions using basic Boolean logic. The NAND gate is provided as a
   fundamental building block (no need to build it).
2. This introduces the Hardware Simulator Java program, the custom Hardware
   Description Language (HDL) and the whole write-test-debug iteration cycle.
3. Being an software guy myself, writing and thinking in HDL was a pleasant
   challenge. I didn't get to do much of this during my undergrad which was not all
   that electronics-focused, so it was quite enjoyable to do it now.
4. I noticed that a couple of test scripts and "ground-truth" comparison files
   provided in the project's source code were incorrect and had to fetch the right
   versions from poking around on Github. I also sent the Nand2Tetris admins an email
   about this; Prof. Shimon responded, acknowledging a recent issue with the software
   suite.
5. Overall, this project was very satisfying and straightforward.

# Project 2: Boolean arithmetic and building an ALU

1. The concept of two's complement was explained clearly with motivation for its
   existence, and illustrated with examples of subtraction and addition with
   overflow.
2. The most thrilling part of this project was to build an Arithmetic and Logic Unit
   from scratch, and really understand how various operations could be built using
   just addition and subtraction.
3. The ALU is to be built in two stages. I thought the first stage was going to be
   difficult (getting all the operations right) and the second stage (detecting
   negative numbers and zero in the output), easy. It was the opposite - I struggled
   with the second stage mostly because I didn't know a quirk of the HDL's syntax. I
   had to read the HDL Guide and also consult the
   [forum](http://nand2tetris-questions-and-answers-forum.52.s1.nabble.com/) for
   guidance.

# Project 3: Building RAM chips

1. This project introduces sequential logic and building a 16K Random Access Memory
   (RAM) chip using banks of registers, which are built from individual registers
   which, in turn, are built from Bits. The D Flip-flop is provided as a fundamental
   building block (no need to build it).
2. This was a very satisfying project to do because working with sequential logic was
   a nice change after two projects of combinatorial logic.
3. Once the basic RAM8 was complete (RAM chip containing just 8 registers), it was a
   breeze to complete the other larger RAM chips, *mutatis mutandis*.
4. Creating the Program Counter (PC) was also very interesting because of the clever
   ways in which internal pins need to be used.

# Looking ahead

Things start to get even more interesting from Project 4 onward. It is about learning
the assembly language of the particular computer that is being built and writing
programs in it using the reference assembler provided. Project 5 is to create a full
computer using the ALU and RAM that were just built earlier, and Project 6 is to
write an assembler in any high-level language, to replace the provided assembler.

Really excited for the upcoming projects!
