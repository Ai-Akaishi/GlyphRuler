### Copyright © 2025 赤石愛
### This software is released under the MIT License, see LICENSE.

### 単語で区切れない時
### #line - #charを追加
data modify storage ruler: line_widths append value 0
scoreboard players operation #line Ruler -= #char Ruler
execute store result storage ruler: line_widths[-1] int 1 run scoreboard players get #line Ruler
### #line = #char, #word = #char
scoreboard players operation #line Ruler = #char Ruler
scoreboard players operation #word Ruler = #char Ruler
