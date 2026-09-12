#!/usr/bin/env python3
"""Ingest JW 2026-09-12 deltas into decisoes-source without duplicating."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = Path(r"D:/ai-projects/lawfare-timeline/_data/justicewatch/justicawatch-brasil.json")
DST = ROOT / "data/decisoes-source.json"

src = json.loads(SRC.read_text(encoding="utf-8"))
dst = json.loads(DST.read_text(encoding="utf-8"))

jw_by_corpus = {str(c.get("id_corpus")): c for c in src["casos"] if c.get("id_corpus")}
jw_oruam = jw_by_corpus["1798"]
jw_karen = jw_by_corpus["1799"]
jw_lazaro = next(c for c in src["casos"] if "Lázaro" in (c.get("nome") or ""))

CRIME = {
    "trafico",
    "homicidio",
    "estupro",
    "latrocinio",
    "foragido",
    "corrupcao",
    "milicia",
    "pcc",
}

# --- meta ---
meta = dst.setdefault("_meta", {})
meta["generated_at"] = "2026-09-12"
meta["periodo"] = "2005–2026"
meta["revisao_jw"] = (
    "justicawatch-brasil.json updated 2026-09-12 — DI-010 Karen Tanaka; "
    "merge Oruam DI-009; JW-018 Lázaro alleged; stats/alertas alinhados"
)
gerado = list(meta.get("gerado_de") or [])
note = "justicawatch-brasil.json (lawfare-timeline, updated 2026-09-12)"
if note not in gerado:
    gerado.append(note)
meta["gerado_de"] = gerado

# --- stats (R4: keep hc_traficantes null) ---
ss = src.get("estatisticas") or {}
dst["estatisticas"] = {
    "hc_traficantes_stj_2024": None,
    "hc_stj_2024_conjur": ss.get("hc_stj_2024_conjur"),
    "hc_stj_2024_privilegiado": ss.get("hc_stj_2024_privilegiado"),
    "hc_stj_2024_concessoes_total": ss.get("hc_stj_2024_concessoes_total"),
    "hc_trafico_stf_2024": ss.get("hc_trafico_stf_2024"),
    "taxa_reincidencia_br": ss.get("taxa_reincidencia_br"),
    "populacao_carceraria": ss.get("populacao_carceraria"),
    "foragidos_hc_marco_aurelio_2020": ss.get("foragidos_hc_marco_aurelio_2020", 21),
    "casos_ancora": None,
    "hc_stj_2024_nota": ss.get("hc_stj_2024_nota"),
}

for d in dst.get("divergencias_nao_reconciliadas") or []:
    if d.get("indicador") == "hc_traficantes_stj_2024":
        d["valor_a"]["numero"] = ss.get("hc_stj_2024_conjur", 10127)
        d["valor_b"]["numero"] = ss.get("hc_traficantes_stj_2024", 9166)
        d["status"] = (
            "não reconciliado — exibir valor_a (10.127 ConJur/STJ) e valor_b (9.166 Seif); "
            "ver também stats.hc_stj_2024_privilegiado=1578 e concessoes_total=20114"
        )

dst["alertas_sistemicos"] = [
    {
        "nivel": "alto",
        "titulo": "Intervalo de Fuga — Liminares Monocráticas",
        "descricao": (
            "Janela entre liminar monocrática e análise colegiada explorada por ao menos "
            "21 réus em 2020 (ver JW-013, JW-014)."
        ),
    },
    {
        "nivel": "alto",
        "titulo": "Tráfico Privilegiado Desfigurado",
        "descricao": (
            "EREsp 1.887.511 (2021) fixou que quantidade isolada não afasta o §4º. "
            "Aplicações documentadas em 311 kg (2022) e 832 kg (2024). Em 2024, 1.578 HCs "
            "do STJ aplicaram o privilegiado (ConJur). O caso DI-006/1809 (110 kg, MPF "
            "provido) mostra que o mecanismo não é absoluto (cluster P01-B, DI-001 a DI-006)."
        ),
    },
    {
        "nivel": "alto",
        "titulo": "Ausência de Banco Nacional de Solturas",
        "descricao": "BNMP 3.0 não correlaciona solturas com reincidência.",
    },
    {
        "nivel": "medio",
        "titulo": "Cautelares 2026 — desclassificação e pena antecipada",
        "descricao": (
            "Oruam (DI-009/1798): revoga preventiva de tentativa de homicídio e permanece "
            "foragido por lavagem. Karen Tanaka (DI-010/1799): revoga tornozeleira após "
            "2 anos sem denúncia em investigação de R$ 35 mi ligada ao PCC."
        ),
    },
]

casos = dst["casos"]

# --- merge DI-009 Oruam (no new card) ---
di009 = next(c for c in casos if c.get("id") == "DI-009")
di009["ref"] = jw_oruam.get("ref")
di009["tribunal"] = "TJRJ"
di009["tipo"] = jw_oruam.get("tipo") or di009.get("tipo")
di009["tipo_decisao"] = jw_oruam.get("tipo") or di009.get("tipo_decisao")
fontes = list(di009.get("fontes") or [])
for f in jw_oruam.get("fontes") or []:
    if f and f not in fontes:
        fontes.append(f)
di009["fontes"] = fontes
crime = list(di009.get("crime_tags") or [])
for t in jw_oruam.get("tags") or []:
    if t in CRIME and t not in crime:
        crime.append(t)
di009["crime_tags"] = crime
tags = list(di009.get("tags") or [])
for t in jw_oruam.get("tags") or []:
    if t not in tags:
        tags.append(t)
di009["tags"] = tags
di009["lawfare_id"] = 1798
if jw_oruam.get("descricao_detalhada"):
    # preserve as optional field for build fallback path
    di009["descricao"] = jw_oruam["descricao_detalhada"]
di009["promovido_em"] = "2026-09-12"
di009["promovido_por"] = (
    "jusmonitor sync — merge metadados justicawatch-brasil.json (1798) sem novo card"
)
print("merged DI-009 Oruam")

# --- DI-010 Karen ---
if not any(c.get("id") == "DI-010" or c.get("lawfare_id") == 1799 for c in casos):
    casos.append(
        {
            "id": "DI-010",
            "lawfare_id": 1799,
            "data": "2026-08-01",
            "ano": 2026,
            "titulo": (
                "Karen Tanaka ('Japa do PCC') — Justiça de SP revoga tornozeleira "
                "em investigação de R$ 35 mi"
            ),
            "nome": jw_karen.get("nome"),
            "tipo": jw_karen.get("tipo"),
            "tipo_decisao": jw_karen.get("tipo"),
            "tribunal": "TJSP",
            "ref": jw_karen.get("ref"),
            "grupo": "foragidos_impacto",
            "evidence_status": "ev-confirmed",
            "crime_tags": ["trafico", "pcc"],
            "tags": list(jw_karen.get("tags") or []),
            "instituicoes": ["TJSP"],
            "relevancia": "alta",
            "valor_envolvido": "R$ 35.000.000,00 (investigação de lavagem)",
            "fontes": list(jw_karen.get("fontes") or []),
            "analise": (
                "Cautelar 2026: revogação de tornozeleira após >2 anos sem denúncia — "
                "risco de pena antecipada. Cluster com DI-009 (Oruam)."
            ),
            "promovido_em": "2026-09-12",
            "promovido_por": (
                "jusmonitor sync — ingestão justicawatch-brasil.json id_corpus 1799"
            ),
        }
    )
    print("added DI-010")
else:
    print("DI-010 already present")

# --- JW-018 Lázaro alleged ---
if not any(
    "Lázaro" in (c.get("titulo") or c.get("nome") or "") for c in casos
):
    casos.append(
        {
            "id": "JW-018",
            "lawfare_id": None,
            "data": "2021-01-01",
            "ano": 2021,
            "titulo": "Lázaro Barbosa — Progressão ignorando laudo de periculosidade",
            "nome": jw_lazaro.get("nome"),
            "tipo": jw_lazaro.get("tipo"),
            "tipo_decisao": jw_lazaro.get("tipo"),
            "tribunal": "TJGO",
            "ref": jw_lazaro.get("ref"),
            "grupo": "progressao_regime",
            "evidence_status": "ev-alleged",
            "crime_tags": ["homicidio", "estupro"],
            "tags": list(jw_lazaro.get("tags") or []),
            "instituicoes": ["TJGO"],
            "relevancia": "alta",
            "valor_envolvido": None,
            "fontes": [],
            "lacuna_investigativa": (
                "R1/R2 (2026-09-12): justicawatch-brasil.json traz fontes genéricas "
                "(homes G1/Metrópoles), não URL de matéria específica. Mantido "
                "ev-alleged até fonte verificável."
            ),
            "promovido_em": "2026-09-12",
            "promovido_por": (
                "jusmonitor sync — reingresso condicional do JW sem promover a confirmed"
            ),
        }
    )
    print("added JW-018 Lázaro as ev-alleged")
else:
    print("Lázaro already present")

casos.sort(key=lambda c: c.get("data") or "", reverse=True)
dst["casos"] = casos
dst["estatisticas"]["casos_ancora"] = len(casos)

DST.write_text(json.dumps(dst, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"casos={len(casos)}")
print("ids=", [c.get("id") for c in casos])
