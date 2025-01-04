Since VQsX is a bytecode based vector engine, it has its own machine code. The [instruction set](Instruction%20Set.md) is generated as machine code for the vector engine to interpret and execute; the bytecode is the machine code of VQsX. Because the machine code of VQsX is not readable as with other architectures, there is a standardized assembly language provided to simplify writing VQsX vector programs.

Writing in VQsX assembly not as powerful as writing in VQsX bytecode/machine code, but allows the programming of VQsX engines to be simpler.

VQsX assembly does not allow direct access to the [registers](Registers.md) for its not needed as VQsX does not aim to be turing complete. Instead there are several instructions in the instruction set to make use of the registers.

There are several syntactic sugars in VQsX that are translated at assembly time. These syntactic sugars won't be present in the final vector program. They are just to make programming easier.
## Syntactic Sugars
The VQsX assembly language contains features not present in the vector engine itself, such as labels. It's also simpler as there is only one JUMP and CALL instructions; It's up to the assembler to decide which instructions to use.

## Filename
The VQsX assembly language assembler source files is recommended to have the file extension of **.vS**.

The compiled vector program's specifics is specified in the [instruction set](Instruction%20Set.md#Machine%20Code).

## Syntax
VQsX assembly resembles 6502 assembly with a sprinkle of Javascript and Shell script.

There are identifiers in VQsX assembly for labels. These labels are present to allow simplified call instructions. These identifiers are specified in [identifiers](#Identifiers).

The VQsX assembly language has labels, which are valid identifiers that ends with a ":" to signify it as a label. The labels may not have any indentation.

Each instruction mnemonic must be indented by 1 tab or 4 spaces to signify it as an instruction instead of a label. The instructions must be a valid mnemonic or full name, capitalized. Each instruction must be on their own line and may be terminated with a semicolon (**;**).

A comment starts with a **#** and may be anywhere. 

VQsX assembly has Directives. Directives are specified in [Directives](#Directives)

Examples of VQsX assembly are present in [Examples](Examples.md). The basic example is [General Demo](Examples.md#General%20Demo).
### Identifiers
A valid identifier is any string that starts with an alphabetical character or an underscore, and may contain alphanumerical characters and underscores. **_a** and **a1** are valid identifiers while **1a** and **a+c** are invalid identifiers.

### Directives
Directives are used to indicate the assembler to change its assembling behavior.

Directives are not part of the assembly language and final compiled program, but is instead used to simplify assembly. Directives don't even have to be standardized, or even supported. They can be assembler specific. 

A directive (to the assembler) starts with a **.** and continued with the directive string. An example of a directive is `.include`.

These are standardized directives:
- Include
	- `.include <path_to_included>`
	- `<path_to_included>` is the path to a VQsX assembly source file that is to be included and inserted in place of the directive.
Even if Directives are standardized, they don't need to be included. The standardization is only there so if an assembler intends on having a directive implemented, it will be implemented in the same way no matter what.

## Assembler
VQsX assembly needs an assembler for assembling the assembly language program into a vector program. This section will standardize the assembler's interface so differing implementations can still have a unified interface for assembling. This also allows tools to not worry about compatibility with different assemblers.

The general name for the program is **vqsxasm**.

### Structure of The Assembler's CLI

`vqsxasm [options] <input_file>`

### Flags and Arguments

- Input
	- `<input_file>`
	- **REQUIRED**
	- This argument specifies the input file for the assembler to assembler.
	- To enable interactive mode explicitly, pass `-` as the input file name. If you want to compile a file called `-`, pass either the absolute or relative path of `-`.
- Output
	- `-o, --output`
	- **OPTIONAL** with values (`-o a.vBin`)
	- Default: `a.vBin`.
	- This argument specifies the output file. This output file is the assembled vector program.
- Verbosity
	- `-V, --verbosity`
	- **OPTIONAL** with values (`-V 1`)
	- Default: `1`.
	- Values
		- `0`: Silent (No output at all). 
		- `1`: Errors only.
		- `2`: Progress and Errors.
		- `3`: Assembly steps, Progress and Errors.
	- This argument specifies the verbosity of the assembler
- Help
	- `-h, --help`
	- **OPTIONAL**
	- This flag displays a help message for the assembler, showing all flags and usages.
- Directives
	- `-D, --directive`
	- **OPTIONAL** with values (`-D include`). Arguments can be repeated (`-D include -D macro`)
	- Values: Directives to enable.
	- Default: None.
	- This argument specifies what directive to enable.
		- For standard compliance, you should not activate any directives (Don't use `-D` flags).
- Jump Translation
	- `-J, --jump`
	- **OPTIONAL** with values (`-D IPC`)
	- Values
		- `ipc` - Only use [IPC](Registers.md) based jumps and calls ([JIPC & CIPC](Instruction%20Set.md))
		- `mst` - Only use [MST](Registers.md) based jumps and calls ([JMST & CMST](Instruction%20Set.md))
		- `auto` - Allows the assembler to choose whether to use [MST](Registers.md) or [IPC](Registers.md) based jumps and calls. This may depend on the location of the jump/call and target.
	- Default: `auto`
	- This argument specifies how are jumps and calls translated to in the final compiled binary.

### Exit Code
The exit code of the assembler is also specified.
- `0`: Success
- `1`: Assembly failure
- `2`: Non assembly related failure