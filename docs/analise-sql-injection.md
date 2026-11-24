# Análise: SQL Injection no laboratório

Revisão técnica do código e testes locais; não é transcrição do Hermes.

## Contexto e escopo

Python e SQLite em memória, uma conta fictícia, sem servidor ou acesso à
rede. Escopo: bypass do login e regressão da correção.

## Achado e evidência

A função `login` em `examples/app_vulneravel.py` concatena usuário e senha
na consulta: **CWE-89**. O usuário `' OR 1=1 -- `, com senha incorreta, gera:

```sql
SELECT username FROM users WHERE username = '' OR 1=1 -- ' AND password = 'incorreta'
```

A condição verdadeira seleciona a conta; o comentário remove a verificação
da senha. `fetchone()` encontra uma linha e o login retorna `True`.
Pré-condições: entrada controlável e ao menos uma conta no banco.

## Impacto, probabilidade e severidade

- **Confidencialidade:** bypass demonstrado, mas não há dados privados no
  programa. Em produção, dependeria dos recursos acessíveis pela sessão.
- **Integridade:** decisão de autenticação incorreta demonstrada; alteração
  de dados de negócio não foi demonstrada.
- **Disponibilidade:** nenhuma interrupção demonstrada. Este bypass não
  comprova execução de múltiplos comandos no SQLite.
- **Impacto 1:** conta fictícia e retorno booleano, sem recurso protegido.
- **Probabilidade 2:** exige execução local, com entrada simples e sem
  controle eficaz no login vulnerável.
- **Severidade 2, baixa**, pela matriz didática; confiança alta neste escopo.
  Uma aplicação pública com dados reais exige nova avaliação contextual.

## MITRE ATT&CK

[T1190 — Exploit Public-Facing Application](https://attack.mitre.org/techniques/T1190/)
é um mapeamento possível quando uma aplicação pública é explorada para
acesso inicial. Este script local não demonstra esse cenário. A fraqueza
é classificada diretamente por [CWE-89](https://cwe.mitre.org/data/definitions/89.html).

## Correção

Em `app.py`, `login` usa `WHERE username = ?` e passa `(username,)`
separadamente. O driver vincula o valor, impedindo que a entrada altere
a instrução. A parametrização é recomendada pela
[OWASP](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html).
A senha é verificada fora da consulta. A segunda falha da amostra, senha
em texto puro, foi substituída por PBKDF2-HMAC-SHA256 com 600.000 iterações
e sal individual aleatório de 16 bytes.

## Validação e limites

`python -m unittest discover -s tests -v` verifica login legítimo, senha
errada, bypass nos dois campos, usuário inexistente, aspas como dado e
armazenamento sem senha em texto puro. A revisão do caminho de login
corrigido não encontrou concatenação SQL.

Isso mitiga a injeção neste fluxo. Não é uma varredura completa ou aplicação
pronta para produção: faltam controle de tentativas, sessões, autorização,
transporte seguro e gestão do ciclo de vida das senhas. O retorno antecipado
para usuário inexistente permite diferenças de tempo. A credencial é pública
e exclusivamente didática.

**Próximo passo:** por que remover aspas seria inferior a vincular parâmetros?
