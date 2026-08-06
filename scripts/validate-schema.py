#!/usr/bin/env python3
"""Validate JusMonitor unified / contribution JSON against schema rules."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

TRACKS = {"captura_institucional", "decisoes_impacto"}
EVIDENCE = {"ev-confirmed", "ev-alleged"}
GRUPOS_CAPTURA = {
    "corrupcao_judicial",
    "cnj_disciplinar",
    "penduricalhos",
    "chokepoint_stf",
    "eleitoral_tse",
    "outros_judiciario",
}
GRUPOS_DECISOES = {
    "soltura_hc",
    "progressao_regime",
    "arquivamento",
    "jurisprudencia_estrutural",
    "foragidos_impacto",
}
ALL_GRUPOS = GRUPOS_CAPTURA | GRUPOS_DECISOES
REQUIRED = ("id", "data", "titulo", "track", "grupo", "evidence_status")


def fail(msg: str) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(1)


def is_real_source(s: str) -> bool:
    return isinstance(s, str) and s.startswith(("http://", "https://"))


def validate_card(card: dict, idx: int, where: str) -> None:
    for key in REQUIRED:
        if key not in card or card[key] in (None, ""):
            fail(f"{where}[{idx}] missing required field '{key}'")
    if card["track"] not in TRACKS:
        fail(f"{where}[{idx}] invalid track '{card['track']}'")
    if card["evidence_status"] not in EVIDENCE:
        fail(f"{where}[{idx}] invalid evidence_status '{card['evidence_status']}'")
    if card["grupo"] not in ALL_GRUPOS:
        fail(f"{where}[{idx}] invalid grupo '{card['grupo']}'")

    # Checagem cruzada track<->grupo — antes disso, um card captura_institucional
    # com grupo de decisoes_impacto (ou vice-versa) passava sem erro, porque
    # ALL_GRUPOS era a união dos dois conjuntos.
    if card["track"] == "captura_institucional" and card["grupo"] not in GRUPOS_CAPTURA:
        fail(
            f"{where}[{idx}] grupo '{card['grupo']}' pertence a decisoes_impacto, "
            f"mas track é captura_institucional"
        )
    if card["track"] == "decisoes_impacto" and card["grupo"] not in GRUPOS_DECISOES:
        fail(
            f"{where}[{idx}] grupo '{card['grupo']}' pertence a captura_institucional, "
            f"mas track é decisoes_impacto"
        )

    if not isinstance(card.get("tags", []), list):
        fail(f"{where}[{idx}] tags must be a list")
    if not isinstance(card.get("fontes", []), list):
        fail(f"{where}[{idx}] fontes must be a list")

    # R1 (ver METODOLOGIA.md: "ev-alleged... pendente, nunca exibida como fato
    # confirmado" — o inverso implícito é que ev-confirmed EXIGE fonte real).
    # Esta checagem estava ausente: o script validava que fontes é uma lista,
    # nunca que ela tem conteúdo. Foi assim que 11/11 cards de decisoes_impacto
    # foram publicados em 2026-08-05 como ev-confirmed com fontes:[].
    if card["evidence_status"] == "ev-confirmed":
        fontes = card.get("fontes", [])
        if not any(is_real_source(f) for f in fontes):
            fail(
                f"{where}[{idx}] evidence_status='ev-confirmed' mas fontes[] não tem "
                f"nenhuma URL real (http/https). Rebaixe para 'ev-alleged' ou adicione fonte."
            )


def validate_unified(path: Path) -> None:
    data = json.loads(path.read_text(encoding="utf-8"))
    if "schema_version" not in data:
        fail(f"{path.name}: missing schema_version")
    if "cards" not in data or not isinstance(data["cards"], list):
        fail(f"{path.name}: missing cards[]")
    for i, card in enumerate(data["cards"]):
        validate_card(card, i, "cards")
    print(f"OK {path.name}: {len(data['cards'])} cards")


def validate_contributions() -> None:
    folder = DATA / "contributions"
    if not folder.exists():
        return
    for path in sorted(folder.glob("*.json")):
        if path.name.startswith("_"):
            continue
        payload = json.loads(path.read_text(encoding="utf-8"))
        items = payload if isinstance(payload, list) else payload.get("cards", [payload])
        for i, card in enumerate(items):
            # Allow incomplete drafts only if they have titulo+track at minimum during PR review
            if "track" not in card:
                card = {**card, "track": "captura_institucional"}
            if "grupo" not in card:
                card = {**card, "grupo": "outros_judiciario"}
            if "evidence_status" not in card:
                card = {**card, "evidence_status": "ev-alleged"}
            if "id" not in card:
                card = {**card, "id": f"tmp-{i}"}
            if "data" not in card:
                card = {**card, "data": "0001-01-01"}
            validate_card(card, i, path.name)
        print(f"OK contribution {path.name}")


def main() -> None:
    unified = DATA / "unified.json"
    if not unified.exists():
        fail("data/unified.json not found — run scripts/build-unified.py first")
    validate_unified(unified)
    validate_contributions()
    print("All validations passed.")


if __name__ == "__main__":
    main()
