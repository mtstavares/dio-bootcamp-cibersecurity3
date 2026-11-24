# Análise do código vulnerável

Data UTC: 2026-11-24T11:41:36.262229+00:00

Provedor: openrouter

Modelo solicitado: `nvidia/nemotron-3.5-lightning:free`

Sessão: `local-a8667fc5e01addddea90457818481ee7927a878df9cf48c6d9ae466a106e6344`

Exit code: 0

## Prompt enviado

Leia AGENTS.md, agent/persona.md, agent/knowledge/security-basics.md e skills/vulnerability-analysis/SKILL.md. Sou dono deste laboratorio local, sem rede, com dados ficticios. Pode executar somente os testes Python locais. Como mentor de AppSec, analise examples/app_vulneravel.py, explique o bypass, relacione CWE e MITRE ATT&CK com suas limitacoes e me ajude a entender como corrigir. Use o formato padronizado da skill. Nao altere arquivos. Nao leia docs/analise-sql-injection.md nem outros relatorios prontos; derive a analise do codigo. Responda em portugues. Execute python examples/app_vulneravel.py e registre a saida real antes de concluir a analise. Nao trate resultados esperados como observados.

## Resposta literal do Hermes

A execução confirmou a vulnerabilidade. Ambos os testes retornaram `True`, incluindo o bypass. Agora vou produzir a análise no formato padronizado da skill.

---
**Análise de Vulnerabilidade: SQL Injection em `examples/app_vulneravel.py`**

- **Contexto e escopo:** Laboratório local isolado, sem rede, com dados fictícios. O proprietário tem autorização total. O código usa SQLite em memória e inclui intencionalmente uma amostra vulnerável para fins educacionais (comentado no cabeçalho e na linha 9).

- **Achado e evidência:** O `login()` (linhas 15-20) constrói a query SQL mediante concatenação de strings:
  ```python
  query = "SELECT username FROM users WHERE username = '" + username + "' AND password = '" + password + "'`
  ```
  A entrada `username` é inserida diretamente sem vinculação de parâmetros. O teste na linha 27 (`' OR 1=1 -- `) faz a query retornar verdadeiro para qualquer senha, bypassando o login. Isso exemplifica CWE-89 (SQL Injection). A execução confirmada: `Bypass por SQL Injection: True`.

- **Impacto (C/I/D):**
  - **Confidencialidade:** Bypass de login permite leitura não autorizada de todas as linhas da tabela `users`. Em produção com dados reais, isso expondo credenciais de todos os usuários.
  - **Integridade:** Dados poderiam ser alterados ou deletados após o acesso indevido.
  - **Disponibilidade:** Em cenário extremo, injeções poderiam impactar a disponibilidade do banco.
  - No ambiente de laboratório com dados fictícios, o impacto se restringe à integridade dos dados da simulação.

- **Probabilidade:** 3 (em escala 1-3). A técnica `' OR 1=1 -- ` é amplamente conhecida, o código-fonte está exposto e o ambiente não tem controles de entrada. Em produção com entrada validada, a probabilidade seria baixa, mas neste laboratório a exploração é trivial.

- **Severidade:** Impacto 3 × Probabilidade 3 = 9 (crítica) na matriz local. No entanto, como é laboratório local com dados fictícios e autorização do dono, a classificação pratica pode ser considerada **alta** para fins de treinamento, com confiança **alta** na evidência (executado e reproduzido).

- **MITRE ATT&CK:** T1190 (Exploração de Aplicação da Web para Acesso Inicial) contextualiza o padrão de comportamento adversário quando uma aplicação exposta é explorada. **Limitação:** Não se aplica plenamente aqui porque o cenário é um laboratório local isolado, não uma aplicação pública acessível na internet. A técnica de injeção de query ainda se enquadra em padrões de exploração de código, mas T1190 destina-se a acesso inicial em ambientes de produção expostos.

- **Correção:** Substituir a concatenação por vinculação de parâmetros (placeholders). O SQLite aceita `?` como placeholder:
  ```python
  # Antes (vulnerável):
  query = "SELECT username FROM users WHERE username = '" + username + "' AND password = '" + password + "'"
  
  # Depois (corrigido):
  query = "SELECT username FROM users WHERE username = ? AND password = ?"
  connection.execute(query, (username, password))
  ```
  Essa mudança elimina a causa raiz — a entrada nunca mais é interpretada como código SQL, tratando-se apenas como dado. **Risco residual:** Recomenda-se também aplicar validação de tipo e regra de negócio como controle complementar (ex: verificar se username corresponde ao padrão esperado), mas a parametrização sozinha já corrige a injecão.

- **Validação:** Execução do script original: `Bypass por SQL Injection: True` (confirmado). Após a correção (non-executado neste relatório), o esperado é que o bypass retorne `False` mantendo o login legítimo em `True`. **Limitação:** Apenas análise estática + teste do exemplo atual; não foi aplicada correção no código fonte para evitar modificar o arquivo original (conforme instrução). Uma validação completa exigiria reescrever o `login()` com parâmetros vinculados e reexecutar o script.

- **Próximo passo:** O senhor compreende a diferença entre concatenação de strings (vulnerável) e vinculação de parâmetros/placeholders (correção)? A mudança elimina a causa pois a entrada do usuário nunca mais influencia a estrutura da query SQL.

---
**Resumo:** O código apresenta SQL Injection clássico (CWE-89) pela construção de query via concatenação. A execução confirmou o bypass. A correção consiste em usar parâmetros vinculados (`?` no SQLite). Em ambiente local com dados fictícios e autorização, a severidade é alta para fins de treinamento, mas o risco real seria crítico em aplicação de produção com dados sensíveis.

## Saídas literais de terminal

```text
{'output': '/usr/bin/bash: line 10: cd: too many arguments', 'exit_code': 2, 'error': None}
```

```text
{'output': 'Login legítimo: True\r\nBypass por SQL Injection: True', 'exit_code': 0, 'error': None}
```

