#!/usr/bin/env python3
"""Build data/unified.json from captura + decisões + contributions."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

TRACK_CAPTURA = "captura_institucional"
TRACK_DECISOES = "decisoes_impacto"
SCHEMA_VERSION = "1.1.0"

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

CURADORIA_FIELDS = (
    "lawfare_id",
    "analise",
    "lacuna_investigativa",
    "ponto_de_inflexao",
    "promovido_em",
    "promovido_por",
)


def load_json(path: Path):
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def slug_id(prefix: str, text: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return f"{prefix}-{s[:48]}"


def is_real_source(s) -> bool:
    return isinstance(s, str) and s.startswith(("http://", "https://"))


def enforce_r1(card: dict, where: str) -> None:
    """R1: ev-confirmed exige pelo menos 1 URL real em fontes[]."""
    if card.get("evidence_status") != "ev-confirmed":
        return
    fontes = card.get("fontes") or []
    if not any(is_real_source(f) for f in fontes):
        cid = card.get("id", "?")
        raise SystemExit(
            f"R1 violada em {where} id={cid}: evidence_status=ev-confirmed "
            f"sem URL http(s) em fontes[]. Rebaixe para ev-alleged ou adicione fonte."
        )


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
        for key in CURADORIA_FIELDS:
            if c.get(key) not in (None, ""):
                card[key] = c.get(key)
        if card["grupo"] not in GRUPOS_CAPTURA:
            raise SystemExit(
                f"grupo '{card['grupo']}' inválido para captura id={card.get('id')}"
            )
        enforce_r1(card, "captura")
        cards.append(card)
    return cards


def classify_decisao_grupo(tipo: str, tags: list[str]) -> str:
    if "foragido" in tags:
        return "foragidos_impacto"
    if tipo in DECISAO_GRUPO_MAP:
        return DECISAO_GRUPO_MAP[tipo]
    # prefix match for tipos longos do sync enriquecido
    for key, grupo in DECISAO_GRUPO_MAP.items():
        if tipo.startswith(key):
            return grupo
    return "soltura_hc"


def build_decisao_descricao(c: dict, tipo: str, tribunal: str, ref: str) -> str:
    for key in ("descricao", "descricao_detalhada", "descricao_resumo"):
        val = (c.get(key) or "").strip()
        if val:
            return val
    parts = []
    if c.get("analise"):
        parts.append(str(c["analise"]).strip())
    if c.get("ponto_de_inflexao"):
        parts.append("Ponto de inflexão: " + str(c["ponto_de_inflexao"]).strip())
    if c.get("lacuna_investigativa"):
        parts.append("Lacuna: " + str(c["lacuna_investigativa"]).strip())
    if parts:
        return " ".join(parts)
    return f"{tipo} · {tribunal}. Referência: {ref}".strip(" ·")


def normalize_decisoes(raw: dict) -> tuple[list[dict], dict, list, list, list]:
    stats = raw.get("estatisticas") or {}
    alertas = raw.get("alertas_sistemicos") or []
    conflitos = raw.get("conflitos_resolvidos") or []
    divergencias = raw.get("divergencias_nao_reconciliadas") or []
    cards = []
    for i, c in enumerate(raw.get("casos", []), start=1):
        tags = list(c.get("tags") or [])
        crime_tags = list(c.get("crime_tags") or [])
        if not crime_tags:
            crime_tags = [t for t in tags if t in CRIME_TAGS]
        ano = c.get("ano") or 2000
        titulo = (c.get("titulo") or c.get("nome") or "").strip()
        tipo = (c.get("tipo_decisao") or c.get("tipo") or "").strip()
        tribunal = (c.get("tribunal") or "").strip()
        ref = c.get("ref") or ""
        fontes = [s for s in (c.get("fontes") or []) if s and s != "N/A"]
        desc = build_decisao_descricao(c, tipo, tribunal, ref or "")

        if c.get("grupo") in GRUPOS_DECISOES:
            grupo = c["grupo"]
        else:
            grupo = classify_decisao_grupo(tipo, tags + crime_tags)

        ev = c.get("evidence_status")
        if ev not in ("ev-confirmed", "ev-alleged"):
            ev = "ev-confirmed" if any(is_real_source(f) for f in fontes) else "ev-alleged"

        card_id = c.get("id") or slug_id("jw", f"{ano}-{tribunal}-{titulo}")
        data = (c.get("data") or f"{ano}-01-01")[:10]

        relevancia = c.get("relevancia")
        if not relevancia:
            pool = set(tags) | set(crime_tags)
            relevancia = "alta" if ("foragido" in pool or "pcc" in pool) else "media"

        instituicoes = c.get("instituicoes") or ([tribunal] if tribunal else [])

        card = {
            "id": card_id,
            "data": data,
            "titulo": titulo,
            "descricao": desc,
            "grupo": grupo,
            "gravidade": c.get("gravidade"),
            "relevancia": relevancia,
            "instituicoes": instituicoes,
            "tags": tags,
            "fontes": fontes,
            "evidence_status": ev,
            "valor_envolvido": c.get("valor_envolvido"),
            "track": TRACK_DECISOES,
            "crime_tags": crime_tags,
            "tipo_decisao": tipo,
            "ref": ref if ref else None,
            "tribunal": tribunal or None,
        }
        for key in CURADORIA_FIELDS:
            if c.get(key) not in (None, ""):
                card[key] = c.get(key)

        enforce_r1(card, "decisoes")
        cards.append(card)
    return cards, stats, alertas, conflitos, divergencias


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
            enforce_r1(item, path.name)
            out.append(item)
    return out


def build():
    captura_raw = load_json(DATA / "captura.json")
    decisoes_raw = load_json(DATA / "decisoes-source.json")

    captura_cards = normalize_captura(captura_raw)
    decisoes_cards, dec_stats, alertas, conflitos, divergencias = normalize_decisoes(
        decisoes_raw
    )
    contrib_cards = load_contributions()

    meta = decisoes_raw.get("_meta") or {}
    sync_decisoes = (
        meta.get("generated_at")
        or meta.get("generated")
        or meta.get("updated")
        or "2026-08-06"
    )

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
        "gerado_de": meta.get("gerado_de")
        or "justicawatch-brasil.json (T-209) / sync reconciliado",
        "sync_date": sync_decisoes,
        "total": len(decisoes_cards),
        "track": TRACK_DECISOES,
        "estatisticas": dec_stats,
        "conflitos_resolvidos": conflitos,
        "divergencias_nao_reconciliadas": divergencias,
        "cards": decisoes_cards,
    }
    with (DATA / "decisoes.json").open("w", encoding="utf-8") as f:
        json.dump(decisoes_out, f, ensure_ascii=False, indent=1)

    all_cards = captura_cards + decisoes_cards + contrib_cards
    all_cards.sort(key=lambda c: c.get("data") or "", reverse=True)

    sync_date = captura_raw.get("sync_date") or sync_decisoes

    unified = {
        "schema_version": SCHEMA_VERSION,
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
        "conflitos_resolvidos": conflitos,
        "divergencias_nao_reconciliadas": divergencias,
        "cards": all_cards,
    }

    out_path = DATA / "unified.json"
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(unified, f, ensure_ascii=False, indent=1)

    print(f"OK {out_path}", file=sys.stdout)
    print(
        f"  schema={SCHEMA_VERSION} total={unified['total']} "
        f"captura={len(captura_cards)} decisoes={len(decisoes_cards)} "
        f"contrib={len(contrib_cards)} conflitos={len(conflitos)} "
        f"divergencias={len(divergencias)}"
    )


if __name__ == "__main__":
    build()
