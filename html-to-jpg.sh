#!/bin/bash
# Usage: ./html-to-jpg.sh <input.html> <output.jpg> [width] [height]
# Renders HTML in headless Chrome, then converts the PNG to JPG through a
# canvas in a second Chrome pass (this box has no PIL, ImageMagick or netpbm).
set -e
IN="$1"; OUT="$2"; W="${3:-1600}"; H="${4:-900}"
T=$(mktemp -d)
google-chrome --headless=new --disable-gpu --no-sandbox --hide-scrollbars \
  --window-size="$W,$H" --screenshot="$T/s.png" "file://$(realpath "$IN")" >/dev/null 2>&1
{
  printf '%s' '<!doctype html><meta charset="utf-8"><body><div id="o"></div><script>
var i=new Image();i.onload=function(){var c=document.createElement("canvas");
c.width=i.width;c.height=i.height;var x=c.getContext("2d");
x.fillStyle="#fff";x.fillRect(0,0,c.width,c.height);x.drawImage(i,0,0);
document.getElementById("o").textContent="@@@"+c.toDataURL("image/jpeg",0.94).split(",")[1]+"@@@";};
i.src="data:image/png;base64,'
  base64 -w0 "$T/s.png"
  printf '%s' '";</script></body>'
} > "$T/conv.html"
google-chrome --headless=new --disable-gpu --no-sandbox --virtual-time-budget=15000 \
  --dump-dom "file://$T/conv.html" 2>/dev/null \
  | grep -o '@@@[A-Za-z0-9+/=]*@@@' | head -1 | sed 's/@@@//g' | base64 -d > "$OUT"
rm -rf "$T"
file "$OUT"
