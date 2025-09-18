### Copyright © 2025 赤石愛
### This software is released under the MIT License, see LICENSE.

# storage ruler: in{width:315}

### パディング計算
execute store result score #_ Ruler run data get storage ruler: in.width
scoreboard players set #word Ruler 4
scoreboard players operation #_ Ruler /= #word Ruler

data modify storage ruler: pad set value {512:"",256:"",128:"",64:"",32:"",16:"",8:"",4:"",2:"",1:""}
execute if score #_ Ruler matches 512.. run data modify storage ruler: pad.512 set value "                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                "
execute if score #_ Ruler matches 512.. run scoreboard players remove #_ Ruler 512
execute if score #_ Ruler matches 256.. run data modify storage ruler: pad.256 set value "                                                                                                                                                                                                                                                                "
execute if score #_ Ruler matches 256.. run scoreboard players remove #_ Ruler 256
execute if score #_ Ruler matches 128.. run data modify storage ruler: pad.128 set value "                                                                                                                                "
execute if score #_ Ruler matches 128.. run scoreboard players remove #_ Ruler 128
execute if score #_ Ruler matches 64.. run data modify storage ruler: pad.64 set value "                                                                "
execute if score #_ Ruler matches 64.. run scoreboard players remove #_ Ruler 64
execute if score #_ Ruler matches 32.. run data modify storage ruler: pad.32 set value "                                "
execute if score #_ Ruler matches 32.. run scoreboard players remove #_ Ruler 32
execute if score #_ Ruler matches 16.. run data modify storage ruler: pad.16 set value "                "
execute if score #_ Ruler matches 16.. run scoreboard players remove #_ Ruler 16
execute if score #_ Ruler matches 8.. run data modify storage ruler: pad.8 set value "        "
execute if score #_ Ruler matches 8.. run scoreboard players remove #_ Ruler 8
execute if score #_ Ruler matches 4.. run data modify storage ruler: pad.4 set value "    "
execute if score #_ Ruler matches 4.. run scoreboard players remove #_ Ruler 4
execute if score #_ Ruler matches 2.. run data modify storage ruler: pad.2 set value "  "
execute if score #_ Ruler matches 2.. run scoreboard players remove #_ Ruler 2
execute if score #_ Ruler matches 1.. run data modify storage ruler: pad.1 set value " "
execute if score #_ Ruler matches 1.. run scoreboard players remove #_ Ruler 1

function ruler:padding/concat with storage ruler: pad
