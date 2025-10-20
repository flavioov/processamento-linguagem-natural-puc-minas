"""
Configurações centralizadas do projeto.
Carrega variáveis de ambiente e valida configurações.
"""
import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

class Config:
    """Configurações da aplicação."""

    # Diretórios
    BASE_DIR = Path(__file__).parent.parent
    DATA_DIR = BASE_DIR / os.getenv("DATA_DIR", "data/anamnese")
    LOG_DIR = BASE_DIR / "logs"

    # Ollama
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://11.7.0.2:11434")
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1:8b")
    OLLAMA_TEMPERATURE = float(os.getenv("OLLAMA_TEMPERATURE", "0"))

    # Embeddings
    EMBEDDING_MODEL = os.getenv(
        "EMBEDDING_MODEL",
        "sentence-transformers/all-MiniLM-L6-v2"
    )

    # Processamento de Texto
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))

    # Retrieval
    RETRIEVAL_K = int(os.getenv("RETRIEVAL_K", "2"))
    RETRIEVAL_TYPE = os.getenv("RETRIEVAL_TYPE", "similarity")

    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE")

    SYSTEM_MESSAGE = os.getenv("SYSTEM_MESSAGE", "Você é um assistente que traz respostas concisas."
                                                 "")
    @classmethod
    def validate(cls):
        """Valida as configurações."""
        errors = []

        if not cls.DATA_DIR.exists():
            errors.append(f"Diretório de dados não encontrado: {cls.DATA_DIR}")

        if cls.CHUNK_SIZE <= 0:
            errors.append("CHUNK_SIZE deve ser maior que 0")

        if cls.CHUNK_OVERLAP >= cls.CHUNK_SIZE:
            errors.append("CHUNK_OVERLAP deve ser menor que CHUNK_SIZE")

        if cls.RETRIEVAL_K <= 0:
            errors.append("RETRIEVAL_K deve ser maior que 0")

        if errors:
            raise ValueError(f"Erros de configuração:\n" + "\n".join(f"  - {e}" for e in errors))

        # Criar diretórios necessários
        cls.LOG_DIR.mkdir(parents=True, exist_ok=True)

# Instância global de configuração
config = Config()

# Validar na importação
try:
    config.validate()
except ValueError as e:
    print(f"⚠️  AVISO: {e}")
