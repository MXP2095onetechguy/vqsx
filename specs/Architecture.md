VQsX is designed to execute from RAM. VQsX is a little-endian architecture. The word size of VQsX is 16 bits, paired with 64-bit addressing. The byte size for VQsX is still 8-bits.

All instructions in VQsX are variable-length encoded. The first byte is the instruction before fetching n-more bytes as the operand(s) depending on the fetched instruction. 

VQsX uses clock signals for execution. Execution is triggered on rising-edge signals. This is to allow compatibility for a wide-array of components and tooling.

The vector engine operates on two's complement and IEEE 754. Despite the vector engine being 16-bit-worded, it is capable of doing 64-bit arithmetic and floating point math, with its integer size being 64-bits.

## Stack
There are two stacks in VQsX, which are implemented via [registers](Registers.md#Stack%20Registers) and RAM. The registers control the stack start and bound addresses in RAM. There are 3 stacks:
- State: The state stack is used to manage the pen's state. This does not include the pen's position.
- Position: The position stack is used to manage the pen's position
- Call: The call stack is used to manage the subroutines of VQsX

## Faults
There are also faults which can be triggered. If a fault is triggered, then the vector engine will halt and the corresponding [status register flag](Registers.md#Status%20Register) is raised. Faults can be triggered by things such as bad (illegal/invalid) instruction calls, and stack faults. Faults basically are things that halt the vector engine that isn't by the user's own will or the external hardware's will.


## NEXT
VQsX also has an interrupt and synchronization primitive. This primitive is known as the NEXT signal. Its used for when the main external hardware needs to manipulate the vector program on runtime without halting the vector engine. Without the NEXT signal, manipulating the vector program during rune time would have many race conditions.

NEXT signals are like interrupts. If the vector engine is told to wait for a NEXT signal, either via [instructions](Instruction%20Set.md) or [pins](Pins.md), then the vector engine will wait until a NEXT signal is triggered. This NEXT signal is triggered via the [TRIGNEXT pin](Pins.md).

The TRIGNEXT pin is used to wake the vector engine from waiting for a NEXT signal. If the NEXT signal is triggered while VQsX is not waiting for a next signal, the vector engine silently continues as if the NEXT signal was never even triggered in the first place.

## Color
VQsX support color. VQsX though uses index based colors. This is to simplify programming the vector engine.

Here are the supported colors:

| Value (8-bits) | Color                 | Hex (RGB) |
| -------------- | --------------------- | --------- |
| 0              | Bright Red            | \#FF5555  |
| 1              | Bright Green          | \#55FF55  |
| 2              | Bright Blue           | \#5555FF  |
| 3              | Bright Yellow         | \#FFFF55  |
| 4              | Bright Magenta        | \#FF55FF  |
| 5              | Bright Cyan           | \#55FFFF  |
| 6              | Bright Orange         | \#FFAA55  |
| 7              | Bright Pink           | \#FF69B4  |
| 8              | Bright Lime           | \#AAFF55  |
| 9 **!**        | Bright Sky Blue       | \#55AAFF  |
| 10             | Bright Purple         | \#AA55FF  |
| 11             | Bright Teal           | \#55FFAA  |
| 12             | Azure                 | \#F0FFFF  |
| 13             | Bright White          | \#FFFFFF  |
| 14             | Bright Beige          | \#FFDD99  |
| 15             | Lavender              | \#E6E6FA  |
| 16             | Fuchsia               | \#FF00FF  |
| 17             | Olive                 | \#808000  |
| 18             | Brown                 | \#8B4513  |
| 19             | Light Brown           | \#BC8F8F  |
| 20             | Tan                   | \#D2B48C  |
| 21             | Gold                  | \#FFD700  |
| 22-255         | Bright Red (Reserved) | \#FF55555 |
The reserved color if selected always defaults to red. Reserved colors can be redefined by the implementation or hardware; they can be vendor-specific extensions. For portability reasons, always stick to the unreserved and well-defined colors.

**!** Colors starting with 9 are extended colors. These are still mandatory.