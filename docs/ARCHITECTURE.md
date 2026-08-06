# Architecture

```
lawfare-timeline/_data/lawfare.json
        │
        ▼
extract_jusmonitor.py  ──►  jusmonitor_data.json  ──►  data/captura.json
        │
justicawatch sidecar (T-209)  ──►  data/decisoes-source.json
        │
data/contributions/*.json  (PRs comunidade)
        │
        ▼
scripts/build-unified.py
        │
        ▼
data/unified.json  (+ captura-cards.json, decisoes.json)
        │
        ▼
index.html / app.js  ← fetch('/data/unified.json')
```

## Trilhas

| `track` | Origem | Grupos |
|---------|--------|--------|
| `captura_institucional` | extract JusMonitor | penduricalhos, corrupcao_judicial, cnj_disciplinar, chokepoint_stf, eleitoral_tse, outros_judiciario |
| `decisoes_impacto` | T-209 JustiçaWatch | soltura_hc, progressao_regime, arquivamento, jurisprudencia_estrutural, foragidos_impacto |

## Regras R1–R7 (schema 1.1.0)

Assimiladas em `docs/METODOLOGIA.md`, `docs/DATA_SCHEMA.md` e `docs/schema.json`.

- **R1** — `ev-confirmed` exige URL real em `fontes[]` (hard-fail em `build-unified.py` e `validate-schema.py`)
- **R3/R4** — `conflitos_resolvidos` e `divergencias_nao_reconciliadas` propagam de `decisoes-source.json` para `unified.json`
- **R5** — campos `promovido_em` / `promovido_por` preservados na normalização
- Curadoria opcional preservada: `lawfare_id`, `analise`, `lacuna_investigativa`, `ponto_de_inflexao`

## Deploy

- Vercel: root estático, `cleanUrls`, cache 300s em `/data/*`
- Regenerar JSON no CI local / pré-commit editorial antes do push

## Relação com outros repos

| Repo | Papel |
|------|--------|
| `lawfare-timeline` | Corpus canônico + scripts extract |
| `gosurf.site` | Espelho editorial; `/jusmonitor` aponta para este domínio |
| `jusmonitor.vercel.app` | Produto canônico |
