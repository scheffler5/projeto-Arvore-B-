# 🚀 GabrielSQL Database Engine

<div align="center">

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![Structure](https://img.shields.io/badge/Structure-B%2B%20Tree-green?style=for-the-badge)
![Storage](https://img.shields.io/badge/Storage-Disk%20Persistence-orange?style=for-the-badge)

</div>

---

### 📖 Sobre o Projeto

Um **SGBD (Sistema Gerenciador de Banco de Dados)** construído do zero em Python.
Este projeto implementa um *Storage Engine* completo baseado na estrutura de dados **Árvore B+ (B+ Tree)**, simulando operações reais de I/O em disco, paginação de memória e persistência binária.

O objetivo é demonstrar como bancos de dados relacionais (como MySQL ou PostgreSQL) funcionam "por baixo do capô", gerenciando grandes volumes de dados de forma eficiente.

---

## 🧠 Funcionalidades Principais

* **Persistência Real:** Os dados não ficam apenas na RAM. Tudo é serializado e salvo em arquivos binários (`.db`) simulando blocos de disco.
* **Árvore B+ Completa:** Implementação algorítmica robusta com **Splits Proativos** (divisão de nós cheios antes da descida) e crescimento dinâmico.
* **Disk Manager Customizado:** Simula um HD físico, controlando leitura e escrita de páginas (Pages) de tamanho fixo (ex: 4KB) e contabilizando estatísticas de uso.
* **SQL Parser:** Interpretador de comandos capaz de entender instruções SQL básicas (`CREATE`, `INSERT`, `SELECT`, `SOURCE`).
* **Auto-Increment Inteligente:** Gerenciamento automático de Chaves Primárias (PK).
* **Análise de Performance:** Ferramenta de benchmark integrada para medir tempo de inserção vs. busca e auditar a estrutura da árvore.

---

## 📂 Estrutura do Projeto

O projeto segue uma arquitetura modular, separando a lógica de armazenamento da interface do usuário.

```text
GabrielSQL/
│
├── Main.py                  # 🏁 Ponto de entrada (Console SQL Interativo)
│
├── Tabelas/                 # ⚙️ O "Core" do Banco de Dados
│   ├── bplustree.py         # Lógica da Árvore (Insert, Search, Split, Navegação)
│   ├── node.py              # Estrutura do Nó/Página (Keys, Children, Values)
│   └── disk_manager.py      # Camada física (Leitura/Escrita de bytes no arquivo)
│
├── Comandos/                # 🗣️ Interpretador de Linguagem
│   ├── interpreter.py       # Regex para entender strings SQL
│   └── processor.py         # Validação de regras e ponte para a Árvore
│
└── Analise/                 # 📊 Ferramentas de Teste & Benchmark
    ├── main_analise.py      # Executor de Benchmarks automatizados
    └── funcoes/             # Geradores de dados e auditores de estrutura

---

## 🛠️ Detalhes Técnicos

### 1. O Motor (`Tabelas/bplustree.py`)
O cérebro do sistema.
* **`insert(data)`**: Gerencia a inserção. Verifica se a raiz está cheia e realiza o *Root Split* se necessário.
* **`_insert_non_full`**: Navega recursivamente até a folha. Usa a técnica de *Proactive Split* (se encontrar um filho cheio no caminho, divide antes de entrar).
* **`search(key)`**: Realiza a busca em complexidade $O(\log_t n)$, descendo da raiz até a folha correta carregando apenas as páginas necessárias.

### 2. A Memória (`Tabelas/node.py`)
A representação dos dados.
* **`to_bytes()` / `from_bytes()`**: Usa a biblioteca `pickle` para serializar o objeto Nó em um bloco de bytes exato para gravação no disco.
* **Integridade:** Garante que as chaves (`keys`) e valores (`values`) dentro de uma página estejam sempre sincronizados.

### 3. O Disco (`Tabelas/disk_manager.py`)
O simulador de Hardware.
* **`read_page(id)` / `write_page(id)`**: Faz o `seek` no arquivo físico e lê/escreve blocos de tamanho fixo (padronizado em 4096 bytes), gerando estatísticas de I/O (`[STATS]`).

---

## ⚡ Como Rodar

Certifique-se de ter o **Python 3.x** instalado. Não é necessário instalar bibliotecas externas.

### 1. Modo Console (SQL Interativo)
Execute na raiz do projeto para abrir o terminal do banco de dados:
```bash
python Main.py


### 2. Modo Benchmark (Teste de Stress)

Para ver a árvore processando grandes volumes e gerar relatórios de performance:

```bash
python Analise/main_analise.py
🧪 Teste Rápido (SQL)
Copie e cole a sequência abaixo no console do Main.py para testar todas as funcionalidades:

##1. Criar uma tabela:
```sql
CREATE TABLE usuarios (id INT PRIMARY KEY, nome STR, cargo STR)

##2. Inserir dados (Auto-Increment ativado com NULL):

```sql
INSERT INTO usuarios VALUES (NULL, Gabriel, Admin)


```sql
INSERT INTO usuarios VALUES (NULL, Ana, Developer)

##3. Buscar um registro pela Chave Primária:


```sql
SELECT * FROM usuarios WHERE id = 1


Resultado Esperado: Você verá logs de [DISK] e [STATS] mostrando exatamente quantas leituras e escritas foram necessárias no disco físico para realizar cada operação.

📊 Performance Esperada
Exemplo de output do módulo de análise:

Plaintext

OPERAÇÃO        | QTD      | MÉDIA (s)    
---------------------------------------
INSERT          | 1000     | 0.000712     
SELECT_PK       | 1000     | 0.000176 
    
Nota: O SELECT é drasticamente mais rápido que o INSERT, comprovando a eficiência da estrutura B+ Tree para leitura de dados.