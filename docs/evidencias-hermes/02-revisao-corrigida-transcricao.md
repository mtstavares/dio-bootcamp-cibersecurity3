# Revisão da correção e testes

Data UTC: 2026-11-24T11:36:40.449868+00:00

Provedor: openrouter

Modelo solicitado: `openrouter/free`

Sessão: `local-3e22241a399ba8c7e21d600ba3f236cf4ca0daf267b3da2b17de1f5f37aebe81`

Exit code: 0

## Prompt enviado

Leia AGENTS.md, agent/persona.md, agent/knowledge/security-basics.md e skills/vulnerability-analysis/SKILL.md. Sou dono deste laboratorio local, sem rede e com dados ficticios. Revise app.py e execute python -m unittest discover -s tests -v. O SQL Injection foi mitigado neste caminho? Mostre evidencias, confira o login legitimo e explique o que a validacao nao cobre. Use o formato da skill. Nao altere arquivos e nao leia relatorios prontos em docs. Responda em portugues.

## Resposta literal do Hermes

Contexto e escopo:
- Autorização: você é dono deste laboratório local, sem rede, com dados fictícios. Escopo aprovado para análise defensiva deste laboratório.
- Ambiente: Windows local, Python, SQLite em memória.
- Exposição: nenhuma (sem servidor HTTP). Lacuna: escopo limitado à função de login e ao banco criados para o lab.

Achado e evidência:
- No caminho corrigido (app.py, linhas 30-37), a query usa placeholder vinculado: "SELECT salt, password_hash FROM users WHERE username = ?" com os valores na tupla (username,). Não há concatenação, f-string nem interpolação. A senha nunca vai para SQL: é processada com hash PBKDF2-HMAC-SHA256 (salt individual, 600 mil iterações) e comparada com hmac.compare_digest.
- No caminho vulnerável (examples/app_vulneravel.py, linhas 15-20), a query era montada por concatenação de strings, o que permitia o bypass.
- Evidência de execução: rodei "python -m unittest discover -s tests -v" e os 7 testes passaram (OK). Rodei "python app.py" e obtive: "Login legítimo: True" e "Bypass por SQL Injection: False".

Impacto (C/I/D):
- Confidencialidade: bypass autenticando como outro usuário foi reproduzido no lab vulnerável; no corrigido, bloqueado. Impacto plausível de leitura de conta, restrito a dado fictício neste laboratório.
- Integridade: possível sujeição de identidade/autenticação.
- Disponibilidade: não impactada neste cenário local.

Probabilidade:
- No contexto local (sem rede, ambiente controlado), probabilidade de exploração real avaliada como baixa. Confiança média, pois faltam dados de exposição real.

Severidade:
- Impacto x probabilidade na escala didática local: baixa no lab (dado fictício); faixa que seria alta/crítica se houvesse dados reais. Não é CVSS.

MITRE ATT&CK:
- T1190 com ressalva: aplicação local sem exposição pública; a técnica se relaciona à exploração de app exposto para acesso inicial, mas aqui o contexto local justifica a análise e o script local não comprova uso real dessa técnica.

Correção:
- Causa tratada: query construída por concatenação. Correção aplicada: valores vinculados como parâmetros (?), hash com salt individual e comparação com compare_digest.
- Risco residual: a proteção cobre a superfície de login testada; validação de entrada por si só não blinda contra SQL Injection (é a parametrização que protege). Falhas em outros pontos da aplicação não foram cobertas.

Validação:
- Comando executado: "python -m unittest discover -s tests -v" -> 7 testes, resultado OK.
- Evidência adicional: "python app.py" -> Login legítimo: True; Bypass por SQL Injection: False.
- Limitação: teste de regressão e execução local não certificam segurança de todo o sistema.

Próximo passo: para verificar seu entendimento, me diga: por que a correção usa "?" (placeholder) em vez de tentar "filtrar" caracteres especiais como aspas no input?

## Saídas literais de terminal

```text
{'output': "dir: cannot access '/b': No such file or directory\ndir: cannot access '/s': No such file or directory\nC\\:\\\\Users\\\\<usuario>\\\\Desktop\\\\Projetos Matheus\\\\Projeto BootCamp\\\\Projeto 3\\\\tests:\n__pycache__  test_login.py", 'exit_code': 2, 'error': None}
```

```text
{'output': 'test_fixed_does_not_store_plaintext_password (test_login.LoginTests.test_fixed_does_not_store_plaintext_password) ... ok\r\ntest_fixed_handles_quotes_as_data (test_login.LoginTests.test_fixed_handles_quotes_as_data) ... ok\r\ntest_fixed_unknown_user (test_login.LoginTests.test_fixed_unknown_user) ... ok\r\ntest_reproduce_and_block_password_bypass (test_login.LoginTests.test_reproduce_and_block_password_bypass) ... ok\r\ntest_reproduce_and_block_username_bypass (test_login.LoginTests.test_reproduce_and_block_username_bypass) ... ok\r\ntest_valid_login_in_both_versions (test_login.LoginTests.test_valid_login_in_both_versions) ... ok\r\ntest_wrong_password_in_both_versions (test_login.LoginTests.test_wrong_password_in_both_versions) ... ok\r\n\r\n----------------------------------------------------------------------\r\nRan 7 tests in 0.786s\r\n\r\nOK', 'exit_code': 0, 'error': None}
```

```text
{'output': 'Login legítimo: True\r\nBypass por SQL Injection: False', 'exit_code': 0, 'error': None}
```

