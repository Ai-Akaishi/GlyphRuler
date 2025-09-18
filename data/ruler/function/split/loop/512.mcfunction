### Copyright © 2025 赤石愛
### This software is released under the MIT License, see LICENSE.

execute unless score #length Ruler matches 512.. run return fail

data modify storage ruler: b512 set string storage ruler: text 0 512
function ruler:split/512
data modify storage ruler: text set string storage ruler: text 512
scoreboard players remove #length Ruler 512

function ruler:split/loop/512
