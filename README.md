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

## Execute o laboratório

Requer Python 3.11 ou superior com SQLite. Sem dependências externas, serviço
web, portas abertas ou banco persistente. Todos os dados são fictícios.
Depois de clonar ou extrair o repositório, abra a pasta que contém este
README no VS Code e use **Terminal → Novo Terminal**. Execute:

```powershell
python examples/app_vulneravel.py
python app.py
python -m unittest discover -s tests -v
```

Na amostra vulnerável, o bypass retorna `True`; na corrigida, `False`.
O login legítimo continua retornando `True`. A amostra vulnerável também
guarda senha em texto puro; a correção usa PBKDF2-HMAC-SHA256 e sal individual.
Leia a [análise](docs/analise-sql-injection.md) para entender o mecanismo e
os limites. Não disponibilize a amostra vulnerável como serviço.

## Rode o agente no Hermes

1. Siga a [instalação oficial do Hermes](https://hermes-agent.nousresearch.com/docs/getting-started/installation),
   que documenta Windows nativo e Linux/WSL2. Para a CLI no Windows, o
   comando oficial é `iex (irm https://hermes-agent.nousresearch.com/install.ps1)`.
2. Abra um novo terminal e execute `hermes setup` para configurar seu provedor
   e modelo. Pode exigir conta e ter custos conforme o provedor. Mantenha
   credenciais na configuração local, fora do repositório.
3. No terminal do VS Code, **entre na pasta deste projeto**, onde está
   `AGENTS.md`, e execute `hermes`.
4. Peça que leia `AGENTS.md`, `agent/persona.md`, o conhecimento de segurança
   e a nova skill. Confira se consegue localizar os arquivos; não presuma
   que a leitura ocorreu só porque a sessão iniciou.
5. Use os [cenários](docs/cenarios.md), registrando a pergunta de contexto,
   a análise e a revisão da correção.

Na instalação preparada nesta máquina, o diretório `skills/` já está
registrado no Hermes. Para pré-carregar a especialização explicitamente:

```powershell
./scripts/hermes-local.ps1 chat --skills vulnerability-analysis --provider openrouter --model nvidia/nemotron-3.5-lightning:free
```

Em outra máquina, registre o caminho absoluto de `skills/` na opção
`skills.external_dirs` do Hermes antes de usar esse comando. Isso permite
ler a skill diretamente do projeto, sem copiar uma versão que fique desatualizada.

Se o agente não encontrar os arquivos, confira a pasta atual e reinicie
a sessão nela. Para diagnóstico de configuração, use `hermes doctor` e
a documentação oficial. O laboratório Python funciona sem Hermes.

## Estado da entrega

Código e especialização preparados, com sete testes locais aprovados.
Hermes v0.23.4 instalado e autenticado no OpenRouter em 24/11/2026, configurado
para modelos gratuitos. No PowerShell, `./scripts/hermes-local.ps1` inicia
na pasta correta; o runtime local em `.tmp` não entra no Git.
Confira a [saída real dos testes](docs/validacao-local.txt), a
[verificação da instalação](docs/instalacao-hermes.txt) e as
[evidências](docs/evidencias.md). As três conversas foram executadas e
registradas, com [exportações visuais reais](docs/evidencias-hermes/exportacoes/README.md).
Essas imagens renderizam os logs; não são screenshots do Hermes.
A avaliação encontrou limitações de pontuação de risco e adesão ao roteiro,
documentadas sem alterar as respostas originais. A publicação pública ainda
precisa ser concluída. O [roteiro de publicação](docs/publicacao.md) explica
como conectar o repositório da sua conta e enviar o commit preparado.

Origem: DIO Agent, commit `5f5e11d95583d0eabcd883b214ef0e51bfb8889c`.
Esta é uma evolução educacional independente. Antes de entregar, revise
a skill com suas próprias palavras e consiga explicar a correção.
