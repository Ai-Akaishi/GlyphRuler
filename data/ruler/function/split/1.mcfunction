### Copyright © 2025 赤石愛
### This software is released under the MIT License, see LICENSE.

function ruler:split/1-m with storage ruler: b1
execute if score #char Ruler matches 0 run scoreboard players set #char Ruler 9

## サロゲート一旦解除
data modify storage ruler: b1.s set value ""
## 高位サロゲート？
function ruler:split/1-m2 with storage ruler: b1
execute if score #char Ruler matches 0 run return fail

### \nのとき
execute if data storage ruler: b1{c:"\n"} run return run function ruler:split/line_feed

### spaceのとき
execute if data storage ruler: b1{c:" "} run return run function ruler:split/space

### \nでもspaceでもないなら一旦追加
scoreboard players operation #line Ruler += #char Ruler
scoreboard players operation #word Ruler += #char Ruler

### ラインを超えていなければreturn
execute unless score #line Ruler > #line_width Ruler run return fail

### 単語で区切れるなら
execute if score #line Ruler > #word Ruler run return run function ruler:split/break_at_boundary
### 単語で区切れないなら
function ruler:split/break_within_word
