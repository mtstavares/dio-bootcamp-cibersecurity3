"""Exporta registros reais em Markdown e PNG; nao simula telas do Hermes.

Requer Pillow apenas para a exportacao visual: python -m pip install Pillow
Execute na raiz: python scripts/exportar-evidencias.py
"""

import json
from pathlib import Path
import textwrap

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / 'docs/evidencias-hermes'
EXPORT = EVIDENCE / 'exportacoes'
SELECTED = {
    '01-analise-vulneravel-final': 'Análise do código vulnerável',
    '02-revisao-corrigida': 'Revisão da correção e testes',
    '03-ubuntu-contexto-escopo': 'Perguntas antes de comandos',
}


def png_pages(stem, title, content):
    """Renderiza o texto integral; a quebra de linhas nao altera as palavras."""
    font = ImageFont.truetype('C:/Windows/Fonts/consola.ttf', 18)
    heading = ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf', 26)
    note = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 16)
    lines = []
    for original in content.splitlines():
        lines.extend(textwrap.wrap(original, width=91, replace_whitespace=False,
                                   drop_whitespace=False) or [''])
    chunks = [lines[i:i + 52] for i in range(0, len(lines), 52)] or [[]]
    paths = []
    for page, chunk in enumerate(chunks, 1):
        image = Image.new('RGB', (1080, 170 + 25 * len(chunk)), '#f7f9fc')
        draw = ImageDraw.Draw(image)
        draw.rectangle((0, 0, 1080, 104), fill='#14283f')
        draw.text((28, 15), title, font=heading, fill='white')
        draw.text((28, 54), 'Exportação do registro real — não é captura de tela do Hermes.', font=note, fill='#d4e5f4')
        draw.text((28, 78), f'24/11/2026 • página {page}/{len(chunks)} • texto sem correção editorial', font=note, fill='#d4e5f4')
        for index, line in enumerate(chunk):
            draw.text((28, 124 + index * 25), line, font=font, fill='#172b40')
        path = EXPORT / f'{stem}-p{page:02}.png'
        image.save(path)
        paths.append(path)
    return paths


def main():
    EXPORT.mkdir(exist_ok=True)
    index = ['# Exportações dos registros reais', '',
             'As imagens abaixo renderizam as transcrições integrais e as saídas das ferramentas.',
             '**Não são screenshots do terminal nem da interface do Hermes.**', '',
             'Consulte [a avaliação crítica](../../evidencias.md) antes de interpretar as respostas.', '']
    for key, title in SELECTED.items():
        events = [json.loads(line) for line in (EVIDENCE / f'{key}-eventos.jsonl').read_text(encoding='utf-8').splitlines() if line.strip()]
        result = next(event for event in reversed(events) if event.get('type') == 'result')
        meta = json.loads((EVIDENCE / f'{key}-metadados.json').read_text(encoding='utf-8'))
        prompt = (EVIDENCE / f'{key}-prompt.txt').read_text(encoding='utf-8')
        terminals = [event for event in events if event.get('type') == 'tool_result' and event.get('name') == 'terminal']
        text = f"# {title}\n\nData UTC: {meta['started_utc']}\n\nProvedor: {meta['provider']}\n\nModelo solicitado: `{meta['requested_model']}`\n\nSessão: `{result['session_id']}`\n\nExit code: {result['exit_code']}\n\n## Prompt enviado\n\n{prompt}\n\n## Resposta literal do Hermes\n\n{result['text']}\n\n## Saídas literais de terminal\n\n"
        tool_texts = []
        for event in terminals:
            output = json.loads(event['output']) if isinstance(event['output'], str) else event['output']
            tool_texts.append(str(output))
            text += '```text\n' + str(output) + '\n```\n\n'
        if not terminals:
            text += 'Nenhuma execução de terminal registrada nesta sessão.\n'
        (EVIDENCE / f'{key}-transcricao.md').write_text(text, encoding='utf-8')
        index.extend([f'## {title}', '', f'[Transcrição integral](../{key}-transcricao.md)', ''])
        visual = f"Modelo solicitado: {meta['requested_model']}\nSessão: {result['session_id']}\n\nPROMPT\n{prompt}\n\nRESPOSTA LITERAL\n{result['text']}"
        paths = png_pages(key, title, visual)
        if tool_texts:
            paths.extend(png_pages(key + '-terminal', title + ' / terminal', '\n\n'.join(tool_texts)))
        for path in paths:
            index.extend([f'![{title} — {path.stem}]({path.name})', ''])
    (EXPORT / 'README.md').write_text('\n'.join(index), encoding='utf-8')
    print('Exported 3 genuine transcripts and', len(list(EXPORT.glob('*.png'))), 'PNG pages.')


if __name__ == '__main__':
    main()
