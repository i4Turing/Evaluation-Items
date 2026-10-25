"""Generate reports.html from 付费报告全文.md: per animal 8 report pages (1080x1440),
1 persona card (1080x1440) and 1 wallpaper (1080x1920).

Usage: python3 build_reports.py   →  writes reports.html next to this script,
then: node shoot_reports.js reports.html <输出目录>
"""
import html
import pathlib
import re

HERE = pathlib.Path(__file__).resolve().parent
SRC = HERE.parents[1] / "付费报告全文.md"
OUT = HERE / "reports.html"

# 与 笔记01_图片/源文件/build.py 保持同一套动物形象和配色
CAPY = """<svg viewBox="0 0 100 100" width="{s}" height="{s}">
<ellipse cx="22" cy="24" rx="9" ry="8" fill="#8E6640"/><ellipse cx="78" cy="24" rx="9" ry="8" fill="#8E6640"/>
<rect x="12" y="20" width="76" height="70" rx="34" fill="#B5875A"/>
<rect x="22" y="50" width="56" height="38" rx="19" fill="#9C7149"/>
<circle cx="34" cy="42" r="5" fill="#3B2A1E"/><circle cx="66" cy="42" r="5" fill="#3B2A1E"/>
<circle cx="35.5" cy="40.5" r="1.6" fill="#fff"/><circle cx="67.5" cy="40.5" r="1.6" fill="#fff"/>
<ellipse cx="42" cy="66" rx="4" ry="2.6" fill="#3B2A1E"/><ellipse cx="58" cy="66" rx="4" ry="2.6" fill="#3B2A1E"/>
<path d="M44 77 Q50 81 56 77" stroke="#3B2A1E" stroke-width="2.4" fill="none" stroke-linecap="round"/>
</svg>"""

LOOK = {  # code: (emoji or None for the drawn capybara, background tint)
    "AAA": ("🦦", "#F9DCC4"), "AAB": (None, "#F1E3C8"), "ABA": ("🦊", "#FBD3B5"), "ABB": ("🐺", "#D9DEE8"),
    "BAA": ("🐰", "#F8D9E0"), "BAB": ("🐋", "#CFE3F0"), "BBA": ("🐱", "#F6E7B8"), "BBB": ("🦉", "#E4E1F2"),
}

SECTIONS = {  # page: (title, icon)
    2: ("你的表里反差", "🎭"), 3: ("社交模式", "🫂"), 4: ("恋爱模式", "💗"),
    5: ("压力时刻", "🌧️"), 6: ("天赋点", "✨"), 7: ("你的搭档", "💞"),
}


def avatar(code, size):
    emoji, bg = LOOK[code]
    inner = (CAPY.format(s=int(size * 0.7)) if emoji is None
             else f'<span style="font-size:{int(size * 0.56)}px;line-height:1">{emoji}</span>')
    return f'<div class="av" style="width:{size}px;height:{size}px;background:{bg}">{inner}</div>'


def esc(text):
    return html.escape(text, quote=False)


def hook(text):
    return esc(text).replace("其实", '<b class="hl">其实</b>')


def fit(texts):
    """Larger body type on pages with less copy, so short pages don't look empty."""
    n = sum(len(t) for t in texts)
    return 40 if n < 150 else 37 if n < 190 else 35 if n < 270 else 33


# ---------- parse markdown ----------

def parse(md):
    cards = {}
    for m in re.finditer(r"^\| ([AB]{3}) \| \S+ (\S+) \| (.+?) \| (.+?) \|$", md, re.M):
        cards[m[1]] = {"name": m[2], "keywords": [k.strip() for k in m[3].split("/")], "wall": m[4]}

    reports = {}
    for m in re.finditer(r"^## \S+ (\S+?)（([AB]{3})）\n(.*?)(?=^## |\Z)", md, re.M | re.S):
        name, code, body = m[1], m[2], m[3]
        pages = {}
        for pm in re.finditer(r"^\*\*P(\d) [^*]+\*\*\n(.*?)(?=^\*\*P\d|^---|\Z)", body, re.M | re.S):
            pages[int(pm[1])] = pm[2].strip()
        rep = {"name": name}
        quotes = re.findall(r"^> (.+)$", pages[1], re.M)
        rep["hook"] = quotes[1].strip("「」")
        for n in (2, 3, 4, 5):
            rep[n] = re.findall(r"^- \*\*(.+?)\*\*：(.+)$", pages[n], re.M)
        rep[6] = re.findall(r"^- (.+)$", pages[6], re.M)
        rep[7] = [(kind, pcode, text.strip()) for kind, pcode, text in
                  re.findall(r"^- \*\*(最佳|磨合)搭档：\S+ \S+（([AB]{3})）\*\*\n\s+(.+)$", pages[7], re.M)]
        rep["quote"] = re.findall(r"^> 「(.+)」$", pages[8], re.M)[0]
        for n in range(2, 8):
            assert rep[n], f"{code} P{n} parse failed"
        assert len(rep[7]) == 2, f"{code} P7 parse failed"
        reports[code] = rep
    assert len(reports) == 8 and len(cards) == 8, (len(reports), len(cards))
    return reports, cards


# ---------- render ----------

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
body{background:#ddd}
.page{width:1080px;height:1440px;position:relative;overflow:hidden;background:#FFF8F0;margin:0 0 20px;
 font-family:'Noto Sans SC','WenQuanYi Zen Hei',sans-serif;color:#4A3B32}
.page.wall{height:1920px}
.kl{font-family:'ZCOOL KuaiLe','Noto Sans SC',sans-serif;font-weight:400}
.av{border-radius:50%;display:flex;align-items:center;justify-content:center;flex-shrink:0}
.hl{color:#E08A4F;font-weight:900}
.pg{position:absolute;top:44px;right:60px;font-size:28px;color:#B9A898;letter-spacing:2px}
.foot{position:absolute;bottom:40px;left:50%;transform:translateX(-50%);font-size:24px;color:#A8968A;white-space:nowrap}
.top{position:absolute;top:36px;left:60px;display:flex;align-items:center;gap:16px;font-size:30px;font-weight:700;color:#8A7563}
.sec{position:absolute;top:150px;left:70px;right:70px}
.sec h2{font-size:80px;line-height:1.2}
.body{position:absolute;top:290px;left:60px;right:60px;display:flex;flex-direction:column;gap:20px}
.card{background:#fff;border-radius:32px;padding:26px 36px 28px;box-shadow:0 6px 0 #F1E2D3}
.lab{display:inline-block;background:#FDE3CF;color:#C46E35;font-weight:900;font-size:30px;border-radius:999px;padding:6px 22px;margin-bottom:14px}
.txt{font-size:33px;line-height:1.7}
.chips{display:flex;gap:16px;justify-content:center;flex-wrap:wrap}
.chip{background:#fff;border:3px solid #F3B58A;color:#C46E35;border-radius:999px;padding:10px 28px;font-size:34px;font-weight:700}
"""

FOOT = '<div class="foot">仅供娱乐 · 不构成专业评估</div>'


def section(file, inner, cls=""):
    return f'<section class="page {cls}" data-file="{file}">{inner}</section>'


def header(code, rep, n):
    return (f'<div class="top">{avatar(code, 64)}<span>{rep["name"]} · {code}</span></div>'
            f'<div class="pg">{n}/8</div>')


def render(code, rep, card):
    folder = f"{code}_{rep['name']}"
    _, tint = LOOK[code]
    out = []

    # P1 cover
    chips = "".join(f'<span class="chip">{k}</span>' for k in card["keywords"])
    out.append(section(f"{folder}/P1.png", f"""
<div class="pg">1/8</div>
<div style="position:absolute;top:0;left:0;right:0;height:690px;background:{tint};border-radius:0 0 50% 50%/0 0 120px 120px"></div>
<div style="position:absolute;top:90px;left:0;right:0;text-align:center;font-size:32px;font-weight:700;color:#8A7563;letter-spacing:6px">你的专属隐藏人格解读</div>
<div style="position:absolute;top:190px;left:50%;transform:translateX(-50%);border:14px solid #FFF8F0;border-radius:50%">{avatar(code, 440)}</div>
<div style="position:absolute;top:720px;left:0;right:0;text-align:center">
 <div class="kl" style="font-size:130px;line-height:1.1">{rep['name']}</div>
 <div style="font-size:48px;font-weight:900;letter-spacing:14px;color:#E08A4F;margin-top:6px">{code}</div>
</div>
<div style="position:absolute;top:1000px;left:90px;right:90px;text-align:center;font-size:38px;line-height:1.65;font-weight:700;text-wrap:balance">「{hook(rep['hook'])}」</div>
<div class="chips" style="position:absolute;top:1200px;left:60px;right:60px">{chips}</div>
{FOOT}"""))

    # P2–P5 labelled bullets
    for n in (2, 3, 4, 5):
        title, icon = SECTIONS[n]
        fs = fit([t for _, t in rep[n]])
        cards = "".join(f'<div class="card"><div class="lab">{esc(lab)}</div><div class="txt" style="font-size:{fs}px">{esc(t)}</div></div>'
                        for lab, t in rep[n])
        out.append(section(f"{folder}/P{n}.png", f"""{header(code, rep, n)}
<div class="sec"><h2 class="kl">{title} {icon}</h2></div><div class="body">{cards}</div>{FOOT}"""))

    # P6 talents
    title, icon = SECTIONS[6]
    labs = ["你的超能力", "你的优势"]
    fs = fit(rep[6])
    cards = "".join(f'<div class="card"><div class="lab">{labs[i] if i < 2 else "另外"}</div><div class="txt" style="font-size:{fs}px">{esc(t)}</div></div>'
                    for i, t in enumerate(rep[6]))
    out.append(section(f"{folder}/P6.png", f"""{header(code, rep, 6)}
<div class="sec"><h2 class="kl">{title} {icon}</h2></div><div class="body">{cards}</div>{FOOT}"""))

    # P7 partners
    title, icon = SECTIONS[7]
    cards = ""
    fs = fit([t for _, _, t in rep[7]])
    for kind, pcode, text in rep[7]:
        pname = REPORTS[pcode]["name"]
        lab = "最佳搭档" if kind == "最佳" else "磨合搭档"
        cards += (f'<div class="card"><div style="display:flex;align-items:center;gap:26px;margin-bottom:18px">'
                  f'{avatar(pcode, 130)}<div><div class="lab" style="margin:0 0 6px">{lab}</div>'
                  f'<div style="font-size:46px;font-weight:900">{pname} · {pcode}</div></div></div>'
                  f'<div class="txt" style="font-size:{fs}px">{esc(text)}</div></div>')
    out.append(section(f"{folder}/P7.png", f"""{header(code, rep, 7)}
<div class="sec"><h2 class="kl">{title} {icon}</h2></div><div class="body">{cards}</div>{FOOT}"""))

    # P8 closing
    out.append(section(f"{folder}/P8.png", f"""<div class="pg">8/8</div>
<div style="position:absolute;top:150px;left:0;right:0;text-align:center;font-size:34px;font-weight:700;color:#8A7563;letter-spacing:6px">给你的一句话</div>
<div style="position:absolute;top:260px;left:50%;transform:translateX(-50%)">{avatar(code, 300)}</div>
<div class="kl" style="position:absolute;top:640px;left:90px;right:90px;text-align:center;font-size:68px;line-height:1.5;text-wrap:balance">「{esc(rep['quote'])}」</div>
<div style="position:absolute;top:1060px;left:120px;right:120px;background:#fff;border-radius:28px;padding:26px;text-align:center;font-size:30px;line-height:1.6;color:#8A7563;box-shadow:0 6px 0 #F1E2D3">
 你的专属人格卡和手机壁纸在后面 👉<br>记得发给你的搭子，看看 ta 是哪只～</div>
<div style="position:absolute;bottom:44px;left:0;right:0;text-align:center;font-size:24px;color:#A8968A">本测试仅供娱乐，不构成任何心理学或医学评估。</div>"""))

    # persona card
    chips = "".join(f'<span class="chip">{k}</span>' for k in card["keywords"])
    out.append(section(f"{folder}/人格卡.png", f"""
<div style="position:absolute;inset:50px;background:{tint};border-radius:60px"></div>
<div style="position:absolute;inset:80px;background:#FFF8F0;border-radius:44px;border:4px dashed {tint}"></div>
<div style="position:absolute;top:150px;left:0;right:0;text-align:center;font-size:32px;font-weight:700;color:#8A7563;letter-spacing:8px">MY HIDDEN ANIMAL</div>
<div style="position:absolute;top:240px;left:50%;transform:translateX(-50%)">{avatar(code, 400)}</div>
<div style="position:absolute;top:680px;left:0;right:0;text-align:center">
 <div class="kl" style="font-size:120px;line-height:1.1">{rep['name']}</div>
 <div style="font-size:46px;font-weight:900;letter-spacing:14px;color:#E08A4F;margin-top:8px">{code}</div>
</div>
<div class="chips" style="position:absolute;top:930px;left:120px;right:120px">{chips}</div>
<div style="position:absolute;top:1080px;left:150px;right:150px;text-align:center;font-size:32px;line-height:1.6;font-weight:700;text-wrap:balance">「{hook(rep['hook'])}」</div>
<div style="position:absolute;bottom:110px;left:0;right:0;text-align:center;font-size:24px;color:#A8968A">你的隐藏动物人格 · 仅供娱乐</div>""", "card-page"))

    # wallpaper 1080x1920 — top third kept clear for the lock-screen clock
    out.append(section(f"{folder}/壁纸.png", f"""
<div style="position:absolute;inset:0;background:linear-gradient(180deg,#FFF8F0 0%,#FFF8F0 35%,{tint} 100%)"></div>
<div style="position:absolute;top:820px;left:50%;transform:translateX(-50%)">{avatar(code, 480)}</div>
<div class="kl" style="position:absolute;top:1360px;left:60px;right:60px;text-align:center;font-size:76px;line-height:1.4">{card['wall']}</div>
<div style="position:absolute;top:1500px;left:0;right:0;text-align:center;font-size:34px;font-weight:700;color:#8A7563;letter-spacing:8px">{rep['name']} · {code}</div>""",
                       "wall"))
    return out


md = SRC.read_text(encoding="utf-8")
REPORTS, CARDS = parse(md)
pages = []
for c in sorted(REPORTS):
    pages += render(c, REPORTS[c], CARDS[c])

OUT.write_text(f"""<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;700;900&family=ZCOOL+KuaiLe&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body>{''.join(pages)}</body></html>""", encoding="utf-8")
print(f"wrote {OUT} ({len(pages)} pages)")
