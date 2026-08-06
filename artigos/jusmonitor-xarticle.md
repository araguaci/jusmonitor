# JusMonitor: o Judiciário sob evidência pública

O Brasil discute o Judiciário em onda. Escândalo de penduricalho. HC polêmico. Soltura que vira manchete. Depois o ciclo reinicia e o padrão some da memória.

O [JusMonitor](https://jusmonitor.vercel.app) existe para interromper esse ciclo. É um painel open source que junta, no mesmo feed, captura institucional (supersalários, venda de sentenças, CNJ, chokepoints) e decisões de alto impacto (HCs, progressões, arquivamentos em crimes violentos). Cada entrada carrega status evidencial e trilha de fontes. Licença CC0.

Não é opinião disfarçada de dado. É corpus verificável, com aviso explícito: registrar impacto público não implica culpa ou erro do magistrado.

## O que o painel mostra agora

Sync de 5 de agosto de 2026: **87 entradas confirmadas** no feed unificado. Destas, 76 de captura institucional e 11 de decisões de impacto. Vinte e uma marcadas com relevância alta. Outras 62 ficam fora do feed até enriquecimento de fonte — não são apagadas; ficam pendentes.

Três números do próprio painel pesam mais que qualquer slogan:

- **9.166** habeas corpus relacionados a traficantes no STJ em 2024
- **577** HCs de tráfico no STF no mesmo ano
- taxa de reincidência brasileira em torno de **42%**, com população carcerária perto de **834 mil**

Quem quiser debater política criminal sem esses números está debatendo no escuro.

## Duas trilhas, um schema

A trilha `captura_institucional` vem do corpus [lawfare-timeline](https://lawfare-timeline.vercel.app): penduricalhos, corrupção judicial, disciplinar do CNJ, chokepoints do STF, eleitoral/TSE.

A trilha `decisoes_impacto` vem do sidecar T-209 JustiçaWatch: soltura/HC, progressão de regime, arquivamento, jurisprudência estrutural, foragidos de impacto.

As duas viram `data/unified.json`. O site é estático. Sem login. Sem paywall. Sem “confiança no algoritmo”.

## Casos que não cabem em thread

Em maio de 2026, levantamento mostrou o **TJMG** ainda pagando acima do teto a um terço dos magistrados, mesmo após a decisão do STF de 25/03/2026. Em 2025 o tribunal havia pago **R$ 1,22 bilhão** acima do teto — segundo no ranking nacional, atrás do TJSP (R$ 3,94 bilhões). Em 61% dos casos, penduricalhos passaram da metade da remuneração bruta.

Dias depois, ministros do STF publicaram decisões barrando manobras administrativas: reclassificar jurisdição como “difícil provimento”, inventar bônus por acúmulo, pagar em múltiplas folhas. Qualquer ato posterior a 25/03/2026 que amplie remuneração por via indireta foi tratado como nulo.

Do outro lado da mesa, o histórico de decisões: HC 82.959 (progressão em crimes hediondos), ADC 43 (retorno ao trânsito em julgado), liminares monocráticas com janela explorada por ao menos **21 réus** que fugiram em 2020. O painel não “resolve” esses casos. Ele impede que sumam.

## Três alertas sistêmicos

O feed traz alertas de risco, não só fichas isoladas:

1. **Intervalo de fuga** — liminar monocrática antes da análise colegiada cria janela operacional.
2. **Tráfico privilegiado desfigurado** — benefício pensado para réu primário aplicado em apreensões de centenas de quilos.
3. **Ausência de banco nacional de solturas** — o BNMP 3.0 não correlaciona soltura com reincidência.

Isso é desenho institucional, não “erro pontual de juiz X”.

## Evidência ou não entra como fato

O schema é rígido de propósito:

> `ev-confirmed` = fonte jornalística ou documental identificável e verificável.
> `ev-alleged` = sem fonte primária registrada — pendente, nunca tratada como confirmada.

Entradas com descrição vazia ou fonte N/A ficam em `excluidos_pendente_enriquecimento`. Melhor lacuna explícita do que falso positivo vestido de certeza.

## O que isto não é

Não é processo disciplinar. Não substitui acórdão. Não é acusação a magistrado. Não é “anti-STF” de gabinete.

É prestação de contas pública sobre eventos e decisões que já são públicos — só que espalhados, efêmeros e sem classificação evidencial.

Se a independência judicial for real, aguenta luz. Se depender de opacidade, o problema não é o painel.

## Open source de verdade

Repositório: [github.com/araguaci/jusmonitor](https://github.com/araguaci/jusmonitor). Licença CC0. Contribuição via issue ou PR em `data/contributions/`. Contribuição não publica sozinha — há curadoria humana.

Para regenerar o feed: `python scripts/build-unified.py`. Schema em `docs/DATA_SCHEMA.md`. Metodologia em `docs/METODOLOGIA.md`.

Quem discorda de um card pode apontar a fonte. Quem discorda do método pode forkar. O que não dá mais é fingir que o padrão não existe porque a manchete da semana passou.

## Fontes

- JusMonitor — painel e corpus unificado (sync 2026-08-05): [https://jusmonitor.vercel.app](https://jusmonitor.vercel.app)
- Repositório: [https://github.com/araguaci/jusmonitor](https://github.com/araguaci/jusmonitor)
- Corpus upstream: [https://lawfare-timeline.vercel.app](https://lawfare-timeline.vercel.app)
- Metodologia e schema: docs no repositório (METODOLOGIA.md, DATA_SCHEMA.md, ARCHITECTURE.md)
- Casos citados no feed: Estado de Minas (TJMG/teto), Agência Brasil / Correio Braziliense (barreiras a penduricalhos), portal STF (HC 82.959, ADC 43), Estadão (foragidos pós-HC)

*Dossiê completo: [https://jusmonitor.vercel.app](https://jusmonitor.vercel.app)*

---

### **Plano de promoção (v2.1)**

**Tweet de abertura** (sem link externo):

> O Judiciário brasileiro vira manchete e some da memória.  
> Penduricalhos de R$ 1,22 bi no TJMG. 9.166 HCs de tráfico no STJ em 2024. 21 foragidos após liminares em 2020.  
> Abri o JusMonitor: feed open source com captura institucional + decisões de impacto, cada card com fonte e status evidencial.  
> Bookmark se for usar no próximo debate — link completo no primeiro reply.

**Primeiro reply** (links externos):

> Painel: **[https://jusmonitor.vercel.app](https://jusmonitor.vercel.app)**  
> Repo CC0: **[https://github.com/araguaci/jusmonitor](https://github.com/araguaci/jusmonitor)**  
> Corpus: **[https://lawfare-timeline.vercel.app](https://lawfare-timeline.vercel.app)**

**Primeiros ~30 min:** responda replies com substância e rebata os próprios comentários quando fizer sentido. **≤ ~2 posts/dia** na conta para não diluir alcance.

  
