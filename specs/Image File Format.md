Since VQsX is a vector engine, it can be repurposed as a bytecode based image format. It extends the [instruction set](Instruction%20Set.md#Instructions) and [machine code](Instruction%20Set.md#Machine%20Code) binary format to support extra information such as the width, height and color depth of the image in the form of a header. 

This format is known as VQsXi.

The recommended file extension for the VQsXi format is **.vxi**.

## Header

The VQsXi file format has a header which provides important information about the image. The header is little-endian.

Here is the header definition:

| Field           | Offset (Bytes) | Size (Bytes) | Description                                     |
| --------------- | -------------- | ------------ | ----------------------------------------------- |
| Magic Number    | 0              | 5            | Must be **VQsXi** in ASCII.                     |
| Width           | 5              | 2            | Width of the image                              |
| Height          | 7              | 2            | Height of the image                             |
| Color Depth     | 9              | 1            | A toggle for either WB or Index-color graphics. |
| Bytecode Length | 10             | 8            | Size of the bytecode section in bytes.          |
| Padding         | 18             | 14           | Padding in NUL characters. Reserved space.      |
|                 |                |              |                                                 |
The header is designed to be aligned and packable in 32 bytes.
The *Color Depth* field is a toggle, where 0 means WB graphics and a non-0 means Index-color graphics.
## Bytecode
The bytecode is the actual bytecode that does the drawing. It is the bytecode that has the graphical information of the VQsXi file format.

The length is determined by the *Bytecode Length* field of the header.