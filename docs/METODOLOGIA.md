# Metodologia

## Escopo

O JusMonitor registra **eventos e decisões públicas** relacionados a:

1. Captura institucional do Judiciário (supersalários/penduricalhos, venda de sentenças, disciplinar CNJ, chokepoints)
2. Decisões de alto impacto social (soltura, progressão, arquivamento/nulidade em crimes violentos)

## Critérios evidenciais

| Status | Critério |
|--------|----------|
| `ev-confirmed` | Fonte jornalística ou documental identificável e verificável no momento da curadoria |
| `ev-alleged` | Entrada sem fonte primária registrada — **pendente**, nunca exibida como fato confirmado |

## O que isto não é

- Não é acusação a magistrados
- Não implica erro jurídico em cada decisão listada
- Não substitui leitura integral de acórdãos/portarias

## Lacunas

Entradas do corpus com descrição vazia ou fonte `N/A` ficam em `excluidos_pendente_enriquecimento` até enriquecimento — não são descartadas do corpus upstream.

## Atualização

1. Rodar extract no `lawfare-timeline` (captura)
2. Atualizar sidecar decisões se necessário
3. `python scripts/build-unified.py`
4. `python scripts/validate-schema.py`
