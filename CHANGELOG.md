# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/) e este projeto segue [Versionamento Semântico](https://semver.org/spec/v2.0.0.html).

## [1.2.0] - 2026-08-10

### Adicionado
- Rodapé atualizado com o crédito de desenvolvimento: "Desenvolvido por `@artesdosul`".
- Integração do snippet do contador de visitas e tráfego hospedado em `stats.artesdosul.com`.
- Exibição dinâmica da versão do painel (`v1.2.0`) e da data da última coleta de dados no rodapé do site.
- Criação deste arquivo `CHANGELOG.md` para documentar a evolução e o versionamento do projeto.

---

## [1.1.0] - 2026-08-06

### Adicionado
- Assimilação das regras de evidência `R1–R7` para reconciliação de decisões judiciais de impacto.
- Metadados Open Graph (OG) e Twitter Card no cabeçalho do `index.html` para melhorar o compartilhamento nas redes sociais, junto com a imagem de destaque `og-jusmonitor.webp`.
- Estruturação da documentação seguindo o Padrão Sentinel.
- Adicionado o arquivo `data/ecosystem.json` com o mapeamento dos hubs do Ecossistema SELVA.

### Modificado
- Refatoração dos scripts de build e validação de dados (`build-unified.py`, `validate-schema.py`, `validate-evidence-rules.py`).
- Atualização geral do `README.md` com instruções detalhadas de setup, segurança, LGPD e governança de dados.

---

## [1.0.0] - 2026-08-05

### Adicionado
- Lançamento inicial do JusMonitor Open Source.
- Painel interativo com filtros por trilha, grupo, crime, evidência e busca textual de casos.
- Estrutura base de dados unificada: `captura_institucional` (oriundo de `lawfare-timeline`) e `decisoes_impacto` (oriundo do JustiçaWatch).
- Gráfico/Grid de estatísticas agregadas de risco sistêmico e alertas.
