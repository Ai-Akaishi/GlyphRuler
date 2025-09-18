### Copyright © 2025 赤石愛
### This software is released under the MIT License, see LICENSE.

### spaceのとき

### space分入れられるなら追加
scoreboard players add #line Ruler 4
execute unless score #line Ruler > #line_width Ruler run return run scoreboard players set #word Ruler 0
### 入れられないなら改行に同じ
scoreboard players remove #line Ruler 4
function ruler:split/line_feed
