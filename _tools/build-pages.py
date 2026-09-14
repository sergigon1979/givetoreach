#!/usr/bin/env python3
"""Builds the homepage in Portuguese, Spanish, French and German from the English page.

index.html is the source of the design (its <style> block is copied verbatim) and of the
waitlist form; the words come from _tools/lang/<code>.py, each written by a native reader on
2026-09-14. The form in all five pages posts to the relay's /waitlist (RELAY below); after the
first deploy, replace RELAY here and in index.html and run this script again.

    python3 _tools/build-pages.py        # from the site root; rewrites pt/ es/ fr/ de/index.html

The underscore keeps this directory out of the published site (GitHub Pages runs Jekyll).
"""
import html, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RELAY = 'https://give-to-reach-relay.REPLACE-AFTER-DEPLOY.workers.dev'
ACTION = RELAY + '/waitlist'
CODES = ['pt', 'es', 'fr', 'de']
VOLUMES = ['lt5', '5to20', '20to50', 'gt50']

# the short labels the native blocks do not carry
FORM = {
    'en': dict(name='Name', email='Email', linkedin='Your LinkedIn profile', choose='Choose one', opts=['fewer than 5', '5 to 20', '20 to 50', 'more than 50']),
    'pt': dict(name='Nome', email='E-mail', linkedin='O seu perfil no LinkedIn', choose='Escolha uma opção', opts=['menos de 5', '5 a 20', '20 a 50', 'mais de 50']),
    'es': dict(name='Nombre', email='Correo electrónico', linkedin='Tu perfil de LinkedIn', choose='Elige una opción', opts=['menos de 5', 'de 5 a 20', 'de 20 a 50', 'más de 50']),
    'fr': dict(name='Nom', email='E-mail', linkedin='Votre profil LinkedIn', choose='Choisissez une réponse', opts=['moins de 5', 'de 5 à 20', 'de 20 à 50', 'plus de 50']),
    'de': dict(name='Name', email='E-Mail', linkedin='Ihr LinkedIn-Profil', choose='Bitte auswählen', opts=['weniger als 5', '5 bis 20', '20 bis 50', 'mehr als 50']),
}
EN = dict(button='Join the waitlist',
          body='Roughly how many unsolicited B2B emails do you get a week?\n\nWhy do you want this?\n',
          small='Your answers, your address and your profile link are read by me alone, used only to invite you, and deleted when you ask.')

FORM_CSS = '''  form.wl { margin-top: 14px; }
  form.wl label { display: block; font-size: 14px; font-weight: 600; color: #1a1a1a; margin: 12px 0 4px; }
  form.wl input, form.wl select, form.wl textarea { width: 100%; font: inherit; font-size: 16px; color: #1a1a1a; background: #fff; border: 1px solid #bcd9bf; border-radius: 8px; padding: 10px 12px; }
  form.wl textarea { min-height: 84px; resize: vertical; }
  form.wl input:focus, form.wl select:focus, form.wl textarea:focus { outline: 2px solid #1b5e20; outline-offset: 1px; border-color: #1b5e20; }
  form.wl .hp { position: absolute; left: -10000px; top: auto; width: 1px; height: 1px; overflow: hidden; }
  form.wl button.button { border: 0; cursor: pointer; font-family: inherit; margin-top: 16px; }
  form.wl + .small { margin-top: 12px; }
'''
FORM_CSS_MOBILE = '    form.wl button.button { width: 100%; }\n'


def form_html(code, button, body, f, indent='    '):
    q1, q2 = [q.strip() for q in body.strip().split('\n\n')]
    opts = ''.join(f'{indent}    <option value="{v}">{html.escape(o)}</option>\n' for v, o in zip(VOLUMES, f['opts']))
    return f'''{indent}<form class="wl" method="post" action="{ACTION}">
{indent}  <input type="hidden" name="lang" value="{code}">
{indent}  <input type="hidden" name="t" value="">
{indent}  <p class="hp" aria-hidden="true"><label>Website <input type="text" name="website" tabindex="-1" autocomplete="off"></label></p>
{indent}  <label for="wl-name">{html.escape(f['name'])}</label>
{indent}  <input id="wl-name" type="text" name="name" maxlength="120" autocomplete="name">
{indent}  <label for="wl-email">{html.escape(f['email'])}</label>
{indent}  <input id="wl-email" type="email" name="email" maxlength="200" required autocomplete="email">
{indent}  <label for="wl-linkedin">{html.escape(f['linkedin'])}</label>
{indent}  <input id="wl-linkedin" type="text" name="linkedin" maxlength="200" required inputmode="url" autocomplete="off" placeholder="linkedin.com/in/..." pattern="\\s*(https?://)?([a-z]{{1,3}}\\.)?linkedin\\.com/in/[^\\s\\/?#]+/?([?#].*)?\\s*" title="linkedin.com/in/your-name">
{indent}  <label for="wl-volume">{html.escape(q1)}</label>
{indent}  <select id="wl-volume" name="volume" required>
{indent}    <option value="" selected disabled>{html.escape(f['choose'])}</option>
{opts}{indent}  </select>
{indent}  <label for="wl-why">{html.escape(q2)}</label>
{indent}  <textarea id="wl-why" name="why" maxlength="1000" rows="3" required></textarea>
{indent}  <button class="button" type="submit">{html.escape(button)}</button>
{indent}</form>
{indent}<script>document.querySelector('form.wl input[name="t"]').value = Date.now();</script>
'''


def patch_english(en):
    """the form and its CSS into index.html; idempotent, so the script can run again after edits"""
    if 'form.wl' not in en:
        en = en.replace('  .small { font-size: 14px; line-height: 1.5; color: #5f5f5f; }\n',
                        '  .small { font-size: 14px; line-height: 1.5; color: #5f5f5f; }\n' + FORM_CSS, 1)
        en = en.replace('    .button { display: block; text-align: center; }\n',
                        '    .button { display: block; text-align: center; }\n' + FORM_CSS_MOBILE, 1)
        assert en.count('form.wl') > 2, 'CSS anchors not found in index.html'
    m = re.search(r'    <p><a class="button" href="mailto:[^"]*">Join the waitlist</a></p>\n    <p class="small">[^\n]*</p>\n', en)
    if m:
        en = en[:m.start()] + form_html('en', EN['button'], EN['body'], FORM['en']) + f'    <p class="small">{EN["small"]}</p>\n' + en[m.end():]
    else:
        # already a form: refresh it in place (RELAY or labels may have changed)
        m = re.search(r'    <form class="wl".*?</script>\n    <p class="small">[^\n]*</p>\n', en, re.S)
        assert m, 'no waitlist button or form found in index.html'
        en = en[:m.start()] + form_html('en', EN['button'], EN['body'], FORM['en']) + f'    <p class="small">{EN["small"]}</p>\n' + en[m.end():]
    return en


def page(code, t, css):
    steps = ''.join(f'      <li>{s}</li>\n' for s in t['steps'])
    exits = ''.join(f'    <p><strong>{h}</strong> {p}</p>\n' for h, p in t['exits'])
    qa = ''.join(f'      <dt>{q}</dt>\n      <dd>{a}</dd>\n' for q, a in t['qa'])
    small = t['small']  # the data promise under the form
    return f'''<!DOCTYPE html>
<html lang="{t['lang']}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{t['title']}</title>
<meta name="description" content="{html.escape(t['desc'], quote=True)}">
<link rel="icon" href="../logo/give-to-reach-logo-32.png">
{css}
</head>
<body>
<div class="container">
  <p class="lang">{t['switch']}</p>
  <div class="brand"><img src="../logo/give-to-reach-logo-128.png" alt=""><h1>Give to Reach</h1></div>
  <p class="intro">{t['intro']}</p>
  <div class="profile">
    <img src="../sergio-320.jpg" alt="Sergio González">
    <div>
      <h3>Sergio González</h3>
      <p>{t['byline']} <a href="https://www.linkedin.com/in/sgonzalezalonso/" target="_blank" rel="noopener">{t['linkedin']}</a></p>
    </div>
  </div>

  <div class="card how">
    <h2>{t['how']}</h2>
    <ol>
{steps}    </ol>
  </div>
  <div class="banner">{t['banner']}</div>

  <div class="card">
    <h2>{t['notfor']}</h2>
{exits}  </div>

  <div class="card">
    <h2>{t['why']}</h2>
    <p>{t['whyp']}</p>
  </div>

  <div class="card">
    <h2>{t['keeps']}</h2>
    <p>{t['keeps1']}</p>
  </div>

  <div class="card faq">
    <h2>{t['faq']}</h2>
    <dl>
{qa}    </dl>
  </div>

  <div class="card waitlist">
    <p class="eyebrow">{t['eyebrow']}</p>
    <h2>{t['wl']}</h2>
    <p>{t['wlp']}</p>
{form_html(code, t['button'], t['body'], FORM[code])}    <p class="small">{small}</p>
  </div>

  <footer>
    <p><a href="../privacy/">{t['privacy']}</a> &middot; <a href="../terms/">{t['terms']}</a></p>
    <p>{t['foot']}</p>
  </footer>
</div>
</body>
</html>
'''


def main():
    path = os.path.join(ROOT, 'index.html')
    en = open(path, encoding='utf-8').read()
    patched = patch_english(en)
    if patched != en:
        open(path, 'w', encoding='utf-8').write(patched)
        print('index.html: form patched in')
    css = patched[patched.index('<style>'):patched.index('</style>') + len('</style>')]
    for code in CODES:
        ns = {}
        exec(open(os.path.join(ROOT, '_tools', 'lang', code + '.py'), encoding='utf-8').read(), ns)
        t = ns['T']
        assert t['lang'] == code and len(t['qa']) == 5 and len(t['steps']) == 4 and len(t['exits']) == 3, code
        os.makedirs(os.path.join(ROOT, code), exist_ok=True)
        open(os.path.join(ROOT, code, 'index.html'), 'w', encoding='utf-8').write(page(code, t, css))
        print(code + '/index.html written')


if __name__ == '__main__':
    main()
