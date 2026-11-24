# Publicar na sua conta

O projeto local está preparado na branch `main`, com as alterações registradas
em commit. Nenhum repositório público foi criado nesta preparação. O remoto
original da DIO foi renomeado para `upstream`; `origin` fica reservado para
o repositório da sua conta.

Crie na sua conta um repositório **público** chamado
`dio-agent-security-mentor`, sem inicializar README, licença ou gitignore.
No terminal aberto nesta pasta, confira:

```powershell
git status --short
git remote -v
```

Copie a URL HTTPS do repositório da sua conta e use
`git remote add origin URL_COPIADA`, substituindo `URL_COPIADA` pela URL real.
Depois execute `git push -u origin main`. Não inclua credenciais na URL.
O envio usará a autenticação normal do GitHub no seu computador. Se `origin`
já existir, confira sua URL antes de alterá-lo; não use force push.

## Arquivo para transferência

O arquivo `dio-agent-security-mentor.zip`, ao lado da pasta `Projeto 3`,
contém somente os arquivos versionados do commit preparado. Não inclui
`.git`, ambientes Python, runtime do Hermes, configurações locais ou segredos.
Ele serve para transportar o projeto; não é o link a entregar no desafio.
Para publicar pelo site do GitHub, extraia o ZIP e envie os arquivos extraídos
usando **Add file → Upload files**, preservando as pastas. Não envie apenas
o ZIP como conteúdo do repositório.

Abra a raiz do repositório em janela anônima para confirmar visibilidade
pública e links. Envie a URL do repositório, não a de um arquivo.

## Checklist

- [x] Skill com `name` e `description` registrada no `AGENTS.md`.
- [x] Conhecimento, persona e todos os links do README revisados.
- [x] Testes somente no laboratório próprio.
- [x] Conversas reais no Hermes, logs e exportações PNG adicionados.
- [ ] Opcional: complementar com screenshots nativos da interface.
- [ ] Repositório público na sua conta, com nome minúsculo e sem acento.
- [ ] Link da raiz conferido em janela anônima.

Para atualizar a base futuramente, revise as alterações de `upstream`
antes de integrá-las, preservando sua especialização.
