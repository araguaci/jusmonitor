# Data schema

`schema_version`: `1.0.0`

## Envelope `unified.json`

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `schema_version` | string | Versão do schema |
| `sync_date` | string | Data do sync do corpus |
| `gerado_de` | string[] | Fontes usadas no build |
| `licenca` | string | `CC0 1.0` |
| `canonical_url` | string | URL canônica |
| `total` | number | Total de cards |
| `excluidos_pendente_enriquecimento` | number | Lacuna captura |
| `stats` | object | Agregados |
| `alertas_sistemicos` | array | Alertas T-209 |
| `cards` | array | Feed |

## Card

Campos obrigatórios: `id`, `data`, `titulo`, `track`, `grupo`, `evidence_status`.

| Campo | Valores / notas |
|-------|-----------------|
| `track` | `captura_institucional` \| `decisoes_impacto` |
| `grupo` | ver enums abaixo |
| `evidence_status` | `ev-confirmed` \| `ev-alleged` |
| `crime_tags` | `trafico`, `homicidio`, `estupro`, `latrocinio`, `foragido`, `corrupcao`, `milicia`, `pcc` |
| `tipo_decisao` | texto livre (HC monocrático, etc.) |
| `ref` / `tribunal` | trilha decisões |
| `fontes` | URLs |
| `tags` | strings |
| `instituicoes` | strings |
| `relevancia` | `alta` \| `media` \| … |
| `valor_envolvido` | string \| null |

### Grupos captura

`corrupcao_judicial`, `cnj_disciplinar`, `penduricalhos`, `chokepoint_stf`, `eleitoral_tse`, `outros_judiciario`

### Grupos decisões

`soltura_hc`, `progressao_regime`, `arquivamento`, `jurisprudencia_estrutural`, `foragidos_impacto`

## Exemplo contribuição

Ver `data/contributions/_README.json`.
