### Copyright © 2025 赤石愛
### This software is released under the MIT License, see LICENSE.

### 単語で区切れるとき
### #line - #word - 4を追加
data modify storage ruler: line_widths append value 0
scoreboard players operation #line Ruler -= #word Ruler
execute store result storage ruler: line_widths[-1] int 1 run scoreboard players remove #line Ruler 4
### #line = #word
scoreboard players operation #line Ruler = #word Ruler
