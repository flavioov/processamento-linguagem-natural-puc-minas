"""Utilitário para mascaramento de dados pessoais sensíveis em textos.

Este módulo fornece funções para identificar e mascarar informações pessoais
como CPF, RG, CEP, email e números de telefone em strings ou blocos de texto.
"""

import re
from collections.abc import Callable


def mask_cpf(text: str, mask_char: str = "*") -> str:
    """Mascara números de CPF no texto.

    Formatos aceitos:
    - XXX.XXX.XXX-XX
    - XXXXXXXXXXX

    Args:
        text: Texto contendo possíveis CPFs
        mask_char: Caractere usado para mascarar (padrão: *)

    Returns:
        Texto com CPFs mascarados

    Examples:
        >>> mask_cpf("Meu CPF é 123.456.789-00")
        "Meu CPF é ***.***.***-**"
        >>> mask_cpf("CPF: 12345678900")
        "CPF: ***********"
    """

    # CPF com pontuação: XXX.XXX.XXX-XX -> mantém primeiro e último bloco
    def mask_formatted(match):
        cpf = match.group(0)
        # Mantém 123.XXX.XXX-45 (primeiros 3 e últimos 2)
        return f"{cpf[:3]}.{mask_char * 3}.{mask_char * 3}-{cpf[-2:]}"

    pattern_formatted = r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b"
    text = re.sub(pattern_formatted, mask_formatted, text)

    # CPF sem pontuação: 11 dígitos seguidos -> mantém 3 primeiros e 3 últimos
    def mask_plain(match):
        cpf = match.group(0)
        # Mantém 123XXXXX789 (primeiros 3 e últimos 3)
        return f"{cpf[:3]}{mask_char * 5}{cpf[-3:]}"

    pattern_plain = r"\b\d{11}\b"
    text = re.sub(pattern_plain, mask_plain, text)

    return text


def mask_rg(text: str, mask_char: str = "*") -> str:
    """Mascara números de RG no texto, mantendo os 2 primeiros e 2 últimos dígitos.

    Formatos aceitos:
    - XX.XXX.XXX-X
    - XXXXXXXXX

    Args:
        text: Texto contendo possíveis RGs
        mask_char: Caractere usado para mascarar (padrão: *)

    Returns:
        Texto com RGs mascarados

    Examples:
        >>> mask_rg("RG: 12.345.678-9")
        "RG: 12.***.***.9"
        >>> mask_rg("RG: 123456789")
        "RG: 12*****89"
    """

    # RG com pontuação: XX.XXX.XXX-X -> mantém primeiros 2 e último dígito
    def mask_formatted(match):
        rg = match.group(0)
        # Mantém 12.XXX.XXX-9 (primeiros 2 e último 1)
        # Como o RG tem formato XX.XXX.XXX-X, vamos manter os 2 primeiros dígitos
        # e o dígito verificador (último)
        first_two = rg[:2]  # "12"
        last_char = rg[-1]  # "9" ou "X"
        return f"{first_two}.{mask_char * 3}.{mask_char * 3}-{last_char}"

    pattern_formatted = r"\b\d{2}\.\d{3}\.\d{3}-[\dXx]\b"
    text = re.sub(pattern_formatted, mask_formatted, text)

    # RG sem pontuação: 9 dígitos -> mantém 2 primeiros e 2 últimos
    def mask_plain(match):
        rg = match.group(0)
        # Mantém 12XXXXX89 (primeiros 2 e últimos 2)
        return f"{rg[:2]}{mask_char * 5}{rg[-2:]}"

    pattern_plain = r"\b\d{9}\b"
    text = re.sub(pattern_plain, mask_plain, text)

    return text


def mask_cep(text: str, mask_char: str = "*") -> str:
    """Mascara os 3 últimos números de CEPs no texto.

    Formatos aceitos:
    - XXXXX-XXX
    - XXXXXXXX

    Args:
        text: Texto contendo possíveis CEPs
        mask_char: Caractere usado para mascarar (padrão: *)

    Returns:
        Texto com CEPs mascarados

    Examples:
        >>> mask_cep("CEP: 12345-678")
        "CEP: 12345-***"
        >>> mask_cep("CEP: 12345678")
        "CEP: 12345***"
    """

    # CEP com hífen: XXXXX-XXX -> mantém XXXXX e mascara os 3 últimos
    def mask_formatted(match):
        cep = match.group(0)
        # Mantém 12345-XXX (primeiros 5 e mascara os 3 últimos)
        return f"{cep[:5]}-{mask_char * 3}"

    pattern_formatted = r"\b\d{5}-\d{3}\b"
    text = re.sub(pattern_formatted, mask_formatted, text)

    # CEP sem hífen: 8 dígitos -> mantém os 5 primeiros e mascara os 3 últimos
    def mask_plain(match):
        cep = match.group(0)
        # Mantém 12345XXX (primeiros 5 e mascara os 3 últimos)
        return f"{cep[:5]}{mask_char * 3}"

    pattern_plain = r"\b\d{8}\b"
    text = re.sub(pattern_plain, mask_plain, text)

    return text


def mask_email(text: str, mask_char: str = "*") -> str:
    """Mascara endereços de email no texto.

    Mantém as 4 primeiras letras do usuário e o domínio completo sem máscara.

    Args:
        text: Texto contendo possíveis emails
        mask_char: Caractere usado para mascarar (padrão: *)

    Returns:
        Texto com emails mascarados

    Examples:
        >>> mask_email("Email: user@example.com")
        "Email: user@example.com"
        >>> mask_email("Email: username@example.com")
        "Email: user****@example.com"
        >>> mask_email("Email: jo@example.com")
        "Email: jo@example.com"
    """
    pattern = r"\b([a-zA-Z0-9._%+-]+)(@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})\b"

    def replace_email(match):
        local_part = match.group(1)  # Parte antes do @
        domain_part = match.group(2)  # Parte depois do @ (incluindo @)

        # Se o usuário tiver 4 caracteres ou menos, não mascara
        if len(local_part) <= 4:
            return local_part + domain_part

        # Mantém os 4 primeiros caracteres e mascara o resto
        visible_part = local_part[:4]
        masked_part = mask_char * (len(local_part) - 4)

        return visible_part + masked_part + domain_part

    text = re.sub(pattern, replace_email, text)

    return text


def mask_phone(text: str, mask_char: str = "*") -> str:
    """Mascara números de telefone no texto (formatos brasileiros).

    Mantém apenas os últimos 4 dígitos visíveis.

    Formatos aceitos:
    - (XX) XXXXX-XXXX (celular com DDD)
    - (XX) XXXX-XXXX (fixo com DDD)
    - XX XXXXX-XXXX
    - XX XXXX-XXXX
    - XXXXXXXXXXX (11 dígitos)
    - XXXXXXXXXX (10 dígitos)

    Args:
        text: Texto contendo possíveis telefones
        mask_char: Caractere usado para mascarar (padrão: *)

    Returns:
        Texto com telefones mascarados

    Examples:
        >>> mask_phone("Tel: (11) 98765-4321")
        "Tel: (**) *****-4321"
        >>> mask_phone("Tel: 11987654321")
        "Tel: *******4321"
    """

    # Telefone com parênteses e hífen: (XX) XXXXX-XXXX ou (XX) XXXX-XXXX
    def replace_phone_full(match):
        phone = match.group(0)
        # Extrair apenas os dígitos
        digits = re.sub(r"\D", "", phone)
        last_four = digits[-4:]

        if len(digits) == 11:  # Celular: (XX) XXXXX-XXXX
            return f"({mask_char * 2}) {mask_char * 5}-{last_four}"
        else:  # Fixo: (XX) XXXX-XXXX
            return f"({mask_char * 2}) {mask_char * 4}-{last_four}"

    pattern_full = r"\(\d{2}\)\s*\d{4,5}-\d{4}"
    text = re.sub(pattern_full, replace_phone_full, text)

    # Telefone sem parênteses: XX XXXXX-XXXX ou XX XXXX-XXXX
    def replace_phone_space(match):
        phone = match.group(0)
        digits = re.sub(r"\D", "", phone)
        last_four = digits[-4:]

        if len(digits) == 11:  # Celular: XX XXXXX-XXXX
            return f"{mask_char * 2} {mask_char * 5}-{last_four}"
        else:  # Fixo: XX XXXX-XXXX
            return f"{mask_char * 2} {mask_char * 4}-{last_four}"

    pattern_space = r"\b\d{2}\s+\d{4,5}-\d{4}\b"
    text = re.sub(pattern_space, replace_phone_space, text)

    # Telefone apenas números: 11 dígitos
    def replace_plain_11(match):
        phone = match.group(0)
        last_four = phone[-4:]
        return f"{mask_char * 7}{last_four}"

    pattern_plain_11 = r"\b\d{11}\b"
    text = re.sub(pattern_plain_11, replace_plain_11, text)

    # Telefone apenas números: 10 dígitos
    def replace_plain_10(match):
        phone = match.group(0)
        last_four = phone[-4:]
        return f"{mask_char * 6}{last_four}"

    pattern_plain_10 = r"\b\d{10}\b"
    text = re.sub(pattern_plain_10, replace_plain_10, text)

    return text


def mask_birth_date(text: str, mask_char: str = "*") -> str:
    """Mascara datas de nascimento no texto completamente.

    Formatos aceitos:
    - DD/MM/AAAA
    - DD-MM-AAAA
    - DD.MM.AAAA

    Args:
        text: Texto contendo possíveis datas de nascimento
        mask_char: Caractere usado para mascarar (padrão: *)

    Returns:
        Texto com datas mascaradas

    Examples:
        >>> mask_birth_date("Data de Nascimento: 15/03/1953")
        "Data de Nascimento: **/**/****"
        >>> mask_birth_date("Nascido em 01-05-1980")
        "Nascido em **-**-****"
    """
    # Data com barra: DD/MM/AAAA
    pattern_slash = r"\b\d{2}/\d{2}/\d{4}\b"
    text = re.sub(
        pattern_slash, f"{mask_char * 2}/{mask_char * 2}/{mask_char * 4}", text
    )

    # Data com hífen: DD-MM-AAAA
    pattern_dash = r"\b\d{2}-\d{2}-\d{4}\b"
    text = re.sub(
        pattern_dash, f"{mask_char * 2}-{mask_char * 2}-{mask_char * 4}", text
    )

    # Data com ponto: DD.MM.AAAA
    pattern_dot = r"\b\d{2}\.\d{2}\.\d{4}\b"
    text = re.sub(pattern_dot, f"{mask_char * 2}.{mask_char * 2}.{mask_char * 4}", text)

    return text


def mask_prontuario(text: str, mask_char: str = "*") -> str:
    """Mascara números de prontuário no texto, mantendo os 3 últimos dígitos visíveis.

    Detecta números de prontuário com base em padrões contextuais:
    - Precedidos por palavras como "Prontuário", "Pront.", "Registro"
    - Números com 6-10 dígitos

    Args:
        text: Texto contendo possíveis números de prontuário
        mask_char: Caractere usado para mascarar (padrão: *)

    Returns:
        Texto com prontuários mascarados

    Examples:
        >>> mask_prontuario("Prontuário: 0876532")
        "Prontuário: ****532"
        >>> mask_prontuario("Pront. 123456789")
        "Pront. ******789"
    """
    # Padrão para detectar prontuário com contexto
    # Busca por palavras-chave seguidas de números
    patterns = [
        r"(Prontuário[:\s]+)(\d{6,10})\b",
        r"(Pront\.?[:\s]+)(\d{6,10})\b",
        r"(Registro[:\s]+)(\d{6,10})\b",
        r"(Nº do prontuário[:\s]+)(\d{6,10})\b",
    ]

    def mask_number(match):
        prefix = match.group(1)
        number = match.group(2)
        # Mantém os últimos 3 dígitos
        last_three = number[-3:]
        masked_part = mask_char * (len(number) - 3)
        return f"{prefix}{masked_part}{last_three}"

    for pattern in patterns:
        text = re.sub(pattern, mask_number, text, flags=re.IGNORECASE)

    return text


def mask_all_pii(
    text: str,
    mask_char: str = "*",
    custom_patterns: dict[str, str] | None = None,
) -> str:
    """Mascara todos os tipos de dados pessoais identificáveis (PII) no texto.

    Args:
        text: Texto contendo possíveis dados pessoais
        mask_char: Caractere usado para mascarar (padrão: *)
        custom_patterns: Dicionário com padrões regex customizados e suas substituições

    Returns:
        Texto com todos os dados pessoais mascarados

    Examples:
        >>> text = "CPF: 123.456.789-00, Email: user@example.com, Tel: (11) 98765-4321"
        >>> mask_all_pii(text)
        "CPF: ***.***.***.**, Email: ****@***.com, Tel: (**) *****-****"
    """
    # Aplica todas as máscaras na ordem
    masked_text = text

    # Ordem de aplicação: mais específicos primeiro para evitar conflitos
    masked_text = mask_name(masked_text, mask_char)
    masked_text = mask_birth_date(masked_text, mask_char)
    masked_text = mask_prontuario(masked_text, mask_char)
    masked_text = mask_cpf(masked_text, mask_char)
    masked_text = mask_rg(masked_text, mask_char)
    masked_text = mask_email(masked_text, mask_char)
    masked_text = mask_phone(masked_text, mask_char)
    masked_text = mask_cep(masked_text, mask_char)

    # Aplica padrões customizados se fornecidos
    if custom_patterns:
        for pattern, replacement in custom_patterns.items():
            masked_text = re.sub(pattern, replacement, masked_text)

    return masked_text


def mask_name(text: str, mask_char: str = "*") -> str:
    """Mascara nomes de pessoas no texto.

    O texto deve estar no formato "Nome: <nome completo da pessoa>"

    Regras de mascaramento:
    - Mantém a primeira letra de cada nome visível
    - Mascara o restante de cada nome
    - Nomes com 1 letra permanecem visíveis
    - Preposições comuns (de, da, do, dos, das) permanecem visíveis

    Args:
        text: Texto contendo possíveis nomes
        mask_char: Caractere usado para mascarar (padrão: *)

    Returns:
        Texto com nomes mascarados

    Examples:
        >>> mask_name("Nome: João Silva")
        "Nome: J*** S*****"
        >>> mask_name("Nome: Maria da Silva Santos")
        "Nome: M**** da S***** S*****"
        >>> mask_name("Nome: Pedro de Oliveira")
        "Nome: P**** de O*******"
    """
    # Padrão para capturar "Nome: " seguido do nome completo até o final da linha
    # Usa $ para indicar final da linha com flag MULTILINE
    pattern = r"(Nome:\s*)([A-Za-zÀ-ÿ ]+?)(?=\n|$)"

    # Preposições que devem permanecer visíveis
    prepositions = {"de", "da", "do", "dos", "das", "e"}

    def mask_full_name(match):
        prefix = match.group(1)  # "Nome: "
        full_name = match.group(2).strip()  # Nome completo

        # Divide o nome em partes
        name_parts = full_name.split()
        masked_parts = []

        for part in name_parts:
            # Se for preposição, mantém visível
            if part.lower() in prepositions or len(part) == 1:
                masked_parts.append(part)
            # Senão, mascara mantendo apenas a primeira letra
            else:
                first_letter = part[0]
                masked = first_letter + (mask_char * (len(part) - 1))
                masked_parts.append(masked)

        return prefix + " ".join(masked_parts)

    text = re.sub(pattern, mask_full_name, text, flags=re.IGNORECASE | re.MULTILINE)

    return text


# Dicionário de funções de mascaramento disponíveis
MASKING_FUNCTIONS: dict[str, Callable] = {
    "nome": mask_name,
    "cpf": mask_cpf,
    "rg": mask_rg,
    "cep": mask_cep,
    "email": mask_email,
    "phone": mask_phone,
    "birth_date": mask_birth_date,
    "prontuario": mask_prontuario,
    "all": mask_all_pii,
}


def mask_pii(
    text: str, pii_types: list[str] | None = None, mask_char: str = "*", **kwargs
) -> str:
    """Função flexível para mascarar tipos específicos de PII.

    Args:
        text: Texto a ser mascarado
        pii_types: Lista de tipos de PII para mascarar.
                   Opções: ['nome', 'cpf', 'rg', 'cep', 'email', 'phone', 'birth_date', 'prontuario', 'all']
                   Se None, mascara todos os tipos.
        mask_char: Caractere usado para mascarar (padrão: *)
        **kwargs: Argumentos adicionais para funções específicas

    Returns:
        Texto mascarado

    Examples:
        >>> mask_pii("Nome: João Silva", pii_types=['nome'])
        "Nome: J*** S*****"
        >>> mask_pii("CPF: 123.456.789-00", pii_types=['cpf'])
        "CPF: ***.***.***.** "
        >>> mask_pii("Email: user@example.com, CPF: 123.456.789-00")
        "Email: ****@***.com, CPF: ***.***.***-**"
        >>> mask_pii("Data de Nascimento: 15/03/1953, Prontuário: 0876532", pii_types=['birth_date', 'prontuario'])
        "Data de Nascimento: **/**/****  , Prontuário: ****532"
    """
    if pii_types is None or "all" in pii_types:
        return mask_all_pii(text, mask_char, **kwargs)

    masked_text = text
    for pii_type in pii_types:
        if pii_type in MASKING_FUNCTIONS and pii_type != "all":
            func = MASKING_FUNCTIONS[pii_type]
            masked_text = func(masked_text, mask_char)

    return masked_text


if __name__ == "__main__":
    text = """
    Dados do paciente:
    Nome: João da Silva
    CPF: 123.456.789-00
    RG: 12.345.678-9
    Email: joao.silva@email.com
    Telefone: (11) 98765-4321
    CEP: 12345-678
    """
    masked = mask_pii(text=text, pii_types=["all"])
    print(masked)
