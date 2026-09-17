#!/usr/bin/env python3
"""Builds the homepage in Portuguese, Spanish, French and German from the English page.

The design lives in styles.css, which every page links; this script only assembles markup.
The words come from _tools/lang/<code>.py, each written by a native reader on 2026-09-14.
The form in all five pages posts to the relay's /waitlist (RELAY below); after the first
deploy, replace RELAY here and in index.html and run this script again.

    python3 _tools/build-pages.py        # from the site root; rewrites pt/ es/ fr/ de/index.html

index.html is written by hand — this script never touches it.
The underscore keeps this directory out of the published site (GitHub Pages runs Jekyll).
"""
import html, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RELAY = 'https://give-to-reach-relay.sergigon.workers.dev'
ACTION = RELAY + '/waitlist'
CODES = ['pt', 'es', 'fr', 'de']
VOLUMES = ['lt5', '5to20', '20to50', 'gt50']

# the short labels the native blocks do not carry
FORM = {
    'pt': dict(email='E-mail', linkedin='O seu perfil no LinkedIn', choose='Escolha uma opção', opts=['menos de 5', '5 a 20', '20 a 50', 'mais de 50']),
    'es': dict(email='Correo electrónico', linkedin='Tu perfil de LinkedIn', choose='Elige una opción', opts=['menos de 5', 'de 5 a 20', 'de 20 a 50', 'más de 50']),
    'fr': dict(email='E-mail', linkedin='Votre profil LinkedIn', choose='Choisissez une réponse', opts=['moins de 5', 'de 5 à 20', 'de 20 à 50', 'plus de 50']),
    'de': dict(email='E-Mail', linkedin='Ihr LinkedIn-Profil', choose='Bitte auswählen', opts=['weniger als 5', '5 bis 20', '20 bis 50', 'mehr als 50']),
}


def form_html(code, button, body, f, small):
    q1, q2 = [q.strip() for q in body.strip().split('\n\n')]
    opts = ''.join(f'            <option value="{v}">{html.escape(o)}</option>\n' for v, o in zip(VOLUMES, f['opts']))
    return f'''      <form class="wl" method="post" action="{ACTION}">
        <input type="hidden" name="lang" value="{code}">
        <input type="hidden" name="t" value="">
        <p class="hp" aria-hidden="true"><label>Website <input type="text" name="website" tabindex="-1" autocomplete="off"></label></p>
        <div class="field">
          <label for="wl-email">{html.escape(f['email'])}</label>
          <input id="wl-email" type="email" name="email" maxlength="200" required autocomplete="email">
        </div>
        <div class="field">
          <label for="wl-linkedin">{html.escape(f['linkedin'])}</label>
          <input id="wl-linkedin" type="text" name="linkedin" maxlength="200" required inputmode="url" autocomplete="off" placeholder="linkedin.com/in/..." pattern="\\s*(https?://)?([a-z]{{1,3}}\\.)?linkedin\\.com/in/[^\\s\\/?#]+/?([?#].*)?\\s*" title="linkedin.com/in/your-name">
        </div>
        <div class="field">
          <label for="wl-volume">{html.escape(q1)}</label>
          <select id="wl-volume" name="volume" required>
            <option value="" selected disabled>{html.escape(f['choose'])}</option>
{opts}          </select>
        </div>
        <div class="field">
          <label for="wl-why">{html.escape(q2)}</label>
          <textarea id="wl-why" name="why" maxlength="1000" rows="3" required></textarea>
        </div>
        <div><button class="button" type="submit">{html.escape(button)}</button></div>
        <p class="fine">{small}</p>
      </form>
'''


def page(code, t):
    steps = ''.join(f'        <li>{s}</li>\n' for s in t['steps'])
    exits = ''.join(f'      <p><strong>{h}</strong> {p}</p>\n' for h, p in t['exits'])
    qa = ''.join(f'      <div class="qa">\n        <dt>{q}</dt>\n        <dd>{a}</dd>\n      </div>\n' for q, a in t['qa'])
    langs = t['switch'].replace(' · ', ' ')  # the new header spaces them with flex gap
    return f'''<!DOCTYPE html>
<html lang="{t['lang']}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{t['title']}</title>
<meta name="description" content="{html.escape(t['desc'], quote=True)}">
<link rel="icon" href="../logo/give-to-reach-logo-32.png">
<link rel="stylesheet" href="../styles.css">
</head>
<body>
<div class="wrap">

  <header class="top">
    <a class="mark" href="../"><img src="../logo/give-to-reach-logo-128.png" alt=""><span>Give to Reach</span></a>
    <nav class="langs">{langs}</nav>
  </header>

  <section class="hero">
    <h1 class="lede">{t['intro']}</h1>
    <div class="byline">
      <img src="../sergio-320.jpg" alt="Sergio González">
      <p><strong>Sergio González</strong> — {t['byline']} <a href="https://www.linkedin.com/in/sgonzalezalonso/" target="_blank" rel="noopener">{t['linkedin']}</a></p>
    </div>
  </section>

  <section class="row">
    <h2>{t['how']}</h2>
    <div>
      <ol class="steps">
{steps}      </ol>
      <div class="notes">
        <p>{t['known']}</p>
        <p>{t['banner']}</p>
      </div>
    </div>
  </section>

  <section class="row">
    <h2>{t['notfor']}</h2>
    <div class="prose">
{exits}    </div>
  </section>

  <section class="row">
    <h2>{t['why']}</h2>
    <div class="prose">
      <p>{t['whyp']}</p>
    </div>
  </section>

  <section class="row">
    <h2>{t['keeps']}</h2>
    <div class="prose">
      <p>{t['keeps1']}</p>
    </div>
  </section>

  <section class="row">
    <h2>{t['faq']}</h2>
    <dl class="faq">
{qa}    </dl>
  </section>

  <section class="row wl">
    <h2>{t['eyebrow']}</h2>
    <div>
      <h3>{t['wl']}</h3>
      <p>{t['wlp']}</p>
{form_html(code, t['button'], t['body'], FORM[code], t['small'])}    </div>
  </section>

  <footer class="site">
    <p>{t['foot']}</p>
    <p class="links"><a href="../privacy/">{t['privacy']}</a> <a href="../terms/">{t['terms']}</a></p>
  </footer>
</div>
<script>
  document.querySelectorAll('form.wl input[name="t"]').forEach(function (i) {{ i.value = Date.now(); }});
  document.querySelectorAll('form.wl').forEach(function (f) {{
    f.addEventListener('submit', function () {{ f.querySelector('input[name="t"]').value = Date.now(); }});
  }});
</script>
</body>
</html>
'''


def main():
    for code in CODES:
        ns = {}
        exec(open(os.path.join(ROOT, '_tools', 'lang', code + '.py'), encoding='utf-8').read(), ns)
        t = ns['T']
        assert t['lang'] == code and len(t['qa']) == 5 and len(t['steps']) == 4 and len(t['exits']) == 3 and t['known'].startswith('* '), code
        os.makedirs(os.path.join(ROOT, code), exist_ok=True)
        open(os.path.join(ROOT, code, 'index.html'), 'w', encoding='utf-8').write(page(code, t))
        print(code + '/index.html written')


if __name__ == '__main__':
    main()
