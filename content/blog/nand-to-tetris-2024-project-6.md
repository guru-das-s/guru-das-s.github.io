Title: Nand2Tetris - Project 6 (Assembler)
Date: Sun Oct 13 07:32:02 PM PDT 2024
tldr: How I wrote an assembler for the Hack computer in Rust, complete with code excerpts and explanations.
Tags: nand2tetris, rust, opensource

I wrote a two-pass assembler for the Hack assembly language!

This is the sixth and final project of the first half (Hardware) of the Nand2Tetris
course. In [Project 6](https://www.nand2tetris.org/course), the task is to write an
[assembler](https://en.wikipedia.org/wiki/Assembly_language#Assembler) for the Hack
assembly language. Unlike the previous projects which could only be written using the
custom hardware description language (HDL) used by the Nand2Tetris project, Projects
6 to 12 allow the use of any programming language that is convenient. I chose to
write the assembler in Rust because I wanted to continue building substantial things
with it and learn more of its features in the process.

Follow my progress on Github here:
[guru-das-s/nand2tetris](https://github.com/guru-das-s/nand2tetris/commits/master/).

---

[TOC]

---

# Introducing: The `has` assembler

My Hack assembler is named `has` - a simple portmanteau of the two words. It has the
following calling card:

```
$ cargo run --release --bin has -- --help
    Finished `release` profile [optimized] target(s) in 0.12s
     Running `/home/gurus/projects/nand2tetris/target/release/has --help`
Hack assembler

Converts Hack assembly files to Hack binary

Usage: has [OPTIONS] --filename <FILENAME>

Options:
  -f, --filename <FILENAME>
          Path to Hack ASM file (e.g. Max.asm)

  -o, --output <OUTPUT>
          Output filename (e.g. Max.hack)

  -h, --help
          Print help (see a summary with '-h')

  -V, --version
          Print version
```

The only required argument to the assembler is the input filename. The default output
filename is the input filename with the extension replaced by `.hack` unless
overridden by the `--output` flag.

Defining a separate binary `[[bin]]` for the assembler in `Cargo.toml` seemed a
natural choice to keep using this same repository for all future projects and easily
build separate binaries for them:
```toml
[[bin]]
name = "has"
path = "projects/6/has/src/main.rs"
```

# Code walkthrough

I followed the same sequence of developing the Hack assembler as suggested in the
project docs - first, developing the ability to assemble symbol-less asm files and
then adding a symbol table and enabling the handling of symbols too. [Source code
here](https://github.com/guru-das-s/nand2tetris/tree/master/projects/6/has/src).

There are four modules in the project in addition to `main.rs`:
```
$ tree projects/6/has/src/
projects/6/has/src/
├── main.rs
├── parser.rs
├── spec.rs
├── symboltable.rs
└── to_binary.rs
```

## Main data structures used

The fact that there is a finite number of valid values for each of the fields in a
C-instruction and a max value for the number contained in an A-instruction led me to
choose enums as my fundamental data structure to base all the logic on.

The members of Rust enums have two forms:[ref][Defining an Enum - The Rust Programming
Language](https://doc.rust-lang.org/book/ch06-01-defining-an-enum.html)[/ref]

1. Regular C-like enum members/variants that are just equated to constant values, and
2. Arbitrary constructions of structs/tuples/enums of any datatype!

This makes it really intuitive to represent the various forms that a valid line of
Hack assembly code can take:

```rust
pub enum HackLine {
    Whitespace,
    Comment,
    Label {
        label: String,
    },
    A {
        value: u16,
    },
    Variable {
        name: String,
    },
    C {
        dest: Option<Destination>,
        comp: Option<Comp>,
        jump: Option<Jump>,
    },
}
```

I chose to represent a raw A-instruction (with a value spelt out explicitly) and a
variable separately even though the latter is also technically a valid A-instruction.
The members of `HackLine::C` are all `Options` in order to differentiate erroneous
`None` values from valid `<enum>::Null` values.

The `HackLine` enum is `pub` because I'm using modules to encapsulate code cleanly as
separate files and I need the enum to be visible to all modules in the project. This
enum lives in the `parser.rs` module.

`Destination` and `Jump` are C-style enums. Excerpts edited for brevity:

```rust
pub enum Destination {
    Null = 0,
    M = 1,
    D = 2,
    ...
}
pub enum Jump {
    Null = 0,
    JGT = 1,
    JEQ = 2,
    JGE = 3,
    ...
}
```

`Comp` is also one, too, but with a custom `impl` that defines helper functions to
map synonym enum variants such as `Comp::A` and `Comp::M` to the same hex values and figuring out
the corresponding `a`-value for an enum variants.

```rust
pub enum Comp {
    Zero,
    One,
    MinusOne,
    D,
    A,
    M,
    NotD,
    NotA,
    NotM,
    MinusD,
    ...
}
impl Comp {
    pub fn to_u8(&self) -> u8 {
        match self {
            Comp::Zero => 0b101010,
            Comp::One => 0b111111,
            Comp::MinusOne => 0b111010,
            Comp::D => 0b001100,
            Comp::A | Comp::M => 0b110000,
            Comp::NotD => 0b001101,
            Comp::NotA | Comp::NotM => 0b110001,
            ...
        }
    }
}
```

This `impl` was required because Rust does not allow multiple enum variants to be
equated to the same numeric value.

These enums all live in the `spec.rs` module - which, originally, was intended to
capture all the specifications of the Hack asm language but now appears to contain
only the specifications of the C-instruction, the A-instruction being relatively
trivial to represent.

The symbol table is represented as follows, and it lives in its own `symboltable.rs`
module, along with its attendant `impl` methods [ref][Methods - Rust by
Example](https://doc.rust-lang.org/rust-by-example/fn/methods.html)[/ref].

```rust
pub struct SymbolTable {
    next_free_ram_address: u16,
    m: HashMap<String, u16>,
}
```

## Code flow

Starting from the `main.rs` entry point: 

After the `clap` crate does its thing and parses command-line arguments passed to the
program, we read the contents of the input asm file into a `Vec` and `assemble()` it,
passing to `assemble()` a mutable reference to a `symbol_table` duly initialized with
known arch-specific symbols.

`assemble()` shows the two-pass architecture of the assembler. Why are two passes
required? It is primarily to handle labels in the asm source file that are forward
references, i.e. the first use of the label in an instruction occurs _before_ its
definition, thus making it impossible to know _at that first-use location_ what code
memory location to translate the label to.

So in the first pass, the input file is iterated through line-by-line and only
`HackLine::Label`s are processed, adding labels to the list of known symbols in the
`symbol_table` and storing their code memory locations in the symbol table's hashmap.
In the second pass, each line is parsed, including the labels and variables and
converted to its binary representation.

The `parser.rs` module parses each line and returns the `HackLine` enum variants it
maps to, or an `Err()` if the line is not a valid Hack asm line.

The `to_binary.rs` module then takes in the parsed line, i.e. the `HackLine` enum
type and converts it to its binary representation. Here, Rust's automatic
destructuring of enum types allows for easily accessing the parsed data of the
`HackLine` enum type.

```rust
pub fn binary_of(line: HackLine, symboltable: &mut SymbolTable) -> Option<String> {
    match line {
        HackLine::Whitespace | HackLine::Comment | HackLine::Label { .. } => None,
        HackLine::A { value } => Some(binary_of_a_type_instruction(value)),
        HackLine::C { dest, comp, jump } => Some(binary_of_c_type_instruction(
            dest.unwrap(),
            comp.unwrap(),
            jump.unwrap(),
        )),
        HackLine::Variable { name } => Some(binary_of_variable(name, symboltable)),
    }
}
```
The implementation of `binary_of_variable()` bears illustration here (the other two
functions are relatively straightforward):

```rust
fn binary_of_variable(variable: String, symbol_table: &mut SymbolTable) -> String {
    if !symbol_table.is_known(&variable) {
        symbol_table.add_new_variable(&variable);
    }
    let value = symbol_table.get_variable_address(&variable);
    return binary_of_a_type_instruction(value);
}
```

# Does `has` output match the stock assembler's?

With the assembler in place, I also wrote a shell script to verify that it matches
the output of the stock assembler that is provided by the Nand2Tetris team in the
repo. It first runs the stock assembler, `tools/Assembler.sh`, on all the `.asm`
files in the Project 6 directory to generate the "ground truth" `.hack` files. The
stock assembler converts a Hack asm file named, say, `Test.asm` to `Test.hack`.

Next, I run my `has` assembler on the same files, taking care to specify a different suffix
to the output binary in order to distinguish it from the ground truth files. The `has`
assembler converts a Hack asm file named, say, `Test.asm` to `Test.has.hack`.

These two files are `diff`-ed in the next step. Since the `set -e` command is set in
the test script, any mismatches in the files will cause the `diff` command to error
out and, consequently, the test script itself. Let's run the test script to check:

```
$ ./projects/6/test.sh && echo "No diffs!"
Assembling /home/gurus/projects/nand2tetris/projects/6/rect/Rect.asm
Assembling /home/gurus/projects/nand2tetris/projects/6/rect/RectL.asm
Assembling /home/gurus/projects/nand2tetris/projects/6/max/Max.asm
Assembling /home/gurus/projects/nand2tetris/projects/6/max/MaxL.asm
Assembling /home/gurus/projects/nand2tetris/projects/6/add/Add.asm
Assembling /home/gurus/projects/nand2tetris/projects/6/pong/Pong.asm
Assembling /home/gurus/projects/nand2tetris/projects/6/pong/PongL.asm
    Finished `release` profile [optimized] target(s) in 0.02s
     Running `target/release/has -f projects/6/rect/Rect.asm -o projects/6/rect/Rect.has.hack`
    Finished `release` profile [optimized] target(s) in 0.02s
     Running `target/release/has -f projects/6/rect/RectL.asm -o projects/6/rect/RectL.has.hack`
    Finished `release` profile [optimized] target(s) in 0.03s
     Running `target/release/has -f projects/6/max/Max.asm -o projects/6/max/Max.has.hack`
    Finished `release` profile [optimized] target(s) in 0.02s
     Running `target/release/has -f projects/6/max/MaxL.asm -o projects/6/max/MaxL.has.hack`
    Finished `release` profile [optimized] target(s) in 0.02s
     Running `target/release/has -f projects/6/add/Add.asm -o projects/6/add/Add.has.hack`
    Finished `release` profile [optimized] target(s) in 0.02s
     Running `target/release/has -f projects/6/pong/Pong.asm -o projects/6/pong/Pong.has.hack`
    Finished `release` profile [optimized] target(s) in 0.02s
     Running `target/release/has -f projects/6/pong/PongL.asm -o projects/6/pong/PongL.has.hack`
No diffs!
```

Yes - no diffs.

The script also cleans up after itself using the Bash `trap <command> EXIT` method.
This causes `<command>` to run at the end of the Bash script's execution - either
graceful or erroneous. In this case, I clean up all the generated `.hack` files in a
`cleanup()` routine upon `EXIT`.

# Post-completion thoughts

Writing this assembler was really rewarding not just in terms of learning how a basic
two-pass assembler works but also because it afforded me the means and opportunity to
learn more about Rust:

- Rust enums and their automatic destructuring in `match`es
- Rust associated methods vs plain functions in `impl`s
- Smartly using `None` to indicate an error condition that should not happen vs
    a valid "empty" value such as, say, `Destination::Null`
- The compiler forcing me to learn about chaining `.as_ref()` to continue accessing a
    variable more than once
- Working with modules and setting visibility to functions via `pub`
- Adding `#[cfg(debug_assertions)]` to `println!()` macros to effectively make them
    debug prints
- Using the `clap` crate for parsing command line arguments and doc comments
- Appreciating how Rust forces you to contend with all possible values of an enum and
    also errors

The end of Project 6 marks the half-way point of the entire Nand2Tetris course. I'm
half way done! This is so cool. With the so-called "Hardware" half of the course
behind me, now I'm focussed on the next half, the "Software" half. Since the official
website does not offer PDFs of the relevant chapters from the textbook for the
remaining projects, I bought [the
textbook](https://www.amazon.com/dp/0262539802?ref=ppx_yo2ov_dt_b_fed_asin_title)
instead.

During the course of the next projects, I'll be building a virtual machine
translator, a compiler for a Java-like high-level language, and an operating system
for the Hack computer. I am really excited to read the textbook and learn about
compilers and a "stack machine" in detail.

Finally, since I recently added tags to all my blog posts, it is now convenient to
view all my Nand2Tetris-related posts by checking [tag:
nand2tetris]({tag}nand2tetris).

---
