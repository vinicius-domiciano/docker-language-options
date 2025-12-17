# docker-language-options

### Docker Image Manager CLI

Projeto em **Python + Bash + Docker** para **gerenciar imagens Docker** a partir de definições simples, permitindo:

* Criar imagens automaticamente via **Dockerfile gerado pelo sistema**
* Instalar imagens diretamente do **Docker Hub**
* Gerenciar **linguagens** e **versões** de forma centralizada
* Manter uma estrutura baseada em **Clean Architecture**

---

## 📌 Visão Geral

Este projeto fornece uma **CLI (Command Line Interface)** que abstrai a complexidade da criação e manutenção de imagens Docker. Ele utiliza arquivos de configuração (YAML/JSON) e comandos bem definidos para garantir organização, escalabilidade e fácil manutenção.

A arquitetura foi pensada seguindo princípios da **Clean Architecture**, separando regras de negócio, casos de uso, infraestrutura e interface.

---

## 🧱 Arquitetura (Clean Architecture)

```
project-root/
│
├── domain/                # Regras de negócio puras
│   ├── entities/          # Entidades (Language, Version, ImageConfig)
│   └── interfaces/        # Contratos (ports)
│
├── application/           # Casos de uso
│   ├── use_cases/         # new_language, new_version, remove_version...
│   └── services/          # Orquestração de regras
│
├── infrastructure/        # Implementações externas
│   ├── docker/            # Dockerfile generator, docker build/run
│   ├── filesystem/        # YAML/JSON handlers
│   └── shell/             # Execução de comandos bash
│
├── interfaces/            # Interface com o usuário
│   └── cli/               # argparse / commands
│
├── config/
│   └── languages.yaml     # Definição das linguagens e versões
│
├── main.py                # Entry point
└── README.md
```

---

## ⚙️ Requisitos

* Python **3.10+**
* Docker instalado e configurado
* Linux / WSL / macOS (Windows com Docker Desktop funciona)

---

## 🚀 Uso

### Comando base

```bash
python main.py --option <command> [arguments]
```

### Help

```bash
python main.py -h
```

### Opções disponíveis

```
--option {new:language,new:version,rm:language,rm:version,ch:version,conf:prepare}
```

---

## 🧪 Exemplos de Uso

### ➕ Criar nova linguagem

```bash
python main.py --option new:language --language python
```

### ➕ Criar nova versão de uma linguagem

```bash
python main.py --option new:version --language python --version 3.12
```

### ❌ Remover versão

```bash
python main.py --option rm:version --language python --version 3.9
```

### 🔄 Alterar versão ativa

```bash
python main.py --option ch:version --language python --version 3.12
```

---

## 🧩 Preparar configuração via JSON

### Tipos aceitos

```
--type {JSON, JSON_PATH}
```

### JSON direto

```bash
python main.py --option conf:prepare --type JSON
```

### JSON via arquivo

```bash
python main.py --option conf:prepare --type JSON_PATH --file_path ./config/image.json
```

---

## ▶️ Script de Inicialização (start.sh)

O projeto inclui um script `start.sh` que serve como **atalho de execução** e **documentação viva** dos principais comandos disponíveis na CLI.

### Exemplo de `start.sh`

```bash
#!/bin/bash

### help
python3 -m sources.main --help

### Insert new language
# python3 -m sources.main --option=new:language --language=node

### Insert new version with JSON_PATH
# python3 -m sources.main --option=new:version --type=JSON_PATH \
#     --file_path=./sources/insert_new_dockerfile_version.json
#     # ou
#     --file_path=./sources/insert_new_image_version.json

### Remove Language:
# python3 -m sources.main --option=rm:language --language=java

### Remove version
# python3 -m sources.main --option=rm:version --language=java --version=java11

### Change version
# python3 -m sources.main --option=ch:version --language=java --version=java11

### Configure Project, create file aliases.sh and add to .bashrc
# python3 -m sources.main --option=conf:prepare

# reload_aliases
```

### Objetivo do script

* Centralizar os comandos disponíveis
* Facilitar testes manuais
* Servir como referência rápida para novos desenvolvedores
* Evitar erros de digitação em comandos longos

> 💡 Recomenda-se manter apenas **um comando ativo por vez**, comentando os demais.

---

## 🐳 Dockerfile Automático

O sistema gera o **Dockerfile dinamicamente** com base:

* Linguagem
* Versão
* Dependências
* Comandos de build

Exemplo gerado:

```Dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "main.py"]
```

---

## 📄 Configuração (languages.yaml)

```yaml
python:
  versions:
    - 3.10
    - 3.11
    - 3.12
  default: 3.12
```

---

## 🧠 Princípios Aplicados

* Clean Architecture
* Dependency Inversion
* CLI desacoplada do domínio
* Infraestrutura substituível (Docker, filesystem, shell)

---

## 📌 Próximos Passos (Sugestões)

* [ ] Logs estruturados
* [ ] Testes unitários nos use cases
* [ ] Plugin para novas linguagens
* [ ] Exportação de imagens versionadas
* [ ] Publicação no PyPI

---

## 🧑‍💻 Autor

Projeto criado para facilitar o gerenciamento de ambientes Docker com foco em **produtividade**, **padronização** e **manutenibilidade**.

Se quiser, posso:

* Ajustar o README ao código real
* Criar diagrama da arquitetura
* Criar testes base
* Revisar se está 100% Clean Architecture
