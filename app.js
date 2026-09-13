(function () {
  "use strict";

  const TRACK_LABELS = {
    todos: "Todos",
    captura_institucional: "Captura institucional",
    decisoes_impacto: "Decisões de impacto",
  };

  const GROUP_LABELS = {
    todos: "Todos os grupos",
    corrupcao_judicial: "Corrupção judicial",
    cnj_disciplinar: "CNJ disciplinar",
    penduricalhos: "Penduricalhos",
    chokepoint_stf: "Chokepoint STF",
    eleitoral_tse: "Eleitoral / TSE",
    outros_judiciario: "Outros (judiciário)",
    soltura_hc: "Soltura / HC",
    progressao_regime: "Progressão de regime",
    arquivamento: "Arquivamento / nulidade",
    jurisprudencia_estrutural: "Jurisprudência estrutural",
    foragidos_impacto: "Foragidos",
  };

  const CRIME_LABELS = {
    todos: "Todos crimes",
    trafico: "Tráfico",
    homicidio: "Homicídio",
    estupro: "Crimes sexuais",
    latrocinio: "Latrocínio",
    foragido: "Foragido",
    corrupcao: "Corrupção",
    milicia: "Milícia",
    pcc: "PCC",
  };

  const EV_LABELS = {
    todos: "Toda evidência",
    "ev-confirmed": "Confirmado",
    "ev-alleged": "Alegado / pendente",
  };

  const ICONS = {
    penduricalhos:
      '<svg class="icon icon-stroke card-icon" viewBox="0 0 24 24" aria-hidden="true"><rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 7V5a2 2 0 00-2-2h-4a2 2 0 00-2 2v2"/><path d="M12 12v4"/><path d="M10 14h4"/></svg>',
    corrupcao_judicial:
      '<svg class="icon icon-stroke card-icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3v18"/><path d="M5 8h14"/><path d="M7 8l5 5 5-5"/></svg>',
    cnj_disciplinar:
      '<svg class="icon icon-stroke card-icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>',
    chokepoint_stf:
      '<svg class="icon icon-stroke card-icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M3 21h18"/><path d="M5 21V8l7-4 7 4v13"/><path d="M9 21v-6h6v6"/></svg>',
    eleitoral_tse:
      '<svg class="icon icon-stroke card-icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 01-2 2H5a2 2 0 01-2-2V5a2 2 0 012-2h11"/></svg>',
    soltura_hc:
      '<svg class="icon icon-stroke card-icon" viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 019.9-1"/><path d="M12 16v2"/></svg>',
    progressao_regime:
      '<svg class="icon icon-stroke card-icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14"/><path d="M13 5l7 7-7 7"/></svg>',
    arquivamento:
      '<svg class="icon icon-stroke card-icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M22 19a2 2 0 01-2 2H4a2 2 0 01-2-2V5a2 2 0 012-2h5l2 3h9a2 2 0 012 2z"/></svg>',
    jurisprudencia_estrutural:
      '<svg class="icon icon-stroke card-icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 19.5A2.5 2.5 0 016.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 014 19.5v-15A2.5 2.5 0 016.5 2z"/></svg>',
    foragidos_impacto:
      '<svg class="icon icon-stroke card-icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/><path d="M12 9v4"/><path d="M12 17h.01"/></svg>',
    trafico:
      '<svg class="icon icon-stroke card-icon" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7v6l4 2"/></svg>',
    default:
      '<svg class="icon icon-stroke card-icon" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 8v4"/><path d="M12 16h.01"/></svg>',
  };

  const state = {
    track: "todos",
    grupo: "todos",
    crime: "todos",
    evidence: "todos",
    q: "",
  };

  let raw = null;
  let cards = [];

  function esc(s) {
    return String(s || "").replace(/[&<>"']/g, function (c) {
      return {
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#39;",
      }[c];
    });
  }

  function iconFor(card) {
    if (card.crime_tags && card.crime_tags.indexOf("foragido") !== -1) {
      return ICONS.foragidos_impacto;
    }
    if (card.crime_tags && card.crime_tags.indexOf("trafico") !== -1) {
      return ICONS.trafico;
    }
    return ICONS[card.grupo] || ICONS.default;
  }

  function fmtNum(n) {
    if (n == null) return "—";
    if (typeof n === "string") return n;
    return n.toLocaleString("pt-BR");
  }

  function hcStjDisplay() {
    const divs = raw.divergencias_nao_reconciliadas || [];
    const d = divs.find(function (x) {
      return x.indicador === "hc_traficantes_stj_2024";
    });
    if (d && d.valor_a && d.valor_b) {
      return fmtNum(d.valor_a.numero) + " / " + fmtNum(d.valor_b.numero);
    }
    return fmtNum((raw.stats || {}).hc_traficantes_stj_2024);
  }

  function renderStats() {
    const s = raw.stats || {};
    const el = document.getElementById("statGrid");
    const items = [
      [raw.total, "casos no painel", ""],
      [s.captura, "captura institucional", "gold"],
      [s.decisoes, "decisões de impacto", "teal"],
      [s.ev_confirmed, "ev-confirmed", ""],
      [hcStjDisplay(), "HC tráfico STJ (2024, R4)", "red"],
      [s.foragidos_hc_marco_aurelio_2020, "foragidos via HC (2020)", "red"],
    ];
    el.innerHTML = items
      .map(function (item) {
        return (
          '<div class="stat-cell"><span class="stat-num ' +
          (item[2] || "") +
          '">' +
          (typeof item[0] === "string" ? esc(item[0]) : fmtNum(item[0])) +
          '</span><span class="stat-lbl">' +
          item[1] +
          "</span></div>"
        );
      })
      .join("");
  }

  function renderAlertas() {
    const list = raw.alertas_sistemicos || [];
    const el = document.getElementById("alertsGrid");
    if (!list.length) {
      el.innerHTML =
        '<p class="empty-state">Nenhum alerta sistêmico no corpus atual.</p>';
      return;
    }
    el.innerHTML = list
      .map(function (a) {
        const nivel = a.nivel || "medio";
        const label =
          nivel === "alto"
            ? "Risco alto"
            : nivel === "baixo"
              ? "Atenção"
              : "Risco médio";
        return (
          '<div class="alert-card ' +
          esc(nivel) +
          '"><div class="alert-level">' +
          esc(label) +
          '</div><div class="alert-title">' +
          esc(a.titulo) +
          '</div><div class="alert-text">' +
          esc(a.descricao) +
          "</div></div>"
        );
      })
      .join("");
  }

  function renderDataTable() {
    const s = raw.stats || {};
    const tbody = document.getElementById("dataTableBody");
    const rows = [
      ["Casos captura institucional", s.captura, raw.sync_date, "lawfare-timeline", "Extract JusMonitor"],
      ["Casos decisões de impacto", s.decisoes, "2005–2026", "T-209 JustiçaWatch", "Sidecar reconciliado R1–R7"],
      ["HC traficantes STJ (R4)", hcStjDisplay(), "2024", "STJ/ConJur × dossiê Seif", "Divergência não reconciliada"],
      ["HC/RHC tráfico STJ (ConJur)", s.hc_stj_2024_conjur, "2024", "ConJur/STJ", "Até 26/dez/2024"],
      ["HC tráfico privilegiado STJ", s.hc_stj_2024_privilegiado, "2024", "ConJur/STJ", "Aplicação do §4º"],
      ["Concessões HC/RHC STJ (total)", s.hc_stj_2024_concessoes_total, "2024", "ConJur/STJ", "Base do percentual 49,1%"],
      ["HC tráfico STF", s.hc_trafico_stf_2024, "2024", "Fontes públicas", "Agregado"],
      ["Taxa reincidência BR", s.taxa_reincidencia_br, "—", "Fontes públicas", "Indicador contextual"],
      ["População carcerária", s.populacao_carceraria, "—", "Fontes públicas", "Contexto"],
      ["Foragidos HC Marco Aurélio", s.foragidos_hc_marco_aurelio_2020, "2020", "Estadão", "Investigação"],
      ["Pendentes enriquecimento", raw.excluidos_pendente_enriquecimento, raw.sync_date, "corpus", "Lacuna de dados"],
      ["Conflitos resolvidos (R3)", (raw.conflitos_resolvidos || []).length, raw.sync_date, "curadoria", "Ver envelope unified"],
      ["Divergências abertas (R4)", (raw.divergencias_nao_reconciliadas || []).length, raw.sync_date, "curadoria", "Dois valores exibidos"],
    ];
    tbody.innerHTML = rows
      .map(function (r) {
        const val = typeof r[1] === "string" ? r[1] : fmtNum(r[1]);
        return (
          "<tr><td>" +
          esc(r[0]) +
          '</td><td class="num-up">' +
          esc(val) +
          "</td><td>" +
          esc(r[2]) +
          "</td><td>" +
          esc(r[3]) +
          "</td><td>" +
          esc(r[4]) +
          "</td></tr>"
        );
      })
      .join("");
  }

  function renderDivergencias() {
    const el = document.getElementById("divergenciasBox");
    if (!el) return;
    const list = raw.divergencias_nao_reconciliadas || [];
    if (!list.length) {
      el.innerHTML =
        "<p>Nenhuma divergência numérica aberta no envelope atual.</p>";
      return;
    }
    el.innerHTML = list
      .map(function (d) {
        const a = d.valor_a || {};
        const b = d.valor_b || {};
        return (
          "<p><strong>" +
          esc(d.indicador || "indicador") +
          "</strong> (" +
          esc(d.regra_aplicada || "R4") +
          "): " +
          esc(fmtNum(a.numero)) +
          " (" +
          esc(a.fonte || "fonte A") +
          ") vs " +
          esc(fmtNum(b.numero)) +
          " (" +
          esc(b.fonte || "fonte B") +
          "). " +
          esc(d.status || "") +
          "</p>"
        );
      })
      .join("");
  }

  function chip(label, count, attrs, active) {
    const extra = Object.keys(attrs)
      .map(function (k) {
        return k + '="' + esc(attrs[k]) + '"';
      })
      .join(" ");
    return (
      '<button type="button" class="chip' +
      (active ? " active" : "") +
      '" ' +
      extra +
      ">" +
      esc(label) +
      (count != null ? " (" + count + ")" : "") +
      "</button>"
    );
  }

  function renderFilters() {
    const tracks = document.getElementById("filterTrack");
    const groups = document.getElementById("filterGroup");
    const crimes = document.getElementById("filterCrime");
    const evidence = document.getElementById("filterEvidence");

    const trackCounts = { todos: cards.length };
    const groupCounts = {};
    const crimeCounts = {};
    const evCounts = { todos: cards.length };

    cards.forEach(function (c) {
      trackCounts[c.track] = (trackCounts[c.track] || 0) + 1;
      groupCounts[c.grupo] = (groupCounts[c.grupo] || 0) + 1;
      evCounts[c.evidence_status] = (evCounts[c.evidence_status] || 0) + 1;
      (c.crime_tags || []).forEach(function (t) {
        crimeCounts[t] = (crimeCounts[t] || 0) + 1;
      });
    });

    tracks.innerHTML =
      '<span class="filters-label">Trilha:</span>' +
      Object.keys(TRACK_LABELS)
        .map(function (k) {
          if (k !== "todos" && !trackCounts[k]) return "";
          return chip(TRACK_LABELS[k], trackCounts[k] || 0, { "data-track": k }, state.track === k);
        })
        .join("");

    const groupOrder = [
      "todos",
      "penduricalhos",
      "corrupcao_judicial",
      "cnj_disciplinar",
      "chokepoint_stf",
      "eleitoral_tse",
      "soltura_hc",
      "progressao_regime",
      "arquivamento",
      "jurisprudencia_estrutural",
      "foragidos_impacto",
      "outros_judiciario",
    ];
    groups.innerHTML =
      '<span class="filters-label">Grupo:</span>' +
      groupOrder
        .map(function (k) {
          if (k !== "todos" && !groupCounts[k]) return "";
          const count = k === "todos" ? cards.length : groupCounts[k];
          return chip(GROUP_LABELS[k], count, { "data-grp": k }, state.grupo === k);
        })
        .join("");

    const crimeKeys = ["todos"].concat(Object.keys(CRIME_LABELS).filter(function (k) {
      return k !== "todos" && crimeCounts[k];
    }));
    crimes.innerHTML =
      '<span class="filters-label">Crime:</span>' +
      crimeKeys
        .map(function (k) {
          const count = k === "todos" ? null : crimeCounts[k];
          return chip(CRIME_LABELS[k], count, { "data-crime": k }, state.crime === k);
        })
        .join("");

    evidence.innerHTML =
      '<span class="filters-label">Evidência:</span>' +
      Object.keys(EV_LABELS)
        .map(function (k) {
          if (k !== "todos" && !evCounts[k]) return "";
          return chip(EV_LABELS[k], evCounts[k] || 0, { "data-ev": k }, state.evidence === k);
        })
        .join("");
  }

  function matches(c) {
    if (state.track !== "todos" && c.track !== state.track) return false;
    if (state.grupo !== "todos" && c.grupo !== state.grupo) return false;
    if (state.evidence !== "todos" && c.evidence_status !== state.evidence) return false;
    if (state.crime !== "todos") {
      if (!(c.crime_tags || []).includes(state.crime) && !(c.tags || []).includes(state.crime)) {
        return false;
      }
    }
    if (!state.q) return true;
    const hay = [
      c.titulo,
      c.descricao,
      (c.tags || []).join(" "),
      (c.instituicoes || []).join(" "),
      (c.crime_tags || []).join(" "),
      c.ref || "",
      c.tribunal || "",
      c.tipo_decisao || "",
      c.lacuna_investigativa || "",
      c.id != null ? String(c.id) : "",
    ]
      .join(" ")
      .toLowerCase();
    return hay.indexOf(state.q) !== -1;
  }

  function cardHTML(c) {
    const fontesHTML =
      c.fontes && c.fontes.length
        ? '<div class="card-sources">' +
          c.fontes
            .slice(0, 4)
            .map(function (u) {
              return (
                '<a href="' +
                esc(u) +
                '" target="_blank" rel="noopener">↗ ' +
                esc(u) +
                "</a>"
              );
            })
            .join("") +
          "</div>"
        : "";
    const tagsHTML = (c.tags || [])
      .slice(0, 6)
      .map(function (t) {
        return '<span class="tag">' + esc(t) + "</span>";
      })
      .join("");
    const valorHTML = c.valor_envolvido
      ? '<div class="card-valor">' + esc(c.valor_envolvido) + "</div>"
      : "";
    const refHTML = c.ref
      ? '<div class="card-ref">' + esc(c.ref) + (c.tribunal ? " · " + esc(c.tribunal) : "") + "</div>"
      : "";
    const lacunaHTML = c.lacuna_investigativa
      ? '<div class="card-ref">Lacuna: ' + esc(c.lacuna_investigativa) + "</div>"
      : "";
    const evClass = c.evidence_status === "ev-confirmed" ? "confirmed" : "alleged";
    const trackLabel =
      c.track === "decisoes_impacto" ? "Decisões" : "Captura";

    return (
      '<article class="card" data-track="' +
      esc(c.track) +
      '">' +
      '<div class="card-top">' +
      '<span class="card-date">' +
      iconFor(c) +
      esc(c.data) +
      "</span>" +
      '<div class="card-badges">' +
      '<span class="badge badge-track-' +
      esc(c.track) +
      '">' +
      trackLabel +
      "</span>" +
      '<span class="badge badge-grp-' +
      esc(c.grupo) +
      '">' +
      esc(GROUP_LABELS[c.grupo] || c.grupo) +
      "</span>" +
      '<span class="badge badge-ev ' +
      evClass +
      '">' +
      esc(c.evidence_status) +
      "</span>" +
      "</div></div>" +
      "<h3>" +
      esc(c.titulo) +
      "</h3>" +
      "<p>" +
      esc(c.descricao) +
      "</p>" +
      valorHTML +
      refHTML +
      lacunaHTML +
      '<div class="card-meta">' +
      tagsHTML +
      "</div>" +
      fontesHTML +
      "</article>"
    );
  }

  function renderFeed() {
    const list = cards.filter(matches);
    document.getElementById("countRow").innerHTML =
      "<b>" + list.length + "</b> de " + cards.length + " casos exibidos";
    const container = document.getElementById("cardList");
    container.innerHTML = list.length
      ? list.map(cardHTML).join("")
      : '<div class="empty-state">Nenhum caso corresponde aos filtros atuais.</div>';
  }

  function bindFilters() {
    document.getElementById("filterTrack").addEventListener("click", function (e) {
      const btn = e.target.closest("[data-track]");
      if (!btn) return;
      state.track = btn.getAttribute("data-track");
      renderFilters();
      renderFeed();
    });
    document.getElementById("filterGroup").addEventListener("click", function (e) {
      const btn = e.target.closest("[data-grp]");
      if (!btn) return;
      state.grupo = btn.getAttribute("data-grp");
      renderFilters();
      renderFeed();
    });
    document.getElementById("filterCrime").addEventListener("click", function (e) {
      const btn = e.target.closest("[data-crime]");
      if (!btn) return;
      state.crime = btn.getAttribute("data-crime");
      renderFilters();
      renderFeed();
    });
    document.getElementById("filterEvidence").addEventListener("click", function (e) {
      const btn = e.target.closest("[data-ev]");
      if (!btn) return;
      state.evidence = btn.getAttribute("data-ev");
      renderFilters();
      renderFeed();
    });
    document.getElementById("search").addEventListener("input", function (e) {
      state.q = e.target.value.trim().toLowerCase();
      renderFeed();
    });
  }

  function renderEcosystem(hubs) {
    const el = document.getElementById("ecoGrid");
    if (!el) return;
    if (!hubs || !hubs.length) {
      el.innerHTML = '<div class="eco-empty">Ecossistema indisponível.</div>';
      return;
    }
    el.innerHTML = hubs
      .map(function (h) {
        const current = !!h.current;
        const title = esc(h.title || "");
        const desc = esc(h.description || "");
        const href = esc(h.href || "#");
        const badge = current ? '<span class="eco-badge">este hub</span>' : "";
        if (current) {
          return (
            '<div class="eco-card is-current" aria-current="page">' +
            '<div class="eco-card-title">' +
            title +
            badge +
            "</div>" +
            '<p class="eco-card-desc">' +
            desc +
            "</p></div>"
          );
        }
        return (
          '<a class="eco-card" href="' +
          href +
          '" target="_blank" rel="noopener noreferrer">' +
          '<div class="eco-card-title">' +
          title +
          "</div>" +
          '<p class="eco-card-desc">' +
          desc +
          "</p></a>"
        );
      })
      .join("");
  }

  function boot(data) {
    raw = data;
    cards = data.cards || [];
    const syncText = data.sync_date || "—";
    document.getElementById("syncDate").textContent = syncText;
    const footerSync = document.getElementById("footer-sync-date");
    if (footerSync) footerSync.textContent = syncText;
    document.getElementById("lacunaText").textContent =
      (data.excluidos_pendente_enriquecimento || 0) +
      " entradas do corpus de captura correspondem ao escopo temático mas carecem de descrição/fonte estruturada — excluídas do painel até enriquecimento.";
    renderStats();
    renderAlertas();
    renderDataTable();
    renderDivergencias();
    renderFilters();
    renderFeed();
    bindFilters();
  }

  const gotop = document.getElementById("gotop");
  window.addEventListener("scroll", function () {
    gotop.classList.toggle("show", window.scrollY > 500);
  });
  gotop.addEventListener("click", function () {
    window.scrollTo({ top: 0, behavior: "smooth" });
  });

  fetch("data/unified.json")
    .then(function (r) {
      if (!r.ok) throw new Error("HTTP " + r.status);
      return r.json();
    })
    .then(boot)
    .catch(function (err) {
      document.getElementById("cardList").innerHTML =
        '<div class="error-state">Falha ao carregar data/unified.json — ' +
        esc(err.message) +
        "</div>";
    });

  fetch("data/ecosystem.json")
    .then(function (r) {
      if (!r.ok) throw new Error("HTTP " + r.status);
      return r.json();
    })
    .then(renderEcosystem)
    .catch(function () {
      const el = document.getElementById("ecoGrid");
      if (el) el.innerHTML = '<div class="eco-empty">Falha ao carregar data/ecosystem.json.</div>';
    });
})();
