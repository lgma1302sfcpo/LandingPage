# Sistema de Landing Pages para Clientes Locais

## Estrutura de Pastas

```
landing-pages-clientes/
├── README.md                    # Este arquivo
├── vercel.json                  # Config de deploy
├── mensagens/
│   └── prospeccao-whatsapp.md   # Templates de mensagens
├── clientes/
│   ├── esmalteria-brandao/
│   │   └── index.html           # Landing page
│   ├── salao-maria/
│   │   └── index.html
│   └── barbearia-santos/
│       └── index.html
└── assets/                      # Imagens compartilhadas (opcional)
```

## Como Funciona

Cada cliente fica em uma pasta separada. Quando você faz deploy no Vercel:
- `esmalteria-brandao` → `seusite.vercel.app/esmalteria-brandao`
- `salao-maria` → `seusite.vercel.app/salao-maria`

## Hospedagem Gratuita (Vercel)

### Passo 1: Criar conta no Vercel
1. Acesse https://vercel.com
2. Clique em "Sign Up" → "Continue with GitHub" (ou email)
3. Crie uma conta gratuita

### Passo 2: Instalar Vercel CLI
```bash
npm install -g vercel
```

### Passo 3: Fazer login
```bash
vercel login
```

### Passo 4: Deploy
Na pasta `landing-pages-clientes`, execute:
```bash
vercel --prod
```

Pronto! Seu site estará em algo como:
`https://landing-pages-clientes.vercel.app`

### Passo 5: Acessar os demos
- Esmalteria Brandão: `https://seusite.vercel.app/esmalteria-brandao`
- Próximo cliente: `https://seusite.vercel.app/nome-do-cliente`

## Alternativa: Netlify

### Passo 1: Criar conta
1. Acesse https://netlify.com
2. Sign up com GitHub ou email

### Passo 2: Deploy manual
1. Vá em "Sites" → "Add new site" → "Deploy manually"
2. Arraste a pasta `landing-pages-clientes` para a área de upload
3. Pronto!

### Passo 3: Renomear URL
1. Clique no site criado
2. "Site settings" → "Change site name"
3. Escolha algo como: `demos-landing.netlify.app`

## Fluxo de Trabalho

### Adicionar novo cliente:

1. Crie pasta em `clientes/nome-do-cliente/`
2. Copie e adapte o `index.html` de outro cliente
3. Faça deploy: `vercel --prod`
4. Envie o link: `seusite.vercel.app/nome-do-cliente`

### Quando o cliente fechar:

1. Troque as imagens do Unsplash pelas fotos reais dele
2. Registre um domínio próprio (ex: esmalteriabrandao.com.br)
3. Configure o domínio no Vercel/Netlify
4. Mova para uma pasta/projeto separado (opcional)

## Dicas de Organização

### Para demos (prospecção):
- Adicione `<meta name="robots" content="noindex">` no HTML
- Isso evita que o Google indexe antes do cliente aprovar

### Para produção (cliente fechou):
- Remova o `noindex`
- Troque para domínio próprio
- Adicione Google Analytics (opcional)

## URLs Sugeridas

| Tipo | Formato |
|------|---------|
| Demo | `demos-landing.vercel.app/nome-cliente` |
| Produção | `nomecliente.com.br` ou `nomecliente.vercel.app` |

## Custos

| Item | Vercel/Netlify | Domínio .com.br |
|------|----------------|-----------------|
| Hospedagem | Grátis | - |
| SSL (https) | Grátis | - |
| Domínio | - | ~R$ 40/ano |
| **Total** | **R$ 0** | **~R$ 40/ano** |
