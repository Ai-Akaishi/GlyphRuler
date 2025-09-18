### Copyright © 2025 赤石愛
### This software is released under the MIT License, see LICENSE.

## default文字
$execute store result score #char Ruler run data get storage ruler: chars.default."$(s)$(c)" 2
## unifont文字
$execute if score #char Ruler matches 0 store result score #char Ruler run data get storage ruler: chars.unifont."$(s)$(c)"
## どっちでもなければreturn
execute if score #char Ruler matches 0 run return fail

## char / 2 + 1
execute store result storage ruler: _ int 0.5 run scoreboard players add #char Ruler 2
execute store result score #char Ruler run data get storage ruler: _
