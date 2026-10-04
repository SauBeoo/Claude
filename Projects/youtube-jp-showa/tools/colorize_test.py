# -*- coding: utf-8 -*-
"""Test AI to mau phim den trang (Zhang 2016 / OpenCV dnn, CPU).
Usage: python tools/colorize_test.py <in.mp4> <out.mp4>
"""
import sys
import cv2
import numpy as np

MODELS = r"E:\Claude\Projects\youtube-jp-showa\06_VIDEO\_footage_test\_colorize"

def main(src, dst):
    net = cv2.dnn.readNetFromCaffe(
        MODELS + r"\colorization_deploy_v2.prototxt",
        MODELS + r"\colorization_release_v2.caffemodel")
    pts = np.load(MODELS + r"\pts_in_hull.npy").transpose().reshape(2, 313, 1, 1)
    net.getLayer(net.getLayerId("class8_ab")).blobs = [pts.astype(np.float32)]
    net.getLayer(net.getLayerId("conv8_313_rh")).blobs = [np.full([1, 313], 2.606, np.float32)]

    cap = cv2.VideoCapture(src)
    fps = cap.get(cv2.CAP_PROP_FPS) or 25
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    out = cv2.VideoWriter(dst, cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))

    i = 0
    prev_ab = None
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        img = frame.astype(np.float32) / 255.0
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        L = lab[:, :, 0]
        Ls = cv2.resize(L, (224, 224)) - 50
        net.setInput(cv2.dnn.blobFromImage(Ls))
        ab = net.forward()[0].transpose((1, 2, 0))
        ab = cv2.resize(ab, (w, h))
        # giam flicker: tron 60% frame nay + 40% frame truoc
        if prev_ab is not None:
            ab = 0.6 * ab + 0.4 * prev_ab
        prev_ab = ab
        # ha bao hoa nhe cho ra chat phim cu (mau AI goc hay loe)
        ab *= 0.82
        colorized = np.concatenate((L[:, :, np.newaxis], ab), axis=2)
        bgr = cv2.cvtColor(colorized, cv2.COLOR_LAB2BGR)
        out.write((np.clip(bgr, 0, 1) * 255).astype(np.uint8))
        i += 1
        if i % 50 == 0:
            print(f"{i}/{n} frames", flush=True)
    cap.release(); out.release()
    print(f"XONG {i} frames -> {dst}")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
