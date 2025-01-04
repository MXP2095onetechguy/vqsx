VQsX has several pins which is used to communicate intent to the vector engine. 

This table shows what pins are available. This does not include the data addressing pins required for i/o and data/addressing flow. Only the execution pins are shown. **THIS MAY CHANGE IN THE FUTURE**

| Name     | Description                                                                                                                                                                                                                                  |
| -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| TRIGNEXT | A pin that is set high to trigger a NEXT signal, causing the vector engine to continue execution. This does nothing if the vector engine isn't waiting for a NEXT signal.<br><br>NEXT signals are described in [NEXT](Architecture.md#NEXT). |
| WAITNEXT | A pin that is set to wait until a NEXT signal is generated. This behaves as if **WNXT** [instruction](Instruction%20Set.md) was executed.<br><br>NEXT signals are described in [NEXT](Architecture.md#NEXT).                                 |
| CLOCK    | A pin that is used for clock signals. This pin is used to tell VQsX when to execute. This input pin responds to rising-edge signals (LOW to HIGH). This pin does nothing on falling edge.                                                    |
| HALT     | A pin that is set to a high value to halt the vector engine.                                                                                                                                                                                 |