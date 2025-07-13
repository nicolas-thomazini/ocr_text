# Family Search OCR - Frontend

Frontend React para o sistema Family Search OCR, desenvolvido para análise e melhoria de documentos antigos italianos para pesquisa genealógica.

## 🚀 Tecnologias

- **React 18** - Biblioteca JavaScript para interfaces
- **TypeScript** - Tipagem estática
- **Vite** - Build tool e dev server
- **Tailwind CSS** - Framework CSS utilitário
- **React Query** - Gerenciamento de estado e cache
- **React Hook Form** - Gerenciamento de formulários
- **React Dropzone** - Upload de arquivos com drag & drop
- **Lucide React** - Ícones modernos
- **Axios** - Cliente HTTP

## 📦 Instalação

1. Instale as dependências:
```bash
npm install
```

2. Configure as variáveis de ambiente:
```bash
cp .env.example .env
```

3. Edite o arquivo `.env` com suas configurações:
```env
VITE_API_URL=http://localhost:8000
VITE_APP_NAME=Family Search OCR
```

## 🏃‍♂️ Executando o Projeto

### Desenvolvimento
```bash
npm run dev
```

O frontend estará disponível em `http://localhost:3000`

### Build para Produção
```bash
npm run build
```

### Preview do Build
```bash
npm run preview
```

## 🏗️ Estrutura do Projeto

```
src/
├── components/          # Componentes reutilizáveis
│   ├── FileUpload.tsx   # Upload de arquivos
│   ├── DocumentList.tsx # Lista de documentos
│   └── Statistics.tsx   # Estatísticas
├── pages/              # Páginas da aplicação
│   └── Dashboard.tsx   # Dashboard principal
├── hooks/              # Hooks personalizados
│   ├── useDocuments.ts # Hook para documentos
│   ├── useAI.ts        # Hook para IA
│   └── useStatistics.ts # Hook para estatísticas
├── services/           # Serviços de API
│   └── api.ts          # Cliente da API
├── types/              # Definições de tipos TypeScript
│   └── index.ts        # Tipos principais
└── utils/              # Utilitários
```

## 🔧 Funcionalidades

### Dashboard Principal
- **Visão Geral**: Estatísticas e documentos recentes
- **Documentos**: Lista completa de documentos processados
- **Upload**: Interface de upload com drag & drop

### Upload de Documentos
- Suporte a múltiplos formatos (PNG, JPG, PDF, etc.)
- Drag & drop de arquivos
- Progresso de upload em tempo real
- Preview de arquivos

### Visualização de Documentos
- Lista paginada de documentos
- Informações detalhadas (tamanho, data, confiança)
- Status de processamento
- Ações (visualizar, excluir)

### Estatísticas
- Total de documentos
- Documentos processados
- Confiança média
- Precisão da IA
- Documentos do dia

## 🔌 Integração com Backend

O frontend se comunica com o backend através da API REST:

- **Base URL**: Configurada via `VITE_API_URL`
- **Proxy**: Configurado no Vite para desenvolvimento
- **Autenticação**: Suporte a tokens JWT
- **Upload**: Multipart form data
- **Cache**: React Query para cache inteligente

## 🎨 Design System

### Cores
- **Primary**: Azul (#3B82F6)
- **Secondary**: Cinza (#64748B)
- **Success**: Verde (#10B981)
- **Warning**: Amarelo (#F59E0B)
- **Error**: Vermelho (#EF4444)

### Componentes
- **Botões**: `.btn-primary`, `.btn-secondary`
- **Cards**: `.card`
- **Inputs**: `.input-field`

## 📱 Responsividade

O frontend é totalmente responsivo e funciona em:
- Desktop (1024px+)
- Tablet (768px - 1023px)
- Mobile (320px - 767px)

## 🧪 Testes

```bash
# Executar testes
npm run test

# Executar testes em modo watch
npm run test:watch

# Cobertura de testes
npm run test:coverage
```

## 📦 Build e Deploy

### Build de Produção
```bash
npm run build
```

### Deploy
O build gera arquivos estáticos na pasta `dist/` que podem ser servidos por qualquer servidor web.

## 🔒 Segurança

- Validação de tipos com TypeScript
- Sanitização de inputs
- Headers de segurança configurados
- CORS configurado para desenvolvimento

## 🤝 Contribuição

1. Faça fork do projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT.
