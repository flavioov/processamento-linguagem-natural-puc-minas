"""
Sistema de logging configurável.
"""
import logging
import sys
from pathlib import Path
from simple_rag.config import config

def setup_logger(name: str = "simple_rag") -> logging.Logger:
    """
    Configura e retorna uma instância de logger.

    Args:
        name: Nome do logger

    Returns:
        Logger configurado
    """
    logger = logging.getLogger(name)

    # Evitar duplicação de handlers
    if logger.handlers:
        return logger

    logger.setLevel(getattr(logging, config.LOG_LEVEL))

    # Handler para console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_format = logging.Formatter(
        '%(levelname)s - %(message)s'
    )
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)

    # Handler para arquivo (se configurado)
    if config.LOG_FILE:
        log_file = Path(config.LOG_FILE)
        log_file.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_format = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
        )
        file_handler.setFormatter(file_format)
        logger.addHandler(file_handler)

    return logger

# Logger padrão do módulo
logger = setup_logger()
