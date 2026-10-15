# -*- coding: utf-8 -*-
import os, re, json, html, shutil, sys
sys.path.insert(0, os.path.dirname(__file__))
from content import *

OUT = "/home/claude/rimessaggio/sito"
PAGES = ["index", "prices", "faq", "location", "contact", "privacy"]
NAVP = [("prices", "prices"), ("faq", "how"), ("location", "where"), ("contact", "contact")]
SB_URL = "https://faemhbtebrjyyvapdziw.supabase.co"
ANON = os.environ.get("ANON", "")
e = html.escape

def md(s):  # **grassetto** -> <b>, righe vuote -> paragrafi
    s = e(s, quote=False)
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    return "".join("<p>%s</p>" % p.replace("\n", "<br>") for p in s.split("\n\n"))

def mdi(s):
    s = e(s, quote=False)
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s).replace("\n\n", "<br><br>").replace("\n", "<br>")

ART = '''<svg viewBox="0 0 560 440" role="img" aria-label="%s" fill="none" stroke-linecap="round" stroke-linejoin="round">
<defs><filter id="w" x="-5%%" y="-5%%" width="110%%" height="110%%"><feTurbulence type="fractalNoise" baseFrequency=".022" numOctaves="3" seed="7" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" scale="16"/></filter></defs>
<g filter="url(#w)"><path d="M18 120C60 60 170 44 270 62S480 40 540 110C560 190 536 330 520 394C400 420 150 426 40 396C14 320 4 190 18 120Z" fill="#a9c4dc" opacity=".55"/>
<path d="M60 160C130 120 250 130 330 150S470 160 506 210C512 280 498 340 480 372C380 392 190 390 90 366C60 320 50 220 60 160Z" fill="#7fa6c8" opacity=".45"/></g>
<circle cx="448" cy="92" r="26" fill="#f4c430"/>
<g stroke="#fff" stroke-width="5" pathLength="1">
<path class="dr" style="--i:0" pathLength="1" d="M70 372V222L280 150L490 222V372"/>
<path class="dr" style="--i:1" pathLength="1" d="M70 222L280 150L490 222"/>
<path class="dr" style="--i:2" pathLength="1" d="M52 372H508"/>
<path class="dr" style="--i:3" pathLength="1" d="M110 372V250H450V372"/>
<path class="dr" style="--i:4" pathLength="1" d="M126 340V296Q126 280 142 280H252Q268 280 268 296V340Z"/>
<path class="dr" style="--i:5" pathLength="1" d="M126 308H268M160 280V250"/>
<circle class="dr" style="--i:6" pathLength="1" cx="196" cy="344" r="18"/>
<path class="dr" style="--i:7" pathLength="1" d="M268 332H296"/>
<path class="dr" style="--i:8" pathLength="1" d="M318 332H430L412 366H336Z"/>
<path class="dr" style="--i:9" pathLength="1" d="M374 332V284L410 332"/>
<path class="dr" style="--i:10" pathLength="1" d="M350 306H398"/>
</g></svg>'''

def head(L, c, page, depth=1):
    t = c["title"][page]; d = c["desc"][page]
    alts = "".join('<link rel="alternate" hreflang="%s" href="../%s/%s.html">' % (l, l, page if page != "index" else "index") for l in ("it", "en", "de"))
    return ('<!doctype html><html lang="%s"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>%s</title><meta name="description" content="%s"><meta name="robots" content="noindex,nofollow">'
            '<meta property="og:title" content="%s"><meta property="og:description" content="%s"><meta property="og:type" content="website">'
            '<link rel="icon" href="../assets/favicon.png"><link rel="preload" href="../assets/fonts/famgro.woff" as="font" type="font/woff" crossorigin>'
            '<link rel="stylesheet" href="../assets/style.css">%s</head><body>') % (L, e(t), e(d), e(t), e(d), alts)

def top(L, c, page):
    n = c["nav"]
    links = "".join('<a href="%s.html"%s>%s</a>' % (p, ' aria-current="page"' if p == page else "", e(n[k])) for p, k in NAVP)
    lang = "".join('<a href="../%s/%s.html" lang="%s" hreflang="%s"%s>%s</a>' % (l, page, l, l, ' aria-current="true"' if l == L else "", l.upper()) for l in ("it", "en", "de"))
    login = '<a class="btn s" href="%s">%s</a>' % (AREA, e(n["login"]))
    return ('<a class="skip" href="#main">%s</a><header class="top"><div class="wrap"><a class="brand" href="index.html"><img src="../assets/logo-120.png" alt="" width="44" height="44"><span><b>Garda Center</b><span>%s</span></span></a>'
            '<nav class="nav" aria-label="Menu">%s%s<span class="lang" aria-label="%s">%s</span></nav>'
            '<button class="burger" aria-expanded="false" aria-controls="menu" aria-label="%s"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"><path d="M3 6h18M3 12h18M3 18h18"/></svg></button></div>'
            '<div class="menu" id="menu"><div class="wrap">%s%s<span class="lang">%s</span></div></div></header><main id="main">') % (
            e(n["skip"]), e(c["brand_sub"]), links, login, e(n["lang"]), lang, e(n["menu"]), links, login, lang)

def foot(L, c):
    f = c["foot"]; n = c["nav"]; s = SEDI
    return ('</main><footer><div class="wrap"><div class="cols"><div><b style="color:#fff;font-size:1.15rem">Garda Center</b><p style="margin-top:8px">%s</p></div>'
            '<div><h3>%s</h3><ul><li><a href="tel:%s">%s</a></li><li><a href="tel:%s">%s</a></li><li><a href="mailto:%s">%s</a></li></ul></div>'
            '<div><h3>%s</h3><ul><li>%s<br>%s, %s</li><li>%s<br>%s, %s</li></ul></div>'
            '<div><h3>%s</h3><ul><li><a href="%s">%s</a></li><li><a href="%s">%s</a></li><li><a href="%s" rel="noopener">Facebook</a></li><li><a href="%s" rel="noopener">Instagram</a></li></ul></div></div>'
            '<div class="legal">%s · <a href="privacy.html">%s</a></div></div></footer>') % (
        e(c["brand_sub"]), e(f["c"]), PHONE1.replace(" ", ""), PHONE1, PHONE2.replace(" ", ""), PHONE2, EMAIL, EMAIL,
        e(f["s"]), e(s["cam"]["nome"]), e(s["cam"]["ind"]), e(s["cam"]["comune"]), e(s["cas"]["nome"]), e(s["cas"]["ind"]), e(s["cas"]["comune"]),
        e(f["l"]), AREA, e(n["login"]), GEST, e(f["gest"]), FB, IG, e(f["rights"]), e(f["privacy"]))

BOT_HTML = '<button class="bot-fab" id="botfab" aria-haspopup="dialog"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 5h16v11H9l-5 4z"/></svg><span></span></button><div class="bot" id="bot" role="dialog" aria-modal="false" aria-labelledby="bot-t"></div>'

def tail(L, page, extra=""):
    return BOT_HTML + extra + '<script src="../assets/gc-core.js"></script><script src="../assets/bot-data.js"></script><script src="../assets/site.js"></script></body></html>'

def build_ribbon(c):
    y = c["year"]
    lis = "".join('<li%s>%s</li>' % (' class="o"' if 3 <= i <= 8 else "", m) for i, m in enumerate(c["months"]))
    return ('<div class="year"><h2>%s</h2><p class="sub">%s</p><div style="position:relative"><span class="now" id="now">%s</span><ol class="ribbon" id="ribbon" role="img" aria-label="%s">%s</ol></div>'
            '<div class="legend"><div><i></i>%s</div><div><i class="c"></i>%s</div></div><p class="state" id="state" data-o="%s" data-c="%s"></p></div>') % (
        e(y["h"]), e(y["sub"]), e(y["now"]), e(y["aria"]), lis, e(y["o"]), e(y["c"]), e(y["s_open"]), e(y["s_closed"]))

def table(cap, cols, rows, cls=""):
    th = "".join("<th scope=col>%s</th>" % e(x) for x in cols)
    tr = "".join("<tr><th scope=row>%s</th>%s</tr>" % (e(r[0]), "".join("<td>%s</td>" % e(x) for x in r[1:])) for r in rows)
    return '<div class="tw"><table><caption>%s</caption><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>' % (e(cap), th, tr)

def table2(cap, rows):
    tr = "".join("<tr><th scope=row>%s</th><td>%s</td></tr>" % (e(a), e(b)) for a, b in rows)
    return '<div class="tw"><table><caption>%s</caption><tbody>%s</tbody></table></div>' % (e(cap), tr)

def sedi_html(c, mapload=False):
    out = ""
    for k in ("cam", "cas"):
        s = SEDI[k]; q = s["q"].replace(" ", "+")
        out += '<div class="sede"><h3>%s · %s</h3><address>%s<br>%s</address>' % (e(s["nome"]), e(s["comune"]), e(s["ind"]), e(s["cap"]))
        if mapload:
            out += ('<div class="mappa" data-q="%s" style="margin-top:14px"><div><p>%s</p><button class="btn s" type="button">%s</button></div></div>' % (e(q), e(c["W"]["priv"]), e(c["W"]["load"])))
        out += '<p style="margin-top:12px"><a href="https://www.google.com/maps/search/?api=1&amp;query=%s" rel="noopener">%s</a></p></div>' % (q, e(c["W"]["maps"] if mapload else c["sedi"]["go"]))
    return out

def page_index(L, c):
    h = c["hero"]; i = c["inc"]; pr = c["pr"]; st = c["steps"]
    o = head(L, c, "index") + top(L, c, "index")
    o += ('<section class="hero"><div class="wrap"><div><h1>%s</h1><p class="lede">%s</p><div class="cta"><a class="btn p" href="contact.html?m=posto">%s</a><a class="btn" href="prices.html">%s</a></div></div><figure class="art">%s</figure></div>'
          '<div class="wrap">%s</div></section>') % (e(h["h1"]), e(h["lede"]), e(h["c1"]), e(h["c2"]), ART % e(h["art"]), build_ribbon(c))
    o += '<section class="band"><div class="wrap two w"><div><h2>%s</h2><p>%s</p></div><div><h3>%s</h3><ul class="list">%s</ul><p style="margin-top:20px"><b style="font-family:var(--f-t)">%s.</b> %s</p></div></div></section>' % (
        e(c["indoor"]["h"]), e(c["indoor"]["p"]), e(i["h"]), "".join("<li><b>%s</b><span>%s</span></li>" % (e(a), e(b)) for a, b in i["items"]), e(i["sec_h"]), e(i["sec"]))
    o += '<section><div class="wrap two w"><div><h2>%s</h2><p class="sub">%s</p></div><div class="prezzi-mini">%s</div></div></section>' % (
        e(pr["h"]), e(pr["sub"]), "".join('<a href="prices.html"><span class="n">%s<small>%s</small></span><span class="v">%s %s</span></a>' % (e(a), e(d), e(pr["from_"]), e(b)) for a, b, d in pr["rows"]) + '<p style="margin-top:16px"><a href="prices.html">%s</a></p>' % e(pr["all"]))
    o += '<section class="band"><div class="wrap two w"><h2>%s</h2><ol class="steps">%s</ol></div></section>' % (e(st["h"]), "".join("<li><b>%s</b><span>%s</span></li>" % (e(a), e(b)) for a, b in st["items"]))
    o += '<section><div class="wrap"><h2>%s</h2><p class="sub">%s</p><div class="sedi" style="margin-top:28px">%s</div></div></section>' % (e(c["sedi"]["h"]), e(c["sedi"]["p"]), sedi_html(c))
    o += '<section class="band"><div class="wrap"><h3>%s</h3><p>%s</p><ul class="altre">%s</ul></div></section>' % (e(c["altre"]["h"]), e(c["altre"]["p"]),
        "".join("<li>%s</li>" % (('<a href="%s" rel="noopener">%s</a>' % (u, e(n))) if u else e(n)) for n, u in ALTRE))
    ct = c["cta"]
    o += '<section class="dark cta-band"><div class="wrap"><h2>%s</h2><div class="cta"><a class="btn p" href="contact.html">%s</a><a class="btn" style="color:#fff;border-color:#fff" href="%s">%s</a></div></div></section>' % (e(ct["h"]), e(ct["c1"]), AREA, e(ct["c2"]))
    return o + foot(L, c) + tail(L, "index")

def page_prices(L, c):
    P_ = c["P"]; cc = P_["calc"]
    o = head(L, c, "prices") + top(L, c, "prices")
    o += '<section><div class="wrap"><h1>%s</h1><p class="sub">%s</p>' % (e(P_["h1"]), e(P_["sub"]))
    opts = "".join('<option value="%s">%s</option>' % (k, e(v)) for k, v in cc["types"])
    o += ('<form class="calc" id="calc" style="margin-top:28px" novalidate><h2>%s</h2><div class="row"><div><label for="ct">%s</label><select id="ct">%s</select></div><div><label for="cl">%s</label><input id="cl" inputmode="decimal" autocomplete="off" placeholder="6,5"></div>'
          '<button class="btn p" type="submit">%s</button></div><div class="chk" id="cdxw"><input type="checkbox" id="cdx"><label for="cdx">%s</label></div><div class="out" id="cout" aria-live="polite"></div></form>') % (
          e(cc["h"]), e(cc["t"]), opts, e(cc["l"]), e(cc["go"]), e(cc["dx"]))
    o += '</div></section>'
    a = P_["ann"]; s = P_["sea"]; ex = P_["ex"]; tr = P_["tr"]; inc = c["inc"]
    o += '<section class="band"><div class="wrap two"><div>%s</div><div>%s<p class="nota">%s</p></div></div></section>' % (table2(a["cap"], a["rows"]), table(s["cap"], s["col"], s["rows"]), e(s["note"]))
    o += '<section><div class="wrap two"><div><h2>%s</h2><ul class="list">%s</ul></div><div>%s</div></div></section>' % (
        e(P_["inc"]["h"]), "".join("<li><b>%s</b><span>%s</span></li>" % (e(x), e(y)) for x, y in inc["items"]), table2(ex["cap"], ex["rows"]))
    o += '<section class="band"><div class="wrap">%s<p class="nota">%s</p><p class="nota">%s</p><div class="cta" style="margin-top:20px"><a class="btn p" href="contact.html?m=posto">%s</a></div></div></section>' % (
        table(tr["cap"], tr["col"], tr["rows"]), e(tr["note"]), e(P_["foot"]), e(c["hero"]["c1"]))
    return o + foot(L, c) + tail(L, "prices", '<script>window.GCP=%s</script>' % json.dumps({k: cc[k] for k in ("r_ann","r_tr","need","tr_none")}, ensure_ascii=False))

def page_faq(L, c):
    o = head(L, c, "faq") + top(L, c, "faq")
    o += '<section><div class="wrap"><h1>%s</h1><div class="faq" style="margin-top:28px">%s</div><div class="cta" style="margin-top:32px"><a class="btn p" href="contact.html">%s</a></div></div></section>' % (
        e(c["nav"]["how"]), "".join('<details id="%s"><summary>%s</summary>%s</details>' % (i, e(q), md(a)) for i, q, a in c["FAQ"]), e(c["cta"]["c1"]))
    ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"\*\*", "", a).replace("\n\n", " ")}} for i, q, a in c["FAQ"]]}
    return o + foot(L, c) + tail(L, "faq", '<script type="application/ld+json">%s</script>' % json.dumps(ld, ensure_ascii=False).replace("</", "<\\/"))

def page_location(L, c):
    W = c["W"]
    o = head(L, c, "location") + top(L, c, "location")
    o += '<section><div class="wrap"><h1>%s</h1><p class="sub">%s</p><div class="sedi" style="margin-top:32px">%s</div><p class="nota" style="margin-top:28px">%s</p><div class="cta" style="margin-top:20px"><a class="btn p" href="contact.html">%s</a></div></div></section>' % (
        e(W["h1"]), e(W["sub"]), sedi_html(c, True), e(W["note"]), e(c["cta"]["c1"]))
    return o + foot(L, c) + tail(L, "location")

def page_contact(L, c):
    K = c["K"]
    opts = lambda lst: "".join('<option value="%s">%s</option>' % (k, e(v)) for k, v in lst)
    o = head(L, c, "contact") + top(L, c, "contact")
    o += ('<section><div class="wrap two w"><div><h1>%s</h1><p class="sub">%s</p><p style="margin-top:24px"><b style="font-family:var(--f-t)">%s</b><br><a href="tel:%s">%s</a><br><a href="tel:%s">%s</a><br><a href="mailto:%s">%s</a></p></div>'
          '<form class="f" id="cform" novalidate data-url="%s/functions/v1/contatto" data-key="%s" data-lang="%s">'
          '<div><label for="fm">%s</label><select id="fm" name="motivo">%s</select></div>'
          '<div class="g2"><div><label for="fn">%s</label><input id="fn" name="nome" autocomplete="name" required maxlength="120"></div><div><label for="fe">%s</label><input id="fe" name="email" type="email" autocomplete="email" required maxlength="160"></div></div>'
          '<div class="g2"><div><label for="ft">%s</label><input id="ft" name="telefono" type="tel" autocomplete="tel" maxlength="40"></div><div><label for="fy">%s</label><select id="fy" name="mezzo">%s</select></div></div>'
          '<div class="g2"><div><label for="fl">%s</label><input id="fl" name="lunghezza" inputmode="decimal" maxlength="6"></div><div class="chk" style="align-self:end;padding-bottom:12px"><input type="checkbox" id="fd" name="asse"><label for="fd">%s</label></div></div>'
          '<div><label for="fg">%s</label><textarea id="fg" name="messaggio" required maxlength="3000"></textarea><p class="hint">%s</p></div>'
          '<div class="hp" aria-hidden="true"><label for="fw">Web</label><input id="fw" name="sito" tabindex="-1" autocomplete="off"></div>'
          '<div class="chk"><input type="checkbox" id="fc" name="consenso" required><label for="fc">%s</label></div>'
          '<button class="btn p" type="submit" id="fs" style="justify-self:start">%s</button><div class="msg" id="fmsg" role="status" aria-live="polite"></div></form></div></section>') % (
        e(K["h1"]), e(K["sub"]), e(K["direct"]), PHONE1.replace(" ", ""), PHONE1, PHONE2.replace(" ", ""), PHONE2, EMAIL, EMAIL,
        SB_URL, ANON, L, e(K["m"]), opts(K["mopts"]), e(K["n"]), e(K["e"]), e(K["t"]), e(K["ty"]), opts(K["tyopts"]), e(K["len"]), e(K["dx"]), e(K["msg"]), e(K["hint"]), K["priv"], e(K["send"]))
    ms = {k: K[k] for k in ("sending", "ok", "err", "bad", "send")}
    return o + foot(L, c) + tail(L, "contact", '<script>window.GCF=%s</script>' % json.dumps(ms, ensure_ascii=False))

def page_privacy(L, c):
    PV = c["PV"]
    o = head(L, c, "privacy") + top(L, c, "privacy")
    o += '<section><div class="wrap"><h1>%s</h1><div style="margin-top:24px">%s</div></div></section>' % (e(PV["h1"]), "".join(md(p) for p in PV["body"]))
    return o + foot(L, c) + tail(L, "privacy")

def bot_js():
    out = {}
    for L, c in C.items():
        B = dict(c["B"]); f = B.pop("f"); nxt = B.pop("next"); size = B.pop("size")
        a = {i: mdi(ans) for i, q, ans in c["FAQ"]}
        a["size"] = e(size)
        B["a"] = a; B["next"] = nxt; B["locale"] = c["nums"][0]
        s = json.dumps(B, ensure_ascii=False)
        fs = "{" + ",".join("%s:%s" % (k, v) for k, v in f.items()) + "}"
        out[L] = "(function(){var B=" + s + ";B.f=" + fs + ";" \
                 "var nf=new Intl.NumberFormat(B.locale,{style:'currency',currency:'EUR',maximumFractionDigits:0});" \
                 "var nn=new Intl.NumberFormat(B.locale,{maximumFractionDigits:2});" \
                 "B.m=function(v){return nf.format(v)};B.n=function(v){return nn.format(v)};" \
                 "B.f=(function(f){var r={};for(var k in f){r[k]=f[k]}return r})(B.f);" \
                 "GCB." + L + "=B;})();"
    # le funzioni f usano B: le ricreiamo dentro la chiusura sopra (B è locale)
    return "var GCB={};\n" + "\n".join(out[l] for l in ("it", "en", "de")) + "\n"

def main():
    for L in ("it", "en", "de"):
        os.makedirs(os.path.join(OUT, L), exist_ok=True)
        c = C[L]
        for p in PAGES:
            fn = {"index": page_index, "prices": page_prices, "faq": page_faq, "location": page_location, "contact": page_contact, "privacy": page_privacy}[p]
            open(os.path.join(OUT, L, p + ".html"), "w", encoding="utf-8").write(fn(L, c))
    open(os.path.join(OUT, "assets", "bot-data.js"), "w", encoding="utf-8").write(bot_js())
    open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(
        '<!doctype html><html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex">'
        '<title>Garda Center</title><link rel="icon" href="assets/favicon.png"><script>var l=(navigator.language||"it").slice(0,2).toLowerCase();location.replace((l==="de"||l==="en"?l:"it")+"/index.html")</script>'
        '<noscript><meta http-equiv="refresh" content="0;url=it/index.html"></noscript></head><body><p><a href="it/index.html">Italiano</a> · <a href="en/index.html">English</a> · <a href="de/index.html">Deutsch</a></p></body></html>')
    print("ok")
main()
