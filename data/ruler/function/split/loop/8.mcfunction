### Copyright ©### Copyright © 2025 赤石愛
### This software is released under the MIT License, see LICENSE.

execute unless score #length Ruler matches 8.. run return fail

data modify storage ruler: b8 set string storage ruler: text 0 8
function ruler:split/8
data modify storage ruler: text set string storage ruler: text 8
scoreboard players remove #length Ruler 8

function ruler:split/loop/8
