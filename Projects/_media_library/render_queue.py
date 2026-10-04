#!/usr/bin/env python3
"""render_queue.py — chạy TUẦN TỰ nhiều wrapper render .cmd, không bao giờ song song.

Vì sao tồn tại (chốt 2026-08-20): máy 6 nhân/6 luồng, một lượt libx264 đã ăn cả 6 nhân.
Chạy 2 render SONG SONG không nhanh hơn tổng thời gian (2 tiến trình giành nhau cùng
6 nhân) mà còn làm máy đơ + tăng rủi ro OOM-kill (bệnh cũ: máy tự kill ffmpeg chạy dài).
→ Nhiều video thì XẾP HÀNG: xong video A mới chạy video B.

Cách dùng (luôn chạy nền theo render-background.md — tool này là MỘT tiến trình dài):
    python E:\\Claude\\Projects\\_media_library\\render_queue.py ^
        E:\\...\\06_VIDEO\\a\\run_render.cmd  E:\\...\\06_VIDEO\\b\\run_render.cmd

- Mỗi .cmd giữ nguyên khuôn render-background.md §2 (tự redirect log + EXITCODE của nó).
- Tool chạy từng cái, in exit code; một cái gãy KHÔNG chặn cái sau (video độc lập),
  nhưng tổng kết cuối liệt kê cái nào gãy, và exit 1 nếu có bất kỳ cái nào gãy.
- Tự hạ priority BELOW_NORMAL (các .cmd con thừa hưởng) — máy mượt trong lúc chạy hàng.
"""
import subprocess
import sys
import time
from pathlib import Path


def low_priority():
    if sys.platform == "win32":
        try:
            import ctypes
            k32 = ctypes.windll.kernel32
            k32.GetCurrentProcess.restype = ctypes.c_void_p  # HANDLE 64-bit — thiếu là fail im lặng
            h = ctypes.c_void_p(k32.GetCurrentProcess())
            k32.SetPriorityClass(h, 0x00004000)  # BELOW_NORMAL
        except Exception:
            pass


def main():
    cmds = [Path(a) for a in sys.argv[1:]]
    if not cmds:
        raise SystemExit("Cách dùng: python render_queue.py <run1.cmd> <run2.cmd> ...")
    missing = [c for c in cmds if not c.exists()]
    if missing:
        raise SystemExit("[LỖI] không thấy file: " + ", ".join(str(m) for m in missing))

    low_priority()
    print(f"HÀNG ĐỢI RENDER: {len(cmds)} việc, chạy tuần tự (priority BELOW_NORMAL)")
    results = []
    for i, c in enumerate(cmds, 1):
        t0 = time.time()
        print(f"\n[{i}/{len(cmds)}] {c}  — bắt đầu {time.strftime('%H:%M:%S')}", flush=True)
        # cwd = folder chứa .cmd để đường dẫn tương đối trong wrapper vẫn đúng
        r = subprocess.run(["cmd", "/c", str(c)], cwd=str(c.parent))
        mins = (time.time() - t0) / 60
        results.append((c, r.returncode, mins))
        print(f"[{i}/{len(cmds)}] exit={r.returncode}  ({mins:.1f} phút)", flush=True)

    print("\n===== TỔNG KẾT HÀNG ĐỢI =====")
    bad = 0
    for c, rc, mins in results:
        mark = "OK " if rc == 0 else "GÃY"
        if rc != 0:
            bad += 1
        print(f"  {mark} exit={rc:<3} {mins:6.1f}'  {c}")
    if bad:
        print(f"[CẢNH BÁO] {bad}/{len(results)} việc gãy — đọc render.log của từng video.")
    raise SystemExit(1 if bad else 0)


if __name__ == "__main__":
    main()
