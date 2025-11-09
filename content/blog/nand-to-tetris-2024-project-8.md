Title: Nand2Tetris - Project 8 (VM Translator Part 2)
Date: Sat Nov  8 09:19:59 PM PST 2025
tldr: Part two of the Nand2Tetris VM Translator in Rust, complete with code excerpts and rationale behind design choices made.
Tags: nand2tetris, rust, opensource

In [Project
8](https://drive.google.com/file/d/1BexrNmdqYhKPkqD_Y81qNAUeyfzl-ZtO/view) of
[Nand2Tetris](https://www.nand2tetris.org/course), we get to finish the
implementation of the VM Translator that was begun in [Project
7]({filename}nand-to-tetris-2024-project-7.md). Having gotten the hang of translating
arithmetic and logical VM commands from there, we now focus on translating the
remaining VM commands that deal with control flow and function call flow - specifically,
`label`, `goto`, `if-goto`, `function`, `call` and `return`.

This completes the implementation of the VM Translator, i.e. the Jack language
compiler's backend &ndash; but let's not get ahead of ourselves. This project was an
order of magnitude more involved to put together than Project 7 because it's really
three tasks in one, in decreasing order of difficulty:

1. Translate the control flow VM commands.
2. Translate the function call flow VM commands.
3. Two parts:
    - (a) Handle both a single `.vm` file as input as well as a directory containing `.vm`
   files.
    - (b) When translating the multiple `.vm` files together from a directory, add "bootstrapping"
   code as preamble.

As always, the code is here:
[guru-das-s/nand2tetris](https://github.com/guru-das-s/nand2tetris/tree/master/projects/7).
In hindsight, the generated assembly "phrases" could indeed be better optimized and
not so verbose, but that's a task for another day.

---

[TOC]

---

# Preparatory refactoring

While scoping out the changes required to support the control flow statements, I
realized that thus far, the first argument to a VM command was geared to support only
a `Segment` [ref] An example to refresh one's memory: the segment in the `push local
5` VM command is `local`.[/ref] and not a named label or a function name. This was
[remedied][gh-1] with the help of the [`todo!()`
macro](https://doc.rust-lang.org/std/macro.todo.html) to get things compiled and
moving.

# Task 1: Emit code for the control flow VM commands

## The `label` and `goto` commands

The codegen for these two commands are trivial and are almost natively supported by
the asm syntax without the need for any extra scaffolding.

```rust
pub const LABEL: &str = r#"// LABEL
(XYZ)
"#;

pub const GOTO: &str = r#"// GOTO
@XYZ
0;JMP
"#;
```

## The `if-goto` command

The syntax of this command is:
```
gt // Or any other logical comparison operator
if-goto LABEL
```
In hindsight, I implemented this command in a very roundabout fashion:

```rust
pub const IF_GOTO: &str = r#"// IF_GOTO
// first, get results of prev bool op
@SP
M=M-1
A=M
D=M
@DONTJUMP.XYZ
D;JEQ
@LABL
0;JMP
(DONTJUMP.XYZ)
"#;
```
That is, if the result of the previous boolean operation is `false`, jump over the
part where we do the unconditional jump to the target label; else, take the jump.
This can be simplified to "take the jump if the result is `true`":
```
...
@LABL
D;JNE
"#;
...
```

# Task 2: Emit code for the function-related VM commands

## Changes to phrases that occur within a function

The codegen for the control flow VM commands, and phrases that use phrase-local
labels, are both affected by their occurrence within a function body.

The symbol names need to be made unique; otherwise, the assembler will not resolve
them to the intended addresses [ref] Described
[here]({filename}nand-to-tetris-2024-project-7.md#labels-must-be-unique-for-conditional-operator-phrases)
in more detail. [/ref]. This is made by prefixing label symbol names and phrase-local labels
by the function's name.

```rust
pub const LABEL_IN_FUNC: &str = r#"// LABEL_IN_FUN
(FUNC$XYZ)
"#;

pub const GOTO_IN_FUNC: &str = r#"// GOTO_IN_FUN
@FUNC$XYZ
0;JMP
"#;
```

## The `function` command

The syntax of this command is:
```asm
function functionName nVars
```
with the following semantics:

> _Here starts the declaration of a function that has name functionName and nVars
> local variables_

The codegen for this command followed as two parts: to first emit a label containing
the function name, and then the emission of as many local variables as is specified.
This forms the "function frame" on the stack.

```rust
let mut function_phrase = phrases::FUNCTION.replace("FUNC", func_name);
function_phrase += &phrases::FUNCTION_LOCAL_VAR.repeat(num_local_vars as usize);
Ok(function_phrase)
```
The phrases are listed in [`phrases.rs`][fun-phrases].

## The `call` command

The syntax of this command is:
```asm
// <numArgs> arguments to functionName have been pushed to stack
call functionName numArgs
```
Before we `call` a function, we must first know where to return to after executing
that function. This necessarily has to be the first instruction *following* the
`call`. How do we determine this address and use this in the emitted asm?

This may seem like a circular problem in asm land because at this
point in the (to-be-translated) asm code...

```
VM land             asm land
-------             --------
call multiply       <to-be-emitted call code>
                    <to-be-emitted call code>
                    <to-be-emitted call code>
                    ...
                    <to-be-emitted call code>

pop temp 0          ADDRESS_TO_JUMP_TO_AFTER_CALL: <pop code follows>
```
...how do we know the `ADDRESS_TO_JUMP_TO_AFTER_CALL` if we haven't finished writing
the implementation of `call` yet?

The solution is to preemptively add a "return label" to the end of the `call` asm,
say, `@CALLER$ret` and then save that label name to the stack as the first step.
Remember, we can easily use a symbol that is defined only later because the assembler
will trivially take care of it in its first pass where it resolves symbol names to
addresses.

And since we can `call` any (`CALLEE`) function more than once from a given (`CALLER`)
function, we need to make the "return label" unique, so we need to tack on a
monotonically-increasing number to it: `@CALLER$ret.XYZ` (we will replace the `XYZ`
with the number in code).

The rest of the steps are to:

* save the current context (registers) to the stack
* modify the `ARG` pointer-register to point to the start of the `numArgs` number of function arguments
* that were pushed to the stack prior to the `call`
* modify the `LCL` pointer-register to point to the top of the stack for the callee
   function's use.
* actually jump to the callee function's code and start executing it

The implementation of `call` is listed in [`phrases.rs`][call-phrase].

## The `return` command

The syntax of this command is:
```asm
return // no arguments
```
This trivial-seeming command is the yin to the yang of `call`. It does a ton of heavy
lifting from its vantage point in the callee's code:

* Replacing the caller-pushed function arguments with the function's return value
* Invalidating the callee's function frame in the stack
* Restoring the (register) context saved on the stack by the caller, and finally,
* Jumping to the "return label", the instruction right after the `call`.

The implementation of `return` is listed in [`phrases.rs`][return-phrase].

# Task 3: Emit bootstrapping code

When translating a single file, the corresponding `.tst` test script provided in the
project src directory sets up the stack pointer to its value in the standard mapping
(`256`) and takes care of setting up any arguments as necessary. When translating
multiple files, however, we need to add this bootstrapping code first thing before
any other translations can take place.

The bootstrapping code sets `SP` to `256` and then `call`s `Sys.init`.

The implementation of the bootstrap is listed in [`phrases.rs`][bootstrap-phrase].

# Reflections

> _Any sufficiently advanced technology is indistinguishable from magic_
>
> _- Arthur C. Clarke_

There are broadly three parts to a magic trick: the pledge, the turn and the
prestige:

* the *pledge* forms the setup of the trick, the *mise en place*. The audience is
    shown something ordinary: a rabbit sitting on a table.
* the *turn* generates great surprise: the rabbit disappears!
* the *prestige* is the climax of the trick and provides resolution: the rabbit
    reappears from a hat. The audience marvels at the trick and wonders how it was
    achieved.

Allowing for some poetic licence, this basic structure may be applied to our
understanding of the implementation of a function call.

* `function` as the *pledge*: We know that `multiply()` multiplies two numbers
    together.
* `call` as the *turn*: Execution jumps from the caller to the callee and the
    multiplication takes place!
* `return` as the *prestige*: We magically return to wherever we left with the result
    of the multiplication ready and waiting for us in the caller's context.

Only, we now know how this was achieved.

# Test script

Following the example of the test scripts added in the previous two projects, I added
one for Project 8 too.

```
$ ./projects/8/test.sh
   Compiling nand2tetris v0.1.0 (/home/gurus/projects/nand2tetris)
    Finished `release` profile [optimized] target(s) in 2.84s
     Running `target/release/vmt -i projects/8/ProgramFlow/BasicLoop/BasicLoop.vm`
End of script - Comparison ended successfully
    Finished `release` profile [optimized] target(s) in 0.02s
     Running `target/release/vmt -i projects/8/ProgramFlow/FibonacciSeries/FibonacciSeries.vm`
End of script - Comparison ended successfully
    Finished `release` profile [optimized] target(s) in 0.02s
     Running `target/release/vmt -i projects/8/FunctionCalls/SimpleFunction/SimpleFunction.vm`
End of script - Comparison ended successfully
    Finished `release` profile [optimized] target(s) in 0.02s
     Running `target/release/vmt -i projects/8/FunctionCalls/NestedCall/`
End of script - Comparison ended successfully
    Finished `release` profile [optimized] target(s) in 0.02s
     Running `target/release/vmt -i projects/8/FunctionCalls/FibonacciElement/`
End of script - Comparison ended successfully
    Finished `release` profile [optimized] target(s) in 0.02s
     Running `target/release/vmt -i projects/8/FunctionCalls/StaticsTest/`
End of script - Comparison ended successfully
```

# Postscript

The code was complete in August and I had begun work on this post shortly thereafter.
Life intervened (many times) as I tried to make progress on finishing this post, and
I could only publish this blog post now. No AI tools or LLMs were used in writing
this post.

[gh-1]: https://github.com/guru-das-s/nand2tetris/commit/f925735fee5ca55976f96adaad3060b0bcd4d388
[fun-phrases]: https://github.com/guru-das-s/nand2tetris/blob/master/projects/7/vmt/src/phrases.rs#L375-L388
[call-phrase]: https://github.com/guru-das-s/nand2tetris/blob/master/projects/7/vmt/src/phrases.rs#L309-L373
[return-phrase]: https://github.com/guru-das-s/nand2tetris/blob/master/projects/7/vmt/src/phrases.rs#L390-L448
[bootstrap-phrase]: https://github.com/guru-das-s/nand2tetris/blob/master/projects/7/vmt/src/phrases.rs#L450-L518

---
