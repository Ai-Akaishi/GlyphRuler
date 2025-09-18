### Copyright © 2025 赤石愛
### This software is released under the MIT License, see LICENSE.

scoreboard objectives add Ruler dummy "For GlyphRuler Datapack"
scoreboard players set #line Ruler 0
scoreboard players set #word Ruler 0
data modify storage ruler: line_widths set value []
data modify storage ruler: b1.s set value ""

function ruler:init/chars_default
function ruler:init/chars_unifont
function ruler:init/surrogates
