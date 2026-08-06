# Data schema

`schema_version`: `1.1.0` (era `1.0.0` — bump em 2026-08-06: adiciona R1–R7 e `docs/schema.json`)

> **Contrato formal:** este documento é a versão legível; `docs/schema.json` (JSON Schema
> Draft 2020-12) é a versão validável — mesma regra, duas formas. Em caso de divergência
> entre os dois, `schema.json` é a fonte de verdade (é o que `scripts/validate-schema.py`
> deveria checar, e o que qualquer ferramenta padrão de JSON Schema consegue rodar).

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
| `divergencias_nao_reconciliadas` | array | **Novo.** Ver R4 — indicador com 2+ valores de fontes distintas, nenhum descartado |
| `conflitos_resolvidos` | array | **Novo.** Ver R3 — eventos duplicados entre seeds, com a resolução registrada |
| `cards` | array | Feed |

## Card

Campos obrigatórios: `id`, `data`, `titulo`, `track`, `grupo`, `evidence_status`.

| Campo | Valores / notas |
|-------|-----------------|
| `track` | `captura_institucional` \| `decisoes_impacto` |
| `grupo` | ver enums abaixo — **deve pertencer ao conjunto do próprio track** (checagem cruzada, ver Regra R1-adjacente em `validate-schema.py`) |
| `evidence_status` | `ev-confirmed` \| `ev-alleged` |
| `crime_tags` | `trafico`, `homicidio`, `estupro`, `latrocinio`, `foragido`, `corrupcao`, `milicia`, `pcc` |
| `tipo_decisao` | texto livre (HC monocrático, etc.) |
| `ref` / `tribunal` | trilha decisões |
| `fontes` | URLs — **ver R1** |
| `tags` | strings |
| `instituicoes` | strings |
| `relevancia` | `alta` \| `media` \| … |
| `valor_envolvido` | string \| null |

### Campos de curadoria (opcionais, novos em 1.1.0)

Preservados por `scripts/build-unified.py` desde o patch de 2026-08-06 (antes eram
descartados silenciosamente na normalização):

| Campo | Descrição |
|-------|-----------|
| `lawfare_id` | Vínculo com o corpus principal lawfare-timeline, quando aplicável |
| `analise` | Sempre `ev-inference` — nunca em `titulo`/`descricao` |
| `lacuna_investigativa` | Texto livre — o que falta verificar nesta entrada |
| `ponto_de_inflexao` | Fato que muda o sentido do caso (ex: réu já tinha passagem por homicídio) |
| `promovido_em` / `promovido_por` | Data + autor/sessão de qualquer mudança de `evidence_status` — rastreabilidade da própria curadoria (R5) |

### Regra R1 — evidence_status ⇄ fontes (agora explícita e validada)

**`evidence_status: "ev-confirmed"` exige pelo menos 1 item em `fontes[]` que seja uma URL
real (`http://` ou `https://`).** Um campo `ref` em texto livre (ex: `"HC 191.836 — Min.
Marco Aurélio"`) identifica o processo, mas **não conta como fonte** — não é verificável
sem uma URL.

Esta regra sempre esteve implícita na `METODOLOGIA.md` (ver seção "Critérios evidenciais"),
mas não era checada em nenhum lugar do pipeline até 2026-08-06. É por isso que
`data/decisoes-source.json` chegou a produção em 2026-08-05 com 11/11 cards
`ev-confirmed` e `fontes: []` — o gate documentado (`validate-schema.py`, passo 4 da
Metodologia) rodava e dizia "OK" porque nunca checava conteúdo de `fontes[]`, só que era
uma lista. Agora é checada em três camadas independentes:

1. `scripts/build-unified.py` — hard-fail no build (não deixa nem gerar `unified.json`)
2. `scripts/validate-schema.py` — hard-fail na validação pós-build
3. `docs/schema.json` — contrato formal, checável por qualquer ferramenta JSON Schema

### Grupos captura

`corrupcao_judicial`, `cnj_disciplinar`, `penduricalhos`, `chokepoint_stf`, `eleitoral_tse`, `outros_judiciario`

### Grupos decisões

`soltura_hc`, `progressao_regime`, `arquivamento`, `jurisprudencia_estrutural`, `foragidos_impacto`

## `data/decisoes-source.json` (entrada, formato legado)

Formato **diferente** do Card acima — usado só como entrada de `build-unified.py`, nunca
como saída. Campos: `ano` (int), `nome`, `tipo`, `tribunal`, `ref`, `tags`, `fontes`,
opcionalmente `grupo`/`evidence_status`/`id`/`lawfare_id` explícitos (se ausentes, o script
infere — ver `ARCHITECTURE.md`). R1 se aplica aqui também, na entrada, não só na saída.

## Exemplo contribuição

Ver `data/contributions/_README.json`.
