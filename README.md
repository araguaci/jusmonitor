# JusMonitor

Painel **open-source** de monitoramento do Judiciário brasileiro.

- **Captura institucional** — penduricalhos, corrupção judicial, CNJ, chokepoints do STF
- **Decisões de impacto** — HCs, solturas, progressões e arquivamentos em crimes violentos

**URL canônica:** [https://jusmonitor.vercel.app](https://jusmonitor.vercel.app)  
**Repositório:** [github.com/araguaci/jusmonitor](https://github.com/araguaci/jusmonitor)  
**Licença:** [CC0 1.0](LICENSE)  
**Fonte de dados:** corpus [lawfare-timeline](https://lawfare-timeline.vercel.app) + sidecar T-209 JustiçaWatch

## Quickstart

```bash
# regenerar data/unified.json
python scripts/build-unified.py

# validar schema
python scripts/validate-schema.py

# servir localmente
python -m http.server 8080
# abrir http://localhost:8080
```

## Stack

Site estático (HTML/CSS/JS) + JSON em `/data/` + deploy Vercel (`vercel.json`).

| Arquivo | Papel |
|---------|--------|
| `index.html` + `app.js` + `styles.css` | UI premium com filtros |
| `data/unified.json` | Feed unificado (gerado) |
| `data/captura.json` | Seed captura (extract lawfare) |
| `data/decisoes-source.json` | Seed T-209 JustiçaWatch |
| `scripts/build-unified.py` | Merge + normalização |
| `scripts/validate-schema.py` | CI / validação local |

## Docs

- [Architecture](docs/ARCHITECTURE.md)
- [Data schema](docs/DATA_SCHEMA.md)
- [Metodologia](docs/METODOLOGIA.md)
- [Roadmap](docs/ROADMAP.md)
- [Contribuir](CONTRIBUTING.md)

## Modelos

UI e schema inspirados nos artefatos `gosurf.site/artigos/jusmonitor.html` (feed JusMonitor) e `jusmonitor-backup.html` (JustiçaWatch).
