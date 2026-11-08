#!/usr/bin/env python3
"""Minatokan Kasumi unofficial English guide: static site builder. Output goes to docs/."""
import json, os, html as H

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "docs")
BASE = "https://masabee1029.github.io/minatokan-kasumi-guide/"
BOOK = "https://www.jhpds.net/minatokan/uw/uwp3100/uww3101.do?yadNo=317522"
CHECKED = "November 8, 2026"
# Entity-encoded, same as the ryokan's own site does, to limit address harvesting.
MAIL = "&#105;&#110;&#102;&#111;&#64;&#109;&#105;&#110;&#97;&#116;&#111;&#107;&#97;&#110;&#46;&#106;&#112;"
TEL = "+81-796-36-3330"

NAV = [("index.html", "Home"), ("sunset.html", "Sunset"), ("crab.html", "Crab"),
       ("rooms-baths.html", "Rooms &amp; Baths"), ("getting-there.html", "Getting There"),
       ("nearby.html", "Nearby"), ("faq.html", "FAQ"), ("how-to-book.html", "How to Book")]

CSS = """
:root{--paper:#fbf5ea;--card:#fffdf8;--ink:#1b2333;--soft:#566072;--line:#e7dcc8;--sun:#c8401a;--sun2:#e8a24a;--sea:#143a55;--tint:#f6e7d2}
@media (prefers-color-scheme:dark){:root{--paper:#10161f;--card:#18202c;--ink:#f1ebe0;--soft:#aab3c0;--line:#2d3848;--sun:#ff8a5c;--sun2:#f0b566;--sea:#9fd0ee;--tint:#222b38}}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--paper);color:var(--ink);font:17px/1.7 "DM Sans",system-ui,sans-serif;padding-bottom:76px}
h1,h2,h3{font-family:Fraunces,Georgia,serif;font-weight:600;line-height:1.18;letter-spacing:-.01em;text-wrap:balance}
h2{font-size:clamp(26px,4vw,36px);margin:56px 0 14px}h3{font-size:21px;margin:26px 0 6px}
p{margin:0 0 14px}a{color:var(--sun)}
.wrap{max-width:900px;margin:0 auto;padding:0 16px}
.top{position:sticky;top:0;z-index:20;background:var(--paper);border-bottom:1px solid var(--line)}
.bar{display:flex;align-items:center;justify-content:space-between;gap:12px;max-width:1040px;margin:0 auto;padding:10px 16px}
.brand{font:600 19px Fraunces,Georgia,serif;color:var(--ink);text-decoration:none}.brand small{font:500 12px "DM Sans",sans-serif;color:var(--soft);margin-left:6px}
nav.menu{display:flex;gap:4px;overflow-x:auto;max-width:1040px;margin:0 auto;padding:0 12px 8px;scrollbar-width:none}
nav.menu::-webkit-scrollbar{display:none}
nav.menu a{flex:none;padding:5px 11px;border-radius:99px;color:var(--soft);font-size:14px;text-decoration:none}
nav.menu a.on{background:var(--tint);color:var(--ink);font-weight:600}
.btn{display:inline-block;background:var(--sun);color:#fff;font-weight:600;padding:12px 20px;border-radius:10px;text-decoration:none;line-height:1.25}
@media (prefers-color-scheme:dark){.btn{color:#1a1208}}
.btn:hover{filter:brightness(1.08)}.btn.ghost{background:none;color:var(--sun);box-shadow:inset 0 0 0 1.5px var(--sun)}
.bar .btn{padding:8px 13px;font-size:14px;flex:none}
.hero{position:relative;color:#fff8ec;background:#23203f;overflow:hidden}
.hero>img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}.hero:after{content:"";position:absolute;inset:0;background:linear-gradient(100deg,rgba(18,14,38,.86) 0%,rgba(18,14,38,.62) 52%,rgba(18,14,38,.22) 100%)}
.hero .in{position:relative;z-index:1;max-width:900px;margin:0 auto;padding:clamp(56px,10vw,104px) 16px clamp(92px,14vw,130px)}
.eyebrow{font-size:14px;letter-spacing:.09em;text-transform:uppercase;opacity:.9;margin-bottom:12px}
.hero h1{font-size:clamp(36px,6.4vw,62px);margin:0 0 16px;max-width:17em}
.hero p.lead{font-size:clamp(18px,2.4vw,21px);max-width:34em;margin-bottom:22px}
.hero .btn{background:#fff3df;color:#8c2a0d}.hero .note{display:block;font-size:13.5px;margin-top:10px;opacity:.9}
figure.ph{margin:20px 0}figure.ph img{display:block;width:100%;height:auto;border-radius:12px}figure.ph figcaption{font-size:14px;color:var(--soft);margin-top:7px;line-height:1.45}
.pagehead{background:linear-gradient(170deg,#2b2750 0%,#a43e2e 72%,#e8a24a 130%);color:#fff8ec;padding:clamp(40px,7vw,66px) 0 clamp(34px,6vw,56px)}
.pagehead h1{font-size:clamp(32px,5.4vw,50px);margin:0 0 10px}.pagehead p{font-size:19px;margin:0;max-width:36em}
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:0;margin:-44px 0 0;position:relative;background:var(--card);border:1px solid var(--line);border-radius:14px}
.stats div{padding:16px 14px;border-left:1px solid var(--line)}.stats div:first-child{border-left:0}
.stats b{display:block;font:600 31px/1.1 Fraunces,Georgia,serif;color:var(--sun)}.stats span{font-size:14px;color:var(--soft);line-height:1.35;display:block;margin-top:4px}
@media (max-width:640px){.stats{grid-template-columns:1fr 1fr}.stats div:nth-child(3){border-left:0}.stats div:nth-child(n+3){border-top:1px solid var(--line)}}
.grid3{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}.grid2{display:grid;grid-template-columns:1fr 1fr;gap:14px}
@media (max-width:700px){.grid3,.grid2{grid-template-columns:1fr}}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:18px}.card h3{margin-top:0}.card p:last-child{margin:0}
.card a.more{font-weight:600}
.know{background:var(--tint);border-radius:12px;padding:18px 20px;margin:18px 0}.know h3{margin-top:0}.know ul{margin:0;padding-left:20px}.know li{margin:6px 0}
table{width:100%;border-collapse:collapse;font-size:16px;background:var(--card)}
th,td{padding:10px 12px;border:1px solid var(--line);text-align:left;vertical-align:top}th{background:var(--tint);font-weight:600}
.tw{overflow-x:auto;margin:14px 0;-webkit-overflow-scrolling:touch}.tw table{min-width:520px}.tw table.two{min-width:0}
.ctaband{margin:44px 0 0;padding:24px;background:var(--sea);color:#fff;border-radius:14px}
@media (prefers-color-scheme:dark){.ctaband{background:#1d3a50}}
.ctaband h2{margin:0 0 8px;font-size:27px;color:#fff}.ctaband p{margin:0 0 14px}.ctaband a:not(.btn){color:#ffd9a8}
.ctaband .btn{background:#fff3df;color:#8c2a0d;margin:0 8px 8px 0}.ctaband .btn.ghost{background:none;color:#fff;box-shadow:inset 0 0 0 1.5px #fff}
details{background:var(--card);border:1px solid var(--line);border-radius:10px;margin:8px 0;padding:0 16px}
summary{cursor:pointer;font-weight:600;padding:13px 0;list-style-position:outside}details[open] summary{border-bottom:1px solid var(--line);margin-bottom:10px}details p{margin-bottom:12px}
ol.steps{counter-reset:s;list-style:none;margin:14px 0;padding:0}ol.steps li{counter-increment:s;position:relative;padding:0 0 14px 50px}
ol.steps li:before{content:counter(s);position:absolute;left:0;top:0;width:35px;height:35px;border-radius:50%;background:var(--sun);color:#fff;text-align:center;font:600 18px/35px Fraunces,Georgia,serif}
pre{white-space:pre-wrap;background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px;font:15px/1.6 ui-monospace,Menlo,monospace}
.small{font-size:14.5px;color:var(--soft)}
.ainote{margin:0;padding:7px 16px;background:var(--tint);color:var(--ink);font-size:14.5px;line-height:1.45;text-align:center}
.closing{margin:44px 0 0;border-left:4px solid var(--sun2);padding:4px 0 4px 16px;font-size:18px}.closing p{margin:0}
footer{margin-top:56px;border-top:1px solid var(--line);padding:24px 0 12px;font-size:14.5px;color:var(--soft)}footer a{color:var(--soft)}
.sticky{position:fixed;left:0;right:0;bottom:0;z-index:30;display:flex;align-items:center;justify-content:space-between;gap:12px;background:var(--card);border-top:1px solid var(--line);padding:10px 16px}
.sticky span{font-size:14px;color:var(--soft);line-height:1.3}.sticky .btn{flex:none;padding:10px 15px;font-size:15px}
.fxjs .fx{opacity:0;transform:translate3d(-14px,20px,0);clip-path:inset(0 0 26% 0);transition:opacity .75s ease,transform .75s ease,clip-path .85s ease}
.fxjs .fx.on{opacity:1;transform:none;clip-path:inset(-20px)}
.fxjs .fx.done{opacity:1;transform:none;clip-path:none;transition:none}
@media (prefers-reduced-motion:reduce){.fxjs .fx{opacity:1;transform:none;clip-path:none;transition:none}}
"""

FX = """<script>(function(){var d=document.documentElement;d.classList.add('fxjs');
var q=[].slice.call(document.querySelectorAll('.fx'));
function t(){var h=innerHeight;q=q.filter(function(e){if(e.getBoundingClientRect().top<h*.94){e.classList.add('on');setTimeout(function(){e.classList.add('done')},1100);return false}return true})}
addEventListener('scroll',t,{passive:true});addEventListener('resize',t);addEventListener('load',t);t();
[300,1000,2500].forEach(function(m){setTimeout(t,m)});
document.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('a[data-go]');if(a&&window.gtag)gtag('event',a.getAttribute('data-go')+'_click',{page_path:location.pathname})});
})();</script>"""


def book(label="See rooms &amp; rates", cls="btn"):
    return f'<a class="{cls}" data-go="booking" href="{BOOK}" target="_blank" rel="noopener">{label}</a>'


def ctaband(title="Your dates, straight from the ryokan"):
    return f"""<section class="ctaband fx"><h2>{title}</h2>
<p>Every booking on this guide goes to Minatokan's own reservation site, so you see its current plans and prices. The pages are in Japanese, and <a href="how-to-book.html">this walkthrough</a> explains each step in English.</p>
{book()} <a class="btn ghost" data-go="contact" href="mailto:{MAIL}">Email the ryokan</a> <a class="btn ghost" data-go="tel" href="tel:+81796363330">Call {TEL}</a></section>"""


def closing(step, question):
    return f'<section class="closing fx"><p>Thank you for spending time with Kasumi today. {step} {question}</p></section>'


def table(head, rows):
    h = "".join(f"<th>{c}</th>" for c in head)
    b = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    cls = ' class="two"' if len(head) == 2 else ""
    return f'<div class="tw fx"><table{cls}><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table></div>'


STATS = """<div class="wrap"><section class="stats fx" aria-label="Minatokan at a glance">
<div><b>10</b><span>guest rooms in the whole ryokan</span></div>
<div><b>3</b><span>rooms with a private sea-view bath</span></div>
<div><b>4.7/5</b><span>from 2,089 reviews on Jalan, Japan's big travel site (Nov 8, 2026)</span></div>
<div><b>Free</b><span>pickup from JR Kasumi Station, about 10 minutes away</span></div>
</section></div>"""

PHOTOS = "https://www.jalan.net/yad317522/photo/"


def fig(name, alt, what="the view"):
    return (f'<figure class="ph fx"><img src="img/{name}.jpg" alt="AI-generated image of {alt}" width="1024" height="572" loading="lazy">'
            f'<figcaption>AI-generated image to suggest {what}. It is not a photo of Minatokan. '
            f'<a href="{PHOTOS}" target="_blank" rel="noopener">See real photos on Jalan</a></figcaption></figure>')


HOME = f"""<section class="hero"><img src="img/hero.jpg" alt="AI-generated image of a sunset over the Sea of Japan from a pine-covered headland" width="1024" height="572"><div class="in">
<div class="eyebrow">10-room onsen ryokan · Kasumi, Hyogo</div>
<h1>Your sunset over the Sea of Japan, then a table full of crab</h1>
<p class="lead">Minatokan (三七十館) sits on the Kasumi coast, about 30 minutes by limited express beyond Kinosaki Onsen. You get an onsen bath facing the sea, seafood from the local port and a small house with only 10 rooms.</p>
{book()}<span class="note">Opens the ryokan's own booking site, in Japanese. <a href="how-to-book.html" style="color:#ffe0b0">English walkthrough</a>. Background is an AI-generated image.</span>
</div></section>
{STATS}
<div class="wrap">
<h2 class="fx">Three reasons travelers go the extra 30 minutes</h2>
<div class="grid3">
<article class="card fx"><h3>A title earned by sunsets</h3><p>The ryokan carries the name "Japan's 100 Most Beautiful Sunsets" in its title, and its baths look out over the sea.</p><a class="more" href="sunset.html">Sunset times by month</a></article>
<article class="card fx"><h3>Crab for most of the year</h3><p>Kasumi's red snow crab season opens in September, and prized Matsuba crab follows on November 6.</p><a class="more" href="crab.html">Which crab, which month</a></article>
<article class="card fx"><h3>Run by seafood people</h3><p>Minatokan grew out of Minatozushi, a local sushi bar. Its Jalan page cites a 2025 award: first in sales among inns of 10 rooms or fewer in Kinki-Hokuriku.</p><a class="more" href="rooms-baths.html">Rooms and baths</a></article>
</div>
<div class="grid2">{fig("bath", "a round ceramic tub by a window facing the sea at dusk", "a private sea-view bath")}{fig("crab", "a crab dinner on a low wooden table in a tatami room", "a crab dinner")}</div>
<section class="know fx"><h3>Worth knowing before you choose</h3><ul>
<li>Standard rooms have no private bath or toilet. If an en-suite matters to you, the 3 sea-view bath rooms are the ones to look for.</li>
<li>All rooms are tatami, with low tables at about 35 cm. Low chairs are available if you ask.</li>
<li>The communal baths are indoors, with sea views. Private open-air bathing comes with the 3 special rooms.</li>
<li>December to March brings heavy snow here, and the usual cancellation fees still apply in bad weather.</li>
<li>Most plans are priced per adult, so a total for two is double the number you first see.</li>
</ul></section>
<h2 class="fx">What each season puts on your table</h2>
""" + table(["Season", "On the menu (examples from the ryokan)", "Outside"], [
    ["Spring", "Kasumi crab, live sakura prawns, sandfish, abalone, blackthroat seaperch, sea urchin, Tajima beef", "Red sunsets and squid-boat lights on the horizon"],
    ["Summer", "Live squid sashimi, rock oysters, Tajima beef, charcoal BBQ lunch by the beach", "Imagoura Beach, about 3 minutes by car, with a free shuttle"],
    ["Autumn", "Kasumi crab full course, matsutake and other mushrooms, Tajima beef", "Kasumi crab fishing opens September 1"],
    ["Winter", "Matsuba snow crab, tagged Shibayama and Kasumi crab, live crab shabu-shabu", "Snow, crab season at its height, ski slopes from 30 minutes by car"],
]) + ctaband() + closing("A good small step is comparing the sunset time for your travel month.", '<a href="sunset.html">Which month are you hoping to see Kasumi?</a>') + "</div>"

MONTHS = [("January", "17:10"), ("February", "17:42"), ("March", "18:08"), ("April", "18:33"), ("May", "18:58"), ("June", "19:18"),
          ("July", "19:17"), ("August", "18:52"), ("September", "18:10"), ("October", "17:27"), ("November", "16:55"), ("December", "16:49")]


def plan_note(t):
    h = int(t[:2]) + int(t[3:]) / 60
    if h < 17.6:
        return "Well before dinner, so you can watch from the bath"
    if h < 18.0:
        return "Just before the 18:00 dinner start"
    return "After dinner can begin, so a later dinner time helps"


SUNSET = """<div class="wrap">
""" + fig("sunset", "a sunset over the Sea of Japan from a pine-covered headland", "a Sea of Japan sunset") + """<h2 class="fx">Where the name comes from</h2>
<p class="fx">The ryokan's full name in Japanese means "the onsen inn of Japan's 100 sunset spots," and its English site calls the area "Japan's 100 Most Beautiful Sunset." Local tourism listings connect the title to this stretch of coast, naming Imagoura and Okami Park among the viewpoints.</p>
<h2 class="fx">Sunset time in Kasumi, month by month</h2>
<p class="fx">Dinner at Minatokan starts from 18:00, and the ryokan asks your preferred time. Use the table to choose between watching from the bath and watching before your meal.</p>
""" + table(["Mid-month", "Approx. sunset (Japan time)", "How it fits your evening"], [[m, t, plan_note(t)] for m, t in MONTHS]) + """
<p class="small fx">Calculated for Kasumi at 35.63°N, 134.63°E for the 15th of each month. Real times shift by a few minutes, and hills or cloud can change what you see.</p>
<h2 class="fx">Three places to watch</h2>
<div class="grid3">
<article class="card fx"><h3>From your own bath</h3><p>The 3 sea-view bath rooms have a semi-open-air tub facing the Sea of Japan, ready for you at any hour of your stay.</p></article>
<article class="card fx"><h3>From the communal bath</h3><p>The men's and women's baths overlook the sea. A hedge outside protects privacy, and the ryokan says the sunset still shows above it.</p></article>
<article class="card fx"><h3>From Imagoura</h3><p>Imagoura Beach is about 3 minutes by car, and Okami Park is a known hilltop viewpoint nearby. The front desk can point you the right way.</p></article>
</div>
<section class="know fx"><h3>Your best odds</h3><p>The ryokan singles out spring through summer for red sunsets and the lights of fishing boats on the horizon. Winter skies here are often unsettled, so a winter trip is usually more about crab and snow.</p></section>
""" + ctaband("Pick a room that faces the sunset") + closing("A useful next step is choosing between a sea-side and a mountain-side room when you compare plans.", '<a href="rooms-baths.html">Would you like to see how the rooms differ?</a>') + "</div>"

CRAB = """<div class="wrap">
<h2 class="fx">Matsuba crab or Kasumi crab?</h2>
<p class="fx">Kasumi is a real crab town, with two different stars. Your travel month decides which one you can taste.</p>
""" + fig("crab", "a crab dinner on a low wooden table in a tatami room", "a crab dinner") + """
""" + table(["", "Matsuba crab", "Kasumi crab (Kasumi-gani)"], [
    ["What it is", "Snow crab from the San'in coast. Matsuba is the regional name", "Red snow crab landed at Kasumi Port"],
    ["Season", "From November 6, through about March", "From September 1, through the end of May"],
    ["Why people seek it", "The famous winter delicacy of this coast", "Kasumi is the only port in the Kinki region landing red snow crab"],
    ["Tags", "Port tags mark branded crab, including Shibayama from next door", "Selected crabs are tagged too"],
]) + """
<h2 class="fx">How Minatokan serves it</h2>
<div class="grid2">
<article class="card fx"><h3>Full-course dinners</h3><p>Courses bring crab in several styles, such as sashimi, charcoal-grilled, shabu-shabu and boiled. A tank of live crab greets you near the entrance.</p></article>
<article class="card fx"><h3>Other tastes from the area</h3><p>Plans can add Tajima beef steak, live abalone, blackthroat seaperch or morning-caught squid. Choices differ by plan and season.</p></article>
</div>
<h2 class="fx">What a crab plan costs</h2>
""" + table(["Example plan", "Standard room, per adult", "Sea-view bath room, per adult"], [
    ["Tagged Kasumi crab full course, 2 crabs per person", "from ¥32,780", "from ¥35,780"],
    ["Same course with fresh sashimi", "from ¥34,280", "from ¥37,280"],
    ["Same course with Tajima beef steak choice", "from ¥35,780", "from ¥38,780"],
]) + f"""
<p class="small fx">Tax included, with no date selected, as shown on the ryokan's booking site on {CHECKED}. Your date, room and group size change the price. Bath tax of ¥150 per adult is added on top.</p>
<h2 class="fx">Snow crab, Matsuba and king crab</h2>
<p class="fx">"Snow crab" is the species, and "Matsuba" is what people on this coast call the males. King crab is a different animal, more closely tied to northern waters such as Hokkaido, so you would not expect it as the local catch here.</p>
<section class="know fx"><h3>Booking for crab season</h3><p>With only 10 rooms, popular winter dates can fill early. When your date is full, the ryokan accepts waiting-list requests by phone or email.</p></section>
""" + ctaband("See this season's crab plans") + closing("A small next step is matching your dates to the season above.", '<a href="how-to-book.html">Would a guide to the booking page help?</a>') + "</div>"

ROOMS = """<div class="wrap">
<h2 class="fx">Three room types, one big difference</h2>
""" + table(["Room", "View", "Private bath and toilet", "Extra"], [
    ["Sea-view bath room (3 rooms only)", "Sea of Japan", "Yes. Semi-open-air bath with shower area, usable any time during your stay, plus a bidet toilet", "About ¥3,000 more per adult"],
    ["Sea-side Japanese room", "Sea of Japan", "No. The booking page marks it as having no bath or toilet", "Standard rate"],
    ["Mountain-side Japanese room", "Mountain side", "No. The booking page marks it as having no bath or toilet", "Standard rate"],
]) + """
""" + fig("room", "a tatami room with a low table and a window facing the sea", "a tatami room with a sea view") + """<p class="fx">All 10 rooms are tatami. The ryokan describes itself as a small wooden house, which keeps the atmosphere quiet and means pets and mahjong are not allowed.</p>
<h2 class="fx">The onsen</h2>
<div class="grid2">""" + fig("bath", "a round ceramic tub by a window facing the sea at dusk", "a private sea-view bath") + fig("onsen", "an indoor hot spring bath with a wide window facing a sunset", "an indoor bath with a sea view") + """</div>
<div class="grid2">
<article class="card fx"><h3>Communal baths</h3><p>One indoor bath each for men and women, with a view of the Sea of Japan. The ryokan calls them modest in size, matched to a 10-room house.</p></article>
<article class="card fx"><h3>The water</h3><p>Jalan lists the source as Ishii Onsen, with water added, heated and recirculated through filters. There is no sauna and no communal open-air bath.</p></article>
</div>
<section class="know fx"><h3>Bath hours</h3><p>The Japanese FAQ (2021) says the communal baths are open 24 hours. The older English page lists 15:00 to 24:00 and 6:00 to 9:30. The front desk can confirm when you check in.</p></section>
<h2 class="fx">Small comforts</h2>
""" + fig("yukata", "colorful yukata hanging on a wooden rack", "a choice of colorful yukata") + """
<div class="grid3">
<article class="card fx"><h3>Yukata</h3><p>Yukata in your room, and women can choose one more from 30 colorful patterns at no cost. Staff can help you put it on.</p></article>
<article class="card fx"><h3>In your room</h3><p>Toothbrush, razor for men, hand soap, cotton swabs, hair dryer, towels and an air purifier. A humidifier is free on request while supplies last.</p></article>
<article class="card fx"><h3>Around the house</h3><p>Wi-Fi throughout, and all shared toilets have bidet seats. Luggage can stay at the front desk before and after your stay.</p></article>
</div>
<section class="know fx"><h3>Tattoos and accessibility</h3><p>We could not find a published tattoo policy or details about stairs and elevators. A short email before booking will get you the current answer, and a sample is on the <a href="how-to-book.html#ask">How to Book page</a>.</p></section>
""" + ctaband("Check which rooms are open") + closing("A helpful next step is deciding whether a private bath is a must for you.", '<a href="getting-there.html">Shall we look at how to get there?</a>') + "</div>"

ACCESS = """<div class="wrap">
<h2 class="fx">By train, with a free ride at the end</h2>
<p class="fx">Your stop is <b>JR Kasumi Station</b> on the San'in Line. Minatokan picks you up there for free and takes you back the next day. The drive is about 10 minutes.</p>
""" + fig("train", "a small train running beside a green coast and blue sea", "the coastal scenery. The real train may look different") + table(["From", "Approx. time to Kasumi", "Notes"], [
    ["Kinosaki Onsen", "About 30 minutes", "By Limited Express Hamakaze"],
    ["Himeji", "About 2 hours", "By Limited Express Hamakaze"],
    ["Kobe", "About 3 hours", "By Limited Express Hamakaze"],
    ["Osaka", "About 3 hours 30 minutes", "By Limited Express Hamakaze from Osaka Station"],
    ["Kyoto", "About 3 hours", "Hamakaze does not start in Kyoto. A common route is a limited express toward Kinosaki Onsen, then onward on the San'in Line"],
]) + """
<p class="small fx">Times come from the ryokan's access page and travel sources. The Hamakaze runs about 3 round trips a day and not every service runs the full route, so it pays to confirm your train with JR West.</p>
<h3 class="fx">Arranging your pickup</h3>
<p class="fx">If you know your arrival time, the comments box in your reservation is the place to share it. If you decide on the day, a phone call to the ryokan works. Staff will also stop at a souvenir shop on the way if you ask.</p>
<h2 class="fx">By air and by car</h2>
<div class="grid2">
<article class="card fx"><h3>Airports</h3><p>Tajima Airport is about 30 minutes by car, and Tottori Airport about 40 minutes.</p></article>
<article class="card fx"><h3>Driving</h3><p>From Osaka or Kobe, the usual route follows the expressways to Tajima Airport IC, then Route 312 and Route 178 toward Kasumi. Free parking holds 17 cars.</p></article>
</div>
<p class="fx">The ryokan sits a little above the main road. If your car is large or low to the ground, tell the staff and they will guide you to a second lot. Two Lawson convenience stores are about 7 minutes away by car.</p>
<section class="know fx"><h3>Traveling December to March</h3><p>This area gets heavy snow and sudden weather changes. If your car or train gets stuck, the ryokan offers to collect guests for free from places as far as Wadayama or Toyooka, so a phone call is your best move. A seasonal "crab bus" also runs in winter, and the ryokan can tell you about it.</p></section>
""" + ctaband("Have your route? Look at your dates") + closing("A small next step is looking up your train on the JR West site.", '<a href="nearby.html">Would you like ideas for the day before or after?</a>') + "</div>"

NEARBY = """<div class="wrap">
<h2 class="fx">Pair it with Kinosaki Onsen</h2>
<p class="fx">Kinosaki's famous bathhouse town is about 30 minutes away by limited express, so you can spend a night in each. You could enjoy Kinosaki's lanes first, then continue to Kasumi for the sunset and a quieter evening.</p>
<h2 class="fx">Times by car from Minatokan</h2>
""" + table(["Place", "By car", "Why go"], [
    ["Morning market", "2 min", "Local food and an early start"],
    ["Sightseeing boat", "3 min", "See the Geopark coastline from the water"],
    ["Imagoura Beach", "3 min", "The closest beach, with free shuttle from the ryokan"],
    ["Fishing and boat fishing", "4 min", "Boat and raft fishing, with a guest discount"],
    ["Daijo-ji Temple", "10 min", "Sliding-door paintings by Maruyama Okyo"],
    ["Amarube Bridge", "15 min", "A railway viaduct high above the village"],
    ["Ojiro Ski Area", "30 min", "Winter snow close by"],
    ["Kinosaki Marine World", "40 min", "An aquarium on the coast"],
    ["Tajima Great Buddha", "40 min", "A large statue inland"],
    ["Tottori Sand Dunes", "50 min", "Japan's famous dunes, an easy day trip"],
]) + """
<h2 class="fx">Amarube Bridge</h2>
<p class="fx">Amarube Station is about 10 minutes west of Kasumi on the San'in Line local train, since the Hamakaze does not stop there. The old steel trestle was replaced by a concrete bridge in 2010, and part of it now forms the Sora no Eki observation deck, about 40 meters above the ground.</p>
<h2 class="fx">San'in Kaigan Geopark</h2>
""" + fig("coast", "rock cliffs and sea stacks on a clear green sea", "the rocky coastline") + """
<p class="fx">Minatokan stands inside the San'in Kaigan National Park, on a coast recognized as a Geopark. You can read the rock and sea stacks from the sightseeing boat or from the shore.</p>
<section class="know fx"><h3>Summer at the ryokan</h3><p>In July and August, staying guests have been offered a free marine activity such as rock fishing, plus paid trial diving from ¥12,000 and a charcoal BBQ lunch by the beach. Offers change, so the ryokan can confirm this year's list.</p></section>
""" + ctaband("Build your Kasumi night into the trip") + closing("A good small step is choosing the one place above you would most like to see.", '<a href="faq.html">Do you have a question the FAQ can answer?</a>') + "</div>"

FAQS = [
 ("Booking and payment", [
  ("Where do I book?", "All reservations on this guide go to Minatokan's own booking site. The site is in Japanese, and our How to Book page translates each step."),
  ("How late can I book?", "The plan we checked accepted reservations until 17:00 on the day of the stay. Limits can differ by plan."),
  ("What if my date is full?", "The ryokan accepts waiting-list requests by phone or email."),
  ("Which payment methods work?", "Cash or card. Jalan lists JCB, Visa, Mastercard, American Express, Diners and debit cards at the ryokan, and its FAQ also mentions PayPay. An older English page says only Visa and Mastercard, so carrying some cash is a sensible backup. Online card payment at booking is offered on some plans."),
  ("When do cancellation fees begin?", "Generally 30% from 7 days before, 50% from 5 days before, 70% from 3 days before and 100% on the day or for a no-show. Some plans differ, so it helps to read the plan you pick."),
  ("Do weather cancellations cost anything?", "The same fees apply. December to March brings heavy snow here, so the ryokan suggests watching the forecast and changing your booking early if needed."),
  ("Can I stay alone?", "The Jalan FAQ says there are no one-person plans available online, and invites solo travelers to phone the ryokan directly."),
  ("Are there extra charges?", "A bath tax of ¥150 per adult is charged separately."),
 ]),
 ("Rooms and stay", [
  ("What are the check-in and check-out times?", "Check-in from 15:00, check-out by 10:00. If you will arrive after 18:00, the ryokan asks you to let them know."),
  ("Do all rooms have a bath and toilet?", "No. The 3 sea-view bath rooms do. The sea-side and mountain-side rooms are marked as having no bath or toilet."),
  ("Are there Western-style beds?", "All 10 rooms are Japanese-style tatami rooms."),
  ("Is sitting on the floor required?", "In-room meals use tables about 35 cm high. Low chairs are available for small children and anyone with difficulty sitting."),
  ("Can you hold my luggage?", "Yes. The front desk can keep bags before check-in and after check-out."),
  ("Is there Wi-Fi?", "Yes, Wi-Fi is available throughout the building."),
  ("Are pets allowed?", "No. The building is wooden and small, so pets cannot stay."),
  ("Is there a yukata for me?", "Yes. Each room has yukata, and women can pick one more from 30 colorful patterns for free. Staff can help you dress."),
 ]),
 ("Baths", [
  ("When are the communal baths open?", "The Japanese FAQ (2021) says 24 hours. An older English page lists 15:00 to 24:00 and 6:00 to 9:30. The front desk can confirm."),
  ("Is the private sea-view bath available all night?", "Yes. It is yours at any time from check-in until check-out, and it has a shower and washing area."),
  ("Is there a communal open-air bath?", "Jalan lists one indoor bath each for men and women, with no communal open-air bath or sauna."),
  ("Are tattoos allowed?", "We could not find a published policy. The ryokan can give you the current answer by email or phone."),
 ]),
 ("Meals and celebrations", [
  ("What time is dinner?", "Dinner begins from 18:00, and the ryokan asks what time you prefer."),
  ("Can I come only for a meal?", "Yes, there are day-use meal plans in a private dining room. Dinner runs from 18:00 to 21:00. Bathing can be added for ¥650, which covers a rental hand towel and the bath tax."),
  ("Can you prepare a cake or champagne?", "Yes, with advance notice. Birthday cakes start from ¥3,460 for a 12 cm size, and champagne and flowers can be arranged to your budget."),
  ("I have a food allergy.", "The ryokan asks you to tell them beforehand, and the comments box on the booking form is a good place to do so."),
 ]),
 ("Getting there", [
  ("Is there a station shuttle?", "Yes. The ryokan picks you up at JR Kasumi Station for free and takes you back the next day."),
  ("Is parking free?", "Yes. There is room for 17 cars, and a second lot for large or low vehicles."),
  ("Is there a convenience store nearby?", "Two Lawson stores are about 7 minutes away by car."),
  ("What if snow stops my trip?", "Call the ryokan right away. It offers free pickup for stranded guests, including from Wadayama or Toyooka."),
 ]),
 ("Children", [
  ("Is there a children's breakfast?", "Yes. Children can have either the adult breakfast or a children's breakfast, chosen when you book."),
  ("Are there children's yukata?", "Yes, in blue and pink. Yukata for very small children may be long, so ask ahead. Rentals are ¥200 when not included."),
  ("Can you warm baby food?", "Please bring your own milk or baby food. The kitchen can warm food and sterilize bottles if you ask the staff."),
 ]),
 ("Summer activities", [
  ("Is there a shuttle to the beach?", "Yes, free shuttles run to beaches in town. Parking at Imagoura Beach by your own car costs extra."),
  ("Can I try scuba diving?", "Trial dives start from ¥12,000 per person with gear and a guide, in July and August. A license course is also offered."),
  ("Can I rinse off after the beach?", "Yes, there is a shower space, and guests can use a washing machine. Please check at the front desk first."),
 ]),
]

_f = ""
for cat, qs in FAQS:
    _f += f'<h2 class="fx">{cat}</h2>' + "".join(f"<details class=\"fx\"><summary>{q}</summary><p>{a}</p></details>" for q, a in qs)
FAQ = f"""<div class="wrap">
<p class="small fx" style="margin-top:26px">Answers are rewritten in our own words from the Q&amp;A that Minatokan publishes on Jalan and on its own website, checked {CHECKED}. Some source answers are several years old, so the ryokan's word is always the final one.</p>
{_f}
{ctaband("Still curious? The ryokan can answer directly")}
{closing("A quick email with your dates is often the easiest next step.", '<a href="how-to-book.html#ask">Would a ready-to-send sample help?</a>')}
</div>"""

BOOKING = f"""<div class="wrap">
<h2 class="fx">Your booking in 5 steps</h2>
<p class="fx">The reservation pages are in Japanese. Your browser's translate button helps a lot, and this page tells you what each part means.</p>
<ol class="steps fx">
<li><b>Open the plan list.</b> {book("Open Minatokan's booking site", "btn ghost")}</li>
<li><b>Enter your stay.</b> Set the date, nights, rooms and guests, then press <b>再検索</b> (search again).</li>
<li><b>Compare plans.</b> Each plan shows room types with a price <b>per adult</b>, tax included. Rooms marked <b>※バスなしトイレなし</b> have no bath or toilet.</li>
<li><b>Open your plan.</b> Press <b>詳細・予約</b> (details and booking) and read the cancellation rules.</li>
<li><b>Finish your reservation.</b> Press <b>予約へ進む</b> (go to booking), then follow the form. The comments box is where your pickup time and allergies go.</li>
</ol>
<h2 class="fx">Words you will see</h2>
""" + table(["Japanese", "Meaning"], [
    ["宿泊日", "Check-in date"], ["日付未定", "Date not decided"], ["泊", "Nights"], ["部屋", "Rooms"], ["大人 / 子供", "Adults / children"],
    ["朝/夕あり", "Breakfast and dinner included"], ["夕/部屋出し", "Dinner served in your room"], ["夕/個室利用", "Dinner in a private dining room"],
    ["日本海の見えるお部屋", "Room with a Sea of Japan view"], ["山側のお部屋", "Mountain-side room"], ["展望風呂付き", "With private sea-view bath"],
    ["大人1名（税込）", "Price per adult, tax included"], ["合計（税込）", "Total, tax included"], ["現地決済", "Pay at the ryokan"], ["オンラインカード決済", "Pay online by card"],
    ["キャンセル規定", "Cancellation policy"], ["入湯税", "Bath tax (¥150 per adult)"], ["予約内容照会", "Look up your reservation"],
]) + """
<h2 class="fx">Cancellation fees</h2>
""" + table(["When you cancel", "Fee"], [
    ["7 to 6 days before", "30%"], ["5 to 4 days before", "50%"], ["3 to 1 days before", "70%"], ["On the day", "100%"], ["No-show", "100%"],
]) + f"""
<p class="small fx">From the plan we checked on {CHECKED}. Each plan shows its own rules, and they apply even in bad weather.</p>
<h2 id="ask" class="fx">Prefer to ask first?</h2>
<p class="fx">Email <a data-go="contact" href="mailto:{MAIL}">{MAIL}</a> or call <a data-go="tel" href="tel:+81796363330">{TEL}</a>. A short message with clear dates is easy for a small ryokan to answer, and you are welcome to use this one.</p>
<pre class="fx">Hello. I would like to stay at Minatokan.
Date: (check-in date) for (number) night(s)
Guests: (number) adults, (number) children
Room: sea-view bath room / sea-view room / mountain-side room
Arrival: JR Kasumi Station at (time). May I use the free pickup?
Question: (for example, tattoo policy, food allergy, stairs)
Thank you very much.</pre>
<p class="small fx">Telling the ryokan you are writing in English is helpful. We could not confirm how much English the staff use, so short sentences may work best.</p>
{ctaband("Ready when you are")}
{closing("A small next step is writing down your dates and party size.", 'Which room type sounds right for your stay?')}
</div>"""

SOURCES = [
 ("Minatokan official website (Japanese)", "https://www.minatokan.jp/"), ("Minatokan official website (English)", "https://www.minatokan.jp/en/"),
 ("Minatokan on Jalan", "https://www.jalan.net/yad317522/"), ("Minatokan Q&amp;A on Jalan", "https://www.jalan.net/yad317522/qa/"),
 ("Red snow crab, Visit Hyogo", "https://www.hyogo-tourism.jp/world/food/11"), ("Kami Town, Visit Hyogo", "https://www.hyogo-tourism.jp/world/review/detail_210.html"),
 ("Limited Express Hamakaze, Ekitan", "https://ekitan.com/en/article/hamakaze"), ("Snow crab season in Kinosaki, JNTO", "https://www.japan.travel/en/ca/news/it-s-snow-crab-season-in-kinosaki-onsen/"),
 ("Amarube Viaduct, Wikipedia", "https://en.wikipedia.org/wiki/Amarube_Viaduct"), ("Kasumi travel feature, ATT Japan", "https://att-japan.net/en/kasumi_kitakinki2024/"),
]
ABOUT = f"""<div class="wrap">
<h2 class="fx">Thank you for being here</h2>
<p class="fx">We appreciate your interest in Kasumi. This guide exists so that travelers who read English can discover a small ryokan on the Sea of Japan and feel confident booking it.</p>
<h2 class="fx">This is an unofficial guide</h2>
<p class="fx">This site is independent. It is not run by, endorsed by or affiliated with Minatokan. All reservations and questions about your stay go directly to the ryokan, which is the only source for current plans, prices and rules.</p>
<h2 class="fx">How it is made</h2>
<ul class="fx">
<li>Text was drafted with AI assistance, using the public sources below.</li>
<li>Facts are rewritten in our own words. Guest reviews and the ryokan's photos are not copied here.</li>
<li>Nothing on this site describes a personal stay.</li>
<li>Every image was created with generative AI (Google Gemini) from written descriptions, and each one is labeled. They suggest the mood only, and do not show the real ryokan, rooms, food or view. <a href="https://www.jalan.net/yad317522/photo/" target="_blank" rel="noopener">Real photos are on Jalan</a>.</li>
<li>This site has no ads and earns nothing from your booking.</li>
<li>Sunset times are calculated estimates.</li>
</ul>
<p class="fx">The Jalan rating and all prices were read on {CHECKED} and can change.</p>
<h2 class="fx">Sources</h2>
<ul class="fx">{''.join(f'<li><a href="{u}" target="_blank" rel="noopener">{t}</a></li>' for t, u in SOURCES)}</ul>
<h2 class="fx">Corrections</h2>
<p class="fx">If you represent the ryokan, or you spot something out of date, you can <a href="https://github.com/masabee1029/minatokan-kasumi-guide/issues" target="_blank" rel="noopener">open a correction request</a>, and we will fix or remove it promptly.</p>
{closing("A good small step is taking a look at the season you would like to visit.", '<a href="index.html">Which part of Kasumi drew you here?</a>')}
</div>"""

PAGES = {
 "index.html": ("Minatokan, Kasumi: Sunset Onsen &amp; Snow Crab Ryokan (Unofficial Guide)", "An English guide to Minatokan, a 10-room onsen ryokan in Kasumi, Hyogo, known for Sea of Japan sunsets and snow crab, 30 minutes from Kinosaki Onsen.", None, None, HOME),
 "sunset.html": ("Japan's 100 Most Beautiful Sunset Spots: Kasumi Ryokan Sunset Guide", "Sunset times by month in Kasumi, the best places to watch over the Sea of Japan, and how to time your evening at Minatokan.", "A sunset worth planning around", "Month-by-month times for Kasumi, one of the coasts behind Minatokan's sunset title.", SUNSET),
 "crab.html": ("Matsuba Crab vs Kasumi Red Snow Crab: Season Guide for Hyogo", "Matsuba crab season, Kasumi red snow crab season, and what crab kaiseki plans cost at Minatokan ryokan in Kasumi, Hyogo.", "Crab, month by month", "Which crab you can taste in Kasumi, and what a full-course plan costs.", CRAB),
 "rooms-baths.html": ("Minatokan Rooms and Onsen: Ryokan with Private Open-Air Bath in Hyogo", "Compare Minatokan's sea-view bath rooms and standard tatami rooms, and learn about the onsen, bath hours and yukata.", "Rooms and baths", "Choose your view and your bath before you choose your plan.", ROOMS),
 "getting-there.html": ("How to Get to Kasumi from Osaka, Kyoto and Kinosaki Onsen", "Train times to JR Kasumi Station from Osaka, Kyoto, Kobe and Kinosaki Onsen, Minatokan's free pickup, airports, driving and winter travel.", "Getting to Kasumi", "Trains, the free station pickup, and what to expect in snow.", ACCESS),
 "nearby.html": ("Things to Do Near Kasumi: Amarube Bridge, Kinosaki, San'in Geopark", "Places near Minatokan in Kasumi with driving times, including Amarube Bridge, Kinosaki Onsen, Tottori Sand Dunes and the San'in Kaigan Geopark.", "Around Kasumi", "Sights within an hour, with driving times from the ryokan.", NEARBY),
 "faq.html": ("Minatokan Kasumi FAQ in English: Rooms, Payment, Pickup, Children", "English answers to common questions about staying at Minatokan: booking, payment, cancellation, baths, meals, children and access.", "Frequently asked questions", "The ryokan's common questions, in plain English.", FAQ),
 "how-to-book.html": ("How to Book Minatokan Ryokan in English: Step-by-Step Guide", "An English walkthrough of Minatokan's Japanese booking site, with a glossary, cancellation fees and an email sample for the ryokan.", "How to book Minatokan", "An English map of a Japanese reservation page.", BOOKING),
 "about.html": ("About This Unofficial Minatokan Guide", "About this independent English guide to Minatokan in Kasumi: who it is for, how it is made and its sources.", "About this guide", "Independent, ad-free, and clear about its sources.", ABOUT),
}


def jsonld(fn, title, desc):
    if fn == "faq.html":
        data = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for _, qs in FAQS for q, a in qs]}
    else:
        data = {"@context": "https://schema.org", "@type": "Article", "headline": H.unescape(title), "description": desc, "url": BASE + ("" if fn == "index.html" else fn),
                "about": {"@type": "Thing", "name": "Minatokan ryokan, Kasumi, Hyogo, Japan"}, "dateModified": "2026-11-09", "inLanguage": "en"}
    return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False).replace("</", "<\\/") + "</script>"


def page(fn, title, desc, head, sub, body):
    url = BASE + ("" if fn == "index.html" else fn)
    nav = "".join(f'<a href="{f}"{" class=on" if f == fn else ""}>{t}</a>' for f, t in NAV)
    ph = f'<section class="pagehead"><div class="wrap"><h1>{head}</h1><p>{sub}</p></div></section>' if head else ""
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><meta name="description" content="{H.escape(desc)}"><link rel="canonical" href="{url}">
<meta property="og:type" content="website"><meta property="og:title" content="{title}"><meta property="og:description" content="{H.escape(desc)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{BASE}img/sunset.jpg"><meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='7' fill='%23231f47'/%3E%3Ccircle cx='16' cy='20' r='8' fill='%23f4b25c'/%3E%3Crect y='20' width='32' height='12' fill='%23143a55'/%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600&family=Fraunces:opsz,wght@9..144,600&display=swap" rel="stylesheet">
<script async src="https://www.googletagmanager.com/gtag/js?id=G-EHWF25C1RB"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-EHWF25C1RB');</script>
{jsonld(fn, title, desc)}<style>{CSS}</style></head><body>
<header class="top"><div class="bar"><a class="brand" href="index.html">Minatokan<small>Unofficial guide</small></a>{book("Book direct")}</div><nav class="menu" aria-label="Pages">{nav}</nav></header>
<p class="ainote">This site uses AI-generated images. <span lang="ja">このサイトはAI画像を使用しています。</span></p>
<main>{ph}{body}</main>
<footer><div class="wrap"><p><b>Unofficial guide.</b> Not affiliated with Minatokan. Bookings and questions go directly to the ryokan: <a data-go="contact" href="mailto:{MAIL}">email</a>, <a data-go="tel" href="tel:+81796363330">{TEL}</a>.</p>
<p>Minatokan, 906 Kasumi-ku Sakai, Kami-cho, Mikata-gun, Hyogo 669-6541, Japan. Facts checked {CHECKED}. Drafted with AI assistance. This site uses AI-generated images. <span lang="ja">このサイトはAI画像を使用しています。</span> <a href="about.html">About this guide</a></p></div></footer>
<div class="sticky"><span>Direct with the ryokan, 10 rooms only</span>{book("See rooms &amp; rates")}</div>
{FX}</body></html>"""


def main():
    os.makedirs(os.path.join(OUT, "img"), exist_ok=True)
    for fn, (t, d, hd, sb, body) in PAGES.items():
        open(os.path.join(OUT, fn), "w", encoding="utf-8").write(page(fn, t, d, hd, sb, body))
    urls = "".join(f"<url><loc>{BASE}{'' if f == 'index.html' else f}</loc><lastmod>2026-11-09</lastmod></url>" for f in PAGES)
    open(os.path.join(OUT, "sitemap.xml"), "w").write(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>')
    open(os.path.join(OUT, ".nojekyll"), "w").close()
    print("built", len(PAGES), "pages")


if __name__ == "__main__":
    main()
