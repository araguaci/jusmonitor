# JusMonitor

## 🛡️ Sentinel Status
- **Status:** 🟢 Produção
- **Tier:** A
- **Health:** 85% / **ROI Potencial:** open data cívico (CC0) — funil reputacional para corpus lawfare-timeline
- **Stack:** HTML/CSS/JS, Python, JSON estático, Vercel

---

Painel open-source de monitoramento do Judiciário brasileiro: captura institucional (penduricalhos, corrupção judicial, CNJ, chokepoints) e decisões de alto impacto (HCs, solturas, progressões, arquivamentos), com classificação evidencial R1–R7 e trilha de fontes.

**URL canônica:** [https://jusmonitor.vercel.app](https://jusmonitor.vercel.app)  
**Repositório:** [github.com/araguaci/jusmonitor](https://github.com/araguaci/jusmonitor)  
**Licença:** [CC0 1.0](LICENSE)  
**Fonte de dados:** corpus [lawfare-timeline](https://lawfare-timeline.vercel.app) + sidecar T-209 JustiçaWatch

## Ecossistema SELVA

Mesma disciplina: **fonte auditável, hipótese ≠ fato**, deploy público rastreável. Cada hub tem escopo próprio — não misturar categorias.

| Projeto | URL | Papel |
|---|---|---|
| **JusMonitor** (este) | [jusmonitor.vercel.app](https://jusmonitor.vercel.app/) | Captura institucional + decisões de impacto (R1–R7, CC0) |
| **Lawfare Timeline** | [lawfare-timeline.vercel.app](https://lawfare-timeline.vercel.app/) | Corpus upstream / linha do tempo com fonte auditável |
| **Ecosistema Selva** | [ecosistema-selva.vercel.app](https://ecosistema-selva.vercel.app/) | Meta-hub Sentinel — saúde e navegação dos hubs |
| **Observatório Civil BR** | [observatorio-civil-br.vercel.app](https://observatorio-civil-br.vercel.app/) | Hub investigativo — artefatos e padrões P01–P11 |
| **GoSurf** | [gosurf.site](https://gosurf.site) | Análises, dossiês e insights (ponte editorial) |
| **República Sequestrada** | [republica-sequestrada-hub.vercel.app](https://republica-sequestrada-hub.vercel.app/) | Hub narrativo do eixo |
| **Sabor Brazil** | [sabor-brazil.vercel.app](https://sabor-brazil.vercel.app/) | Catálogo — o nome não é a coisa |
| **Série Demográfica** | [serie-demografica.vercel.app](https://serie-demografica.vercel.app/) | Observatório de mortalidade 2014–2025 |
| **Vítimas do Estado** | [vitimas-do-estado.vercel.app](https://vitimas-do-estado.vercel.app/) | Registro de falha estatal com dano irreversível |
| **Geoengenharia** | [geoengenharia.vercel.app](https://geoengenharia.vercel.app/) | Patentes e modificação climática |
| **O Dragão e a Onça** | [odragaoeaonca.vercel.app](https://odragaoeaonca.vercel.app/) | Série Brasil × China |
| **Abuso Supremo** | [abusosupremo.vercel.app](https://abusosupremo.vercel.app/) | Cronologia de censura 2019–2025 |

Nav canônica (monorepo): `sabor-brazil/data/ecosystem.json` · espelho local: [`data/ecosystem.json`](data/ecosystem.json).  
Eixo Sentinel: [`SENTINEL-EIXO-SELVA.md`](https://github.com/araguaci/ai-projects/blob/main/docs/estrategia/SENTINEL-EIXO-SELVA.md) · meta-hub: [ecosistema-selva.vercel.app](https://ecosistema-selva.vercel.app/).

## 🎯 Visão Geral

O debate público sobre o Judiciário é episódico: manchete, indignação, esquecimento. O JusMonitor mantém um feed verificável e atualizável — cada card com `evidence_status`, fontes URL e regras de reconciliação — para que padrões (penduricalhos, liminares, tráfico privilegiado) não sumam da memória coletiva.

Duas trilhas, um schema (`1.1.0`): `captura_institucional` e `decisoes_impacto`, mescladas em `data/unified.json`.

## 📊 Viabilidade & ROI (Sentinel-Viability Focus)
- **Modelo de Receita:** Open data / CC0 (não SaaS) — valor em reputação, citação e ponte editorial com lawfare-timeline / gosurf
- **Ticket Médio:** R$ 0 (domínio público)
- **ROI Projetado:** alcance cívico + retenção de corpus; monetização indireta via ecossistema de dossiês, não paywall no painel

## 🏗️ Arquitetura & Infra (Sentinel-TechHealth Focus)
- **Frontend:** HTML estático + `app.js` / `styles.css` (filtros, alertas, divergências R4)
- **Backend:** scripts Python de build/validação (sem servidor de aplicação)
- **Persistência:** JSON versionado em `/data/` (`captura.json`, `decisoes-source.json` → `unified.json`)
- **Infra:** Vercel (root estático, `cleanUrls`, cache em `/data/*`)

| Arquivo | Papel |
|---------|--------|
| `index.html` + `app.js` + `styles.css` | UI com filtros e metodologia |
| `data/unified.json` | Feed unificado (gerado) |
| `data/captura.json` | Seed captura (extract lawfare) |
| `data/decisoes-source.json` | Seed T-209 reconciliado (R1–R7) |
| `scripts/build-unified.py` | Merge + normalização + gate R1 |
| `scripts/validate-schema.py` | Validação pós-build |
| `scripts/validate-evidence-rules.py` | Gate evidencial pré-build (seeds) |
| `docs/schema.json` | Contrato JSON Schema 1.1.0 |

## 🛡️ Segurança & LGPD (Sentinel-Security Focus)
> [!IMPORTANT]
> O painel **não coleta** dados pessoais de visitantes (sem login, sem analytics proprietário obrigatório). Registros tratam de **eventos e decisões públicas** já divulgados em fontes oficiais ou jornalísticas. Apresentar um caso **não implica culpa ou erro** do magistrado — registra impacto público. Contribuições externas passam por curadoria humana antes de entrar no feed. Licença CC0 sobre o corpus publicado.

## 🚀 Roadmap de Execução
- [x] **Fase 1: MVP Estrutural** — site estático, schema unificado, CI validate-data, deploy Vercel
- [x] **Fase 2: Governança evidencial** — R1–R7, `schema.json`, seed decisões reconciliado, OG image
- [ ] **Fase 3: Escala editorial** — ampliar corpus HC/progressão, PWA opcional, redirect gosurf → canônico
- [ ] **Fase 4: Integrações** — sync automatizado com extract lawfare-timeline; auditoria card a card da trilha captura

Detalhe: [docs/ROADMAP.md](docs/ROADMAP.md)

## 🛠️ Instruções de Setup

```bash
# regenerar data/unified.json
python scripts/build-unified.py

# validar seeds (R1) e unified
python scripts/validate-evidence-rules.py data/decisoes-source.json
python scripts/validate-evidence-rules.py data/captura.json
python scripts/validate-schema.py

# servir localmente
python -m http.server 8080
# abrir http://localhost:8080
```

## 📚 Docs

- [Architecture](docs/ARCHITECTURE.md)
- [Data schema](docs/DATA_SCHEMA.md) (`1.1.0` — R1–R7)
- [JSON Schema](docs/schema.json)
- [Metodologia](docs/METODOLOGIA.md)
- [Roadmap](docs/ROADMAP.md)
- [Contribuir](CONTRIBUTING.md)

UI e schema inspirados nos artefatos `gosurf.site/artigos/jusmonitor.html` e `jusmonitor-backup.html` (JustiçaWatch).

---
*Este documento segue o Padrão Sentinel para Documentação Estruturada.*
