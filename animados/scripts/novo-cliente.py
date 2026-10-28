"""Cria (ou atualiza) um site animado em animados/clientes/<slug>.

Uso:
  python animados/scripts/novo-cliente.py <slug> --titulo "Nome · Hamburgueria em Cidade" --descricao "..."
  python animados/scripts/novo-cliente.py <slug> --goomer <slug-do-goomer> --titulo ... --descricao ...
  python animados/scripts/novo-cliente.py <slug> --atualizar      # só recopia o modelo/index.html (mantém dados.js)

O que faz:
  1. copia modelo/index.html para clientes/<slug>/index.html, trocando {{TITULO}} e {{DESCRICAO}};
  2. cria clientes/<slug>/dados.js (se ainda não existir):
       - com --goomer: já vem com cardápio, fotos, endereço, horário e link de pedido do Goomer;
       - sem --goomer: copia o exemplo do modelo pra você editar;
  3. registra as rotas /<slug> no vercel.json da raiz.
"""
import argparse
import json
import re
import shutil
import sys
import urllib.request
from pathlib import Path

ANIM = Path(__file__).resolve().parents[1]
ROOT = ANIM.parent
MODELO = ANIM / 'modelo'
UA = {'User-Agent': 'Mozilla/5.0'}
DIAS = {'Dom': 0, 'Seg': 1, 'Ter': 2, 'Qua': 3, 'Qui': 4, 'Sex': 5, 'Sab': 6, 'Sáb': 6}


def get_json(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
        return json.load(r)


def preco(v):
    return 'R$ ' + f'{float(v):.2f}'.replace('.', ',')


def limpa(t):
    t = re.sub(r'\s+', ' ', (t or '').replace('\r', ' ').replace('\n', ' ')).strip()
    return t


def goomer(slug):
    info = get_json(f'https://api-go.goomer.app/v2/establishments/{slug}/info')
    i = info['info']
    store = info['settings']['mm_a_id']
    versao = i['menu'].rstrip('/').split('/')[-1]
    menu = get_json(f'https://ssr-api.goomer.app/v1/abrahao/{store}/menu?menu_version={versao}')

    cardapio = []
    for m in menu['menus']:
        for g in m['groups']:
            itens = []
            for p in g['products']:
                if not p.get('is_available') or not p.get('price') or float(p['price']) < 1:
                    continue  # tira indisponíveis e itens "monte seu combo" de R$ 0,01
                im = (p.get('images') or [{}])[0]
                itens.append({'n': limpa(p['name']), 'p': preco(p['price']), 'd': limpa(p.get('description')),
                              'img': im.get('large', ''), 'thumb': im.get('medium', '')})
            if itens:
                cardapio.append({'cat': limpa(g['name']).title(), 'itens': itens})

    horario = [None] * 7
    ordem = ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sab']
    for h in i.get('hours', []):
        a, b = DIAS.get(h['from'][:3]), DIAS.get(h['to'][:3])
        if a is None or b is None:
            continue
        k = a
        while True:
            horario[k] = [h['open'], h['close']]
            if k == b:
                break
            k = (k + 1) % 7
    return {
        'nome': i['name'],
        'endereco': i.get('address', ''),
        'linkPedido': f'https://{slug}.goomer.app/menu',
        'cardapio': cardapio,
        'horario': horario,
    }


def js(v):
    return json.dumps(v, ensure_ascii=False)


def dados_goomer(g):
    fotos = [it['n'] for c in g['cardapio'] for it in c['itens'] if it['img']]
    linhas = [
        '// Gerado do Goomer. Tudo marcado PREENCHER precisa ser trocado (Instagram, Google Maps, bio).',
        '// Veja o exemplo completo em animados/modelo/dados.js e o passo a passo no animados/README.md.',
        'window.SITE={',
        f"  nome:{js(g['nome'])},",
        "  tamanhoNome:'17.5vw',",
        "  slogan:'PREENCHER · Bairro, Cidade',",
        "  fonteTitulo:'Bangers',",
        "  cores:{destaque:'#ffc719',escuro:'#0d0d0d',contraste:'#e8352a',claro:'#fff6dc'},",
        "  selo:'',",
        "  heroTexto:'PREENCHER: uma frase sobre a casa com <b>o ponto forte</b>.',",
        "  finalTexto:'PREENCHER frase final. <b>Com destaque.</b>',",
        f"  rodape:{js(g['nome'] + ' · ' + g['endereco'] + '. Nota e avaliações do Google em PREENCHER. Fotos do cardápio da casa.')},",
        "  secoes:{destaques:'Os da casa',cardapio:'Cardápio',casa:'Onde fica',casaCurto:'Onde fica'},",
        f"  linkPedido:{js(g['linkPedido'])},",
        "  botaoPedido:'Pedir delivery',",
        "  notaPedido:'Abre o cardápio oficial da casa.',",
        "  instagram:'PREENCHER',",
        f"  buscaGoogle:{js(g['nome'] + ' PREENCHER-CIDADE')},",
        "  textoPino:'Aqui',",
        "  nota:'PREENCHER',",
        '  avaliacoes:0,',
        "  convite:'Já veio aqui? Deixa a sua nota.',",
        "  depoimentos:[{texto:'PREENCHER trecho real 5★',autor:'Nome'}],",
        f"  endereco:{{linha:{js(g['endereco'])},sub:'PREENCHER bairro, cidade',lat:0,lng:0}},",
        f"  horario:{js(g['horario'])},",
        "  vantagens:[{titulo:'PREENCHER',texto:'PREENCHER'}],",
        "  notaCardapio:'Preços do cardápio de delivery da casa.',",
        f"  cardapio:{json.dumps(g['cardapio'], ensure_ascii=False, indent=1)},",
        f"  hero:{js(fotos[:5])},",
        f"  destaques:{js([{'n': n, 'tag': ''} for n in fotos[:6]])},",
        f"  leque:{{titulo:'Pra fechar',sub:'PREENCHER',itens:{js(fotos[-4:])}}},",
        f"  queda:{js(fotos[:12])}",
        '};',
    ]
    return '\n'.join(linhas) + '\n'


def rotas(slug):
    p = ROOT / 'vercel.json'
    d = json.loads(p.read_text(encoding='utf-8'))
    if any(r.get('src') == '/' + slug for r in d['routes']):
        return False
    d['routes'][0:0] = [
        {'src': f'/{slug}', 'dest': f'/animados/clientes/{slug}/index.html'},
        {'src': f'/{slug}/(.*)', 'dest': f'/animados/clientes/{slug}/$1'},
    ]
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('slug')
    ap.add_argument('--titulo', default='')
    ap.add_argument('--descricao', default='')
    ap.add_argument('--goomer', help='slug do Goomer (ex.: uncleblackburger)')
    ap.add_argument('--atualizar', action='store_true', help='só recopia o index.html do modelo')
    a = ap.parse_args()

    dest = ANIM / 'clientes' / a.slug
    dest.mkdir(parents=True, exist_ok=True)
    html_dest = dest / 'index.html'

    titulo, descricao = a.titulo, a.descricao
    if a.atualizar and html_dest.exists():
        # mantém o título e a descrição que o cliente já tinha
        old = html_dest.read_text(encoding='utf-8')
        titulo = titulo or re.search(r'<title>(.*?)</title>', old).group(1)
        descricao = descricao or re.search(r'<meta name="description" content="(.*?)">', old).group(1)
    if not titulo:
        sys.exit('Falta --titulo (ex.: "Nome · Hamburgueria em Bairro, Cidade")')

    html = (MODELO / 'index.html').read_text(encoding='utf-8')
    html = html.replace('{{TITULO}}', titulo).replace('{{DESCRICAO}}', descricao or titulo)
    html_dest.write_text(html, encoding='utf-8')
    print('ok ', html_dest)

    dados = dest / 'dados.js'
    if not dados.exists():
        if a.goomer:
            dados.write_text(dados_goomer(goomer(a.goomer)), encoding='utf-8')
            print('ok ', dados, '(do Goomer; procure PREENCHER)')
        else:
            shutil.copy(MODELO / 'dados.js', dados)
            print('ok ', dados, '(cópia do exemplo; troque tudo)')
    else:
        print('-- ', dados, 'já existe, não mexi')

    if rotas(a.slug):
        print('ok  rota /' + a.slug, 'no vercel.json')


if __name__ == '__main__':
    main()
