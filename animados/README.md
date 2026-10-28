# Sites animados (estilo Pitombas)

Landing pages de **uma página só**, com animação ligada à rolagem, inspiradas em
[pitombas.com.br](https://pitombas.com.br/). Feitas para comércio local com foto de produto
(hamburgueria, pizzaria, açaí, confeitaria, cafeteria…).

Primeiro cliente: **Uncle Black Burger** (Santos), em `clientes/uncle-black-burger/`.

```
animados/
├── README.md               ← este passo a passo
├── modelo/
│   ├── index.html          ← o LAYOUT (não muda entre clientes)
│   └── dados.js            ← exemplo comentado (Uncle Black)
├── scripts/
│   └── novo-cliente.py     ← cria a pasta do cliente + rota na Vercel
└── clientes/
    └── <slug>/
        ├── index.html      ← cópia do modelo (com título/descrição do cliente)
        └── dados.js        ← SÓ ISSO muda: nome, cores, fonte, fotos, cardápio, avaliações…
```

## Como funciona (a "biblioteca")

Não tem framework nem build. É HTML + CSS + JS puro, com 5 bibliotecas carregadas por CDN:

| Biblioteca | Para quê |
|---|---|
| **GSAP 3.13 + ScrollTrigger** | Todas as animações. `pin` trava a seção na tela e `scrub` faz a animação andar junto com a rolagem |
| **Lenis 1.1** | Rolagem suave |
| **Matter.js 0.20** | Física do final (fotos caem e quicam em cima do nome) |
| **Leaflet 1.9** | Mapa com o pino da loja (tiles da Esri) |
| Google Fonts | Fonte dos títulos (escolhida no `dados.js`) + Archivo no texto |

### Seções (de cima pra baixo)

1. **Topo:** nome gigante (letras sobem uma a uma), 5 fotos que caem como quadrinhos e abrem em leque ao rolar, carimbos "★ nota no Google" e um selo livre.
2. **Avaliações:** a nota gigante e o contador de avaliações sobe de 0 até o total. Os depoimentos chegam como balões de fala; o último fica grande no centro.
3. **Destaques:** carrossel controlado pela rolagem (4 a 6 itens). O nome troca letra por letra, com preço e etiqueta.
4. **Leque:** 4 itens que se abrem em leque, com efeito 3D ao passar o mouse (bom para sobremesas e bebidas).
5. **Cardápio completo:** no PC, a foto ao lado troca conforme o mouse. Clicar abre um card com foto grande e o botão de pedir.
6. **A casa:** vantagens, endereço, tabela de horário (o dia de hoje fica destacado), mapa e botões de rota e Instagram.
7. **Final:** fotos redondas caem com física em cima do nome. No PC dá para arrastar com o mouse.

O status **"Aberto agora / Abre hoje às…"** é calculado na hora, pelo fuso de São Paulo.

---

## Passo a passo para um cliente novo

### 1. Escolher o comércio (critérios usados)

- **Instagram com mais de 5 mil seguidores** e **post nos últimos 30 dias** (rede ativa).
- **Está no Google Maps** com nota boa (de preferência ≥ 4,7) e várias avaliações.
- **Não tem site próprio.** O link do Google ou da bio é só cardápio (Goomer, iFood, Anota.ai, Saipos, Brendi), Linktree ou WhatsApp. Esse é o argumento de venda.
- Tem **fotos boas dos produtos** (no cardápio online ou no Instagram).

Como pesquisar rápido:
- Google Maps: `https://www.google.com/maps/search/hamburgueria+<cidade>+SP`. Abra cada resultado e veja o botão "Website" para saber se é site próprio ou só cardápio.
- Seguidores: estando logado no Instagram, abra `instagram.com/<@>/`. O topo do perfil mostra posts, seguidores e a bio.
- Data do último post: abra o post mais recente (não o fixado).

### 2. Juntar os dados

| O quê | Onde achar |
|---|---|
| Nota e nº de avaliações | Google Maps |
| 8 a 10 trechos de avaliações 5★ (só o primeiro nome) | Google Maps, aba "Avaliações" |
| Endereço, latitude e longitude | Google Maps (a URL tem `@-23.96,-46.33`) |
| Horário | Bio do Instagram **e** Google; se divergirem, avise o usuário |
| Cardápio, preços, fotos | Cardápio online (Goomer etc.) |
| Diferenciais (pet friendly, fidelidade, decoração…) | Bio, destaques do Instagram, avaliações |

**Atalho do Goomer:** se o cardápio for `https://<slug>.goomer.app`, o script já baixa o cardápio inteiro com fotos, o endereço e o horário (veja o passo 3).

> Fotos do Goomer (`images.abrahao.com.br`) **não baixam** por curl (dá 403). Elas funcionam no
> navegador, então a página usa as fotos direto de lá, graças ao `<meta name="referrer" content="no-referrer">`.
> Por causa dessa meta, o mapa **tem** que usar tiles da Esri (CARTO e OSM exigem referer).
> Se o cliente fechar, peça as fotos originais e coloque numa pasta `fotos/` do cliente.

### 3. Criar a pasta

Na raiz do repositório (`landing-pages-clientes`):

```bash
# com cardápio do Goomer (já preenche cardápio, fotos, endereço e horário)
python animados/scripts/novo-cliente.py nome-do-cliente --goomer slugdogoomer \
  --titulo "Nome · Hamburgueria em Bairro, Cidade" \
  --descricao "Frase pro Google com nota, bairro e o que vende."

# sem Goomer (copia o exemplo da Uncle Black para você trocar tudo)
python animados/scripts/novo-cliente.py nome-do-cliente --titulo "..." --descricao "..."
```

O script também adiciona a rota `/nome-do-cliente` no `vercel.json`.

### 4. Editar o `dados.js`

Abra `clientes/<slug>/dados.js` e troque tudo que estiver marcado `PREENCHER`. O `modelo/dados.js` explica cada campo. O que mais importa:

- **`nome`**: curto, 1 a 2 palavras. Se passar da tela, diminua **`tamanhoNome`** (ex.: `'13vw'`).
- **`cores`**: 4 cores. `destaque` (fundo do topo), `escuro` (contornos e fundos escuros), `contraste` (seção de destaques e botão principal), `claro` (letras e cartões). Dica: tire as cores do logo ou da fachada.
- **`fonteTitulo`**: qualquer fonte do Google Fonts. Combinações que funcionam:
  - hamburgueria/cartoon: `Bangers`, `Luckiest Guy`
  - mais séria/urbana: `Anton`, `Bebas Neue`
  - doce/confeitaria: `Fredoka`, `Chewy`
- **`cardapio`**: o gerado do Goomer traz **tudo**, inclusive bebidas, refil, molho extra e loja. Apague o que não vende o lugar e deixe as categorias com foto boa.
- **`hero`** (5), **`destaques`** (4 a 6), **`leque`** (exatamente 4) e **`queda`** (até 12): os nomes precisam ser **iguais** aos do cardápio. O script chuta os primeiros com foto, então **escolha as melhores fotos de verdade**. Fotos em pé (retrato) ficam melhores nos quadros.
- **`depoimentos`**: trechos reais e curtos. O último fica gigante, então use o mais forte e mais curto.

### 5. Testar no navegador

```bash
cd animados && python -m http.server 8765
# abra http://localhost:8765/clientes/<slug>/
```

Role a página inteira. Confira o topo (o nome cabe?), os balões, o carrossel, o mapa e o final com física.
Teste também no celular (F12 → modo dispositivo).

### 6. Publicar

Igual às outras landing pages: commit **só** da pasta do cliente e do `vercel.json`, e depois `git push origin main`.
A Vercel publica em `https://landing-page-nine-taupe-20.vercel.app/<slug>/` (com a barra no final).

### Regras das amostras de prospecção

- **Não colocar logo nem telefone** antes do cliente aprovar. O nome aparece só como tipografia, e os botões levam ao cardápio online e ao Instagram.
- Só usar o que o Google, o Instagram e o cardápio confirmam. Nada inventado.

---

## Mexer no layout (vale para todos)

Melhorias de layout vão no `modelo/index.html`. Para levar a melhoria a um cliente que já existe:

```bash
python animados/scripts/novo-cliente.py <slug> --atualizar   # recopia o index.html, mantém o dados.js
```

### Armadilhas que já aconteceram

- **Animação travada no meio:** a animação de entrada (`gsap.from`) e a da rolagem (`scrollTrigger` com `scrub`) **não podem mexer no mesmo elemento**. No modelo, a rolagem anima só os contêineres (`#mega`, `#h-sub`, `.h-foot`, os wrappers dos quadros), com `fromTo` e `immediateRender:false`. A entrada anima as letras (`.ch`) e os `.panel`.
- **Mapa cinza escrito "API KEY REQUIRED":** isso é tile do CARTO com no-referrer. Use Esri.
- **Item não aparece:** o nome em `hero`, `destaques`, `leque` ou `queda` está diferente do cardápio. O console do navegador avisa: "Item não está no cardápio".
