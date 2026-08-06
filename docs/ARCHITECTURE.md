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

## Deploy

- Vercel: root estático, `cleanUrls`, cache 300s em `/data/*`
- Regenerar JSON no CI local / pré-commit editorial antes do push

## Relação com outros repos

| Repo | Papel |
|------|--------|
| `lawfare-timeline` | Corpus canônico + scripts extract |
| `gosurf.site` | Espelho editorial; `/jusmonitor` aponta para este domínio |
| `jusmonitor.vercel.app` | Produto canônico |
