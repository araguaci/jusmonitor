# Metodologia

## Escopo

O JusMonitor registra **eventos e decisões públicas** relacionados a:

1. Captura institucional do Judiciário (supersalários/penduricalhos, venda de sentenças, disciplinar CNJ, chokepoints)
2. Decisões de alto impacto social (soltura, progressão, arquivamento/nulidade em crimes violentos)

## Critérios evidenciais

| Status | Critério |
|--------|----------|
| `ev-confirmed` | Fonte jornalística ou documental identificável e verificável **por URL** no momento da curadoria — mínimo 1 URL em `fontes[]` |
| `ev-alleged` | Entrada sem fonte primária registrada — **pendente**, nunca exibida como fato confirmado |

**Nota de 2026-08-06:** a linha acima ("mínimo 1 URL") era regra implícita, não checada em
código nenhum. `data/decisoes-source.json` foi publicado em 2026-08-05 com 11/11 cards
`ev-confirmed` sem nenhuma URL em `fontes[]` — violação direta desta metodologia que passou
despercebida porque `scripts/validate-schema.py` verificava só que `fontes` era uma lista,
não que tinha conteúdo. Corrigido: ver `DATA_SCHEMA.md` § Regra R1 para as três camadas de
checagem agora em vigor (build, validação pós-build, schema formal).

## Regras de reconciliação (R1–R7)

Formalizadas em 2026-08-06 no cabeçalho `_regras_reconciliacao` de
`data/decisoes-source.json` e em `docs/schema.json`. Resumo:

- **R1** — `ev-confirmed` sem `fontes[]` real é erro estrutural, não estilo.
- **R2** — sem fonte localizável → `ev-alleged`, nunca descartar a entrada.
- **R3** — em duplicidade de evento entre seeds, fonte institucional/primária vence
  dossiê de parte interessada; a perdedora é removida (não duplicada), com a razão
  registrada em `conflitos_resolvidos`.
- **R4** — divergência numérica entre fonte oficial e fonte de parte interessada nunca é
  resolvida por silêncio — os dois valores entram, com nota em
  `divergencias_nao_reconciliadas`, até uma terceira fonte dirimir.
- **R5** — toda promoção `ev-alleged → ev-confirmed` (ou o inverso) registra
  `promovido_em`/`promovido_por`.
- **R6** — checar duplicidade por data+tribunal+tese antes de gerar novo `id`, não só por
  título (títulos podem divergir para o mesmo caso).
- **R7** — casos de controle (evidência que enfraquece a própria tese de um cluster) são
  obrigatórios quando existem no corpus, não opcionais.

## O que isto não é

- Não é acusação a magistrados
- Não implica erro jurídico em cada decisão listada
- Não substitui leitura integral de acórdãos/portarias

## Lacunas

Entradas do corpus com descrição vazia ou fonte `N/A` ficam em
`excluidos_pendente_enriquecimento` até enriquecimento — não são descartadas do corpus
upstream.

**Lacuna aberta (2026-08-06):** `extract_jusmonitor.py` (gera `data/captura.json` a partir
de `lawfare.json`, conforme `ARCHITECTURE.md`) não foi auditado nesta rodada de
reconciliação — só o lado `decisoes_impacto` foi verificado card a card. Os 76 cards de
`captura.json` passam pelo mesmo gate R1 agora (`validate-schema.py`/`build-unified.py`
patchados cobrem os dois tracks), mas isso só pega ausência de `fontes[]` — não confirma
que cada fonte listada de fato sustenta o `evidence_status` atribuído. Verificação
individual do lado captura é trabalho futuro, não coberto por esta sessão.

## Atualização

1. Rodar extract no `lawfare-timeline` (captura) — `extract_jusmonitor.py`
2. Atualizar sidecar decisões se necessário — `data/decisoes-source.json`
3. `python scripts/build-unified.py` (agora falha com R1 violada — corrigir a fonte antes de re-rodar)
4. `python scripts/validate-schema.py` (agora checa R1 e a coerência track↔grupo — antes só validava tipos)
