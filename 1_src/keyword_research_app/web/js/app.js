const DATA_PATHS = [
  "data/keywords_report.json",
  "data/keywords_report.example.json",
];

const COLUMN_HELP = {
  input_order: {
    type: "Número",
    description: "A ordem em que você digitou essa palavra na lista de entrada. Serve só para saber de onde ela veio.",
    source: "Aplicação",
  },
  keyword: {
    type: "Texto",
    description: "A palavra-chave que foi pesquisada, já com espaços extras removidos.",
    source: "Arquivo de entrada",
  },
  avg_monthly_searches: {
    type: "Número inteiro",
    description: "Quantas vezes por mês as pessoas pesquisam esse termo no Google. Número estimado pelo Google Ads, não exato.",
    source: "Google Ads ou MOCK",
  },
  competition: {
    type: "BAIXA / MÉDIA / ALTA",
    description: "Quão concorrida é essa palavra entre anunciantes do Google. ALTA = muita gente pagando para anunciar nela.",
    source: "Google Ads ou MOCK",
  },
  competition_index: {
    type: "0 a 100",
    description: "Versão numérica da competição. 0 = quase ninguém anunciando; 100 = concorrência máxima entre anunciantes.",
    source: "Google Ads ou MOCK",
  },
  low_top_bid: {
    type: "Reais (R$)",
    description: "O mínimo que anunciantes pagam por clique para aparecer no topo do Google com essa palavra.",
    source: "Google Ads ou MOCK",
  },
  high_top_bid: {
    type: "Reais (R$)",
    description: "O máximo que anunciantes pagam por clique para aparecer no topo do Google com essa palavra.",
    source: "Google Ads ou MOCK",
  },
  average_interest: {
    type: "0 a 100",
    description: "A média do interesse das pessoas por esse termo na janela de tempo selecionada. 100 = pico máximo histórico; 0 = ninguém pesquisando.",
    source: "Google Trends",
  },
  peak_interest: {
    type: "0 a 100",
    description: "O maior pico de interesse registrado na janela selecionada. Mostra o teto de popularidade que o termo já atingiu.",
    source: "Google Trends",
  },
  latest_interest: {
    type: "0 a 100",
    description: "O interesse no período mais recente da janela. Mostra se o tema ainda está ativo agora.",
    source: "Google Trends",
  },
  trend_direction: {
    type: "CRESCENTE / ESTÁVEL / DECRESCENTE",
    description: "Resume se o interesse está subindo, estagnado ou caindo ao longo da janela de tempo selecionada.",
    source: "Calculado pela aplicação",
  },
  trend_change: {
    type: "Pontos (+/-)",
    description: "Quanto o interesse mudou ao longo da janela em pontos do índice. Positivo = crescendo; negativo = caindo.",
    source: "Calculado pela aplicação",
  },
  growth_rate: {
    type: "Porcentagem (%)",
    description: "Variação percentual entre o primeiro e o último valor da série. Mostra o crescimento ou queda relativa.",
    source: "Calculado pela aplicação",
  },
  relevance_score: {
    type: "0 a 100",
    description: "Nota final que combina interesse médio (50%), interesse recente (30%) e tendência (20%). Use para comparar e ranquear palavras entre si.",
    source: "Calculado pela aplicação",
  },
  source: {
    type: "Texto",
    description: "De onde vieram os dados: GOOGLE_TRENDS (interesse real), GOOGLE_ADS (volume de busca), ou MOCK (simulação para testes).",
    source: "Pipeline da aplicação",
  },
};

const WINDOW_POINTS = { "7d": 1, "30d": 4, "90d": 13, "1y": Infinity };

const state = {
  report: null,
  rows: [],
  computedRows: [],
  filteredRows: [],
  sortKey: "keyword",
  sortDirection: "asc",
  searchTerm: "",
  timeWindow: "1y",
  activeRow: null,
};

const elements = {
  searchInput: document.getElementById("search-input"),
  sortColumn: document.getElementById("sort-column"),
  sortDirection: document.getElementById("sort-direction"),
  sortAz: document.getElementById("sort-az"),
  sortZa: document.getElementById("sort-za"),
  clearFilters: document.getElementById("clear-filters"),
  status: document.getElementById("status"),
  table: document.getElementById("keywords-table"),
  chartPanel: document.getElementById("chart-panel"),
  chartTitle: document.getElementById("chart-title"),
  chartContent: document.getElementById("chart-content"),
  chartClose: document.getElementById("chart-close"),
};

function computeTrend(values) {
  if (values.length < 2) {
    return { slope: 0, change: 0, direction: "ESTÁVEL" };
  }
  const n = values.length;
  const meanX = (n - 1) / 2;
  const meanY = values.reduce((a, b) => a + b, 0) / n;
  let numerator = 0;
  let denominator = 0;
  for (let i = 0; i < n; i++) {
    numerator += (i - meanX) * (values[i] - meanY);
    denominator += (i - meanX) ** 2;
  }
  const slope = denominator ? numerator / denominator : 0;
  const change = slope * (n - 1);
  const direction = change >= 5 ? "CRESCENTE" : change <= -5 ? "DECRESCENTE" : "ESTÁVEL";
  return {
    slope: Math.round(slope * 100) / 100,
    change: Math.round(change * 100) / 100,
    direction,
  };
}

function computeWindowMetrics(row, windowKey) {
  const timeline = Array.isArray(row.timeline) ? row.timeline : [];
  if (!timeline.length) {
    return { ...row, _windowTimeline: [] };
  }
  const count = WINDOW_POINTS[windowKey] ?? Infinity;
  const sliced = count === Infinity ? timeline : timeline.slice(-count);
  const values = sliced.map((p) => p.interest);

  if (!values.length) {
    return { ...row, _windowTimeline: sliced };
  }

  const sum = values.reduce((a, b) => a + b, 0);
  const average_interest = Math.round((sum / values.length) * 100) / 100;
  const peak_interest = Math.max(...values);
  const latest_interest = values[values.length - 1];

  const trend = computeTrend(values);
  const trend_component = Math.max(0, Math.min(100, 50 + trend.change));
  const relevance_score = Math.round(
    (0.5 * average_interest + 0.3 * latest_interest + 0.2 * trend_component) * 100
  ) / 100;

  return {
    ...row,
    average_interest,
    peak_interest,
    latest_interest,
    trend_slope: trend.slope,
    trend_change: trend.change,
    trend_direction: trend.direction,
    relevance_score,
    _windowTimeline: sliced,
  };
}

async function loadJson() {
  let lastError = null;

  for (const path of DATA_PATHS) {
    try {
      const response = await fetch(path, { cache: "no-store" });
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }

      const report = await response.json();
      validateReport(report);
      return { report, path };
    } catch (error) {
      lastError = error;
    }
  }

  throw new Error(`Nao foi possivel carregar os dados JSON. Detalhe: ${lastError.message}`);
}

function validateReport(report) {
  if (!report || !Array.isArray(report.columns) || !Array.isArray(report.rows)) {
    throw new Error("JSON sem estrutura obrigatoria: metadata, columns e rows.");
  }

  const obsoleteColumns = new Set([
    "contextual_query",
    "comparison_anchor",
    "context_average_interest",
    "anchor_average_interest",
  ]);
  const hasObsoleteColumns = report.columns.some((column) =>
    obsoleteColumns.has(column.key)
  );
  if (report.metadata?.source === "GOOGLE_TRENDS" && hasObsoleteColumns) {
    throw new Error(
      "Relatorio antigo ou incompatível. Execute novamente a coleta " +
      "individual de três meses."
    );
  }
}

function renderControls(columns) {
  elements.sortColumn.innerHTML = "";

  columns.forEach((column) => {
    const option = document.createElement("option");
    option.value = column.key;
    option.textContent = column.label;
    elements.sortColumn.appendChild(option);
  });

  elements.sortColumn.value = state.sortKey;
}

function renderTable() {
  const { columns } = state.report;
  elements.table.innerHTML = "";

  const thead = document.createElement("thead");
  const headerRow = document.createElement("tr");

  columns.forEach((column) => {
    const th = document.createElement("th");
    th.scope = "col";
    th.tabIndex = 0;
    th.dataset.key = column.key;
    th.setAttribute("aria-sort", getAriaSort(column.key));
    th.appendChild(createHeaderContent(column));
    th.classList.toggle("is-sorted", state.sortKey === column.key);
    th.addEventListener("click", () => sortByColumn(column.key));
    th.addEventListener("keydown", (event) => {
      if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        sortByColumn(column.key);
      }
    });
    headerRow.appendChild(th);
  });

  thead.appendChild(headerRow);
  elements.table.appendChild(thead);

  const tbody = document.createElement("tbody");

  if (state.filteredRows.length === 0) {
    const emptyRow = document.createElement("tr");
    const emptyCell = document.createElement("td");
    emptyCell.className = "empty-state";
    emptyCell.colSpan = columns.length;
    emptyCell.textContent = "Nenhum resultado encontrado.";
    emptyRow.appendChild(emptyCell);
    tbody.appendChild(emptyRow);
  } else {
    state.filteredRows.forEach((row) => {
      const tr = document.createElement("tr");
      tr.setAttribute("role", "button");
      tr.setAttribute("tabindex", "0");
      tr.setAttribute("aria-label", `Ver gráfico: ${row.keyword}`);
      tr.addEventListener("click", () => openChart(row));
      tr.addEventListener("keydown", (event) => {
        if (event.key === "Enter" || event.key === " ") {
          event.preventDefault();
          openChart(row);
        }
      });

      columns.forEach((column) => {
        const td = document.createElement("td");
        const skipColumns = new Set(["keyword", "input_order", "source"]);
        if (row.skipped && !skipColumns.has(column.key)) {
          td.textContent = "—";
          td.classList.add("cell--skipped");
          td.title = "Bloqueado por HTTP 429 — execute novamente para coletar";
        } else {
          const value = row[column.key];
          td.textContent = formatValue(column.key, value);
          if (isNumericValue(value)) {
            td.classList.add("cell--number");
          }
        }
        tr.appendChild(td);
      });

      tbody.appendChild(tr);
    });
  }

  elements.table.appendChild(tbody);
  updateStatus();
}

function createHeaderContent(column) {
  const content = document.createElement("span");
  content.className = "column-header";

  const label = document.createElement("span");
  label.textContent = getHeaderLabel(column);
  content.appendChild(label);

  const help = getColumnHelp(column);
  if (!help) {
    return content;
  }

  const tooltipId = `column-help-${column.key.replace(/[^a-z0-9_-]/gi, "-")}`;
  const helpWrapper = document.createElement("span");
  helpWrapper.className = "column-help";

  const helpButton = document.createElement("button");
  helpButton.type = "button";
  helpButton.className = "column-help__button";
  helpButton.textContent = "i";
  helpButton.title = help;
  helpButton.setAttribute("aria-label", `Ajuda sobre ${column.label}`);
  helpButton.setAttribute("aria-describedby", tooltipId);
  helpButton.addEventListener("click", (event) => event.stopPropagation());
  helpButton.addEventListener("keydown", (event) => event.stopPropagation());

  const tooltip = document.createElement("span");
  tooltip.id = tooltipId;
  tooltip.className = "column-help__tooltip";
  tooltip.setAttribute("role", "tooltip");
  tooltip.textContent = help;

  helpWrapper.append(helpButton, tooltip);
  content.appendChild(helpWrapper);
  return content;
}

function getColumnHelp(column) {
  const help = COLUMN_HELP[column.key];
  if (!help) {
    return "";
  }
  return `${help.description} (${help.type} — ${help.source})`;
}

function getAriaSort(columnKey) {
  if (state.sortKey !== columnKey) {
    return "none";
  }
  return state.sortDirection === "asc" ? "ascending" : "descending";
}

function getHeaderLabel(column) {
  if (state.sortKey !== column.key) {
    return column.label;
  }

  const marker = state.sortDirection === "asc" ? " ↑" : " ↓";
  return `${column.label}${marker}`;
}

function applySearch() {
  const term = state.searchTerm.trim().toLocaleLowerCase("pt-BR");

  if (!term) {
    state.filteredRows = [...state.computedRows];
    return;
  }

  state.filteredRows = state.computedRows.filter((row) =>
    state.report.columns.some((column) => {
      const value = row[column.key];
      return String(value ?? "").toLocaleLowerCase("pt-BR").includes(term);
    })
  );
}

function applySorting() {
  const directionFactor = state.sortDirection === "asc" ? 1 : -1;

  state.filteredRows.sort((left, right) => {
    const leftValue = left[state.sortKey];
    const rightValue = right[state.sortKey];

    if (isEmpty(leftValue) && isEmpty(rightValue)) {
      return 0;
    }
    if (isEmpty(leftValue)) {
      return 1;
    }
    if (isEmpty(rightValue)) {
      return -1;
    }

    if (isNumericValue(leftValue) && isNumericValue(rightValue)) {
      return (Number(leftValue) - Number(rightValue)) * directionFactor;
    }

    return String(leftValue).localeCompare(String(rightValue), "pt-BR", {
      numeric: true,
      sensitivity: "base",
    }) * directionFactor;
  });
}

function updateTable() {
  applySearch();
  applySorting();
  renderTable();
}

function sortByColumn(columnKey) {
  if (state.sortKey === columnKey) {
    state.sortDirection = state.sortDirection === "asc" ? "desc" : "asc";
  } else {
    state.sortKey = columnKey;
    state.sortDirection = "asc";
  }

  elements.sortColumn.value = state.sortKey;
  elements.sortDirection.value = state.sortDirection;
  updateTable();
}

function clearFilters() {
  state.searchTerm = "";
  state.sortKey = "keyword";
  state.sortDirection = "asc";
  elements.searchInput.value = "";
  elements.sortColumn.value = state.sortKey;
  elements.sortDirection.value = state.sortDirection;
  updateTable();
}

function switchTimeWindow(windowKey) {
  state.timeWindow = windowKey;
  state.computedRows = state.rows.map((row) => computeWindowMetrics(row, windowKey));
  document.querySelectorAll(".time-window__btn").forEach((btn) => {
    btn.classList.toggle("is-active", btn.dataset.window === windowKey);
  });
  if (state.activeRow) {
    const updated = state.computedRows.find((r) => r.keyword === state.activeRow.keyword);
    if (updated) {
      renderChartPanel(updated);
      state.activeRow = updated;
    }
  }
  updateTable();
}

function openChart(row) {
  state.activeRow = row;
  renderChartPanel(row);
  elements.chartPanel.hidden = false;
  elements.chartPanel.scrollIntoView({ behavior: "smooth", block: "nearest" });
}

function closeChart() {
  elements.chartPanel.hidden = true;
  state.activeRow = null;
}

function renderChartPanel(row) {
  const timeline = row._windowTimeline || row.timeline || [];
  elements.chartTitle.textContent = row.keyword;
  if (row.skipped) {
    elements.chartContent.innerHTML =
      "<p class=\"chart-empty\">Dado indisponível — bloqueado por HTTP 429. " +
      "Execute novamente para coletar esta palavra.</p>";
    return;
  }
  elements.chartContent.innerHTML = renderChartSVG(timeline);
}

function evenlySampled(n, maxLabels) {
  if (n <= maxLabels) {
    return Array.from({ length: n }, (_, i) => i);
  }
  const result = [];
  for (let i = 0; i < maxLabels; i++) {
    result.push(Math.round((i * (n - 1)) / (maxLabels - 1)));
  }
  return [...new Set(result)];
}

function renderChartSVG(timeline) {
  if (!timeline.length) {
    return "<p class=\"chart-empty\">Sem dados de timeline para a janela selecionada.</p>";
  }

  const W = 760;
  const H = 240;
  const PL = 44;
  const PR = 16;
  const PT = 16;
  const PB = 40;
  const chartW = W - PL - PR;
  const chartH = H - PT - PB;

  const values = timeline.map((p) => p.interest);
  const dates = timeline.map((p) => String(p.date || "").split("T")[0]);
  const n = values.length;
  const xStep = n > 1 ? chartW / (n - 1) : 0;

  const toX = (i) => PL + i * xStep;
  const toY = (v) => PT + chartH - (v / 100) * chartH;

  const pointsStr = values.map((v, i) => `${toX(i)},${toY(v)}`).join(" ");

  const yTicks = [0, 25, 50, 75, 100];
  const yAxisParts = yTicks.map((v) => {
    const y = toY(v);
    return (
      `<line x1="${PL}" y1="${y}" x2="${W - PR}" y2="${y}" stroke="#e8e8e8" stroke-width="1"/>` +
      `<text x="${PL - 6}" y="${y + 4}" text-anchor="end" font-size="10" fill="#666">${v}</text>`
    );
  });

  const labelIndices = evenlySampled(n, 6);
  const xAxisParts = labelIndices.map((i) => {
    const x = toX(i);
    const d = dates[i] ? dates[i].slice(5) : "";
    return `<text x="${x}" y="${PT + chartH + 20}" text-anchor="middle" font-size="10" fill="#666">${d}</text>`;
  });

  const dotsParts = values.map((v, i) =>
    `<circle cx="${toX(i)}" cy="${toY(v)}" r="2.5" fill="#005fcc"/>`
  );

  return (
    `<svg viewBox="0 0 ${W} ${H}" xmlns="http://www.w3.org/2000/svg" width="100%" aria-label="Gráfico de interesse">` +
    yAxisParts.join("") +
    xAxisParts.join("") +
    `<line x1="${PL}" y1="${PT}" x2="${PL}" y2="${PT + chartH}" stroke="#888" stroke-width="1"/>` +
    `<line x1="${PL}" y1="${PT + chartH}" x2="${W - PR}" y2="${PT + chartH}" stroke="#888" stroke-width="1"/>` +
    `<polyline points="${pointsStr}" fill="none" stroke="#005fcc" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/>` +
    dotsParts.join("") +
    `</svg>`
  );
}

function formatValue(key, value) {
  if (isEmpty(value)) {
    return "";
  }

  if (key.includes("bid")) {
    return Number(value).toLocaleString("pt-BR", {
      style: "currency",
      currency: "BRL",
      minimumFractionDigits: 2,
    });
  }

  if (key === "growth_rate") {
    return `${Number(value).toLocaleString("pt-BR", {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    })}%`;
  }

  if (key === "relevance_score") {
    return `${Number(value).toLocaleString("pt-BR", {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    })} / 100`;
  }

  if (key === "trend_change") {
    return `${Number(value).toLocaleString("pt-BR", {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    })} pts`;
  }

  if (isNumericValue(value)) {
    return Number(value).toLocaleString("pt-BR");
  }

  return String(value);
}

function isNumericValue(value) {
  return value !== null && value !== "" && Number.isFinite(Number(value));
}

function isEmpty(value) {
  return value === null || value === undefined || value === "";
}

function updateStatus() {
  const total = state.rows.length;
  const visible = state.filteredRows.length;
  const source = state.report.metadata?.source ?? "UNKNOWN";
  const generatedAt = state.report.metadata?.generated_at ?? "sem data";
  elements.status.classList.remove("status--error", "status--warning");
  if (source === "MOCK") {
    elements.status.classList.add("status--warning");
    elements.status.textContent =
      `ATENÇÃO: dados simulados | ${visible} de ${total} registros | ` +
      `gerado em ${generatedAt}`;
    return;
  }
  elements.status.textContent =
    `${visible} de ${total} registros | fonte ${source} | ` +
    `gerado em ${generatedAt}`;
}

function handleLoadError(error) {
  elements.status.classList.add("status--error");
  elements.status.textContent = error.message;
  elements.table.innerHTML = "";
}

function bindEvents() {
  elements.searchInput.addEventListener("input", (event) => {
    state.searchTerm = event.target.value;
    updateTable();
  });

  elements.sortColumn.addEventListener("change", (event) => {
    state.sortKey = event.target.value;
    updateTable();
  });

  elements.sortDirection.addEventListener("change", (event) => {
    state.sortDirection = event.target.value;
    updateTable();
  });

  elements.sortAz.addEventListener("click", () => {
    state.sortDirection = "asc";
    elements.sortDirection.value = "asc";
    updateTable();
  });

  elements.sortZa.addEventListener("click", () => {
    state.sortDirection = "desc";
    elements.sortDirection.value = "desc";
    updateTable();
  });

  elements.clearFilters.addEventListener("click", clearFilters);

  document.querySelectorAll(".time-window__btn").forEach((btn) => {
    btn.addEventListener("click", () => switchTimeWindow(btn.dataset.window));
  });

  elements.chartClose.addEventListener("click", closeChart);
}

async function init() {
  try {
    const { report } = await loadJson();
    state.report = report;
    state.rows = [...report.rows];
    state.computedRows = state.rows.map((row) => computeWindowMetrics(row, state.timeWindow));
    state.filteredRows = [...state.computedRows];
    state.sortKey = report.columns[1]?.key ?? report.columns[0].key;
    renderControls(report.columns);
    bindEvents();
    updateTable();
  } catch (error) {
    handleLoadError(error);
  }
}

init();
