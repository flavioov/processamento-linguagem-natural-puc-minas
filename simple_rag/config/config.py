"""Configurações centralizadas do projeto.

Carrega variáveis de ambiente e valida configurações usando Pydantic.
"""

from pathlib import Path

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    """Configurações da aplicação usando Pydantic BaseSettings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Diretórios
    base_dir: Path = Field(default_factory=lambda: Path(__file__).parent.parent)
    data_dir: str = Field(default="data/anamnese", description="Diretório de dados")
    log_dir: Path = Field(default_factory=lambda: Path(__file__).parent.parent / "logs")

    # Ollama
    ollama_base_url: str = Field(
        default="http://11.7.0.2:11434", description="URL base do Ollama"
    )
    ollama_model: str = Field(default="llama3.1:8b", description="Modelo Ollama")
    ollama_temperature: float = Field(
        default=0.0, ge=0.0, le=2.0, description="Temperatura do modelo"
    )

    # Embeddings
    embedding_model: str = Field(
        default="llama3",
        description="Modelo de embeddings",
    )

    # Processamento de Texto
    chunk_size: int = Field(
        default=1000, gt=0, description="Tamanho dos chunks de texto"
    )
    chunk_overlap: int = Field(
        default=200, ge=0, description="Sobreposição entre chunks"
    )

    # Retrieval
    retrieval_k: int = Field(
        default=5, gt=0, description="Número de documentos a recuperar"
    )
    retrieval_type: str = Field(
        default="similarity", description="Tipo de busca no retrieval"
    )

    # Logging
    log_level: str = Field(default="INFO", description="Nível de logging")
    log_file: str | None = Field(default=None, description="Arquivo de log")

    # System Message
    system_message: str = Field(
        default="""
        Você é um médico assistente. Seu papel é procura informações dos pacientes
        nas anamneses salvas no vectorstore e retornar as informações solicitadas.

        Você possui até 2 anamneses salvos no vectorstore: anamnese1 e anamnese2.

        Utilize suas ferramentas para consultar e realizar queries na base de conhecimento privada sobre pacientes
        e suas anamneses.
        """,
        description="Mensagem de sistema para o LLM",
    )

    @field_validator("chunk_overlap")
    @classmethod
    def validate_chunk_overlap(cls, v: int, info) -> int:
        """Valida que chunk_overlap é menor que chunk_size."""
        chunk_size = info.data.get("chunk_size", 1000)
        if v >= chunk_size:
            raise ValueError(
                f"chunk_overlap ({v}) deve ser menor que chunk_size ({chunk_size})"
            )
        return v

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Valida que o log_level é válido."""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        v_upper = v.upper()
        if v_upper not in valid_levels:
            raise ValueError(f"log_level deve ser um de: {', '.join(valid_levels)}")
        return v_upper

    def get_data_dir(self) -> Path:
        """Retorna o caminho completo do diretório de dados."""
        return self.base_dir / self.data_dir


# Instância global de configuração
settings = Config()
