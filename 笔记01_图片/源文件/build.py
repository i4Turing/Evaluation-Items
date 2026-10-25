"""Generate note01.html: 9 (+1 variant) pages of 1080x1440 for Xiaohongshu note 01."""
import pathlib

OUT = pathlib.Path(__file__).with_name("note01.html")  # 生成的 HTML 与本脚本同目录

CAPY = """<svg viewBox="0 0 100 100" width="{s}" height="{s}">
<ellipse cx="22" cy="24" rx="9" ry="8" fill="#8E6640"/><ellipse cx="78" cy="24" rx="9" ry="8" fill="#8E6640"/>
<rect x="12" y="20" width="76" height="70" rx="34" fill="#B5875A"/>
<rect x="22" y="50" width="56" height="38" rx="19" fill="#9C7149"/>
<circle cx="34" cy="42" r="5" fill="#3B2A1E"/><circle cx="66" cy="42" r="5" fill="#3B2A1E"/>
<circle cx="35.5" cy="40.5" r="1.6" fill="#fff"/><circle cx="67.5" cy="40.5" r="1.6" fill="#fff"/>
<ellipse cx="42" cy="66" rx="4" ry="2.6" fill="#3B2A1E"/><ellipse cx="58" cy="66" rx="4" ry="2.6" fill="#3B2A1E"/>
<path d="M44 77 Q50 81 56 77" stroke="#3B2A1E" stroke-width="2.4" fill="none" stroke-linecap="round"/>
</svg>"""

ANIMALS = {
    "AAA": ("海獭", "🦦", "#F9DCC4", "表面是全场气氛组，其实是需要被牵着手才睡得着的海獭。"),
    "AAB": ("水豚", None, "#F1E3C8", "表面跟谁都聊得来，其实你的情绪稳定，是一次次自己消化出来的。"),
    "ABA": ("狐狸", "🦊", "#FBD3B5", "表面嘻嘻哈哈，其实心里门儿清，谁真谁假你一眼就看穿。"),
    "ABB": ("狼", "🐺", "#D9DEE8", "表面好相处，其实边界感拉满；认定的人，你会护很久。"),
    "BAA": ("兔子", "🐰", "#F8D9E0", "表面安安静静，其实内心小剧场每天加更三集。"),
    "BAB": ("鲸", "🐋", "#CFE3F0", "表面淡淡的，其实你的感受力深到连自己都惊讶。"),
    "BBA": ("猫", "🐱", "#F6E7B8", "表面高冷不好接近，其实只是懒得解释，想做的事谁也拦不住。"),
    "BBB": ("雪鸮", "🦉", "#E4E1F2", "表面低调到没存在感，其实你是全场最清醒的那个人。"),
}


def avatar(code, size, extra_style=""):
    name, emoji, bg, _ = ANIMALS[code]
    inner = CAPY.format(s=int(size * 0.7)) if emoji is None else f'<span style="font-size:{int(size*0.56)}px;line-height:1">{emoji}</span>'
    return (f'<div class="av" style="width:{size}px;height:{size}px;background:{bg};{extra_style}">{inner}</div>')


def hl(text):
    return text.replace("其实", '<b class="hl">其实</b>')


QUESTIONS = [
    ("PART 1", "别人眼中的你", "", [
        ("🍲", "一个只认识一个人的饭局，你通常会：", "跟旁边的人搭话，几分钟就聊熟了", "坐在熟人旁边，先听大家聊"),
        ("💬", "群聊里有人发了个冷笑话，没人接：", "我来接，不能让它掉在地上", "默默看着，自己偷偷笑一下"),
        ("🌙", "周五晚上的安排突然取消了：", "赶紧问问还有谁有空", "太好了，终于可以一个人待着"),
        ("🎤", "新学期 / 新入职自我介绍：", "顺便抖个机灵，让大家记住我", "名字 + 一句话，赶紧坐下"),
    ]),
    ("PART 2", "你心里的那个你", "这一页，诚实一点哦🤫", [
        ("📱", "ta 回消息比平时慢了很多：", "忍不住想是不是我哪句话说错了", "大概在忙吧，不影响我干自己的事"),
        ("🎒", "室友 / 同事借了东西一直没还：", "算了算了，开口太尴尬", "直接提醒，是我的就是我的"),
        ("🎬", "看一部公认很好哭的电影：", "前半小时就开始掉眼泪", "会感动，但很少真的哭出来"),
        ("🗣️", "你的想法被人当众否定了：", "表面说“没事”，回去反复想好几天", "不爽一下，然后想想 ta 说得对不对"),
    ]),
    ("PART 3", "你做决定的方式", "", [
        ("✈️", "旅行出发前：", "订好票就行，剩下的到了再说", "攻略、路线、备选方案都做好了"),
        ("💗", "喜欢上一个人：", "藏不住，喜欢就想让 ta 知道", "先观察很久，确认了再说"),
        ("⏰", "deadline 还有一周：", "前五天在“酝酿”，最后两天爆发", "拆成小任务，每天做一点"),
        ("🛒", "想买的东西刚好降价了：", "立刻下单，快乐最重要", "先加购物车，再比比价"),
    ]),
]

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
body{background:#ddd}
.page{width:1080px;height:1440px;position:relative;overflow:hidden;background:#FFF8F0;
 font-family:'Noto Sans SC','WenQuanYi Zen Hei',sans-serif;color:#4A3B32;margin:0 0 20px}
.page.deep{background:#FBEEE1}
.kl{font-family:'ZCOOL KuaiLe','Noto Sans SC',sans-serif;font-weight:400}
.pg{position:absolute;top:44px;right:60px;font-size:28px;color:#B9A898;letter-spacing:2px}
.foot{position:absolute;bottom:40px;left:50%;transform:translateX(-50%);font-size:24px;color:#A8968A;background:rgba(255,248,240,.92);padding:6px 22px;border-radius:999px;z-index:5;white-space:nowrap}
.av{border-radius:50%;display:flex;align-items:center;justify-content:center;flex-shrink:0}
.hl{color:#E08A4F;font-weight:900}
.accent{color:#E08A4F}
.chip{display:inline-block;background:#F3B58A;color:#fff;border-radius:999px;padding:10px 30px;font-size:30px;font-weight:700}
/* question pages */
.qhead{position:absolute;top:84px;left:80px;right:80px}
.qhead .part{font-size:30px;font-weight:900;color:#E08A4F;letter-spacing:4px}
.qhead h2{font-size:72px;margin-top:4px}
.qhead .tip{position:absolute;right:0;bottom:12px;font-size:28px;color:#A38E7C}
.qlist{position:absolute;top:236px;left:70px;right:70px;display:flex;flex-direction:column;gap:16px}
.card{background:#fff;border-radius:30px;padding:18px 30px 20px;box-shadow:0 6px 0 #F1E2D3}
.card .q{font-size:34px;line-height:1.35;font-weight:700;display:flex;align-items:center;gap:14px}
.card .q .n{background:#4A3B32;color:#fff;border-radius:50%;width:44px;height:44px;font-size:26px;display:flex;align-items:center;justify-content:center;flex-shrink:0}
.card .q .ic{margin-left:auto;font-size:40px}
.opt{margin-top:8px;font-size:30px;line-height:1.35;background:#FFF3E8;border-radius:16px;padding:6px 22px;display:flex;gap:16px;align-items:center}
.opt .l{font-weight:900;color:#E08A4F;font-size:34px}
.letter{margin-top:6px;background:#4A3B32;color:#fff;border-radius:28px;padding:24px 30px;text-align:center;font-size:34px;font-weight:700;line-height:1.5}
.letter .y{color:#F7C9A3}
/* result pages */
.rhead{position:absolute;top:96px;left:0;right:0;text-align:center}
.rhead h2{font-size:84px}
.rhead p{font-size:34px;color:#8A7563;margin-top:10px}
.grid{position:absolute;top:300px;left:60px;right:60px;display:grid;grid-template-columns:1fr 1fr;gap:28px}
.cell{background:#fff;border-radius:36px;padding:30px 30px 34px;text-align:center;display:flex;flex-direction:column;align-items:center;box-shadow:0 6px 0 #F1E2D3;height:445px}
.cell .code{font-size:52px;font-weight:900;letter-spacing:6px;margin-top:16px;line-height:1}
.cell .nm{font-size:34px;font-weight:700;color:#E08A4F;margin-top:8px}
.cell .ln{font-size:27px;line-height:1.5;margin-top:12px;color:#5C4A3E}
"""


def page(n, body, cls="", total=9):
    return (f'<section class="page {cls}" id="P{n}"><div class="pg">{str(n)[0]}/{total}</div>{body}'
            f'<div class="foot">仅供娱乐 · 不构成专业评估</div></section>')


pages = []

# P1 cover
cover_av = [
    ("AAA", 250, "left:-60px;top:120px;transform:rotate(-12deg)"),
    ("BBA", 230, "right:-50px;top:90px;transform:rotate(14deg)"),
    ("ABA", 210, "left:-40px;top:560px;transform:rotate(8deg)"),
    ("BAB", 220, "right:-60px;top:520px;transform:rotate(-10deg)"),
    ("AAB", 240, "left:40px;bottom:-40px;transform:rotate(-6deg)"),
    ("BAA", 220, "left:300px;bottom:-60px;transform:rotate(4deg)"),
    ("ABB", 240, "left:540px;bottom:-50px;transform:rotate(-8deg)"),
    ("BBB", 250, "right:-40px;bottom:-30px;transform:rotate(10deg)"),
]
avs = "".join(f'<div style="position:absolute;{st}">{avatar(c, s)}</div>' for c, s, st in cover_av)
pages.append(page(1, f"""{avs}
<div style="position:absolute;top:340px;left:0;right:0;text-align:center">
 <div class="chip" style="font-size:34px;transform:rotate(-3deg)">测完沉默了…</div>
 <h1 class="kl" style="font-size:150px;line-height:1.18;margin-top:40px">你骨子里<br>是哪种动物<span class="accent">？</span></h1>
 <div style="font-size:52px;font-weight:900;margin-top:40px">12 题测出你的<span class="hl" style="background:#FDE3CF;padding:0 12px;border-radius:12px">隐藏人格</span>🐾</div>
 <div style="font-size:32px;color:#8A7563;margin-top:28px">别人眼中的你 vs 心里真实的你</div>
</div>"""))

# P2 rules
steps = [("①", "凭<b class='hl'>第一反应</b>选，别想太久"),
         ("②", "每页数一数：<b class='hl'>A 多还是 B 多</b>？<br>记下这个字母"),
         ("③", "三页凑成<b class='hl'>三个字母</b>（比如 A-B-A）<br>翻到最后查你的动物！")]
steps_html = "".join(f'<div class="card" style="display:flex;gap:26px;align-items:center;padding:24px 34px"><div class="kl" style="font-size:64px;color:#E08A4F">{a}</div><div style="font-size:40px;line-height:1.5;font-weight:700">{b}</div></div>' for a, b in steps)
pages.append(page(2, f"""
<div style="position:absolute;top:96px;left:80px;right:80px">
 <h2 class="kl" style="font-size:96px">玩法超简单 ✍️</h2>
 <div style="display:flex;flex-direction:column;gap:20px;margin-top:36px">{steps_html}</div>
 <div style="margin-top:30px;text-align:center">
  <div style="font-size:30px;color:#8A7563;margin-bottom:18px">你的答题卡</div>
  <div style="display:flex;justify-content:center;align-items:center;gap:22px;font-size:64px;font-weight:900">
   <div style="width:130px;height:130px;border:6px solid #E08A4F;border-radius:28px;display:flex;align-items:center;justify-content:center;color:#E08A4F">A</div>–
   <div style="width:130px;height:130px;border:6px dashed #CBB6A2;border-radius:28px"></div>–
   <div style="width:130px;height:130px;border:6px dashed #CBB6A2;border-radius:28px"></div>
  </div>
 </div>
 <div style="margin-top:30px;background:#FDE9D8;border-radius:28px;padding:26px 34px;font-size:32px;line-height:1.6">
  💡 平局怎么办？以<b>本页最后一题</b>为准～<br>📝 建议截图或拿纸笔记一下哦
 </div>
</div>
<div style="position:absolute;top:1250px;left:0;right:0;text-align:center;font-size:40px;font-weight:900">👉 往后翻，开始测试</div>"""))

# P3-P5 questions
for pi, (part, title, tip, qs) in enumerate(QUESTIONS):
    n0 = pi * 4
    cards = "".join(
        f'<div class="card"><div class="q"><span class="n">{n0+i+1}</span><span>{q}</span><span class="ic">{ic}</span></div>'
        f'<div class="opt"><span class="l">A</span><span>{a}</span></div>'
        f'<div class="opt"><span class="l">B</span><span>{b}</span></div></div>'
        for i, (ic, q, a, b) in enumerate(qs))
    tip_html = f'<div class="tip">{tip}</div>' if tip else ""
    last = '<br><span class="y">🎉 拿好你的三个字母，翻到下一页揭晓！</span>' if pi == 2 else ""
    pages.append(page(3 + pi, f"""
<div class="qhead"><div class="part">{part}</div><h2 class="kl">{title}</h2>{tip_html}</div>
<div class="qlist">{cards}<div class="letter">第 {pi+1} 个字母：A 多 → <span class="y">A</span>　　B 多 → <span class="y">B</span>{last}</div></div>""",
                      cls="deep" if pi == 1 else ""))

# P6-P7 results
for pi, (first, sub) in enumerate([("A", "别人眼中的你很热闹"), ("B", "别人眼中的你很安静")]):
    codes = [c for c in ANIMALS if c[0] == first]
    cells = "".join(
        f'<div class="cell">{avatar(c, 150)}<div class="code">{c}</div><div class="nm">{ANIMALS[c][0]}</div>'
        f'<div class="ln">{hl(ANIMALS[c][3])}</div></div>' for c in codes)
    pages.append(page(6 + pi, f"""
<div class="rhead"><h2 class="kl">你的隐藏动物是……</h2><p>第一个字母是 <b class="hl">{first}</b>：{sub}</p></div>
<div class="grid">{cells}</div>"""))

# P8 pairs
pairs = [("AAA", "BAB"), ("AAB", "BAA"), ("ABA", "BBB"), ("ABB", "BBA")]
pair_html = "".join(
    f'<div class="card" style="display:flex;align-items:center;justify-content:center;gap:30px;padding:16px">'
    f'{avatar(a, 110)}<div style="font-size:38px;font-weight:900;width:110px;text-align:center">{ANIMALS[a][0]}</div>'
    f'<div style="font-size:54px;color:#E08A4F">💞</div>'
    f'<div style="font-size:38px;font-weight:900;width:110px;text-align:center">{ANIMALS[b][0]}</div>{avatar(b, 110)}</div>'
    for a, b in pairs)
pages.append(page(8, f"""
<div class="rhead"><h2 class="kl">你的天选搭档是？💞</h2></div>
<div style="position:absolute;top:260px;left:80px;right:80px;display:flex;flex-direction:column;gap:22px">{pair_html}</div>
<div style="position:absolute;top:1060px;left:60px;right:60px;text-align:center;font-size:36px;line-height:1.6">
 内心同频，性格互补，这样的搭档最舒服✨<br><b>快让你的 <span class="hl">搭子 / 室友 / ta</span> 也测一测</b><br>看看你们是不是天选组合！
</div>"""))

# P9 version A
mini = "".join(f'<div style="position:absolute;{st}">{avatar(c, 150)}</div>' for c, st in [
    ("AAA", "left:70px;top:820px"), ("BAB", "left:250px;top:880px"), ("ABA", "left:430px;top:820px"),
    ("BBB", "left:610px;top:880px"), ("BBA", "left:790px;top:820px")])
pages.append(page(9, f"""
<div style="position:absolute;top:220px;left:0;right:0;text-align:center">
 <h2 class="kl" style="font-size:120px;line-height:1.25">你测出的<br>是哪只<span class="accent">？</span></h2>
 <div style="font-size:48px;font-weight:900;margin-top:40px">评论区报上你的动物 👇</div>
 <div style="font-size:36px;color:#8A7563;margin-top:16px">看看谁和你是同类～</div>
</div>
{mini}
<div style="position:absolute;top:1090px;left:90px;right:90px;background:#fff;border-radius:28px;padding:26px;text-align:center;font-size:32px;line-height:1.6;box-shadow:0 6px 0 #F1E2D3">
 下期解锁：每种动物的<b class="hl">恋爱模式</b>和<b class="hl">社交雷区</b><br>关注我，不错过你的那一期 🐾
</div>""").replace('id="P9"', 'id="P9A"'))

# P9 version B
blur_lines = "".join(f'<div style="height:22px;border-radius:11px;background:#E9D8C8;margin:16px 0;width:{w}%"></div>' for w in (92, 80, 96, 70, 88, 60))
pages.append(page(9, f"""
<div style="position:absolute;top:130px;left:0;right:0;text-align:center">
 <div style="font-size:42px;font-weight:700;color:#8A7563">想知道你那只动物的</div>
 <h2 class="kl" style="font-size:84px;line-height:1.35;margin-top:16px">恋爱模式 · 社交雷区<br>天选搭档 · 隐藏天赋<span class="accent">？</span></h2>
</div>
<div style="position:absolute;top:500px;left:170px;width:740px;height:560px;background:#fff;border-radius:36px;box-shadow:0 10px 0 #F1E2D3;padding:40px;overflow:hidden">
 <div style="display:flex;align-items:center;gap:24px">{avatar("AAA", 120)}<div><div style="font-size:40px;font-weight:900">海獭 · AAA</div><div style="font-size:26px;color:#8A7563">专属解读 P4 · 恋爱模式</div></div></div>
 <div style="filter:blur(7px);margin-top:20px">{blur_lines}</div>
 <div style="position:absolute;left:0;right:0;bottom:0;height:200px;background:linear-gradient(transparent,#fff)"></div>
 <div style="position:absolute;left:0;right:0;bottom:46px;text-align:center;font-size:34px;font-weight:900">🔒 剩余内容在完整版里</div>
</div>
<div style="position:absolute;top:1095px;left:0;right:0;text-align:center">
 <div style="font-size:36px;font-weight:700">8 页专属解读 + 人格卡 + 手机壁纸</div>
 <div class="chip" style="margin-top:22px;font-size:38px;padding:14px 44px">👇 点下方商品，选你的动物</div>
</div>""").replace('id="P9"', 'id="P9B"'))

html = f"""<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;700;900&family=ZCOOL+KuaiLe&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body>{''.join(pages)}</body></html>"""
OUT.write_text(html, encoding="utf-8")
print("wrote", OUT)
