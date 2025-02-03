#!/usr/bin/env python3
import vqsx

STATZ : vqsx.StatusFlags = vqsx.STATUS_ZERO # Good known value

STAT1 = STATZ | vqsx.STATUS_FAULT
STAT2 = STATZ | vqsx.STATUS_HALTED
STAT3 = STATZ | vqsx.STATUS_NEXT

STAT4 = STATZ | vqsx.STATUS_FAULT | vqsx.STATUS_HALTED
STAT5 = STATZ | vqsx.STATUS_FAULT | vqsx.STATUS_NEXT
STAT6 = STATZ | vqsx.STATUS_HALTED | vqsx.STATUS_NEXT

STAT7 : vqsx.StatusFlags = STATZ | STAT1 | STAT2 | STAT3

stats = [STATZ, 
         STAT1, STAT2, STAT3, 
         STAT4, STAT5, STAT6, 
         STAT7]

def helpprint(desc : str, val : vqsx.StatusFlags):
    print(desc, vqsx.status_stringify(val))

for stat in stats:
    helpprint("N/A", stat)