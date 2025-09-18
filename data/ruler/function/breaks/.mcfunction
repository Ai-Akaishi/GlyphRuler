### Copyright © 2025 赤石愛
### This software is released under the MIT License, see LICENSE.

# storage ruler: in{count:4}

### スコア化
execute store result score #_ Ruler run data get storage ruler: in.count

data modify storage ruler: break set value {64:"",32:"",16:"",8:"",4:"",2:"",1:""}
execute if score #_ Ruler matches 64.. run data modify storage ruler: break.64 set value "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
execute if score #_ Ruler matches 64.. run scoreboard players remove #_ Ruler 64
execute if score #_ Ruler matches 32.. run data modify storage ruler: break.32 set value "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
execute if score #_ Ruler matches 32.. run scoreboard players remove #_ Ruler 32
execute if score #_ Ruler matches 16.. run data modify storage ruler: break.16 set value "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
execute if score #_ Ruler matches 16.. run scoreboard players remove #_ Ruler 16
execute if score #_ Ruler matches 8.. run data modify storage ruler: break.8 set value "\n\n\n\n\n\n\n\n"
execute if score #_ Ruler matches 8.. run scoreboard players remove #_ Ruler 8
execute if score #_ Ruler matches 4.. run data modify storage ruler: break.4 set value "\n\n\n\n"
execute if score #_ Ruler matches 4.. run scoreboard players remove #_ Ruler 4
execute if score #_ Ruler matches 2.. run data modify storage ruler: break.2 set value "\n\n"
execute if score #_ Ruler matches 2.. run scoreboard players remove #_ Ruler 2
execute if score #_ Ruler matches 1.. run data modify storage ruler: break.1 set value "\n"
execute if score #_ Ruler matches 1.. run scoreboard players remove #_ Ruler 1

function ruler:breaks/concat with storage ruler: break
