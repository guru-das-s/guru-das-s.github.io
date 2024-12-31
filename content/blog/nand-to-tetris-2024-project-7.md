Title: Nand2Tetris - Project 7 (VM Translator Part 1)
Date: Wed Jan  1 09:58:42 AM PST 2025
tldr: Part one of the Nand2Tetris VM Translator in Rust, complete with code excerpts and rationale behind design choices made.
Tags: nand2tetris, rust, opensource

[Project 7][project7] of Nand2Tetris is about translating virtual machine [ref] No,
not [that][that-vm] virtual machine; rather, the Hack computer virtual machine
conceptualized as a [stack machine][stack-machine]. [/ref] (VM) commands for the Hack
computer platform to a series of Hack assembly language (asm) instructions. The main
focus of this project is determining the sequence of assembly language instructions
corresponding to each VM command, given that the programming model of the computer is
that of a [stack machine][stack-machine]. Here, VM commands are roughly equivalent to
[bytecode][bytecode]. The virtual machine translator that emerges from this project
shall form the backend of the compiler that shall be built upon it.

Continuing my Rust journey from [Project 6]({filename}nand-to-tetris-2024-project-6.md),
this blogpost describes in detail my solution to Project 7 in Rust.

The source code is here:
[guru-das-s/nand2tetris](https://github.com/guru-das-s/nand2tetris/tree/master/projects/7)

##### Problem description

What does a VM file even look like? Here's `SimpleAdd.vm`:

```
// Pushes and adds two constants.

push constant 7
push constant 8
add
```

This is the "bytecode" that the Jack language compiler (which will be introduced
later!) will compile to - the first of a two-step process of converting high-level
Jack language code to Hack asm code.

The goal of this project is to translate the above VM instructions to asm
instructions that effect the intended operations: `push` and `add` in the above
example. A stack area is assigned for us in the RAM of the Hack machine to be used in
the asm instructions. We are responsible for growing and shrinking the stack.

There are code segments other than `constant`, e.g. `BasicTest.vm`:
```
...
pop temp 6
push local 0
push that 5
add
push argument 1
sub
...
```
These segments all map to various designated sections of RAM. The `local` segment
starts from the RAM address stored in the `LCL` RAM address which, as we know from
the Assembler design from [Project 6]({filename}nand-to-tetris-2024-project-6.md), is
a synonym of `RAM[1]`. The `N` in `local N` specifies the offset that must be applied
to the base address stored in `LCL`, i.e. `RAM[LCL + N]`. That's just `local`, though
&ndash; other segments must be interpreted differently as specified in the design
instructions.

There are also operations other than `add` such as `sub` in the above example, all of
which operate on the stack. Being a binary operator needing two operands, `add` adds
the two top-most entries present on the stack. A unary operator such as `not` only
works on the top-most entry on the stack.

##### VM Translator &ndash; Code architecture

The basic idea animating the design of the VM Translator is twofold:

1. having stock "phrases" of asm code corresponding to each combination of arithmetic
   operation, segment, and VM command that are crafted with placeholder-stubs in
   place of the actual values involved in the computation of the offsets required,
   and
2. replacing those stubs with the actual correct values derived from parsing the vm
   commands.

The code is, thus, organized into five modules:

| # | Module         | Function                                                                 |
|---|----------------|--------------------------------------------------------------------------|
| 1 | `main.rs`      | Handles command line args, calls `parser` and `asmwriter`                |
| 2 | `spec.rs`      | Defines basic enums and structs to represent parsed VM commands          |
| 3 | `phrases.rs`   | Stubbed-out asm code fragments for every operation and code segment      |
| 4 | `parser.rs`    | Parses a `.vm` file and returns a `Vec` of `VmCommand`s                  |
| 5 | `asmwriter.rs` | Writes the asm code for each `VmCommand` in the `Vec` to the output file |

##### Development and testing workflow

The first step was to figure out the "phrases", i.e. the sequence of Hack asm
instructions, corresponding to a given vm command such as `push constant 7` and
`add`. But where does one start?

One starts by observing what is actually happening in the memory space when those
commands are being run. The stock `VMEmulator.sh` provides a powerful and convenient
GUI readout of the contents of the stack, RAM memory, the various code segments of
the Hack programming model and the ability to step through each VM command. Every
sample vm program provided has a corresponding `*VME.tst` that runs it on the VM
Emulator.

When the behaviour of the command under scrutiny is thus understood, the next logical
step is to actually write down &ndash; by hand &ndash; the asm instructions that make
those commands happen, and then run them on the stock `CPUEmulator.sh` that we
encountered in [Project 4]({filename}nand-to-tetris-2024-project-5.md). This requires
simulating the test setup conditions that the `*VME.tst` script uses.

For example: While working on the first test (`SimpleAdd.vm`), I ran
`SimpleAddVME.tst` on the VM Emulator and observed the (rather simple) effects on the
Stack Pointer and the Stack. I then inspected the VM test script and recreated what
it was doing by hand-coding its setup phase in asm &ndash; viz., initializing the
Stack Pointer to a small enough value that would be visible in the `CPUEmulator`
without having to scroll down. With this setup, I was able to write the
spectacularly-named `handcode/stuff.asm` (hehe) that helped me hash out the asm
instructions to `push` a few arbitrarily-chosen `constant`s and implement the binary
operator `add` and unary operator `not` for them, testing everything on the
`CPUEmulator`. I followed a similar approach for [the other][handcode] tests and
operations.

The next step was to generalize the phrases from the hand-coded asm files by
stubbing out the arbitrary values with placeholder text `"XYZ"` and code segment
names with `"SEG"` that would be substituted with the values from the parsed `.vm`
files by the VM Translator being developed.

After hooking up the parser logic and asm writer logic in the VM Translator, the
final step was to run the `*.tst` script for each test that would run the asm output file
generated by the VM Translator on the `CPUEmulator` and return success or failure. An
intermediate step was also to compare the asm output file with the one generated by
the stock `VMEmulator`.

##### Interesting problems

###### Labels must be unique for conditional operator phrases

This problem was encountered while working on the second test, `StackTest.vm`. Fresh
from having figured out the basic approach of the overall project in the first test,
`SimpleAdd.vm`, I plugged in the phrases for other arithmetic and conditional
operators, including `Equals`, `Lesser Than` and `Greater Than`, only to eventually
find that the assembler was not translating the labels within those phrases in the
expected manner.

To illustrate the problem: the hand-coded asm implementation of `Equals` is [as
follows][eq]:

```as
// Implement Eq
// ------------

// Get first parameter and store it in D
@SP
M=M-1
A=M
D=M
// D has first parameter now. Get second parameter next
@SP
M=M-1
// Second parameter is in RAM[SP], store it in A
// after dereferencing RAM[SP] which is a pointer
A=M
// M has second parameter now.
D=D-M
@SP
A=M
M=-1
@ISEQUAL
D;JEQ
// We will get here only if
// D is not zero, i.e. the two numbers
// are dissimilar.
@SP
A=M
M=!M
(ISEQUAL)
```
Notice the definition and use of the label `ISEQUAL`. The expectation is that this
label will resolve to the ROM address of the instruction right after `(ISEQUAL)`.

The phrases for the other two conditional operators mentioned above also follow a
similar structure, each using a label to conditionally skip over the result.

The problem occurs when the same phrase is plugged in multiple times in the same file
as the result of multiple occurrences of a conditional operator in the `.vm` file
being translated. When this happens, the label `(ISEQUAL)` is defined multiple times
and the assembler resolves it to the ROM address of the instruction after the _very
last occurrence of the label_. This leads to incorrect jump addresses for all the
other instances of the operator that come before the last occurrence.

It is thus evident that the label in the phrases for conditional operators have to be
made unique so that the assembler can resolve the labels separately. One way to make
this happen is to append a monotonically increasing variable to the label used in the
phrases. This implies the use of a local static variable (in C terms). Example:
instead of `(ISEQUAL)`, use `(ISEQUAL.0)`, `(ISEQUAL.1)`, `(ISEQUAL.2)`, et c.

I implemented local static variables in Rust using `OnceLock`[ref]
The use of the `Mutex` may be unnecessary and even overkill as this program is only
single-threaded. Using `std::sync::atomic` may be sufficient.[/ref]:

```rust
static E: OnceLock<Mutex<u16>> = OnceLock::new();
...
let e = E.get_or_init(|| Mutex::new(0));
...
let mut eq = e.lock().unwrap();
...
*eq += 1;
...
```

Correspondingly, the label in the phrase was amended to `(ISEQUAL.XYZ)` with the
above code replacing `XYZ` with the static variable `eq`[ref][Code
excerpt](https://github.com/guru-das-s/nand2tetris/blob/master/projects/7/vmt/src/spec.rs#L35-L40)
showing labels in conditional phrases being made unique.[/ref].

###### To increment SP, or not to increment SP?

The project instructions caution against forgetting to increment the Stack Pointer
(SP). The SP is to be incremented only for the arithmetic and logic operations
phrases, and not for the phrases that set each code segment's offset and calculate
its address.

###### Implementing the `pop` operation

Implementing the `pop segment i` operation was initially difficult to do without the
use of extra scratch registers &ndash; my [first attempt][unoptimized-pop] utilized
two. But something seemed fishy as running `BasicTestVME.tst` through the
`VMEmulator` did not show those two registers being touched at all:

```as
// Pop local 2 begins now
// ........................
// Step 1: Get value to pop
@SP
M=M-1
A=M
D=M
// Store it in first scratch register
// Only R13, R14 and R15 are free to use
// in my view, the TEMP segment taking up
// R5 - R12 for itself.
// The BasicTestVME.tst does not seem to be
// using R13 - R15 in my test run, or it
// must be cleverly clearing them to not
// give away this insight.
...
// Now, triumphantly do *(M[R14]) = M[R13]
// (R14 is a pointer)
@R13
D=M
@R14
A=M
M=D
```

It wasn't until later that it dawned on me that I could just [use the
stack][optimized-pop] instead.

```as
// Pop local 2 begins now
// ........................
// Step 1: Get data to pop
@SP
M=M-1
A=M
D=M
// Step 2: Push this data to stack
@SP
M=M+1
A=M
M=D
// Now last two elements in stack
// are the same, with SP pointing
// to the last NON-EMPTY element.
// Set SP to the second-to-last spot.
@SP
M=M-1
// Step 3: Calculate address to pop to
@LCL
D=M
@2
D=D+A
// Set SP to this value
@SP
A=M
M=D
// Increment SP
@SP
M=M+1
// Now last two elements of stack are
// (N-1) ----- address
// (N)   ----- data     <SP points here>
// Now, finish it off
@SP
A=M
D=M
@SP
M=M-1
A=M
A=M
M=D
// Now SP points to right place.
```
This, then, translated to a [two-part phrase][pop] for the operation: a preamble and the
actual operation.

###### Implementing the `static` code segment

The `static i` code segment needs to be translated to a variable `@FILE.i` where
`FILE` is the filename of the VM file being translated. Because of the good
level of code encapsulation in the project, it was possible to implement it like
this:
```rust
// XYZ will be handled by VmCommand::code_segment_i(), and
// FILE will be handled by Asmwriter::write().
pub const STATIC: &str = r#"// Push Static XYZ
@FILE.XYZ
A=M
D=A
"#;
```
This is the only point in the project (so far!) that the replacement logic spills
over to an unrelated module (`Asmwriter`):
```rust
    pub fn write(mut self) -> Result<(), Box<dyn Error>> {
        for vmcmd in self.vmcmds {
            let mut asm_code = vmcmd.code()?;

            asm_code = if vmcmd.arg1.is_some_and(|segment| segment == Segment::Static) {
                asm_code.replace("FILE", self.filename)
            } else {
                asm_code
            };

            writeln!(self.file, "{}", asm_code)?;
        }
        Ok(())
    }
}
```

##### What I learnt about Rust programming

New things I learnt about Rust and implemented in Project 7 that I did not in the
previous [Project 6]({filename}nand-to-tetris-2024-project-6.md):

- Followed the idiomatic way of defining a [constructor][rust-constructor] for
    `struct Parser` and `struct Asmwriter` structs and, thus, keeping the `main`
    module [simple][simple-main].
- Used the iterator methods `peekable()` and `peek()` to keep track of the current
    line in the `Vec` of lines constructed from `BufReader`. This helped the design
    conform to the suggested API of `advance()` in the parser.
- Used lifetimes for the first time to yoke the lifetime of a raw string to the
    struct it was embedded in (`struct Asmwriter`) and to store the `Peekable()` line
    iterator in `struct Parser`.
- Used the raw string literal `r#"<string>"#` [syntax][rawstring] to define multiline
    strings for each of the phrases. This made the asm sequences easy to write and
    iterate on.
- Added tests for the very first time: only for the parser, though &ndash; didn't
  have time for any other module.

##### Test script

I wrote a short shell script to ensure that the VM Translator passes all test cases.

```
$ ./projects/7/test.sh && echo "All test cases passed"
    Finished `release` profile [optimized] target(s) in 0.14s
     Running `target/release/vmt -f projects/7/MemoryAccess/BasicTest/BasicTest.vm`
End of script - Comparison ended successfully
    Finished `release` profile [optimized] target(s) in 0.02s
     Running `target/release/vmt -f projects/7/MemoryAccess/PointerTest/PointerTest.vm`
End of script - Comparison ended successfully
    Finished `release` profile [optimized] target(s) in 0.02s
     Running `target/release/vmt -f projects/7/MemoryAccess/StaticTest/StaticTest.vm`
End of script - Comparison ended successfully
    Finished `release` profile [optimized] target(s) in 0.02s
     Running `target/release/vmt -f projects/7/StackArithmetic/SimpleAdd/SimpleAdd.vm`
End of script - Comparison ended successfully
    Finished `release` profile [optimized] target(s) in 0.02s
     Running `target/release/vmt -f projects/7/StackArithmetic/StackTest/StackTest.vm`
End of script - Comparison ended successfully
All test cases passed
```

##### Postscript

I find that writing code is easy while blogging about it is hard and seemingly more
time-consuming. Perfection is the enemy of progress, so I would much rather have an
imperfect blogpost that gets published in a reasonable amount of time than a
fully-fleshed one that takes forever to be published.

The next project, Project 8, extends the VM Translator to add program flow constructs
such as `IF`, `RETURN`, `FUNCTION`, `RETURN`, et c. Looking forward to hacking on
this in the new year!

[project7]: https://www.nand2tetris.org/course
[that-vm]: https://en.wikipedia.org/wiki/Virtual_machine#System_virtual_machines
[stack-machine]: https://en.wikipedia.org/wiki/Stack_machine
[rust-constructor]: https://rust-unofficial.github.io/patterns/idioms/ctor.html
[handcode]: https://github.com/guru-das-s/nand2tetris/tree/master/projects/7/handcode
[rawstring]: https://doc.rust-lang.org/reference/tokens.html#raw-string-literals
[bytecode]: https://en.wikipedia.org/wiki/Bytecode
[eq]: https://github.com/guru-das-s/nand2tetris/blob/master/projects/7/handcode/eq.asm
[unoptimized-pop]: https://github.com/guru-das-s/nand2tetris/blob/a78a71b76e24e371ee3793f19f98b15983cddd6d/projects/7/hand_code_pop_local_2.asm
[optimized-pop]: https://github.com/guru-das-s/nand2tetris/commit/4d4d2e81e9b961dc2d86cddd92b3915f1e5fa190
[pop]: https://github.com/guru-das-s/nand2tetris/blob/master/projects/7/vmt/src/phrases.rs#L235-L263
[simple-main]: https://github.com/guru-das-s/nand2tetris/blob/master/projects/7/vmt/src/main.rs

---
