# -*- coding: utf-8 -*-
"""check_panel.py — gate truoc khi bao "da sua panel". Chay: python check_panel.py

Bon lop, moi lop bit mot loi DA DINH THAT:
  ① thieu <script src="panel.js">        -> KHONG nut nao co handler, giao dien van hien
                                            binh thuong nen trong y nhu "tool khong quet duoc tab"
  ② backtick TRONG template JS_JOBSTATE  -> cat dut chuoi, SyntaxError (dinh 3 LAN)
  ③ id JS goi ma HTML khong co (va nguoc lai)
  ④ cu phap panel.js + cu phap doan JS se chay trong tab Flow (kiem RIENG)
"""
import io
import os
import re
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
os.chdir(os.path.dirname(os.path.abspath(__file__)))
html = io.open("panel.html", encoding="utf-8").read()
js = io.open("panel.js", encoding="utf-8").read()
bad = 0

# ① the script
if '<script src="panel.js"></script>' in html:
    print("① the <script src=panel.js>            ✓")
else:
    print("① the <script src=panel.js>            🔴 THIEU — panel.js se KHONG duoc nap"); bad += 1

# ② backtick trong template JS_JOBSTATE
m = re.search(r"const JS_JOBSTATE = `(.*?)`;", js, re.S)
if not m:
    print("② JS_JOBSTATE                          🔴 khong tim thay khoi template"); bad += 1
    inner = None
else:
    inner = m.group(1)
    hit = [l.strip()[:70] for l in inner.split("\n") if "`" in l]
    if hit:
        print("② backtick trong JS_JOBSTATE           🔴 " + str(len(hit)) + " dong:")
        for l in hit:
            print("     " + l)
        bad += 1
    else:
        print("② backtick trong JS_JOBSTATE           ✓ sach")

# ③ id lech giua HTML va JS
hi = set(re.findall(r'id="([^"]+)"', html))
ji = set(re.findall(r'\$\("([^"]+)"\)', js))
for name, s in (("JS goi ma HTML thieu", ji - hi), ("HTML co ma JS khong dung", hi - ji)):
    if s:
        print(f"③ {name:36} 🔴 {sorted(s)}"); bad += 1
    else:
        print(f"③ {name:36} ✓")

# ④ cu phap
def node_check(path, label):
    global bad
    # 🔴 phai chi dinh encoding: node in loi co ky tu non-ASCII, mac dinh cp1252 tren Windows
    #    lam CHINH GATE crash va che mat noi dung loi (dinh 2026-09-10).
    r = subprocess.run(["node", "--check", path], capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    if r.returncode == 0:
        print(f"④ {label:36} ✓")
    else:
        print(f"④ {label:36} 🔴")
        print("     " + (r.stderr or "").strip().split("\n")[0][:120]); bad += 1

node_check("panel.js", "cu phap panel.js")
if inner is not None:
    tmp = "_check_jobstate_tmp.js"
    io.open(tmp, "w", encoding="utf-8").write("void " + inner.replace("\\\\", "\\") + ";")
    node_check(tmp, "cu phap doan chay trong tab Flow")
    os.remove(tmp)

print()
print("✅ SACH — nap lai extension duoc" if not bad else f"🔴 {bad} loi — SUA XONG MOI BAO LA DA SUA")
sys.exit(1 if bad else 0)
