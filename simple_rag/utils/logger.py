"""Sistema de logging."""

import logging
import sys
from pathlib import Path

from simple_rag.config.config import settings


def setup_logger(name: str = "simple_rag") -> logging.Logger:
    """Configura e retorna uma instância de logger.

    Args:
        name: Nome do logger

    Returns:
        Logger configurado
    """
    logger_ = logging.getLogger(name)

    # Evitar duplicação de handlers
    if logger_.handlers:
        return logger_

    logger_.setLevel(getattr(logging, settings.log_level))
    logger_.propagate = (
        False  # Prevent duplicate logs from propagating to parent loggers
    )

    # Handler para console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_format = logging.Formatter("%(levelname)s - %(message)s")
    console_handler.setFormatter(console_format)
    logger_.addHandler(console_handler)

    # Handler para arquivo (se configurado)
    if settings.log_file:
        log_file = Path(settings.log_file)
        log_file.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_format = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"
        )
        file_handler.setFormatter(file_format)
        logger_.addHandler(file_handler)

    return logger_


# Logger padrão do módulo
logger = setup_logger()
