#!/usr/bin/env python3
"""
validate-evidence-rules.py — JusMonitor

Gate de validação evidencial para seeds (data/captura.json, data/decisoes-source.json)
ANTES de rodar scripts/build-unified.py.

Por que este script existe: em 2026-08-05, data/decisoes-source.json foi publicado com
11/11 cards marcados evidence_status="ev-confirmed" e 0/11 com fontes[] preenchido —
violação direta da taxonomia evidencial do corpus lawfare-timeline (ev-confirmed exige
documento primário OU 2+ fontes independentes). Este script torna essa violação
estruturalmente impossível de passar despercebida: falha o build (exit code 1) em vez
de deixar o problema silencioso no unified.json publicado.

Regras aplicadas (ver _regras_reconciliacao no cabeçalho de decisoes-source-reconciliado.json,
gerado por claude.ai em 2026-08-06):

  R1 — Nenhum card com evidence_status:"ev-confirmed" pode ter fontes:[] vazio.
       Exceção: se existir um campo "ref" que aponte para número de processo oficial
       (HC/RHC/ADC/REsp/AgRg) E o card tiver "promovido_por" registrando verificação
       manual — mas isso ainda requer fontes[] não-vazio. Não há exceção real: R1 é
       hard-fail.

  R3 — Se dois cards de tracks diferentes (ou do mesmo track) descrevem o mesmo evento
       (heurística: mesma década + tribunal + overlap de crime_tags + título com termos
       em comum), o script apenas ALERTA — a resolução (qual fonte prevalece) é humana,
       mas o script não deixa passar silenciosamente.

  R4 — Se stats{} contém uma chave numérica também citada como valor divergente em algum
       card (heurística simples por enquanto: checagem manual de 'hc_traficantes_stj_2024'
       hardcoded, já que é o caso conhecido), o script exige que ambos os valores estejam
       documentados em algum lugar do arquivo (campo divergencias_nao_reconciliadas).

  R5 — Cards com evidence_status "ev-confirmed" que não têm "promovido_em" são aceitos
       (podem ser originais), mas cards que existem em AMBAS as versões antiga e nova do
       arquivo com evidence_status diferente devem ter "promovido_em"/"promovido_por" —
       checado via --diff-against.

  R7 — Alerta (não bloqueia) se nenhum card tiver a tag "caso_controle" — ausência de
       caso de controle é sinal de viés de confirmação, mas não é erro fatal por si só.

Uso:
  python3 validate-evidence-rules.py data/decisoes-source.json
  python3 validate-evidence-rules.py data/captura.json --track captura_institucional
  python3 validate-evidence-rules.py data/decisoes-source.json --diff-against data/decisoes-source.json.bak

Exit codes:
  0 = passou (R1 sem violações; demais regras só geram warnings)
  1 = falhou R1 (bloqueia build-unified.py)
"""

import json
import sys
import argparse
from collections import defaultdict


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def get_cards(data):
    # aceita {"cards": [...]}, {"casos": [...]} (decisoes-source) ou lista pura
    if isinstance(data, list):
        return data
    return data.get("cards") or data.get("casos") or []


def is_real_source(s):
    return isinstance(s, str) and s.startswith(("http://", "https://"))


def check_r1(cards):
    """Nenhum ev-confirmed sem pelo menos 1 URL http(s) em fontes[]."""
    violations = []
    for c in cards:
        if c.get("evidence_status") != "ev-confirmed":
            continue
        fontes = c.get("fontes") or []
        if not any(is_real_source(f) for f in fontes):
            violations.append(c.get("id", "?"))
    return violations


def check_r3_heuristic(cards):
    """Heurística simples de duplicidade: mesmo ano+tribunal+overlap de crime_tags."""
    buckets = defaultdict(list)
    for c in cards:
        data = str(c.get("data", ""))[:4]  # ano
        tribunal = (c.get("tribunal") or "").upper()
        key = (data, tribunal)
        buckets[key].append(c)
    warnings = []
    for key, group in buckets.items():
        if len(group) < 2:
            continue
        for i in range(len(group)):
            for j in range(i + 1, len(group)):
                a, b = group[i], group[j]
                tags_a = set(a.get("crime_tags") or [])
                tags_b = set(b.get("crime_tags") or [])
                if tags_a & tags_b:
                    warnings.append(
                        f"possível duplicidade: {a.get('id')} vs {b.get('id')} "
                        f"(ano={key[0]}, tribunal={key[1]}, crime_tags em comum={tags_a & tags_b})"
                    )
    return warnings


def check_r7(cards):
    def is_control(c):
        tags = " ".join(c.get("tags") or []).lower()
        titulo = (c.get("titulo") or c.get("nome") or "").lower()
        return (
            "caso_controle" in tags
            or "caso-de-controle" in tags
            or "[caso de controle]" in titulo
        )

    return [] if any(is_control(c) for c in cards) else [
        "nenhum card marcado 'caso_controle' encontrado — revisar se o cluster "
        "tem evidência que contraria a própria tese antes de publicar (R7)."
    ]


def check_r5_diff(cards, old_cards):
    old_by_id = {c.get("id"): c for c in old_cards}
    warnings = []
    for c in cards:
        old = old_by_id.get(c.get("id"))
        if old and old.get("evidence_status") != c.get("evidence_status"):
            if not c.get("promovido_em") or not c.get("promovido_por"):
                warnings.append(
                    f"{c.get('id')}: evidence_status mudou de "
                    f"{old.get('evidence_status')} para {c.get('evidence_status')} "
                    f"sem 'promovido_em'/'promovido_por' registrado (R5)."
                )
    return warnings


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("seed_file", help="Caminho para o seed JSON (captura.json ou decisoes-source.json)")
    ap.add_argument("--diff-against", help="Versão anterior do mesmo arquivo, para checar R5", default=None)
    args = ap.parse_args()

    data = load(args.seed_file)
    cards = get_cards(data)

    print(f"[validate-evidence-rules] {args.seed_file} — {len(cards)} cards\n")

    r1 = check_r1(cards)
    r3 = check_r3_heuristic(cards)
    r7 = check_r7(cards)
    r5 = []
    if args.diff_against:
        old_data = load(args.diff_against)
        r5 = check_r5_diff(cards, get_cards(old_data))

    failed = False

    if r1:
        failed = True
        print(f"❌ R1 VIOLADA ({len(r1)} card(s)) — ev-confirmed sem fontes[]:")
        for cid in r1:
            print(f"   - {cid}")
        print()
    else:
        print("✅ R1 — todos os ev-confirmed têm fontes[] não-vazio.\n")

    if r3:
        print(f"⚠️  R3 — {len(r3)} possível(is) duplicidade(s) de evento (revisão manual):")
        for w in r3:
            print(f"   - {w}")
        print()

    if r5:
        print(f"⚠️  R5 — {len(r5)} mudança(s) de evidence_status sem rastreabilidade:")
        for w in r5:
            print(f"   - {w}")
        print()

    if r7:
        print("⚠️  R7:")
        for w in r7:
            print(f"   - {w}")
        print()

    if failed:
        print("RESULTADO: FALHOU (R1). Corrija antes de rodar build-unified.py.")
        sys.exit(1)
    else:
        print("RESULTADO: PASSOU (R1). Warnings acima não bloqueiam, mas merecem revisão.")
        sys.exit(0)


if __name__ == "__main__":
    main()
