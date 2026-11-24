# Fundamentos de segurança

**Vulnerabilidade** é uma fraqueza em código, configuração ou processo.
**Ameaça** é uma fonte ou evento capaz de explorar uma fraqueza.
**Risco** combina a chance de isso acontecer e suas consequências no contexto.
Uma fraqueza confirmada não significa que houve invasão.

## Tríade C/I/D

- **Confidencialidade:** restringir acesso à informação. Exemplo: impedir
  leitura de dados de outra pessoa após um bypass de login.
- **Integridade:** impedir alterações indevidas. Exemplo: proteger permissões
  e registros contra mudanças não autorizadas.
- **Disponibilidade:** manter o serviço acessível. Exemplo: evitar falhas
  causadas por consultas caras ou perda de acesso durante uma configuração.

## Matriz didática de risco

Defina o cenário antes de pontuar. Use o maior impacto plausível e justificado
entre C/I/D; não some os três. Esta matriz é local ao projeto, **não é CVSS**.

| Nota | Impacto | Probabilidade |
|---|---|---|
| 1 | Efeito restrito a dados fictícios ou função de pouco valor | Acesso restrito e pré-condições difíceis |
| 2 | Acesso indevido limitado ou interrupção recuperável | Acesso possível, com pré-condições relevantes |
| 3 | Dados sensíveis, função crítica ou dano amplo | Alvo exposto, caminho simples e controles ausentes |

Severidade = impacto × probabilidade: 1–2 baixa; 3–4 média; 6 alta;
9 crítica. Não existe produto 5, 7 ou 8 nesta escala. Registre a confiança
(baixa, média ou alta) conforme a evidência disponível. Sem dados de exposição
ou consequência, use avaliação provisória ou indeterminada; não adivinhe.
Uma amostra local pode ter severidade baixa e a mesma falha ser grave em
uma aplicação pública com dados reais.

## Práticas defensivas

- Vincule valores por parâmetros SQL. Permita apenas identificadores
  previamente definidos quando precisar de nomes dinâmicos de tabela/coluna.
- Use hash de senha apropriado, sal individual e biblioteca mantida;
  não armazene senha em texto puro nem registre segredos.
- Aplique menor privilégio, autenticação forte, atualizações, backups testados,
  segmentação, registros sem dados sensíveis e revisão de alterações.
- Valide entradas por tipo e regra de negócio como controle complementar.
- Teste a correção e o uso legítimo; registre o que ficou fora do escopo.

## Classificação e referências

CWE-89 descreve SQL Injection. ATT&CK descreve comportamento adversário;
T1190 relaciona exploração de aplicação pública a acesso inicial, e não é
sinônimo de qualquer SQL Injection. CVE identifica vulnerabilidades específicas
publicadas; não atribua um identificador inventado ao exemplo.

- [CWE-89](https://cwe.mitre.org/data/definitions/89.html)
- [OWASP: prevenção de SQL Injection](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)
- [MITRE ATT&CK T1190](https://attack.mitre.org/techniques/T1190/)
