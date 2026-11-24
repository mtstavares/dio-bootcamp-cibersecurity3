# DIO Agent — Mentor de cibersegurança

Especialização do [DIO Agent](https://github.com/digitalinnovationone/dio-agent)
para aprender análise defensiva de vulnerabilidades com contexto, evidências
e correções verificáveis. O objetivo é desenvolver raciocínio de AppSec e
entender o ambiente antes de sugerir comandos. Não há treinamento de modelo:
o comportamento é orientado por arquivos Markdown.

## Melhoria escolhida

**Relatório padronizado:** contexto, achado, impacto em confidencialidade,
integridade e disponibilidade, probabilidade, severidade, MITRE ATT&CK,
correção e validação. Uma matriz didática permite comparar cenários com
justificativas e indicação de incerteza. Não é CVSS.

| Skill adicionada | Quando usar | Processo |
|---|---|---|
| Análise de vulnerabilidades | Revisão defensiva de código ou infraestrutura de laboratório | [SKILL.md](skills/vulnerability-analysis/SKILL.md) |

As seis skills originais foram preservadas. A lista completa está no
[AGENTS.md](AGENTS.md) e o guia original em [README-base.md](README-base.md).

## Arquivos criados e alterados

| Arquivo | Papel |
|---|---|
| [skills/vulnerability-analysis/SKILL.md](skills/vulnerability-analysis/SKILL.md) | Roteiro do agente com `name` e `description` |
| [skills/vulnerability-analysis/README.md](skills/vulnerability-analysis/README.md) | Explicação para pessoas |
| [agent/knowledge/security-basics.md](agent/knowledge/security-basics.md) | Conceitos, C/I/D, matriz e boas práticas |
| [agent/persona.md](agent/persona.md) | Especialização defensiva da persona |
| [AGENTS.md](AGENTS.md) | Registro da skill e do conhecimento |
| [examples/app_vulneravel.py](examples/app_vulneravel.py) | Login vulnerável isolado, em memória |
| [app.py](app.py) | Login corrigido com parâmetros e hash de senha com sal |
| [tests/test_login.py](tests/test_login.py) | Reprodução e regressão da falha |
| [docs/analise-sql-injection.md](docs/analise-sql-injection.md) | Análise técnica do laboratório |
| [docs/cenarios.md](docs/cenarios.md) | Prompts e critérios para testar o agente |
| [docs/evidencias.md](docs/evidencias.md) | Evidências reais e roteiro de capturas |
| [docs/publicacao.md](docs/publicacao.md) | Publicação na sua conta |

