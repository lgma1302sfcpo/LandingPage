"""Monta pesquisa/hamburguerias-<data>.json a partir dos registros VERIFICADOS em
pesquisa/hamburguerias-<data>-verificado.py (lista VERIFICADOS de dicts).

Calcula a pontuação (0–100) com critérios fixos, escreve as 3 mensagens com pequenas
variações (para não soarem como disparo automático) e monta o bloco "site" de cada demo.
Nada é inventado: textos do site só usam campos que vieram do Google/Instagram.

Uso:  python animados/scripts/montar_hamburguerias.py 2026-11-24
"""
import hashlib
import importlib.util
import json
import re
import sys
import unicodedata
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
BASE_URL = 'https://landing-page-nine-taupe-20.vercel.app'
FONTES = {'cartoon': 'Bangers', 'pesada': 'Anton', 'condensada': 'Bebas Neue', 'redonda': 'Luckiest Guy'}


def slugify(s):
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode()
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')


def var(slug, opcoes):
    """Escolhe uma variação fixa por casa (mesma casa = mesmo texto sempre)."""
    return opcoes[int(hashlib.md5(slug.encode()).hexdigest(), 16) % len(opcoes)]


# ---------------- pontuação (0–100) ----------------
def pontuar(v, hoje):
    p = {}
    # 1. ausência de site profissional (20)
    p['site'] = {'nenhum': 20, 'instagram': 20, 'facebook': 19, 'cardapio': 17, 'linktree': 16, 'canva': 13}[v['tipoSite']]
    # 2. frequência de publicações (15) — posts nos últimos 30 dias (todas já postaram nos últimos 30 dias)
    dias = (hoje - date.fromisoformat(v['ultimoPost'])).days
    pm = v.get('postsMes', 0)
    p['posts'] = 15 if pm >= 8 else 13 if pm >= 5 else 10 if pm >= 3 else 7 if pm == 2 else 4
    # 3. qualidade das avaliações (15)
    n, r = v['avaliacoes'], v['nota']
    p['google'] = round(min(15, (r - 4.0) / 1.0 * 9 + (6 if n >= 200 else 5 if n >= 100 else 4 if n >= 50 else 2)))
    # 4. seguidores (10) — conta pequena mas viva converte melhor; muito pequena = menos verba
    f = v['seguidores']
    p['seguidores'] = 10 if 1000 <= f < 4000 else 8 if 500 <= f < 1000 else 5
    # 5. facilidade de contato (10)
    p['contato'] = 10 if v.get('whatsapp') and v.get('whatsappFonte', '').startswith('bio') else 8 if v.get('linkWhatsapp') else 6 if v.get('telefoneGoogle', '').replace(' ', '')[4:5] == '9' else 4
    # 6. identidade visual (10) — avaliação visual do perfil (logo, cores, fotos)
    p['visual'] = v['visual']
    # 7. potencial de crescimento (10) e 8. uso comercial de um site próprio (10): avaliação qualitativa
    p['crescimento'] = v['crescimento']
    p['usoSite'] = v['usoSite']
    total = sum(p.values())
    return max(0, min(100, total)), p, dias


# ---------------- mensagens ----------------
def mensagens(slug, nome, nota):
    ola = var(slug, ['Oi, tudo bem?', 'Olá, tudo bem?', 'Oi! Tudo certo por aí?', 'Olá! Tudo bem?'])
    m1 = var(slug + '1', [
        f'{ola} Sou desenvolvedor de sites e conheci a {nome} pelo Instagram. Acabei montando uma demonstração de site personalizada para vocês, com a nota e algumas avaliações do Google. Posso te enviar para vocês conhecerem?',
        f'{ola} Trabalho criando sites e encontrei a {nome} aqui no Instagram. Montei uma demonstração de como ficaria um site próprio de vocês, já com endereço, horário e as avaliações do Google. Quer que eu te mande para dar uma olhada?',
        f'{ola} Sou desenvolvedor de sites e vi a {nome} pelo Instagram. Fiz uma demonstração de site pensada para a hamburgueria de vocês, incluindo a nota {nota} e avaliações reais do Google. Posso te mandar o link para vocês verem?',
    ])
    m2 = var(slug + '2', [
        f'Que bom! Aqui está: {BASE_URL}/{slug}/\n\nÉ só uma demonstração, ainda não oficial: as fotos e o cardápio aparecem como espaços reservados, e no site de verdade entram as fotos e os itens de vocês. Abre no celular, que fica bem legal. Depois me conta o que achou?',
        f'Opa, segue o link: {BASE_URL}/{slug}/\n\nÉ uma prévia não oficial, feita só para vocês verem a ideia. Onde está "Sua foto aqui" entram as fotos reais, e o cardápio também é montado com os itens e preços de vocês. Se gostar, te explico como funciona sem compromisso.',
        f'Claro! Está aqui: {BASE_URL}/{slug}/\n\nÉ uma demonstração (não é um site oficial ainda): as imagens e o cardápio estão como exemplo, e o resto já usa as informações públicas de vocês no Google. Dá uma olhada com calma e me fala o que achou.',
    ])
    m3 = var(slug + '3', [
        f'Oi, tudo bem? Passando só para saber se você chegou a ver minha mensagem sobre a demonstração de site da {nome}. Se não for o momento, sem problema nenhum. Fico à disposição.',
        f'Olá! Só retomando a mensagem sobre a demonstração de site que preparei para a {nome}. Se tiver interesse em ver, é só me avisar por aqui. Se não, tudo certo também.',
        f'Oi! Não quero incomodar, só confirmando se a mensagem sobre o site da {nome} chegou. Se quiserem ver a demonstração em algum momento, é só chamar.',
    ])
    url = f'{BASE_URL}/{slug}/'
    m4 = var(slug + '4', [
        f'{ola} Sou desenvolvedor de sites e conheci a {nome} pelo Instagram. Montei uma demonstração de como ficaria um site próprio de vocês, já com endereço, horário e as avaliações do Google:\n\n{url}\n\nÉ só uma prévia, não oficial: as fotos e o cardápio estão como exemplo, e no site de verdade entram as fotos e os itens de vocês. Abre no celular e depois me conta o que achou?',
        f'{ola} Trabalho criando sites e encontrei a {nome} aqui no Instagram. Fiz uma demonstração de site personalizada para a hamburgueria, com a nota {nota} e avaliações reais do Google. Dá uma olhada:\n\n{url}\n\nÉ uma prévia não oficial: onde aparecem fotos e cardápio de exemplo entram os de vocês. Se gostar, te explico como funciona, sem compromisso.',
        f'{ola} Sou desenvolvedor de sites e vi a {nome} pelo Instagram. Acabei montando uma demonstração de site para vocês, com endereço, horário e as avaliações do Google. Segue o link:\n\n{url}\n\nÉ só uma demonstração (ainda não é um site oficial): as fotos e o cardápio são exemplos. Me fala o que achou?',
    ])
    return m1, m2, m3, m4


# ---------------- bloco do site ----------------
DIAS = ['dom', 'seg', 'ter', 'qua', 'qui', 'sex', 'sab']


def site(v, slug, hoje):
    curto = v.get('nomeCurto', v['nome'])
    # largura média de letra por fonte (em em): o nome gigante precisa caber em ~90% da tela
    largura = {'cartoon': 0.55, 'redonda': 0.70, 'pesada': 0.45, 'condensada': 0.40}[v.get('fonte', 'cartoon')]
    # Anton/Bebas são mais altas que Bangers: teto menor para não encostar no subtítulo
    teto = {'cartoon': 17.5, 'redonda': 15.5, 'pesada': 13.5, 'condensada': 14.5}[v.get('fonte', 'cartoon')]
    tamanho = f"{min(teto, round(88 / (len(curto) * largura), 1))}vw"
    if v.get('linkWhatsapp'):
        link, botao = v['linkWhatsapp'], 'Pedir no WhatsApp'
    elif v.get('whatsapp'):
        link, botao = 'https://wa.me/55' + re.sub(r'\D', '', v['whatsapp']), 'Pedir no WhatsApp'
    elif v.get('linkPedido'):
        link, botao = v['linkPedido'], v.get('botaoPedido', 'Ver cardápio online')
    else:
        link, botao = f'https://www.instagram.com/{v["instagram"]}/', 'Chamar no Instagram'
    servicos = v.get('servicos', [])
    textos = {'Refeição no local': ('Pra comer lá', 'Dá pra comer no salão.'),
              'Retirada': ('Retirada', 'Pede e passa pra buscar.'),
              'Entrega': ('Delivery', 'Entrega na sua casa.'),
              'Drive-thru': ('Drive-thru', 'Sem sair do carro.')}
    vant = [{'titulo': textos[s][0], 'texto': textos[s][1]} for s in servicos if s in textos]
    for extra in v.get('vantagensExtras', []):         # só fatos confirmados (bio/Google)
        vant.append(extra)
    bairro = v['bairro']
    hero = f'Nota <b>{v["notaTxt"]} no Google</b>, com {v["avaliacoes"]} avaliações. ' + (
        'Delivery, retirada e salão em ' if {'Entrega', 'Refeição no local'} <= set(servicos) else 'Em ') + f'{bairro}, {v["cidade"]}.'
    return {
        'nome': curto, 'nomeCompleto': v['nome'], 'tamanhoNome': v.get('tamanhoNome', tamanho),
        'slogan': f'Hamburgueria · {bairro}, {v["cidade"]}',
        'fonteTitulo': FONTES[v.get('fonte', 'cartoon')], 'cores': v['cores'],
        'selo': 'Delivery' if 'Entrega' in servicos else '',
        'heroTexto': hero,
        'finalTexto': f'Bateu a fome? <b>{"Chama no WhatsApp." if (v.get("whatsapp") or v.get("linkWhatsapp")) else "Bora pedir."}</b>',
        'linkPedido': link, 'botaoPedido': botao,
        'instagram': v['instagram'], 'linkGoogle': f'https://www.google.com/maps?cid={int(v["cidHex"], 16)}',
        'buscaGoogle': f'{v["nome"]} {v["cidade"]}', 'textoPino': v.get('pino', curto[:10]),
        'nota': v['notaTxt'], 'avaliacoes': v['avaliacoes'],
        'convite': 'Já provou? Deixa a sua nota no Google.',
        'depoimentos': v['depoimentos'],
        'endereco': {'linha': v['enderecoLinha'], 'sub': f'{bairro}, {v["cidade"]} ({v["uf"]})', 'lat': v['lat'], 'lng': v['lng']},
        'horario': v['horario'], 'vantagens': vant,
        'verificadoEm': hoje.strftime('%d/%m/%Y'),
        'secoes': {'destaques': 'Destaques', 'cardapio': 'Cardápio', 'casa': 'Onde fica', 'casaCurto': 'Onde fica'},
    }


def main(tag):
    hoje = date.fromisoformat(tag)
    fonte = RAIZ / 'pesquisa' / f'hamburguerias-{tag}-verificado.py'
    spec = importlib.util.spec_from_file_location('verif', fonte)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    leads = []
    for v in mod.VERIFICADOS:
        slug = v.get('slug') or slugify(v['nome'])
        total, partes, dias = pontuar(v, hoje)
        m1, m2, m3, m4 = mensagens(slug, v['nome'], v['notaTxt'])
        leads.append({'slug': slug, 'site': site(v, slug, hoje), 'prospeccao': {
            'pontuacao': total, 'partesPontuacao': partes,
            'cidadeUF': f'{v["cidade"]}/{v["uf"]}', 'seguidores': v['seguidores'],
            'ultimaPublicacao': date.fromisoformat(v['ultimoPost']).strftime('%d/%m/%Y') + f' ({dias} dias)',
            'whatsapp': v.get('whatsapp', '') or (v.get('linkWhatsapp', '') and 'link na bio (sem número)'),
            'fonteWhatsapp': v.get('whatsappFonte', ''), 'telefoneGoogle': v.get('telefoneGoogle', ''),
            'siteAtual': v.get('siteAtual', ''), 'justificativa': v['justificativa'],
            'limitacoes': v.get('limitacoes', ''),
            'mensagemInicial': m1, 'mensagemLink': m2, 'mensagemAcompanhamento': m3, 'mensagemCompleta': m4, 'status': 'Não contatado'}})
    leads.sort(key=lambda L: -L['prospeccao']['pontuacao'])
    destino = RAIZ / 'pesquisa' / f'hamburguerias-{tag}.json'
    destino.write_text(json.dumps({'geradoEm': tag, 'leads': leads}, ensure_ascii=False, indent=1), encoding='utf-8')
    print(f'{len(leads)} leads -> {destino}')


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else date.today().isoformat())
