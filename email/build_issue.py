"""
Build one Breach Watch email issue (HTML) for MailerLite.

Usage:  python3 email/build_issue.py issue.json out.html
issue.json:
{
  "since": "YYYY-MM-DD",            # include Breach Watch entries dated on/after this day (usually last Tuesday)
  "heading": "This week's password and data breaches and what to do",   # optional
  "worth_reading": [ {"title": "...", "source": "...", "summary": "...", "url": "https://..."} ],   # 1-2 items
  "tip": {"title": "...", "text": "..."},
  "site": "https://preview.wordcrypt.com"   # base URL for the demo/breaches links (wordcrypt.com after launch)
}
Stories come from breaches.json in this repo (newest first, max 6).
Design approved by Jim Lucas on 2026-10-27 (test issue 3 + "patented process" closing).
"""
import json, sys, html, datetime, os

E = html.escape
BLUE = "#1663A6"; INK = "#14202e"; MUTED = "#5b6675"; RULE = "#e3e8ef"; BODY = "#2b3542"
TYPECOL = {"Passwords": "#c0392b", "Reused passwords": "#c0392b", "Password managers": "#b9770e",
           "Email list": "#2e6da4", "Business accounts": "#6c4fbf"}

def fmt(d):
    return datetime.date.fromisoformat(d).strftime("%b %-d, %Y")

def main(issue_path, out_path):
    issue = json.load(open(issue_path))
    here = os.path.dirname(os.path.abspath(__file__))
    data = json.load(open(os.path.join(here, "..", "breaches.json")))
    since = issue["since"]
    stories = [e for e in data["entries"] if e["date"] >= since][:6]
    site = issue.get("site", "https://preview.wordcrypt.com").rstrip("/")
    heading = issue.get("heading", "This week's password and data breaches and what to do")
    n = len(stories)

    def story(e, last):
        col = TYPECOL.get(e["type"], MUTED)
        when = e.get("dateLabel") or fmt(e["date"])
        border = "" if last else f"border-bottom:1px solid {RULE};"
        return f"""
<tr><td style="padding:22px 0 {0 if last else 22}px 0;{border}">
  <div style="font:600 12px Arial,sans-serif;color:{col};text-transform:uppercase;letter-spacing:.06em;margin-bottom:6px">{E(e['type'])} &nbsp;·&nbsp; <span style="color:{MUTED};text-transform:none;letter-spacing:0;font-weight:400">{E(when)}</span></div>
  <div style="font:700 19px/1.3 Arial,sans-serif;color:{INK};margin-bottom:8px">{E(e['company'])}: {E(e['title'])}</div>
  <div style="font:15px/1.55 Arial,sans-serif;color:{BODY};margin-bottom:10px">{E(e['summary'])}</div>
  <div style="font:15px/1.55 Arial,sans-serif;color:{BODY};margin-bottom:10px"><strong>What to do:</strong> {E(e.get('tip',''))}</div>
  <a href="{E(e['url'])}" style="font:14px Arial,sans-serif;color:{BLUE}">Read on {E(e['source'])}</a>
</td></tr>"""

    if n:
        count = f"In this issue: {n} breach{'es' if n != 1 else ''} worth knowing about"
        stories_html = "".join(story(e, i == n - 1) for i, e in enumerate(stories))
        preheader = f"{n} breach{'es' if n != 1 else ''} worth knowing about, plus this week's WordCrypt tip."
    else:
        count = "A quiet week: no major password breaches made Breach Watch."
        stories_html = f"""<tr><td style="padding:18px 0 0;font:15px/1.6 Arial,sans-serif;color:{BODY}">No new password or login breaches met our bar this week. The full list is always at Breach Watch.</td></tr>"""
        preheader = "A quiet week for breaches, plus this week's WordCrypt tip."

    wr = "".join(f"""
<tr><td style="padding:12px 0">
  <a href="{E(w['url'])}" style="font:700 16px/1.35 Arial,sans-serif;color:{BLUE};text-decoration:none">{E(w['title'])}</a>
  <div style="font:13px Arial,sans-serif;color:{MUTED};margin:3px 0 5px">{E(w['source'])}</div>
  <div style="font:15px/1.55 Arial,sans-serif;color:{BODY}">{E(w['summary'])}</div>
</td></tr>""" for w in issue.get("worth_reading", []))
    worth_block = "" if not wr else f"""
<tr><td style="padding:18px 32px 4px"><div style="height:1px;background:{RULE}"></div>
  <div style="font:700 13px Arial,sans-serif;color:{BLUE};text-transform:uppercase;letter-spacing:.08em;margin-top:22px">Worth reading</div></td></tr>
<tr><td style="padding:0 32px 6px"><table role="presentation" width="100%" cellpadding="0" cellspacing="0">{wr}</table></td></tr>"""

    tip = issue["tip"]
    out = f"""<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Breach Watch</title></head>
<body style="margin:0;padding:0;background:#f2f4f7">
<div style="display:none;max-height:0;overflow:hidden">{E(preheader)}</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#f2f4f7"><tr><td align="center" style="padding:24px 12px">
<table role="presentation" width="600" cellpadding="0" cellspacing="0" style="max-width:600px;width:100%;background:#ffffff;border:1px solid {RULE};border-radius:8px">
<tr><td align="center" style="padding:28px 32px 18px">
  <table role="presentation" cellpadding="0" cellspacing="0"><tr>
    <td style="padding-right:12px"><img src="https://wordcrypt.com/icon-192.png" width="44" height="44" alt="" style="display:block"></td>
    <td style="font:700 26px Arial,sans-serif;color:{INK}">WordCrypt's <span style="color:{BLUE}">Breach Watch</span></td>
  </tr></table>
  <div style="height:3px;background:{BLUE};margin-top:18px"></div>
</td></tr>
<tr><td style="padding:6px 32px 0">
  <div style="font:700 24px/1.3 Arial,sans-serif;color:{INK}">{E(heading)}</div>
  <div style="font:15px/1.6 Arial,sans-serif;color:{BODY};margin-top:12px">If any of these companies has your information, the "What to do" tip under each story tells you how to protect yourself.</div>
  <div style="margin-top:16px;padding:12px 16px;background:#eef4fb;border-radius:6px;font:600 15px Arial,sans-serif;color:{INK}">{E(count)}</div>
</td></tr>
<tr><td style="padding:4px 32px 8px"><table role="presentation" width="100%" cellpadding="0" cellspacing="0">{stories_html}</table></td></tr>
{worth_block}
<tr><td style="padding:14px 32px 6px">
  <div style="background:#f6f8fb;border-left:4px solid {BLUE};padding:16px 18px;border-radius:0 6px 6px 0">
    <div style="font:700 13px Arial,sans-serif;color:{BLUE};text-transform:uppercase;letter-spacing:.08em;margin-bottom:8px">WordCrypt Tip of the Week</div>
    <div style="font:700 17px Arial,sans-serif;color:{INK};margin-bottom:6px">{E(tip['title'])}</div>
    <div style="font:15px/1.6 Arial,sans-serif;color:{BODY}">{E(tip['text'])}</div>
    <div style="margin-top:10px"><a href="{site}/app/" style="font:600 14px Arial,sans-serif;color:{BLUE}">Try it in the WordCrypt demo →</a></div>
  </div>
</td></tr>
<tr><td style="padding:26px 32px 4px">
  <div style="height:1px;background:{RULE}"></div>
  <div style="font:700 20px/1.3 Arial,sans-serif;color:{INK};margin-top:24px">One breach shouldn't open every door.</div>
  <div style="font:15px/1.6 Arial,sans-serif;color:{BODY};margin-top:10px">We can't stop companies from being breached. But when a site leaks your password, the damage should end there. WordCrypt's patented process creates a different password for every site when you need it and never stores it, so there's no vault holding all your passwords, and a password stolen from one site won't unlock any of the others.</div>
  <div style="font:15px/1.6 Arial,sans-serif;color:{BODY};margin-top:14px">Stay safe out there, and retire your password vault.</div>
  <div style="font:700 15px Arial,sans-serif;color:{INK};margin-top:4px">The WordCrypt Team</div>
</td></tr>
<tr><td align="center" style="padding:26px 32px 30px">
  <a href="{site}/breaches/" style="display:inline-block;background:{BLUE};color:#ffffff;font:700 15px Arial,sans-serif;text-decoration:none;padding:13px 26px;border-radius:5px">See all recent breaches</a>
</td></tr>
<tr><td align="center" style="padding:24px 32px 26px;background:#f3f5f8;border-radius:0 0 8px 8px;font:13px/1.6 Arial,sans-serif;color:{MUTED}">
  <div style="font:700 14px Arial,sans-serif;color:{BLUE}">Brought to you by WordCrypt®</div>
  <div>Patented vaultless password management. Your passwords are never stored.</div>
  <div style="margin-top:8px">WordCrypt is a product of Expojour LLC<br>5719 Whitaker Rd, Naples, FL 34112, United States of America</div>
  <div style="margin-top:10px">You received this email because you signed up for Breach Watch on wordcrypt.com.</div>
  <div style="margin-top:10px;font-size:11px;line-height:1.5;color:#8a8f98">Breach Watch summarizes publicly available news reports and company notices, with a link to each source. Details may change as investigations continue; always check the original source. WordCrypt is not affiliated with the companies or publications mentioned, and their names and trademarks belong to their owners. This email is for general information only and is not legal or security advice.</div>
  <div style="margin-top:12px"><a href="{{$unsubscribe}}" style="color:{MUTED}">Unsubscribe</a></div>
</td></tr>
</table></td></tr></table></body></html>"""
    open(out_path, "w").write(out)
    print(f"stories={n} bytes={len(out)}")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
