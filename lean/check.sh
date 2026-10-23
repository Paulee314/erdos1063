#!/bin/bash
# usage: check.sh File.lean  -> compiles with Mathlib, writes File.out
cd "$(dirname "$0")/erdos1063"
export PATH="$HOME/.elan/bin:$PATH"
f="$1"
( time lake env lean "../$f" ) > "../${f%.lean}.out" 2>&1
echo "EXIT=$?" >> "../${f%.lean}.out"
