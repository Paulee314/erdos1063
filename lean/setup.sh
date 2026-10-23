#!/bin/bash
set -x
cd "$(dirname "$0")"
if [ ! -x "$HOME/.elan/bin/elan" ]; then
  curl https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh -sSf | sh -s -- -y --default-toolchain none --no-modify-path
fi
export PATH="$HOME/.elan/bin:$PATH"
elan --version
if [ ! -d erdos1063 ]; then
  lake +leanprover-community/mathlib4:lean-toolchain new erdos1063 math
fi
cd erdos1063
cat lean-toolchain
lake exe cache get
echo SETUP_DONE
