### Copyright © 2025 赤石愛
### This software is released under the MIT License, see LICENSE.

execute unless score #length Ruler matches 64.. run return fail

data modify storage ruler: b64 set string storage ruler: text 0 64
function ruler:split/64
data modify storage ruler: text set string storage ruler: text 64
scoreboard players remove #length Ruler 64

function ruler:split/loop/64
