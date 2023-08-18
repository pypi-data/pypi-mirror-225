#!/usr/bin/env python3

import json
import plaques as plq

mpbase = plq.Window(h_abs_size = 40, v_abs_size = 14, 
    fill = plq.CharCell(char = ".", color = plq.BLUE), 
    frame = plq.OUTER_HALF)
mpbase.title.text = "12345"
print(mpbase.title.text)
mpchild = plq.Plaque(h_rel_size = 0.5, v_rel_size = 0.6, h_rel_pos = 0.5, 
    v_rel_pos = 0.5, fill = plq.CharCell(char = "+", color = plq.TRANSPARENT, bgcol = plq.RED))
mpbase.content.append(mpchild)
print(mpbase)
print(mpbase.title.text)
print()
mpbase2 = mpbase.copy()
mpchild2 = plq.Text(h_rel_size = 0.5, v_rel_size = 0.5, 
    fill = plq.CharCell(bgcol = plq.MAGENTA))
mpchild2.text = "QWERTY"
mpbase2.content.append(mpchild2)
print(mpbase2)
