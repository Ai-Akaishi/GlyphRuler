### Copyright © 2025 赤石愛
### This software is released under the MIT License, see LICENSE.

# storage ruler: in{text:"abc",line_width:315}

### 初期化
function ruler:init

### 入力を保存
data modify storage ruler: text set from storage ruler: in.text
execute store result score #line_width Ruler run data get storage ruler: in.line_width

### 文字列の長さを計測
execute store result score #length Ruler run data get storage ruler: text

### 分割
function ruler:split/loop/512
function ruler:split/loop/64
function ruler:split/loop/8
function ruler:split/loop/1

### 残ったものを追加
data modify storage ruler: line_widths append value 0
execute store result storage ruler: line_widths[-1] int 1 run scoreboard players get #line Ruler

### 出力
data modify storage ruler: out.line_widths set from storage ruler: line_widths
