# Contribuindo para o JusMonitor

Obrigado por ajudar a documentar o Judiciário brasileiro com fontes verificáveis.

## Regras

1. **Fontes primeiro** — links oficiais (STF, STJ, CNJ, tribunais) ou jornalismo primário
2. **Sem acusação** — registre a decisão/evento e o impacto público; não atribua dolo sem fonte
3. **Schema** — siga [docs/DATA_SCHEMA.md](docs/DATA_SCHEMA.md)
4. **Curadoria** — PRs em `data/contributions/` não entram no feed até merge + rebuild

## Como propor um caso

### Opção A — Issue

Abra uma issue com o template **Novo caso (captura)** ou **Novo caso (decisão)**.

### Opção B — Pull Request

1. Fork + branch
2. Adicione `data/contributions/meu-caso.json` (um card ou `{ "cards": [...] }`)
3. Rode localmente:

```bash
python scripts/build-unified.py
python scripts/validate-schema.py
```

4. Abra o PR usando o template

## Licença

Ao contribuir, você dedica o material ao domínio público sob **CC0 1.0**.
