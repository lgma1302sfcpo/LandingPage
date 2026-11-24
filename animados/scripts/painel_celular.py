"""Gera mensagens/hamburguerias-<data>-celular.html: painel para o celular com botão que abre
o WhatsApp de cada hamburgueria já com a mensagem escrita (wa.me/<número>?text=...).
Uso: python animados/scripts/painel_celular.py 2026-11-24"""
import json, re, sys
from pathlib import Path
RAIZ = Path(__file__).resolve().parents[2]
tag = sys.argv[1]
leads = json.loads((RAIZ / 'pesquisa' / f'hamburguerias-{tag}.json').read_text(encoding='utf-8'))['leads']
dados = []
for i, L in enumerate(leads, 1):
    s, p = L['site'], L['prospeccao']
    conf = bool(p['whatsapp']) and p['whatsapp'].startswith('(')
    num = p['whatsapp'] if conf else p['telefoneGoogle']
    dig = re.sub(r'\D', '', num)
    dados.append({'r': i, 'slug': L['slug'], 'nome': s['nomeCompleto'], 'cidade': p['cidadeUF'], 'pts': p['pontuacao'],
                  'ig': s['instagram'], 'seg': p['seguidores'], 'nota': s['nota'], 'aval': s['avaliacoes'],
                  'num': num, 'wa': '55' + dig, 'conf': conf, 'fixo': len(dig) == 10,
                  'linkBio': p['whatsapp'] == 'link na bio (sem número)', 'just': p['justificativa'],
                  'm': [p['mensagemInicial'], p['mensagemLink'], p['mensagemAcompanhamento']]})
tpl = (RAIZ / 'animados' / 'scripts' / 'painel_celular.tpl.html').read_text(encoding='utf-8')
out = RAIZ / 'mensagens' / f'hamburguerias-{tag}-celular.html'
out.write_text(tpl.replace('/*DADOS*/[]', json.dumps(dados, ensure_ascii=False)), encoding='utf-8')
print(out, len(dados))
