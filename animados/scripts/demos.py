"""Demonstrações de site para hamburguerias (prospecção) — UM template, N arquivos de dados.

Fonte única de verdade: pesquisa/hamburguerias-<data>.json (privado, não vai para a Vercel).
Este script lê esse JSON e gera:

  animados/demos/dados/<slug>.js      só os dados PÚBLICOS de cada casa (nada de nota interna)
  vercel.json                         2 rotas (todas as demos numa regex) + X-Robots-Tag noindex
  pesquisa/hamburguerias-<data>.csv   planilha completa (abre no Excel / Google Sheets)
  mensagens/hamburguerias-<data>.html painel com as 3 mensagens, botão copiar e status (localStorage)

Uso (na raiz de landing-pages-clientes):
  python animados/scripts/demos.py gerar   pesquisa/hamburguerias-2026-11-24.json
  python animados/scripts/demos.py validar pesquisa/hamburguerias-2026-11-24.json
  python animados/scripts/demos.py servir  [porta]     # servidor local com as MESMAS rotas da Vercel

Nada aqui faz deploy, consulta API paga ou envia mensagem.
"""
import csv
import html
import http.server
import json
import re
import socketserver
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]          # landing-pages-clientes
DEMOS = RAIZ / 'animados' / 'demos'
DADOS = DEMOS / 'dados'
VERCEL = RAIZ / 'vercel.json'
BASE_URL = 'https://landing-page-nine-taupe-20.vercel.app'
ROBOTS = 'noindex, nofollow, noarchive, nosnippet'

# campos que vão para o dados.js público (o resto — score, justificativa, mensagens, seguidores — fica só na pesquisa)
PUBLICOS = ['nome', 'nomeCompleto', 'tamanhoNome', 'slogan', 'fonteTitulo', 'cores', 'selo', 'heroTexto',
            'finalTexto', 'linkPedido', 'botaoPedido', 'notaPedido', 'instagram', 'linkGoogle', 'buscaGoogle',
            'textoPino', 'nota', 'avaliacoes', 'convite', 'depoimentos', 'endereco', 'horario', 'vantagens',
            'verificadoEm', 'secoes']


def carregar(caminho):
    d = json.loads(Path(caminho).read_text(encoding='utf-8'))
    return d['leads'] if isinstance(d, dict) else d


def js_dados(lead):
    site = {'demo': True}
    for k in PUBLICOS:
        if k in lead['site']:
            site[k] = lead['site'][k]
    corpo = json.dumps(site, ensure_ascii=False, indent=1)
    return ('// Demonstração NÃO OFICIAL gerada por animados/scripts/demos.py — não edite à mão,\n'
            '// edite a pesquisa JSON e rode "demos.py gerar". Só dados públicos e verificados.\n'
            'window.SITE=' + corpo + ';\n')


def rotas(slugs):
    v = json.loads(VERCEL.read_text(encoding='utf-8'))
    rs = [r for r in v['routes'] if not r.get('dest', '').startswith('/animados/demos/')]
    alvo = '|'.join(sorted(slugs))
    novas = [
        {'src': '/(' + alvo + ')/dados\\.js', 'dest': '/animados/demos/dados/$1.js',
         'headers': {'X-Robots-Tag': ROBOTS, 'Cache-Control': 'public, max-age=600'}},
        {'src': '/(' + alvo + ')/?', 'dest': '/animados/demos/index.html',
         'headers': {'X-Robots-Tag': ROBOTS}},
    ]
    # antes do "pega-tudo" /(.*) -> /clientes/$1
    i = next((k for k, r in enumerate(rs) if r.get('src') == '/(.*)'), len(rs))
    rs[i:i] = novas
    v['routes'] = rs
    VERCEL.write_text(json.dumps(v, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def link_demo(slug):
    return f'{BASE_URL}/{slug}/'


TEM_LINK = re.compile(r'https?://|www\.|\.com|\.app|vercel', re.I)


def validar(leads, verboso=True):
    erros = []
    slugs = set()
    v = json.loads(VERCEL.read_text(encoding='utf-8'))
    existentes = {r['src'].strip('/').split('/')[0] for r in v['routes']
                  if not r.get('dest', '').startswith('/animados/demos/')}
    for L in leads:
        s, site, p = L['slug'], L['site'], L['prospeccao']
        e = lambda m: erros.append(f'{s}: {m}')
        if not re.fullmatch(r'[a-z0-9]+(-[a-z0-9]+)*', s): e('slug inválido')
        if s in slugs: e('slug repetido')
        if s in existentes: e('slug já usado por outra página do projeto')
        slugs.add(s)
        for k in ['nome', 'nomeCompleto', 'instagram', 'nota', 'avaliacoes', 'linkGoogle', 'endereco',
                  'horario', 'depoimentos', 'verificadoEm', 'cores', 'linkPedido']:
            if k not in site or site[k] in (None, '', []): e(f'falta {k}')
        if len(site.get('horario', [])) != 7: e('horario precisa de 7 dias')
        for r in site.get('depoimentos', []):
            if not r.get('texto') or not r.get('autor'): e('depoimento sem texto/autor')
            if ' ' in r.get('autor', '').strip(): e(f'autor com sobrenome: {r["autor"]}')
        for k in ['mensagemInicial', 'mensagemLink', 'mensagemAcompanhamento']:
            if not p.get(k): e(f'falta {k}')
        if TEM_LINK.search(p.get('mensagemInicial', '')): e('mensagem inicial contém link')
        if TEM_LINK.search(p.get('mensagemAcompanhamento', '')): e('mensagem de acompanhamento contém link')
        if link_demo(s) not in p.get('mensagemLink', ''): e('mensagem do link não tem o link exclusivo')
        if site.get('nomeCompleto', '') and site['nomeCompleto'].split()[0].lower() not in p.get('mensagemInicial', '').lower():
            e('mensagem inicial não cita o nome')
        if 'cardapio' in site: e('demo não deve ter cardápio (seria inventado)')
    if verboso:
        print('OK' if not erros else '\n'.join(erros))
    return erros


def gerar(caminho):
    leads = carregar(caminho)
    if validar(leads, verboso=False):
        validar(leads)
        sys.exit('Corrija os erros antes de gerar.')
    DADOS.mkdir(parents=True, exist_ok=True)
    for f in DADOS.glob('*.js'):
        f.unlink()
    for L in leads:
        (DADOS / f"{L['slug']}.js").write_text(js_dados(L), encoding='utf-8')
    rotas([L['slug'] for L in leads])
    base = Path(caminho).with_suffix('')
    tag = base.name                                  # hamburguerias-2026-11-24
    planilha(leads, RAIZ / 'pesquisa' / f'{tag}.csv')
    painel(leads, RAIZ / 'mensagens' / f'{tag}.html', tag)
    print(f'{len(leads)} demos geradas em {DADOS}')
    print(f'rotas atualizadas em {VERCEL.name}; planilha e painel: pesquisa/{tag}.csv, mensagens/{tag}.html')


COLUNAS = ['Pontuação', 'Hamburgueria', 'Cidade/UF', 'Instagram', 'Seguidores', 'Última publicação',
           'WhatsApp comercial', 'Fonte do WhatsApp', 'Telefone no Google', 'Google Maps', 'Nota Google', 'Avaliações', 'Site atual',
           'Demonstração', 'Justificativa', 'Mensagem inicial (sem link)', 'Mensagem com link',
           'Mensagem de acompanhamento', 'Status', 'Verificado em', 'Observações/limitações']


def linha(L):
    s, p = L['site'], L['prospeccao']
    return [p['pontuacao'], s['nomeCompleto'], p['cidadeUF'], '@' + s['instagram'], p['seguidores'],
            p['ultimaPublicacao'], p.get('whatsapp') or 'não confirmado', p.get('fonteWhatsapp', ''), p.get('telefoneGoogle', ''),
            s['linkGoogle'], s['nota'], s['avaliacoes'], p.get('siteAtual') or 'nenhum',
            link_demo(L['slug']), p['justificativa'], p['mensagemInicial'], p['mensagemLink'],
            p['mensagemAcompanhamento'], p.get('status', 'Não contatado'), s['verificadoEm'],
            p.get('limitacoes', '')]


def planilha(leads, destino):
    with open(destino, 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.writer(f, delimiter=';')
        w.writerow(COLUNAS)
        for L in sorted(leads, key=lambda x: -x['prospeccao']['pontuacao']):
            w.writerow(linha(L))


def painel(leads, destino, tag):
    leads = sorted(leads, key=lambda x: -x['prospeccao']['pontuacao'])
    cards = []
    for i, L in enumerate(leads, 1):
        s, p = L['site'], L['prospeccao']
        msgs = ''.join(
            f'<div class="m"><h4>{t}</h4><pre>{html.escape(p[k])}</pre><button data-k="{L["slug"]}:{k}">Copiar</button></div>'
            for t, k in [('1 · Primeiro contato (sem link)', 'mensagemInicial'), ('2 · Se responder com interesse', 'mensagemLink'),
                         ('3 · Acompanhamento (sem resposta)', 'mensagemAcompanhamento')])
        top = '<span class="top">TOP 10</span>' if i <= 10 else ''
        wa = p.get('whatsapp')
        wa_html = (f'<a href="https://wa.me/55{re.sub(r"[^0-9]", "", wa)}" target="_blank" rel="noopener">WhatsApp {html.escape(wa)}</a>' if wa and wa[0] == '('
                   else f'<a href="{html.escape(L["site"]["linkPedido"])}" target="_blank" rel="noopener">WhatsApp (link da bio)</a>' if wa
                   else f'<span class="mut">WhatsApp não confirmado · tel. Google {html.escape(p.get("telefoneGoogle", ""))}</span>')
        cards.append(f'''<article class="c" id="{L["slug"]}">
<header><b class="sc">{p["pontuacao"]}</b><div><h3>{i}. {html.escape(s["nomeCompleto"])} {top}</h3>
<p>{html.escape(p["cidadeUF"])} · @{html.escape(s["instagram"])} · {p["seguidores"]} seguidores · último post {html.escape(p["ultimaPublicacao"])} · ★ {s["nota"]} ({s["avaliacoes"]})</p></div>
<select data-s="{L["slug"]}"><option>Não contatado</option><option>Msg 1 enviada</option><option>Respondeu</option><option>Link enviado</option><option>Acompanhamento enviado</option><option>Negociando</option><option>Fechou</option><option>Sem interesse</option></select></header>
<p class="lk"><a href="https://www.instagram.com/{s["instagram"]}/" target="_blank" rel="noopener">Instagram</a> · {wa_html} · <a href="{html.escape(s["linkGoogle"])}" target="_blank" rel="noopener">Google Maps</a> · <a href="/{L["slug"]}/" target="_blank">demo local</a> · <code>{link_demo(L["slug"])}</code></p>
<p class="j">{html.escape(p["justificativa"])}</p>
{('<p class="lim">⚠ ' + html.escape(p["limitacoes"]) + '</p>') if p.get("limitacoes") else ''}
<div class="ms">{msgs}</div></article>''')
    doc = f'''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow"><title>Prospecção hamburguerias · {tag}</title><style>
body{{font:15px/1.45 system-ui,sans-serif;margin:0;background:#f4f1ea;color:#1b1b1b}}main{{max-width:1100px;margin:0 auto;padding:24px 16px 80px}}
h1{{font-size:26px;margin:0 0 4px}}.sub{{color:#555;margin:0 0 20px}}.c{{background:#fff;border:1px solid #ddd;border-radius:12px;padding:16px;margin:0 0 16px}}
.c header{{display:flex;gap:14px;align-items:flex-start}}.c header div{{flex:1}}.sc{{font-size:24px;background:#1b1b1b;color:#ffc719;border-radius:10px;padding:8px 10px;min-width:56px;text-align:center}}
h3{{margin:0;font-size:18px}}.c header p{{margin:2px 0 0;color:#555;font-size:13px}}.top{{background:#e8352a;color:#fff;font-size:11px;padding:2px 6px;border-radius:4px;vertical-align:middle}}
.lk{{font-size:13px}}.lk code{{font-size:12px;color:#555}}.j{{margin:6px 0}}.lim{{font-size:13px;color:#8a5a00;background:#fff6dc;padding:6px 8px;border-radius:6px}}.mut{{color:#888}}
.ms{{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}}.m{{border:1px solid #e3e3e3;border-radius:8px;padding:10px;display:flex;flex-direction:column}}
.m h4{{margin:0 0 6px;font-size:12px;text-transform:uppercase;color:#666}}pre{{white-space:pre-wrap;font:14px/1.4 system-ui,sans-serif;margin:0 0 8px;flex:1}}
button{{border:0;background:#1b1b1b;color:#fff;border-radius:6px;padding:8px;cursor:pointer}}button.ok{{background:#e8352a}}select{{padding:6px;border-radius:6px}}
@media(max-width:800px){{.ms{{grid-template-columns:1fr}}}}</style></head><body><main>
<h1>Prospecção · hamburguerias</h1><p class="sub">{len(leads)} demonstrações, da maior para a menor pontuação. Nenhuma mensagem é enviada daqui: copie e envie você mesmo. Status fica salvo neste navegador.</p>
{''.join(cards)}</main><script>
var K='hamburguerias-{tag}';var st=JSON.parse(localStorage.getItem(K)||'{{}}');
document.querySelectorAll('select[data-s]').forEach(function(s){{if(st[s.dataset.s])s.value=st[s.dataset.s];s.onchange=function(){{st[s.dataset.s]=s.value;localStorage.setItem(K,JSON.stringify(st))}}}});
document.querySelectorAll('button[data-k]').forEach(function(b){{if(st['c:'+b.dataset.k])b.classList.add('ok');b.onclick=function(){{navigator.clipboard.writeText(b.previousElementSibling.textContent);b.classList.add('ok');b.textContent='Copiado';st['c:'+b.dataset.k]=1;localStorage.setItem(K,JSON.stringify(st))}}}});
</script></body></html>'''
    destino.write_text(doc, encoding='utf-8')


def servir(porta=8790):
    """Servidor local que imita as rotas da Vercel: /<slug>/ -> template, /<slug>/dados.js -> dados/<slug>.js."""
    class H(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **k):
            super().__init__(*a, directory=str(RAIZ), **k)

        def end_headers(self):
            self.send_header('X-Robots-Tag', ROBOTS)
            self.send_header('Cache-Control', 'no-store')
            super().end_headers()

        def translate_path(self, path):
            p = path.split('?')[0]
            partes = [x for x in p.split('/') if x]
            if partes and (DADOS / f'{partes[0]}.js').exists():
                if len(partes) == 2 and partes[1] == 'dados.js':
                    return str(DADOS / f'{partes[0]}.js')
                if len(partes) == 1:
                    return str(DEMOS / 'index.html')
            if len(partes) == 1 and partes[0].startswith('hamburguerias-') and partes[0].endswith('.html'):
                return str(RAIZ / 'mensagens' / partes[0])
            return super().translate_path(path)

    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.ThreadingTCPServer(('127.0.0.1', porta), H) as srv:
        print(f'http://localhost:{porta}/<slug>/   (Ctrl+C para parar)')
        srv.serve_forever()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    cmd = sys.argv[1]
    if cmd == 'gerar':
        gerar(sys.argv[2])
    elif cmd == 'validar':
        sys.exit(1 if validar(carregar(sys.argv[2])) else 0)
    elif cmd == 'servir':
        servir(int(sys.argv[2]) if len(sys.argv) > 2 else 8790)
    else:
        sys.exit(__doc__)
