# Guia de Desenvolvimento

## Configuração do Ambiente

### Setup Rápido

```bash
# Clonar repositório
git clone <url>
cd processamento-linguagem-natural-puc-minas

# Criar ambiente virtual
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# Instalar dependências
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Configurar variáveis de ambiente
cp .env.example .env
# Edite o .env com suas configurações
```

### Verificar Ambiente

```bash
# Verificar se tudo está configurado corretamente
python scripts/check_environment.py
```

## Estrutura de Código

### Organização dos Módulos

```
simple_rag/
├── config.py           # Configurações centralizadas (via .env)
├── logger.py           # Sistema de logging
│
├── core/               # Módulos principais
│   ├── document_loader.py    # Carregamento de documentos
│   ├── text_processor.py     # Divisão em chunks
│   └── vectorstore.py        # Gestão do vector store
│
├── agents/             # Agentes LangGraph
│   └── medical_agent.py      # Agente médico principal
│
├── tools/              # Ferramentas para agentes
│   ├── calculator.py         # add(), multiply()
│   └── retriever.py          # retriever()
│
└── cli.py              # Interface CLI
```

### Fluxo de Dados

```
1. Documentos (.txt) → document_loader.py
2. Chunks → text_processor.py
3. Embeddings → vectorstore.py (HuggingFace)
4. Armazenamento → InMemoryVectorStore
5. Retrieval → retriever.py (ferramenta)
6. LLM + Tools → medical_agent.py
7. Interface → cli.py
```

## Executando os Módulos

### Modo Interativo (Principal)

```bash
python -m simple_rag.cli
```

### Testar Módulos Individuais

**Carregar Documentos:**
```python
from simple_rag.core.document_loader import load_documents
from simple_rag.core.text_processor import split_documents

docs = load_documents()
chunks = split_documents(docs)
print(f"Documentos: {len(docs)}, Chunks: {len(chunks)}")
```

**Testar Vectorstore:**
```bash
python -m simple_rag.core.vectorstore
```

**Testar Agente:**
```bash
python -m simple_rag.agents.medical_agent
```

## Configuração via .env

Todas as configurações estão centralizadas no arquivo `.env`:

```env
# Ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b
OLLAMA_TEMPERATURE=0

# Embeddings
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

# Processamento
DATA_DIR=./data/anamnese
CHUNK_SIZE=1000
CHUNK_OVERLAP=200

# Retrieval
RETRIEVAL_K=4
RETRIEVAL_TYPE=similarity

# Logging
LOG_LEVEL=INFO
LOG_FILE=./logs/app.log
```

## Logging

O sistema usa logs em dois níveis:

- **Console**: INFO e acima (formatação simples)
- **Arquivo**: DEBUG e acima (formatação detalhada com timestamps)

Para ajustar o nível de log:

```env
LOG_LEVEL=DEBUG  # Mais verboso
LOG_LEVEL=INFO   # Padrão
LOG_LEVEL=WARNING  # Apenas avisos e erros
```

## Desenvolvimento

### Adicionar Nova Ferramenta

1. Criar arquivo em `simple_rag/tools/nome_ferramenta.py`
2. Usar decorator `@tool` do LangChain
3. Adicionar ao `__init__.py` do módulo tools
4. Importar em `medical_agent.py` e adicionar à lista `tools`

**Exemplo:**
```python
# simple_rag/tools/nova_ferramenta.py
from langchain.tools import tool

@tool
def minha_ferramenta(arg: str) -> str:
    \"\"\"
    Descrição da ferramenta.

    Args:
        arg: Descrição do argumento

    Returns:
        Resultado
    \"\"\"
    return f"Resultado: {arg}"
```

### Modificar Comportamento do Agente

Edite o SystemMessage em `simple_rag/agents/medical_agent.py`:

```python
SystemMessage(
    content="Você é um assistente médico especializado em..."
)
```

### Adicionar Novo Loader de Documentos

Estenda `document_loader.py` para suportar novos formatos:

```python
from langchain_community.document_loaders import PDFLoader

def load_pdf_documents(pdf_dir: Path) -> List[Document]:
    # Implementação
    pass
```

## Troubleshooting

### Erro de Importação

```bash
# Certifique-se de estar no diretório raiz
cd processamento-linguagem-natural-puc-minas

# Execute como módulo
python -m simple_rag.cli
```

### Ollama não Conecta

```bash
# Verificar se está rodando
curl http://localhost:11434/api/version

# Iniciar se necessário
ollama serve
```

### Modelo não Encontrado

```bash
# Listar modelos
ollama list

# Baixar modelo
ollama pull llama3.1:8b
```

### Diretório de Dados não Encontrado

Verifique o `.env`:

```env
DATA_DIR=./data/anamnese  # Caminho relativo correto
```

### Erro de Configuração

Execute a validação:

```python
from simple_rag.config import config
config.validate()
```

## Testes (Futuro)

Estrutura preparada para testes:

```bash
# Rodar todos os testes
pytest

# Com cobertura
pytest --cov=simple_rag

# Testes específicos
pytest tests/test_document_loader.py
```

## Formatação e Linting

```bash
# Formatar código
black simple_rag/

# Verificar estilo
ruff check simple_rag/

# Auto-fix
ruff check --fix simple_rag/
```

## Comandos Úteis

```bash
# Ativar ambiente
source venv/bin/activate

# Executar aplicação
python -m simple_rag.cli

# Testar vectorstore
python -m simple_rag.core.vectorstore

# Testar agente
python -m simple_rag.agents.medical_agent

# Verificar configuração
python -c "from simple_rag.config import config; print(config.OLLAMA_MODEL)"
```

## Próximos Passos

1. **Testes Automatizados** - Implementar testes unitários
2. **CI/CD** - GitHub Actions
3. **Persistência** - Salvar vectorstore em disco
4. **API REST** - Expor via FastAPI
5. **Docker** - Containerizar aplicação
