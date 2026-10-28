// =====================================================================
//  DADOS DO COMÉRCIO — é só este arquivo que muda de um cliente pro outro
//  (exemplo preenchido: Uncle Black Burger, Santos)
//  Copiar só o que o Google/Instagram/cardápio confirmam. Não inventar.
// =====================================================================
var G='https://images.abrahao.com.br/x900/uploads/6380/product/';   // atalho p/ fotos do Goomer
var T='https://images.abrahao.com.br/x250/uploads/6380/product/';   // mesma foto, versão pequena

window.SITE={
  // ---------- identidade ----------
  nome:'Uncle Black',                       // vai gigante no topo e no final (curto! 1–2 palavras)
  tamanhoNome:'17.5vw',                     // diminua se o nome for longo (ex.: '13vw')
  slogan:'Real burgers only · Gonzaga, Santos',
  fonteTitulo:'Bangers',                    // qualquer fonte do Google Fonts (ex.: 'Anton', 'Bebas Neue', 'Luckiest Guy')
  cores:{
    destaque:'#ffc719',   // fundo do topo e da seção "a casa", preços
    escuro:'#0d0d0d',     // contornos, avaliações, cardápio
    contraste:'#e8352a',  // seção de destaques, botão principal
    claro:'#fff6dc'       // letras do nome, cartões, balões
  },
  selo:'Pet friendly!',                     // 2º carimbo do topo ('' para esconder)
  heroTexto:'Burgers de 160 g com nome de desenho, milkshakes e um deck com quintal na <b>Praça Fernandes Pacheco</b>.',
  finalTexto:'Imagine você + um burger do tio. <b>Vai dar match.</b>',
  rodape:'Uncle Black Burger · Praça Fernandes Pacheco, 23, Gonzaga, Santos (SP). Nota e avaliações do Google em outubro de 2026. Fotos do cardápio da casa.',

  // ---------- títulos das seções ----------
  secoes:{destaques:'Os do tio',cardapio:'Cardápio',casa:'A casinha do tio',casaCurto:'A casinha'},

  // ---------- links ----------
  linkPedido:'https://uncleblackburger.goomer.app/menu',   // cardápio online / iFood / WhatsApp
  botaoPedido:'Pedir delivery',
  notaPedido:'Abre o cardápio oficial da casa.',
  instagram:'uncleblackburger',
  buscaGoogle:'Uncle Black Burger Santos',  // usado nos links "ler/avaliar no Google" e "traçar rota"
  textoPino:'Casa do<br>tio',               // texto da bolinha no mapa

  // ---------- Google ----------
  nota:'4,9',
  avaliacoes:643,
  convite:'Comeu na casinha do tio? Deixa a sua nota.',
  // 8 a 10 trechos curtos de avaliações reais 5★; só o primeiro nome; o ÚLTIMO fica gigante no centro
  depoimentos:[
    {texto:'Hambúrgueres diferentes do padrão ‘pão, carne e queijo’ que vemos por aí, e a carne sempre suculenta.',autor:'Nicole'},
    {texto:'Excelente experiência gastronômica. Local aconchegante e limpo.',autor:'Murilo'},
    {texto:'…decoração inspirada em desenhos e seriados infantis que traz uma sensação gostosa de nostalgia.',autor:'André'},
    {texto:'Estávamos em cinco pessoas e todas foram muito bem atendidas.',autor:'Penélope'},
    {texto:'Tem o melhor cheesecake de ninho com nutella.',autor:'Tielle'},
    {texto:'Que hamburgueria maravilhosa, simplesmente sensacional!',autor:'Gabriely'},
    {texto:'A melhor parte do pós-expediente!',autor:'Lucas'},
    {texto:'Espaço excelente! Hambúrguer maravilhoso! Super recomendo!',autor:'Paula'},
    {texto:'Lugar incrível, perfeito para encontrar os amigos ou marcar um date.',autor:'Mariana'},
    {texto:'Virou meu lugar preferido!',autor:'Fernanda'}
  ],

  // ---------- endereço e horário ----------
  endereco:{linha:'Praça Fernandes Pacheco, 23',sub:'Gonzaga, Santos · CEP 11060-410',lat:-23.9644365,lng:-46.3349164},
  // índice 0 = domingo ... 6 = sábado; null = fechado; fechar '00:00' = meia-noite
  horario:[['19:00','00:00'],['19:00','00:00'],['19:00','00:00'],['19:00','00:00'],['19:00','00:00'],['19:00','00:00'],['19:00','00:00']],
  vantagens:[
    {titulo:'Deck e quintal pet friendly',texto:'Pode levar o cachorro. Tem espaço pra ele também.'},
    {titulo:'Decoração de desenho',texto:'Paredes e cantos inspirados nos desenhos e seriados que a gente via na TV.'},
    {titulo:'Programa de fidelidade',texto:'A cada 10 pedidos de pelo menos R$ 55 no delivery, um cupom de R$ 20.'}
  ],

  // ---------- cardápio completo ----------
  // n = nome, p = preço, d = descrição, img = foto grande (retrato fica melhor), thumb = foto pequena (opcional)
  // selo = etiqueta vermelha opcional (ex.: 'Apimentado', 'Novo'); curto = nome menor no leque (opcional)
  notaCardapio:'Preços do cardápio de delivery da casa. O ponto padrão dos burgers é avermelhado; dá pra pedir do seu jeito.',
  cardapio:[
    {cat:'Burgers',nota:'blend de 160 g',itens:[
      {n:'Especial de Outubro',p:'R$ 56,90',d:'Pão brioche pincelado com caramelo, blend de 160 g, mozarela, abacaxi grelhado e geleia de bacon com abacaxi e hortelã.',img:G+'1242959/assets/images/1601540.jpg?v=1790877482',thumb:T+'1242959/assets/images/1601540.jpg?v=1790877482'},
      {n:'Taz Mania',p:'R$ 52,90',d:'Pão brioche, blend de 160 g, molho de gorgonzola, geleia de pimenta, bacon triturado e jalapeño.',img:G+'1392821/assets/images/1311887.jpeg?v=1770192860',thumb:T+'1392821/assets/images/1311887.jpeg?v=1770192860',selo:'Apimentado'},
      {n:"How You Doin'",p:'R$ 53,90',d:'Pão brioche, dois blends de 100 g, molho de queijos e bacon em tiras.',img:G+'988005/assets/images/918303.jpg?v=1744844959',thumb:T+'988005/assets/images/918303.jpg?v=1744844959'},
      {n:'Pink Phink',p:'R$ 47,90',d:'Pão australiano, blend de 160 g, cheddar cremoso, cebola caramelizada e bacon em tira.',img:G+'988007/assets/images/918281.jpg?v=1744844767',thumb:T+'988007/assets/images/918281.jpg?v=1744844767'},
      {n:'Van Helsing',p:'R$ 45,90',d:'Pão brioche, blend de 160 g, gouda, crispy de cebola, picles e molho de alho.',img:G+'988008/assets/images/918256.jpg?v=1744844270',thumb:T+'988008/assets/images/918256.jpg?v=1744844270'},
      {n:"Ronaldo's Classic",p:'R$ 44,90',d:'Pão brioche, blend de 160 g, mozarela, maionese verde, bacon em tira, alface e tomate.',img:G+'988006/assets/images/918283.jpg?v=1744844793',thumb:T+'988006/assets/images/918283.jpg?v=1744844793'},
      {n:'Hakuna Matata',p:'R$ 44,90',d:'Pão brioche, blend de 160 g, queijo brie, rúcula e geleia de laranja.',img:G+'988009/assets/images/918286.jpg?v=1744844824',thumb:T+'988009/assets/images/918286.jpg?v=1744844824'},
      {n:'Mr. Burns',p:'R$ 43,90',d:'Pão australiano, blend de 160 g, rúcula, barbecue levemente apimentado, alho-poró crispy e mozarela.',img:G+'988010/assets/images/918255.jpg?v=1744844261',thumb:T+'988010/assets/images/918255.jpg?v=1744844261'},
      {n:'Zé Colmeia',p:'R$ 42,90',d:'Pão brioche, blend de 160 g, provolone, bacon em tira e mel.',img:G+'988011/assets/images/918268.jpg?v=1744844414',thumb:T+'988011/assets/images/918268.jpg?v=1744844414'},
      {n:'Cheeseburger',p:'R$ 31,90',d:'Pão brioche, blend de 100 g e mozarela.',img:G+'988013/assets/images/1204648.jpg?v=1763506910',thumb:T+'988013/assets/images/1204648.jpg?v=1763506910'}
    ]},
    {cat:'Lanches',itens:[
      {n:"Frajola's",p:'R$ 42,90',d:'Pão de forma artesanal, 135 g de frango empanado, mozarela, parmesão, molho de tomate picante e alface.',img:G+'988014/assets/images/918248.jpg?v=1744844176',thumb:T+'988014/assets/images/918248.jpg?v=1744844176'},
      {n:'Spider Pig',p:'R$ 43,90',d:'Pão francês redondo, 180 g de linguiça toscana, coalho, mozarela, maionese verde e pico de gallo.',img:G+'988015/assets/images/918282.jpg?v=1744844785',thumb:T+'988015/assets/images/918282.jpg?v=1744844785',selo:'Apimentado'}
    ]},
    {cat:'Appetizers',itens:[
      {n:'Fries Cheddar e Bacon',p:'R$ 40,90',d:'Batata palito com muito cheddar cremoso e bacon crocante triturado.',img:G+'987990/assets/images/1173076.jpg?v=1761631113',thumb:T+'987990/assets/images/1173076.jpg?v=1761631113'},
      {n:'Fries Tradicional',p:'R$ 29,90',d:'Batata palito com molho à parte, à sua escolha.',img:G+'987989/assets/images/918327.jpg?v=1744845206',thumb:T+'987989/assets/images/918327.jpg?v=1744845206'},
      {n:'Cartoonpiry',p:'R$ 38,90',d:'Catupiry Original empanado, 6 unidades. Crocante por fora, derretendo por dentro.',img:G+'987984/assets/images/918295.jpg?v=1744844899',thumb:T+'987984/assets/images/918295.jpg?v=1744844899'},
      {n:'Krusty the Cow',p:'R$ 41,90',d:'Croquete de carne desfiada recheado com mozarela, 8 unidades.',img:G+'987986/assets/images/918328.jpg?v=1744845220',thumb:T+'987986/assets/images/918328.jpg?v=1744845220'},
      {n:'Chicken Thigh',p:'R$ 46,90',d:'Coxinha sem massa, de frango com Catupiry Original, 6 unidades.',img:G+'987983/assets/images/918319.jpg?v=1744845128',thumb:T+'987983/assets/images/918319.jpg?v=1744845128'},
      {n:'Bacon Du Fromage',p:'R$ 39,90',d:'Tiras de bacon empanadas com recheio de mozarela, 8 unidades.',img:G+'987985/assets/images/918332.jpg?v=1744845267',thumb:T+'987985/assets/images/918332.jpg?v=1744845267'},
      {n:"Frodo's Onion Rings",p:'R$ 27,90',d:'Anéis de cebola empanados.',img:G+'987988/assets/images/918262.jpg?v=1744844360',thumb:T+'987988/assets/images/918262.jpg?v=1744844360'}
    ]},
    {cat:'Sobremesas',itens:[
      {n:'Cheesecake de Ninho com Nutella',curto:'Cheesecake de Ninho',p:'R$ 29,90',d:'Cheesecake de Leite Ninho com base de Oreo, cobertura de Nutella e Ninho polvilhado.',img:G+'988052/assets/images/1537552.jpg?v=1783988269',thumb:T+'988052/assets/images/1537552.jpg?v=1783988269'},
      {n:'Berry Bravo Cup',p:'R$ 29,90',d:'Copo de 300 ml com sorvete de creme, calda de frutas vermelhas da casa e Nutella.',img:G+'988050/assets/images/1537556.jpg?v=1783989405',thumb:T+'988050/assets/images/1537556.jpg?v=1783989405'},
      {n:'Petit Gateau Havanna',p:'R$ 27,90',d:'Petit gateau de dulce de leche Havanna com sorvete de creme e calda de frutas vermelhas.',img:G+'988051/assets/images/918329.jpg?v=1744845231',thumb:T+'988051/assets/images/918329.jpg?v=1744845231'}
    ]},
    {cat:'Milkshakes',nota:'400 ml',itens:[
      {n:'Milkshake Nutella & Jack Daniel’s',p:'R$ 41,00',d:'Creme americano, Nutella e whisky Jack Daniel’s, com borda de Nutella. Proibido para menores de 18 anos.',img:G+'988053/assets/images/918306.jpg?v=1744844994',thumb:T+'988053/assets/images/918306.jpg?v=1744844994'},
      {n:'Milkshake Ninho com Nutella',curto:'Shake Ninho',p:'R$ 30,00',d:'Creme americano, Leite Ninho e Nutella, com borda de brigadeiro.',img:G+'988055/assets/images/918308.jpg?v=1744845009',thumb:T+'988055/assets/images/918308.jpg?v=1744845009'},
      {n:'Milkshake Ovomaltine',curto:'Shake Ovomaltine',p:'R$ 29,00',d:'Creme americano e Ovomaltine, com borda de brigadeiro.',img:G+'988056/assets/images/918309.jpg?v=1744845022',thumb:T+'988056/assets/images/918309.jpg?v=1744845022'}
    ]}
  ],

  // ---------- quem aparece em cada seção animada (nomes iguais aos do cardápio) ----------
  hero:["How You Doin'",'Pink Phink','Especial de Outubro','Van Helsing','Taz Mania'],   // 5; o ÚLTIMO fica no centro
  destaques:[                                                                            // 4 a 6, com etiqueta opcional
    {n:'Taz Mania',tag:'Apimentado'},
    {n:'Especial de Outubro',tag:'Só em outubro'},
    {n:"How You Doin'",tag:'Dois blends'},
    {n:'Pink Phink',tag:'Pão australiano'},
    {n:'Van Helsing',tag:''},
    {n:'Hakuna Matata',tag:'Com brie'}
  ],
  leque:{titulo:'Pra fechar',sub:'Milkshake de 400 ml com borda e as sobremesas da casa.',
    itens:['Milkshake Ninho com Nutella','Cheesecake de Ninho com Nutella','Berry Bravo Cup','Milkshake Ovomaltine']},  // exatamente 4
  queda:['Taz Mania','Fries Cheddar e Bacon','Pink Phink','Milkshake Ovomaltine',"How You Doin'",'Cartoonpiry','Especial de Outubro','Van Helsing','Cheesecake de Ninho com Nutella','Zé Colmeia','Mr. Burns','Berry Bravo Cup']  // até 12, viram bolinhas no final
};
