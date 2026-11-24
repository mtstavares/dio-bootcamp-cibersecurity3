"""Coleta autorizada de conversas reais no Hermes e OpenRouter gratuito.

Exemplo: python scripts/coletar-evidencias-hermes.py 03-ubuntu-contexto-novo
Requer Hermes autenticado e skills/ registrado em skills.external_dirs.
Transmite os arquivos didaticos ao provedor; nao executa alvos externos.
"""

import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parents[1]
out = root / 'docs' / 'evidencias-hermes'
out.mkdir(exist_ok=True)
launcher = Path(os.environ['LOCALAPPDATA']) / 'hermes/bin/hermes.exe'
prompts = {
    '01-analise-vulneravel': 'Leia AGENTS.md, agent/persona.md, agent/knowledge/security-basics.md e skills/vulnerability-analysis/SKILL.md. Sou dono deste laboratorio local, sem rede, com dados ficticios. Pode executar somente os testes Python locais. Como mentor de AppSec, analise examples/app_vulneravel.py, explique o bypass, relacione CWE e MITRE ATT&CK com suas limitacoes e me ajude a entender como corrigir. Use o formato padronizado da skill. Nao altere arquivos. Nao leia docs/analise-sql-injection.md nem outros relatorios prontos; derive a analise do codigo. Responda em portugues.',
    '02-revisao-corrigida': 'Leia AGENTS.md, agent/persona.md, agent/knowledge/security-basics.md e skills/vulnerability-analysis/SKILL.md. Sou dono deste laboratorio local, sem rede e com dados ficticios. Revise app.py e execute python -m unittest discover -s tests -v. O SQL Injection foi mitigado neste caminho? Mostre evidencias, confira o login legitimo e explique o que a validacao nao cobre. Use o formato da skill. Nao altere arquivos e nao leia relatorios prontos em docs. Responda em portugues.',
    '03-ubuntu-contexto': 'Tenho um servidor Ubuntu exposto na internet. Quero deixa-lo mais seguro. Que comando devo executar primeiro?',
}
if len(sys.argv) != 2:
    raise SystemExit('Uso: python scripts/coletar-evidencias-hermes.py 03-ubuntu-contexto-novo')
key = sys.argv[1]
if key[:2] not in ('01', '02', '03') or any(c not in 'abcdefghijklmnopqrstuvwxyz0123456789-' for c in key):
    raise SystemExit('Use um identificador seguro iniciado por 01, 02 ou 03.')
prompt = prompts[key[:2] + {'01': '-analise-vulneravel', '02': '-revisao-corrigida', '03': '-ubuntu-contexto'}[key[:2]]]
if key.startswith('01') and key.endswith('final'):
    prompt += ' Execute python examples/app_vulneravel.py e registre a saida real antes de concluir a analise. Nao trate resultados esperados como observados.'
prompt_file = out / (key + '-prompt.txt')
if any(out.glob(key + '-*')):
    raise SystemExit('Ja existem registros com esse identificador. Use outro sufixo para preserva-los.')
prompt_file.write_text(prompt, encoding='utf-8')
model = 'nvidia/nemotron-3.5-lightning:free'
command = [str(launcher), 'chat', '--in', str(root), '--oneshot', '--query-file', str(prompt_file), '--provider', 'openrouter', '--model', model, '--toolsets', 'file,terminal,skills', '--skills', 'vulnerability-analysis', '--max-turns', '12', '--format', 'stream-json']
env = {**os.environ, 'HERMES_HOME': str(Path(os.environ['LOCALAPPDATA']) / 'hermes'), 'PYTHONIOENCODING': 'utf-8', 'PYTHONUTF8': '1'}
start = datetime.datetime.now(datetime.timezone.utc).isoformat()
skill_hash = hashlib.sha256((root / 'skills/vulnerability-analysis/SKILL.md').read_bytes()).hexdigest()
with (out / (key + '-eventos.jsonl')).open('w', encoding='utf-8') as stdout, (out / (key + '-diagnostico.txt')).open('w', encoding='utf-8') as stderr:
    process = subprocess.run(command, cwd=root, env=env, stdout=stdout, stderr=stderr, timeout=330)
metadata = {'started_utc': start, 'finished_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'harness': 'Hermes Agent v0.23.4 official CLI', 'source_commit': '8fc0374447313e276f6b9a2764bfc750190c966a', 'provider': 'openrouter', 'requested_model': model, 'cwd': str(root), 'exit_code': process.returncode, 'command': command[1:]}
metadata['skill_sha256_at_start'] = skill_hash
(out / (key + '-metadados.json')).write_text(json.dumps(metadata, indent=2, ensure_ascii=False), encoding='utf-8')
print(key, 'exit_code=', process.returncode, flush=True)
for line in (out / (key + '-eventos.jsonl')).read_text(encoding='utf-8').splitlines():
    try:
        event = json.loads(line)
    except ValueError:
        continue
    if event.get('type') == 'result':
        print(json.dumps(event, ensure_ascii=False), flush=True)
raise SystemExit(process.returncode)
