#!/usr/bin/env python3
"""Build data/unified.json from captura + decisões + contributions."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

TRACK_CAPTURA = "captura_institucional"
TRACK_DECISOES = "decisoes_impacto"

DECISAO_GRUPO_MAP = {
    "HC coletivo": "soltura_hc",
    "HC coletivo nacional": "soltura_hc",
    "HC monocrático": "soltura_hc",
    "HCs monocráticos": "soltura_hc",
    "Progressão de regime": "progressao_regime",
    "Mudança jurisprudencial": "jurisprudencia_estrutural",
    "ADC plenário": "jurisprudencia_estrutural",
    "Nulidade processual": "arquivamento",
    "Nulidade de prova": "arquivamento",
    "Levantamento anual": "soltura_hc",
    "Distinguishing jurisprudencial": "jurisprudencia_estrutural",
}

CRIME_TAGS = {
    "trafico",
    "homicidio",
    "estupro",
    "latrocinio",
    "foragido",
    "corrupcao",
    "milicia",
    "pcc",
}


def load_json(path: Path):
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def slug_id(prefix: str, text: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return f"{prefix}-{s[:48]}"


def normalize_captura(raw: dict) -> list[dict]:
    cards = []
    for c in raw.get("cards", []):
        card = {
            "id": c.get("id"),
            "data": (c.get("data") or "")[:10],
            "titulo": (c.get("titulo") or "").strip(),
            "descricao": (c.get("descricao") or "").strip(),
            "grupo": c.get("grupo") or "outros_judiciario",
            "gravidade": c.get("gravidade"),
            "relevancia": c.get("relevancia"),
            "instituicoes": c.get("instituicoes") or [],
            "tags": c.get("tags") or [],
            "fontes": c.get("fontes") or [],
            "evidence_status": c.get("evidence_status") or "ev-alleged",
            "valor_envolvido": c.get("valor_envolvido"),
            "track": TRACK_CAPTURA,
            "crime_tags": [],
            "tipo_decisao": None,
            "ref": None,
            "tribunal": None,
        }
        cards.append(card)
    return cards


def classify_decisao_grupo(tipo: str, tags: list[str]) -> str:
    if "foragido" in tags:
        return "foragidos_impacto"
    return DECISAO_GRUPO_MAP.get(tipo or "", "soltura_hc")


def normalize_decisoes(raw: dict) -> tuple[list[dict], dict, list]:
    stats = raw.get("estatisticas") or {}
    alertas = raw.get("alertas_sistemicos") or []
    cards = []
    for i, c in enumerate(raw.get("casos", []), start=1):
        tags = c.get("tags") or []
        crime_tags = [t for t in tags if t in CRIME_TAGS]
        ano = c.get("ano") or 2000
        titulo = (c.get("nome") or "").strip()
        tipo = c.get("tipo") or ""
        tribunal = c.get("tribunal") or ""
        ref = c.get("ref") or ""
        fontes = [s for s in (c.get("fontes") or []) if s and s != "N/A"]
        desc = (
            (c.get("descricao_detalhada") or c.get("descricao_resumo") or "")
            .strip()
            or f"{tipo} · {tribunal}. Referência: {ref}".strip()
        )
        ev = c.get("evidence_status") or (
            "ev-confirmed" if fontes else "ev-alleged"
        )
        card = {
            "id": slug_id("jw", f"{ano}-{tribunal}-{titulo}"),
            "data": f"{ano}-01-01",
            "titulo": titulo,
            "descricao": desc,
            "grupo": classify_decisao_grupo(tipo, tags),
            "gravidade": c.get("gravidade"),
            "relevancia": "alta" if "foragido" in tags or "pcc" in tags else "media",
            "instituicoes": [tribunal] if tribunal else [],
            "tags": tags,
            "fontes": fontes,
            "evidence_status": ev,
            "valor_envolvido": None,
            "track": TRACK_DECISOES,
            "crime_tags": crime_tags,
            "tipo_decisao": tipo,
            "ref": ref,
            "tribunal": tribunal,
        }
        cards.append(card)
    return cards, stats, alertas


def load_contributions() -> list[dict]:
    folder = DATA / "contributions"
    if not folder.exists():
        return []
    out = []
    for path in sorted(folder.glob("*.json")):
        if path.name.startswith("_"):
            continue
        try:
            payload = load_json(path)
        except json.JSONDecodeError as exc:
            raise SystemExit(f"JSON inválido em {path}: {exc}") from exc
        items = payload if isinstance(payload, list) else payload.get("cards", [payload])
        for item in items:
            if not item.get("titulo"):
                continue
            item.setdefault("track", TRACK_CAPTURA)
            item.setdefault("evidence_status", "ev-alleged")
            item.setdefault("grupo", "outros_judiciario")
            item.setdefault("tags", [])
            item.setdefault("fontes", [])
            item.setdefault("instituicoes", [])
            item.setdefault("crime_tags", [])
            item.setdefault("tipo_decisao", None)
            item.setdefault("ref", None)
            item.setdefault("tribunal", None)
            item.setdefault("gravidade", None)
            item.setdefault("relevancia", "media")
            item.setdefault("valor_envolvido", None)
            item.setdefault("descricao", "")
            if not item.get("data"):
                item["data"] = "0001-01-01"
            if not item.get("id"):
                item["id"] = slug_id("contrib", item["titulo"])
            item["_from_contribution"] = path.name
            out.append(item)
    return out


def build():
    captura_raw = load_json(DATA / "captura.json")
    decisoes_raw = load_json(DATA / "decisoes-source.json")

    captura_cards = normalize_captura(captura_raw)
    decisoes_cards, dec_stats, alertas = normalize_decisoes(decisoes_raw)
    contrib_cards = load_contributions()

    # Subset normalizado (captura.json seed original permanece intacto)
    captura_out = {
        "gerado_de": captura_raw.get("gerado_de", "lawfare.json"),
        "sync_date": captura_raw.get("sync_date"),
        "total": len(captura_cards),
        "excluidos_pendente_enriquecimento": captura_raw.get(
            "excluidos_pendente_enriquecimento", 0
        ),
        "track": TRACK_CAPTURA,
        "cards": captura_cards,
    }
    with (DATA / "captura-cards.json").open("w", encoding="utf-8") as f:
        json.dump(captura_out, f, ensure_ascii=False, indent=1)

    decisoes_out = {
        "gerado_de": "justicawatch-brasil.json (T-209)",
        "sync_date": (decisoes_raw.get("_meta") or {}).get("generated", "2026-05-28"),
        "total": len(decisoes_cards),
        "track": TRACK_DECISOES,
        "estatisticas": dec_stats,
        "cards": decisoes_cards,
    }
    with (DATA / "decisoes.json").open("w", encoding="utf-8") as f:
        json.dump(decisoes_out, f, ensure_ascii=False, indent=1)

    all_cards = captura_cards + decisoes_cards + contrib_cards
    all_cards.sort(key=lambda c: c.get("data") or "", reverse=True)

    sync_date = captura_raw.get("sync_date") or decisoes_out["sync_date"]

    unified = {
        "schema_version": "1.0.0",
        "gerado_de": [
            "data/captura.json",
            "data/decisoes-source.json",
            "data/contributions/",
        ],
        "sync_date": sync_date,
        "licenca": "CC0 1.0",
        "canonical_url": "https://jusmonitor.vercel.app",
        "total": len(all_cards),
        "excluidos_pendente_enriquecimento": captura_raw.get(
            "excluidos_pendente_enriquecimento", 0
        ),
        "stats": {
            "captura": len(captura_cards),
            "decisoes": len(decisoes_cards),
            "contributions": len(contrib_cards),
            "ev_confirmed": sum(
                1 for c in all_cards if c.get("evidence_status") == "ev-confirmed"
            ),
            "relevancia_alta": sum(
                1 for c in all_cards if c.get("relevancia") == "alta"
            ),
            "hc_traficantes_stj_2024": dec_stats.get("hc_traficantes_stj_2024"),
            "hc_trafico_stf_2024": dec_stats.get("hc_trafico_stf_2024"),
            "taxa_reincidencia_br": dec_stats.get("taxa_reincidencia_br"),
            "populacao_carceraria": dec_stats.get("populacao_carceraria"),
            "foragidos_hc_marco_aurelio_2020": dec_stats.get(
                "foragidos_hc_marco_aurelio_2020"
            ),
        },
        "alertas_sistemicos": alertas,
        "cards": all_cards,
    }

    out_path = DATA / "unified.json"
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(unified, f, ensure_ascii=False, indent=1)

    print(f"OK {out_path}")
    print(
        f"  total={unified['total']} captura={len(captura_cards)} "
        f"decisoes={len(decisoes_cards)} contrib={len(contrib_cards)}"
    )


if __name__ == "__main__":
    build()
