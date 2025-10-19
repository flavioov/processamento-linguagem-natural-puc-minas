# Diretório de Dados

## Estrutura

```
data/
└── anamnese/          # Documentos de anamnese médica
    ├── camila-rodrigues-de-almeida.txt
    ├── jose-carlos-da-silva.txt
    └── maria-fernanda-oliveira-santos.txt
```

## Formato dos Arquivos

- **Formato**: Texto simples (.txt)
- **Encoding**: UTF-8
- **Conteúdo**: Anamneses médicas de pacientes

## Adicionar Novos Documentos

1. Coloque arquivos `.txt` no diretório `anamnese/`
2. Use encoding UTF-8
3. Os arquivos serão carregados automaticamente na próxima execução do sistema

## Arquivos Atuais

- **camila-rodrigues-de-almeida.txt** - Paciente com lúpus eritematoso sistêmico
- **jose-carlos-da-silva.txt** - Paciente com hipertensão arterial
- **maria-fernanda-oliveira-santos.txt** - Paciente com câncer de tireoide

## Processamento

Os documentos são processados da seguinte forma:

1. **Carregamento**: Todos os arquivos .txt são lidos recursivamente
2. **Divisão**: Textos são divididos em chunks de ~1000 caracteres
3. **Embedding**: Cada chunk é convertido em vetor usando sentence-transformers
4. **Armazenamento**: Vetores são armazenados em memória para busca semântica

## Observações

- Mantenha os documentos neste formato de texto simples
- Evite incluir informações sensíveis reais de pacientes
- Para dados de produção, considere implementar criptografia
