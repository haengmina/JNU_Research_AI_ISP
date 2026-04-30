"""
Generate Infinite-ISP pipeline flow diagram (Visio-style)
Output: infinite_isp_pipeline.png
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import matplotlib.patheffects as pe

FS = 4.0   # font size multiplier

C = {
    "bg":     "#F0F4F8",
    "title":  "#1A237E",
    "input":  "#1565C0",
    "bayer":  "#2E7D32",
    "trans":  "#F57F17",
    "rgb":    "#6A1B9A",
    "aa":     "#BF360C",
    "yuv":    "#00695C",
    "out":    "#37474F",
    "output": "#B71C1C",
    "arrow":  "#455A64",
    "fb":     "#E53935",
}

FW     = 26       # wide enough for 3A boxes
FH     = 85
CX     = 10.0     # main pipeline centre
CX3A   = 21.5     # 3A modules centre
BOX_W  = 7.0
BOX_H  = 2.2
BOX3AW = 6.0
GAP    = 3.0      # vertical gap between box centres

fig = plt.figure(figsize=(FW, FH), facecolor=C["bg"])
ax  = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, FW)
ax.set_ylim(0, FH)
ax.axis("off")

# ── Helpers ────────────────────────────────────────────────────────────────────
def box(cx, cy, label, sub="", color=C["bayer"], w=None, h=BOX_H, fs=None):
    bw = w  if w  is not None else BOX_W
    fs = fs if fs is not None else round(11 * FS)
    rect = FancyBboxPatch(
        (cx - bw / 2, cy - h / 2), bw, h,
        boxstyle="round,pad=0.08",
        facecolor=color, edgecolor="white", linewidth=2.0, zorder=4,
    )
    rect.set_path_effects([pe.withSimplePatchShadow(offset=(3, -3), shadow_rgbFace="#00000033")])
    ax.add_patch(rect)
    if sub:
        ax.text(cx, cy + 0.36, label, ha="center", va="center",
                color="white", fontsize=fs, fontweight="bold", zorder=5)
        ax.text(cx, cy - 0.48, sub, ha="center", va="center",
                color="white", fontsize=round(8 * FS), zorder=5, alpha=0.90)
    else:
        ax.text(cx, cy, label, ha="center", va="center",
                color="white", fontsize=fs, fontweight="bold", zorder=5)

def varrow(x, y_from, y_to, color=C["arrow"], lw=2.0):
    ax.annotate("", xy=(x, y_to), xytext=(x, y_from),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw,
                                mutation_scale=20))

def harrow(x_from, x_to, y, color=C["arrow"], lw=2.0):
    ax.annotate("", xy=(x_to, y), xytext=(x_from, y),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw,
                                mutation_scale=18))

def feedback(x_src, y_src, x_dst, y_dst, label="", bend_x=None):
    bx = bend_x if bend_x is not None else x_src - 0.8
    ax.plot([x_src, bx], [y_src, y_src], color=C["fb"], lw=2.0, zorder=3)
    ax.plot([bx,   bx ], [y_src, y_dst], color=C["fb"], lw=2.0, zorder=3)
    ax.annotate("", xy=(x_dst, y_dst), xytext=(bx, y_dst),
                arrowprops=dict(arrowstyle="-|>", color=C["fb"], lw=2.0,
                                mutation_scale=16))
    if label:
        ax.text(bx - 0.2, (y_src + y_dst) / 2, label,
                ha="right", va="center", fontsize=round(7.5 * FS), color=C["fb"],
                fontstyle="italic", linespacing=1.4, zorder=5)

def domain_band(y_top, y_bot, label, color):
    rect = FancyBboxPatch(
        (0.6, y_bot - 0.4), FW - 1.2, y_top - y_bot + 0.8,
        boxstyle="round,pad=0.0",
        facecolor=color, edgecolor="none", alpha=0.18, zorder=1,
    )
    ax.add_patch(rect)
    ax.text(1.05, (y_top + y_bot) / 2, label,
            ha="center", va="center", fontsize=round(8 * FS), color=color,
            fontweight="bold", rotation=90, zorder=2, alpha=0.85)

# ══════════════════════════════════════════════════════════════════════════════
# Title
# ══════════════════════════════════════════════════════════════════════════════
ax.text(FW / 2, FH - 2.0, "Infinite-ISP Pipeline Flow",
        ha="center", va="center", fontsize=round(22 * FS),
        fontweight="bold", color=C["title"], zorder=5)
ax.text(FW / 2, FH - 3.8, "infinite_isp.py  ·  run_pipeline()",
        ha="center", va="center", fontsize=round(11 * FS), color="#546E7A", zorder=5)
ax.hlines(FH - 5.0, 1.0, FW - 1.0, colors="#90A4AE", linewidth=1.5)

# ══════════════════════════════════════════════════════════════════════════════
# Y positions
# ══════════════════════════════════════════════════════════════════════════════
Y = {}
y = FH - 8.0
for name in [
    "load_raw", "crop", "dpc", "blc", "oecf", "dg", "lsc", "bnr",
    "wb", "demosaic", "ccm", "gc",
    "csc", "ldci", "sharp", "nr2d",
    "rgbc", "scale", "yuv_c", "output",
]:
    Y[name] = y
    y -= GAP

# ── Domain bands ───────────────────────────────────────────────────────────────
domain_band(Y["crop"]    + 1.8, Y["bnr"]     - 1.8, "Bayer Domain",      C["bayer"])
domain_band(Y["demosaic"]+ 1.8, Y["demosaic"]- 1.8, "Demosaic",          C["trans"])
domain_band(Y["ccm"]     + 1.8, Y["gc"]      - 1.8, "RGB Domain",        C["rgb"])
domain_band(Y["csc"]     + 1.8, Y["nr2d"]    - 1.8, "YUV Domain",        C["yuv"])
domain_band(Y["rgbc"]    + 1.8, Y["yuv_c"]   - 1.8, "Output Conversion", C["out"])

# ── Module boxes ───────────────────────────────────────────────────────────────
box(CX, Y["load_raw"], "Load RAW",  "np.fromfile / rawpy.imread",   C["input"])
box(CX, Y["crop"],     "Crop",      "Cropping",                     C["bayer"])
box(CX, Y["dpc"],      "DPC",       "Dead Pixel Correction",        C["bayer"])
box(CX, Y["blc"],      "BLC",       "Black Level Correction",       C["bayer"])
box(CX, Y["oecf"],     "OECF",      "Opto-Electronic Conv. Func.",  C["bayer"])
box(CX, Y["dg"],       "DG",        "Digital Gain",                 C["bayer"])
box(CX, Y["lsc"],      "LSC",       "Lens Shading Correction",      C["bayer"])
box(CX, Y["bnr"],      "BNR",       "Bayer Noise Reduction",        C["bayer"])
box(CX, Y["wb"],       "WB",        "White Balance",                C["bayer"])
box(CX, Y["demosaic"], "Demosaic",  "CFA Demosaicing",              C["trans"])
box(CX, Y["ccm"],      "CCM",       "Color Correction Matrix",      C["rgb"])
box(CX, Y["gc"],       "GC",        "Gamma Correction",             C["rgb"])
box(CX, Y["csc"],      "CSC",       "Color Space Conversion",       C["yuv"])
box(CX, Y["ldci"],     "LDCI",      "Local Dynamic Contrast Impr.", C["yuv"])
box(CX, Y["sharp"],    "Sharp",     "Sharpening",                   C["yuv"])
box(CX, Y["nr2d"],     "NR2D",      "2D Noise Reduction",           C["yuv"])
box(CX, Y["rgbc"],     "RGBC",      "RGB Conversion",               C["out"])
box(CX, Y["scale"],    "Scale",     "Scaling",                      C["out"])
box(CX, Y["yuv_c"],    "YUV_C",     "YUV Format Conversion",        C["out"])
box(CX, Y["output"],   "Output",    "Save / Display Image",         C["output"])

# ── 3A boxes ───────────────────────────────────────────────────────────────────
Y_AWB = (Y["bnr"] + Y["wb"])  / 2
Y_AE  = (Y["gc"]  + Y["csc"]) / 2
box(CX3A, Y_AWB, "AWB", "Auto White Balance  (3A)", C["aa"], w=BOX3AW)
box(CX3A, Y_AE,  "AE",  "Auto Exposure  (3A)",      C["aa"], w=BOX3AW)

# ── Main flow arrows ───────────────────────────────────────────────────────────
pipeline_order = [
    "load_raw","crop","dpc","blc","oecf","dg","lsc","bnr",
    "wb","demosaic","ccm","gc",
    "csc","ldci","sharp","nr2d",
    "rgbc","scale","yuv_c","output",
]
for a, b in zip(pipeline_order, pipeline_order[1:]):
    varrow(CX, Y[a] - BOX_H / 2, Y[b] + BOX_H / 2)

# ── BNR → AWB ─────────────────────────────────────────────────────────────────
harrow(CX + BOX_W / 2, CX3A - BOX3AW / 2, Y["bnr"])
varrow(CX3A, Y["bnr"] - BOX_H / 2 - 0.1, Y_AWB + BOX_H / 2 + 0.1)

# ── GC → AE ───────────────────────────────────────────────────────────────────
harrow(CX + BOX_W / 2, CX3A - BOX3AW / 2, Y["gc"])
varrow(CX3A, Y["gc"] - BOX_H / 2 - 0.1, Y_AE + BOX_H / 2 + 0.1)

# ── AWB feedback → WB ─────────────────────────────────────────────────────────
feedback(
    CX3A - BOX3AW / 2, Y_AWB,
    CX + BOX_W / 2,    Y["wb"],
    label="r_gain / b_gain",
    bend_x=CX3A - BOX3AW / 2 - 0.6,
)

# ── AE feedback → DG ──────────────────────────────────────────────────────────
feedback(
    CX3A - BOX3AW / 2, Y_AE,
    CX + BOX_W / 2,    Y["dg"],
    label="ae_feedback /\ncurrent_gain",
    bend_x=CX3A - BOX3AW / 2 - 0.6,
)

# ── 3A convergence loop annotation ────────────────────────────────────────────
loop_x     = 2.8
loop_y_top = Y["dg"]     + 1.4
loop_y_bot = Y["output"] + 1.4
ax.plot([loop_x, loop_x], [loop_y_bot, loop_y_top], color="#78909C", lw=1.8, zorder=3)
ax.annotate("", xy=(loop_x, loop_y_top), xytext=(loop_x, loop_y_bot),
            arrowprops=dict(arrowstyle="-|>", color="#78909C", lw=1.8, mutation_scale=18))
ax.text(loop_x - 0.3, (loop_y_top + loop_y_bot) / 2,
        "3A Loop\n(render_3a=True)\nrepeat until\nAE converges",
        ha="right", va="center", fontsize=round(8 * FS), color="#455A64",
        fontstyle="italic", linespacing=1.5, zorder=5)

# ══════════════════════════════════════════════════════════════════════════════
# Legend
# ══════════════════════════════════════════════════════════════════════════════
leg_x0 = 1.2
leg_y0 = y - 1.5    # just below the last module row
leg_sp = 1.3

legend_items = [
    (C["input"],  "Load / Input"),
    (C["bayer"],  "Bayer Domain"),
    (C["trans"],  "Demosaic (Transition)"),
    (C["rgb"],    "RGB Domain"),
    (C["yuv"],    "YUV Domain"),
    (C["out"],    "Output Conversion"),
    (C["output"], "Final Output"),
    (C["aa"],     "3A Modules (AWB / AE)"),
]

ax.text(leg_x0, leg_y0 + 1.5, "Legend",
        fontsize=round(10 * FS), fontweight="bold", color=C["title"], zorder=5)

for i, (c, lbl) in enumerate(legend_items):
    ry = leg_y0 - i * leg_sp
    sw = FancyBboxPatch((leg_x0, ry - 0.40), 1.4, 0.9,
                        boxstyle="round,pad=0.03",
                        facecolor=c, edgecolor="white", linewidth=1, zorder=4)
    ax.add_patch(sw)
    ax.text(leg_x0 + 1.8, ry + 0.05, lbl,
            ha="left", va="center", fontsize=round(8.5 * FS), color="#263238", zorder=5)

n = len(legend_items)
fb_ry = leg_y0 - n * leg_sp
ax.annotate("", xy=(leg_x0 + 1.4, fb_ry + 0.05),
            xytext=(leg_x0, fb_ry + 0.05),
            arrowprops=dict(arrowstyle="-|>", color=C["fb"], lw=2.0, mutation_scale=14))
ax.text(leg_x0 + 1.8, fb_ry + 0.05, "3A Feedback",
        ha="left", va="center", fontsize=round(8.5 * FS), color="#263238", zorder=5)

leg_rect = FancyBboxPatch(
    (leg_x0 - 0.5, leg_y0 - (n + 1) * leg_sp - 0.5),
    12.0, (n + 1) * leg_sp + 2.6,
    boxstyle="round,pad=0.05",
    facecolor="white", edgecolor="#B0BEC5", linewidth=1.5, alpha=0.82, zorder=3,
)
ax.add_patch(leg_rect)

# ── Footer ─────────────────────────────────────────────────────────────────────
footer_y = leg_y0 - (n + 1) * leg_sp - 1.2
ax.hlines(footer_y, 1.0, FW - 1.0, colors="#90A4AE", linewidth=1.2)
ax.text(FW / 2, footer_y - 1.0,
        "Infinite-ISP  ·  10xEngineers Pvt Ltd  ·  infinite_isp.py",
        ha="center", va="center", fontsize=round(8.5 * FS), color="#78909C")

# ── Save ───────────────────────────────────────────────────────────────────────
out_path = "infinite_isp_pipeline.png"
fig.savefig(out_path, dpi=150, bbox_inches="tight", facecolor=C["bg"])
print(f"Saved → {out_path}")
