### Copyright © 2025 赤石愛
### This software is released under the MIT License, see LICENSE.

data modify storage ruler: b64 set string storage ruler: b512 0 64
function ruler:split/64
data modify storage ruler: b64 set string storage ruler: b512 64 128
function ruler:split/64
data modify storage ruler: b64 set string storage ruler: b512 128 192
function ruler:split/64
data modify storage ruler: b64 set string storage ruler: b512 192 256
function ruler:split/64
data modify storage ruler: b64 set string storage ruler: b512 256 320
function ruler:split/64
data modify storage ruler: b64 set string storage ruler: b512 320 384
function ruler:split/64
data modify storage ruler: b64 set string storage ruler: b512 384 448
function ruler:split/64
data modify storage ruler: b64 set string storage ruler: b512 448 512
function ruler:split/64
