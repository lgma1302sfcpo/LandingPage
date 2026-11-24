# Demonstrações para prospecção (hamburguerias)

Um **único template** (`index.html`, cópia fiel do `animados/modelo/index.html`) atende todas as
demonstrações. Cada hamburgueria é só um arquivo de dados (`dados/<slug>.js`). Não há build,
banco, API, função serverless nem cron: a Vercel serve arquivos estáticos pelo CDN.

```
animados/demos/
├── index.html          ← template único (layout, animações e fontes do modelo original)
├── dados/<slug>.js     ← GERADO: só dados públicos e verificados de cada casa
└── README.md
pesquisa/hamburguerias-<data>-verificado.py  ← o que foi checado à mão (fonte de verdade)
pesquisa/hamburguerias-<data>.json           ← gerado: lead + site + mensagens + pontuação
pesquisa/hamburguerias-<data>.csv            ← planilha (Excel/Sheets, separador ;)
mensagens/hamburguerias-<data>.html          ← painel com as 3 mensagens, copiar e status
```

## Como as rotas funcionam (custo zero de compute)

`scripts/demos.py gerar` grava **duas** rotas no `vercel.json`, antes do "pega-tudo":

| Pedido | Vai para |
|---|---|
| `/<slug>` ou `/<slug>/` | `animados/demos/index.html` (o mesmo arquivo para todos) |
| `/<slug>/dados.js` | `animados/demos/dados/<slug>.js` |

O template lê o slug do endereço e carrega `/<slug>/dados.js`. Os slugs ficam numa única regex
(`/(slug-a|slug-b|...)/?`), então 30 ou 300 demos continuam sendo 2 rotas. Slug que não está na
lista cai no fluxo normal do projeto (404), não no template.

## O que o modo demonstração muda no layout

Nada no desenho, nas animações, na tipografia ou na ordem das seções. Só:

- `noindex, nofollow, noarchive, nosnippet` na página **e** no cabeçalho `X-Robots-Tag` (rota).
  As demos não entram em sitemap (o projeto não tem sitemap) e não há link para elas em lugar nenhum.
- Selo discreto "Demonstração não oficial" no canto + aviso completo no rodapé.
- Fotos: sem imagem autorizada, cada quadro é uma **ilustração** com "SUA FOTO AQUI".
- Cardápio: sem cardápio confirmado, os itens são espaços reservados ("Seu burger 1", "R$ 00,00").
  Nada de nome de prato, preço ou promoção inventado.
- Avaliações: trechos curtos de avaliações públicas do Google, só o primeiro nome do autor, com
  link "Ler todas no Google" para a ficha da casa e a data da consulta no rodapé.

## Comandos

```bash
python animados/scripts/montar_hamburguerias.py 2026-11-24            # verificado.py -> json
python animados/scripts/demos.py validar pesquisa/hamburguerias-2026-11-24.json
python animados/scripts/demos.py gerar   pesquisa/hamburguerias-2026-11-24.json
python animados/scripts/demos.py servir 8790      # http://localhost:8790/<slug>/
#                                                   painel: http://localhost:8790/hamburguerias-2026-11-24.html
```

Quando um cliente fechar: copie a demo para `animados/clientes/<slug>/` com o
`scripts/novo-cliente.py`, coloque fotos e cardápio reais e tire o `demo:true`.

## noindex não é privado — opções de baixo custo

`noindex` só pede aos buscadores que não listem. Quem tiver o link abre. Se precisar restringir:

1. **Slug com sufixo aleatório** (custo zero, recomendado): `/<nome>-k7q2/`. Ninguém adivinha o
   endereço e o link continua abrindo direto no celular do dono, sem senha.
2. **Senha simples via Vercel Edge Middleware** (Basic Auth): roda só nas rotas de demo e fica no
   plano Hobby, mas adiciona invocações de middleware e um passo a mais para o dono abrir. Use só se
   alguma casa pedir.
3. **Vercel Password Protection / Deployment Protection**: recurso de plano pago. Não recomendado
   para isso.
4. **Tirar do ar** depois de X dias sem resposta: apagar `dados/<slug>.js` + rodar `gerar`.
