# Documentação - Simple RAG

Este diretório contém toda a documentação detalhada do projeto Simple RAG.

## 📚 Índice de Documentação

### Arquitetura e Conceitos

#### [`arquitetura.md`](./arquitetura.md)
Documentação técnica completa sobre a arquitetura do sistema.

**Conteúdo:**
- Visão geral da arquitetura
- Diagrama de componentes
- Fluxo de execução detalhado
- Conceitos técnicos (embeddings, vector store, RAG)
- Detalhes de implementação
- Métricas e performance

---

### Guias de Uso

#### [`notebook.md`](./notebook.md)
Explicação completa do notebook Jupyter (`rag.ipynb`).

**Conteúdo:**
- Explicação célula por célula
- Conceitos de embeddings e busca vetorial
- Exemplos práticos com scores de similaridade
- Exercícios para experimentação
- Casos de uso

---

### Módulo de Mascaramento

#### [`mascaramento-guia-rapido.md`](./mascaramento-guia-rapido.md)
Guia rápido de uso do módulo de mascaramento de dados pessoais.

**Conteúdo:**
- Início rápido
- Tabela de referência de todos os tipos
- Exemplos práticos
- Checklist de uso

#### [`mascaramento-completo.md`](./mascaramento-completo.md)
Documentação completa do módulo de mascaramento.

**Conteúdo:**
- Todas as funcionalidades implementadas
- Estatísticas do projeto
- Exemplos de uso avançados
- Integração com pipeline RAG
- Casos de uso detalhados
- Checklist de implementação

#### [`mascaramento-indice.md`](./mascaramento-indice.md)
Índice de todos os arquivos relacionados ao mascaramento.

**Conteúdo:**
- Estrutura de arquivos
- Localização de componentes
- Estatísticas
- Navegação rápida

---

### Histórico e Mudanças

#### [`ATUALIZACAO_README.md`](./ATUALIZACAO_README.md)
Resumo das últimas atualizações do README.md principal.

**Conteúdo:**
- Alterações realizadas
- Novo diagrama de arquitetura
- Comparação antes/depois
- Verificação de qualidade

---

## 🗂️ Estrutura Completa

```
docs/
├── README.md                        # Este arquivo - índice da documentação
├── arquitetura.md                   # Arquitetura técnica completa
├── notebook.md                      # Explicação do Jupyter Notebook
├── mascaramento-guia-rapido.md      # Guia rápido de mascaramento
├── mascaramento-completo.md         # Documentação completa de mascaramento
├── mascaramento-indice.md           # Índice de arquivos de mascaramento
└── ATUALIZACAO_README.md            # Histórico de atualizações
```

---

## 🚀 Por Onde Começar

### Para Usuários Novos
1. Leia o [`README.md`](../README.md) principal (raiz do projeto)
2. Consulte [`arquitetura.md`](./arquitetura.md) para entender o sistema
3. Experimente com [`notebook.md`](./notebook.md) como guia

### Para Desenvolvedores
1. Leia [`arquitetura.md`](./arquitetura.md) - Entenda os componentes
2. Consulte [`mascaramento-completo.md`](./mascaramento-completo.md) - Recurso importante
3. Use [`mascaramento-guia-rapido.md`](./mascaramento-guia-rapido.md) como referência

### Para Implementar Mascaramento
1. [`mascaramento-guia-rapido.md`](./mascaramento-guia-rapido.md) - Início rápido
2. [`mascaramento-completo.md`](./mascaramento-completo.md) - Referência completa
3. [`mascaramento-indice.md`](./mascaramento-indice.md) - Localizar arquivos

---

## 📖 Documentação Adicional

### No Diretório Raiz
- `README.md` - Guia principal do projeto (instalação, uso, configuração)
- `DOCKER_README.md` - Instruções para execução com Docker
- `pyproject.toml` - Configurações do projeto e dependências

### Exemplos Práticos
- `examples/demo_final_masking.py` - Demonstração completa de mascaramento
- `examples/demo_new_masks.py` - Demo das novas funcionalidades
- `examples/mask_anamnese_example.py` - Exemplo com arquivos médicos

### Notebooks
- `rag.ipynb` - Notebook interativo do sistema RAG

---

## 🔍 Busca Rápida

### Buscar por Tópico

| Tópico | Documento |
|--------|-----------|
| Arquitetura geral | [`arquitetura.md`](./arquitetura.md) |
| Como funciona o RAG | [`arquitetura.md`](./arquitetura.md) |
| Embeddings e vetores | [`notebook.md`](./notebook.md) ou [`arquitetura.md`](./arquitetura.md) |
| Mascaramento de dados | [`mascaramento-guia-rapido.md`](./mascaramento-guia-rapido.md) |
| Tipos de mascaramento | [`mascaramento-completo.md`](./mascaramento-completo.md) |
| ChromaDB | [`arquitetura.md`](./arquitetura.md) |
| LangChain/LangGraph | [`arquitetura.md`](./arquitetura.md) |
| Ollama/LLM | [`arquitetura.md`](./arquitetura.md) |
| Jupyter Notebook | [`notebook.md`](./notebook.md) |

---

## 📊 Estatísticas da Documentação

| Documento | Linhas | Páginas (aprox.) | Nível |
|-----------|---------|------------------|-------|
| `arquitetura.md` | ~600 | ~15 | Técnico |
| `notebook.md` | ~800 | ~20 | Intermediário |
| `mascaramento-completo.md` | ~650 | ~16 | Intermediário |
| `mascaramento-guia-rapido.md` | ~150 | ~4 | Básico |
| `mascaramento-indice.md` | ~350 | ~9 | Referência |

**Total:** ~2,550 linhas de documentação técnica

---

## 🤝 Contribuindo com a Documentação

Se você encontrar erros ou quiser melhorar a documentação:

1. Abra uma issue descrevendo o problema/sugestão
2. Para correções pequenas, faça um PR diretamente
3. Para mudanças grandes, discuta primeiro em uma issue

### Padrões de Documentação

- Use Markdown para todos os documentos
- Inclua exemplos de código quando relevante
- Adicione tabelas para comparações
- Use diagramas Mermaid quando possível
- Mantenha linguagem clara e objetiva

---

## 📞 Suporte

Para dúvidas sobre a documentação:
- Consulte o README.md principal
- Abra uma issue no GitHub
- Revise os exemplos em `examples/`

---

**Última atualização:** 2025-11-09
**Versão do projeto:** 1.2.0
