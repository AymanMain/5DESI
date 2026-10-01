#!/bin/bash
# usage: export.sh name...   -> diagrams/exports/name.png (vector PDF -> 160 dpi PNG)
cd /home/claude/medx3/diagrams
for n in "$@"; do
  rm -f /tmp/$n.pdf
  timeout 100 xvfb-run -a /opt/drawio/drawio -x -f pdf --crop -b 20 -o /tmp/$n.pdf sources/$n.drawio --no-sandbox --disable-gpu >/tmp/e_$n.log 2>&1
  pkill -9 -x drawio; pkill -9 -x Xvfb
  pdftoppm -png -r 160 -singlefile /tmp/$n.pdf exports/$n && echo "OK $n" || echo "FAIL $n"
done
