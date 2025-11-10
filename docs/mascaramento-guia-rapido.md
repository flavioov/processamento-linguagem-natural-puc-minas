# Guia Rápido: Mascaramento de Dados Pessoais

## 🚀 Início Rápido

### Instalação
```python
from simple_rag.utils import mask_all_pii, mask_pii
```

### Uso Básico
```python
# Mascarar todos os dados
text = """
Nome: João Silva
CPF: 123.456.789-00
Email: joao@email.com
"""

masked = mask_all_pii(text)
print(masked)
```

---

## 📋 Todos os Tipos de Mascaramento

| Tipo | Código | Exemplo |
|------|--------|---------|
| Nome | `'nome'` | `João Silva` → `J*** S****` |
| Data Nasc. | `'birth_date'` | `15/03/1953` → `**/**/****` |
| Prontuário | `'prontuario'` | `0876532` → `****532` |
| CPF | `'cpf'` | `123.456.789-00` → `123.***.***-00` |
| RG | `'rg'` | `12.345.678-9` → `12.***.***-9` |
| Email | `'email'` | `user@email.com` → `user@email.com` |
| Telefone | `'phone'` | `(11) 98765-4321` → `(**) *****-4321` |
| CEP | `'cep'` | `12345-678` → `12345-***` |
| Todos | `'all'` | Aplica todas as máscaras |

---

## 💡 Exemplos Práticos

### 1. Mascarar Apenas Nome
```python
from simple_rag.utils import mask_pii

text = "Nome: João Silva, CPF: 123.456.789-00"
masked = mask_pii(text, pii_types=['nome'])
# Resultado: Nome: J*** S****, CPF: 123.456.789-00
```

### 2. Mascarar Nome e CPF
```python
masked = mask_pii(text, pii_types=['nome', 'cpf'])
# Resultado: Nome: J*** S****, CPF: 123.***.***-00
```

### 3. Mascarar Tudo
```python
from simple_rag.utils import mask_all_pii

masked = mask_all_pii(text)
# Mascara todos os tipos de dados
```

### 4. Processar Arquivo
```python
from simple_rag.utils import mask_all_pii

with open('anamnese.txt', 'r') as f:
    content = f.read()

masked = mask_all_pii(content)

with open('anamnese_masked.txt', 'w') as f:
    f.write(masked)
```

---

## 🎯 Características Especiais

### Mascaramento de Nome
```python
# Mantém primeira letra + preposições
"Nome: João da Silva" → "Nome: J*** da S****"
"Nome: Maria de Oliveira" → "Nome: M**** de O*******"
```

### Formatos Suportados
- **Data**: DD/MM/AAAA, DD-MM-AAAA, DD.MM.AAAA
- **CPF**: XXX.XXX.XXX-XX ou XXXXXXXXXXX
- **Telefone**: (XX) XXXXX-XXXX, (XX) XXXX-XXXX, XXXXXXXXXXX

---

## 🧪 Testar

```bash
# Executar testes
python -m simple_rag.utils.test_data_masking

# Executar demonstração
python examples/demo_final_masking.py
```

---

## 📚 Documentação Completa

- **Guia Completo**: `simple_rag/utils/README_MASKING.md`
- **Novas Funções**: `examples/NOVAS_FUNCIONALIDADES.md`
- **Mascaramento de Nomes**: `examples/MASCARAMENTO_NOME.md`
- **Resumo Final**: `RESUMO_MASCARAMENTO_FINAL.md`

---

## ✅ Checklist de Uso

- [ ] Importar função de mascaramento
- [ ] Preparar texto/arquivo a ser mascarado
- [ ] Escolher tipos de dados a mascarar
- [ ] Aplicar mascaramento
- [ ] Verificar resultado
- [ ] Salvar/usar dados mascarados

---

## 🔒 O que Cada Máscara Preserva

| Tipo | Preserva | Mascara |
|------|----------|---------|
| Nome | 1ª letra + preposições | Resto do nome |
| Data Nasc. | **Nada** | Tudo |
| Prontuário | 3 últimos dígitos | Primeiros dígitos |
| CPF | 3 primeiros + 2 últimos | Meio |
| RG | 2 primeiros + 1 último | Meio |
| Email | 4 primeiros + domínio | Resto do usuário |
| Telefone | 4 últimos | DDD + primeiros |
| CEP | 5 primeiros | 3 últimos |

---

**Versão:** 1.2.0
**Atualizado:** 2025-11-09
**Status:** ✅ Pronto para uso
