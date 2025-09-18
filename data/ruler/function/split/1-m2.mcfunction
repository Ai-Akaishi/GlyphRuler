### Copyright © 2025### Copyright © 2025 赤石愛
### This software is released under the MIT License, see LICENSE.

## 高位サロゲートなら、サロゲートに保存して、文字幅を0に
$execute unless data storage ruler: surrogates.high."$(c)" run return fail

data modify storage ruler: b1.s set from storage ruler: b1.c
scoreboard players set #char Ruler 0
