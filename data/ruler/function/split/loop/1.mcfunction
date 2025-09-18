### Copyright © 2025 赤石愛
### This software is released under the MIT License, see LICENSE.

execute unless score #length Ruler matches 1.. run return fail

data modify storage ruler: b1.c set string storage ruler: text 0 1
function ruler:split/1
data modify storage ruler: text set string storage ruler: text 1
scoreboard players remove #length Ruler 1

function ruler:split/loop/1
