### Copyright © 2025 赤石### Copyright © 2025 赤石愛
### This software is released under the MIT License, see LICENSE.

### \nのとき
data modify storage ruler: line_widths append value 0
execute store result storage ruler: line_widths[-1] int 1 run scoreboard players get #line Ruler
scoreboard players set #line Ruler 0
scoreboard players set #word Ruler 0
