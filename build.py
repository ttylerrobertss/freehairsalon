import json, os, html

ROOT = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(ROOT, "data.json")) as f:
    data = json.load(f)

SITE_NAME = "Free Hair Salon"
DOMAIN = "https://freehairsalon.com"

NAV = [
    ("hair-extensions", "Extensions"),
    ("hair-systems", "Hair Systems"),
    ("faq", "FAQ"),
    ("team", "Stylists"),
    ("merch", "Merch"),
]


def esc(s):
    return html.escape(s) if s else ""


def nl2p(text):
    paras = [p.strip() for p in text.split("\n\n")]
    out = []
    for p in paras:
        p = esc(p)
        p = p.replace("\n", "<br>")
        out.append(f"<p>{p}</p>")
    return "\n".join(out)


def header(prefix, active=None, overlay=False):
    links = "\n      ".join(
        f'<a href="{prefix}{slug}/"{" class=\"active\"" if slug == active else ""}>{label}</a>'
        for slug, label in NAV
    )
    cls = "site-header site-header--overlay" if overlay else "site-header"
    return f"""<header class="{cls}">
    <a class="logo" href="{prefix}index.html"><img src="{prefix}assets/img/wordmark.png" alt="{SITE_NAME}"></a>
    <nav>
      {links}
    </nav>
  </header>"""


def footer(prefix):
    return f"""<footer class="site-footer">
    <div class="foot-marks">
      <img class="mark-monogram" src="{prefix}assets/img/monogram.png" alt="{SITE_NAME} monogram">
      <img class="mark-squiggle" src="{prefix}assets/img/squiggle.png" alt="Free Hair">
      <img class="mark-badge" src="{prefix}assets/img/badge.png" alt="Free Hair Take Care badge">
    </div>
    <div class="foot-grid">
      <div>{esc(data['address_line1'])}<br>{esc(data['address_line2'])}</div>
      <div><a href="{esc(data['instagram_salon'])}">Instagram</a></div>
    </div>
    <div class="copy">{esc(data['copyright'])}</div>
  </footer>"""


def page(title, description, body, prefix="", active=None, extra_head="", show_header=True):
    header_html = header(prefix, active) if show_header else ""
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(description)}">
  <link rel="icon" href="{prefix}assets/img/favicon.png">
  <link rel="stylesheet" href="{prefix}assets/css/style.css">
  {extra_head}
</head>
<body>
  {header_html}
  {body}
  {footer(prefix)}
</body>
</html>
"""


def title_band(title):
    return f'<div class="title-band"><h1>{esc(title)}</h1></div>'


def write(relpath, content):
    path = os.path.join(ROOT, relpath)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)


TICKER_ITEM = " &mdash; ".join(["FREE HAIR", "TAKE CARE"] * 10)
TICKER_TRACK = f'<span>{TICKER_ITEM}</span>' * 2

# ---------- Home ----------
home_body = f"""<div class="hero">
    <img class="hero-photo" src="assets/img/{data['hero']['photo']}" alt="Free Hair Salon stylists">
    <div class="hero-overlay">
      <img class="hero-wordmark" src="assets/img/wordmark.png" alt="Free Hair">
      <div class="btn-row">
        <a class="btn" href="{esc(data['general_book_url'])}">Book Now</a>
        <a class="btn" href="hair-extensions/">Extensions</a>
        <a class="btn" href="hair-systems/">Hair Systems</a>
      </div>
    </div>
  </div>
  <div class="ticker"><div class="ticker-track">{TICKER_TRACK}</div></div>
  <section class="headline-section">
    <h1>{esc(data['hero']['headline'])}</h1>
    <div class="link-cols">
      <div>
        <div class="col-label">Free Hair Salon</div>
        <a class="col-value" href="faq/">FAQ</a>
      </div>
      <div>
        <div class="col-label">Meet Our Team</div>
        <a class="col-value" href="team/">Stylists</a>
      </div>
      <div>
        <div class="col-label">Follow Us</div>
        <a class="col-value" href="{esc(data['instagram_salon'])}">freehair.salon</a>
      </div>
    </div>
  </section>"""
write("index.html", page(
    f"{SITE_NAME} — Cincinnati, Ohio",
    "Free Hair Salon is a vegan, cruelty-free, sustainable hair salon in Cincinnati, Ohio. Book your good hair day.",
    home_body,
    show_header=False,
))

# ---------- FAQ ----------
faq_items = []
for q, a in data["faq"]:
    a_html = esc(a).replace(
        "BOOK_LINK", f'<a href="{esc(data["general_book_url"])}">Click here</a>.'
    )
    faq_items.append(f"""<div class="faq-item">
      <h3>{esc(q)}</h3>
      <p>{a_html}</p>
    </div>""")
faq_body = f"""{title_band("Frequently Asked Questions")}
  <main class="page">
    <div class="wrap">
      <div class="faq-list">{''.join(faq_items)}</div>
    </div>
  </main>"""
write("faq/index.html", page(
    f"FAQ — {SITE_NAME}",
    "Booking, cancellation policy, parking, and sustainability FAQs for Free Hair Salon in Cincinnati.",
    faq_body, prefix="../", active="faq",
))

# ---------- Team ----------
team_cards = []
for s in data["stylists"]:
    team_cards.append(f"""<a class="card" href="../{s['slug']}/">
      <img src="../assets/img/{s['photo']}" alt="{esc(s['name'])}">
      <div class="name">{esc(s['name'])}</div>
      <div class="role">{esc(s['role'])}</div>
    </a>""")
team_body = f"""{title_band("Meet the Team")}
  <main class="page">
    <div class="wrap">
      <div class="team-grid">{''.join(team_cards)}</div>
    </div>
  </main>"""
write("team/index.html", page(
    f"Our Stylists — {SITE_NAME}",
    "Meet the stylists at Free Hair Salon in Cincinnati, Ohio.",
    team_body, prefix="../", active="team",
))

# ---------- Individual stylist pages ----------
for s in data["stylists"]:
    actions = []
    if s.get("book_url"):
        actions.append(f'<a class="btn" href="{esc(s["book_url"])}">Book Now</a>')
    if s.get("price_list_slug"):
        actions.append(f'<a class="btn" href="../{s["price_list_slug"]}/">Price List</a>')
    if s.get("hair_system_faq_link"):
        actions.append('<a class="btn" href="../hair-systems/">Hair System FAQ</a>')
    if s.get("text_phone"):
        actions.append(f'<a class="btn" href="tel:{s["text_phone"]}">Text</a>')
    if s.get("email"):
        actions.append(f'<a class="btn" href="mailto:{s["email"]}">Email</a>')
    if s.get("instagram"):
        actions.append(f'<a class="btn" href="{esc(s["instagram"])}">Instagram</a>')

    extra = ""
    if s.get("tagline"):
        extra += f'<p class="bio">{esc(s["tagline"])}</p>'
    if s.get("bio"):
        extra += f'<p class="bio">{esc(s["bio"])}</p>'
    if s.get("unavailable_note"):
        extra += f'<p class="note">{esc(s["unavailable_note"])}</p>'
    if s.get("sms_disclaimer"):
        extra += f'<p class="disclaimer">{esc(s["sms_disclaimer"])}</p>'

    body = f"""<main class="page wrap">
    <div class="stylist-profile">
      <div class="photo"><img src="../assets/img/{s['photo']}" alt="{esc(s['name'])}"></div>
      <div class="info">
        <h1>{esc(s['name'])}</h1>
        <div class="role">{esc(s['role'])}</div>
        {extra}
        <div class="actions">{''.join(actions)}</div>
      </div>
    </div>
  </main>"""
    write(f"{s['slug']}/index.html", page(
        f"{s['name']} — {SITE_NAME}",
        f"{s['name']}, {s['role']} at Free Hair Salon in Cincinnati, Ohio.",
        body, prefix="../",
    ))

# ---------- Blake price list ----------
rows = "".join(
    f'<div class="price-row"><span>{esc(name)}</span><span>${esc(price)}</span></div>'
    for name, price in data["blake_pricelist"]
)
pricelist_body = f"""{title_band("Blake Roberts Price List")}
  <main class="page">
    <div class="wrap">
      <div class="price-table">{rows}</div>
      <p class="price-note">{esc(data['blake_pricelist_note'])}</p>
    </div>
  </main>"""
write("blake-pricelist/index.html", page(
    f"Blake Roberts Price List — {SITE_NAME}",
    "Service pricing for Blake Roberts at Free Hair Salon, Cincinnati.",
    pricelist_body, prefix="../",
))

# ---------- Hair extensions ----------
ext = data["hair_extensions"]
ext_sections = "".join(
    f"<h2>{esc(title)}</h2>{nl2p(body)}" for title, body in ext["sections"]
)
ext_body = f"""{title_band("Extensions FAQ")}
  <main class="page">
    <div class="wrap">
      <div class="content-page">
        <img src="../assets/img/{ext['photo']}" alt="Hair extensions at Free Hair Salon">
        {ext_sections}
        <div class="cta"><a class="btn" href="{esc(data['general_book_url'])}">Book Now</a></div>
      </div>
    </div>
  </main>"""
write("hair-extensions/index.html", page(
    f"Hair Extensions — {SITE_NAME}",
    "Luxury hair extensions in Cincinnati: k-tip and silk weft methods, pricing, and care.",
    ext_body, prefix="../", active="hair-extensions",
))

# ---------- Hair systems ----------
hs = data["hair_systems"]
hs_items = []
for q, a in hs["faq"]:
    a_html = esc(a)
    a_html = a_html.replace("EMAIL_LINK", f'<a href="mailto:{hs["consult_email"]}">{hs["consult_email"]}</a>')
    a_html = a_html.replace("HAIRSKEEN_LINK", '<a href="https://hairskeenusa.com/">Hairskeen</a>')
    hs_items.append(f"<h2>{esc(q)}</h2><p>{a_html}</p>")
hs_body = f"""{title_band("Hair System FAQ")}
  <main class="page">
    <div class="wrap">
      <div class="content-page">
        <img src="../assets/img/{hs['photo']}" alt="Hair systems at Free Hair Salon">
        {''.join(hs_items)}
        <div class="cta"><a class="btn" href="mailto:{hs['consult_email']}">Email to Consult</a></div>
      </div>
    </div>
  </main>"""
write("hair-systems/index.html", page(
    f"Hair Systems — {SITE_NAME}",
    "Custom non-surgical hair systems in Cincinnati. Consultation, pricing, and care details.",
    hs_body, prefix="../", active="hair-systems",
))

# ---------- Merch ----------
merch_items = "".join(f"""<div class="merch-item">
      <img src="../assets/img/{m['image']}" alt="{esc(m['name'])}">
      <div class="name">{esc(m['name'])}</div>
      <div class="price">${esc(m['price'])}</div>
      <a class="btn" href="{esc(m['buy_url'])}">Buy Now</a>
    </div>""" for m in data["merch"])
merch_body = f"""{title_band("Merch")}
  <main class="page">
    <div class="wrap">
      <div class="merch-grid">{merch_items}</div>
    </div>
  </main>"""
write("merch/index.html", page(
    f"Merch — {SITE_NAME}",
    "Free Hair Salon merch: tie dye tees and tote bags.",
    merch_body, prefix="../", active="merch",
))

# ---------- Sitemap ----------
paths = ["/"] + [f"/{s}/" for s in [
    "faq", "team", "hair-extensions", "hair-systems", "merch", "blake-pricelist"
]] + [f"/{s['slug']}/" for s in data["stylists"]]
urls = "\n".join(
    f"  <url><loc>{DOMAIN}{p}</loc></url>" for p in paths
)
write("sitemap.xml", f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{urls}
</urlset>
""")

print("Build complete.")
