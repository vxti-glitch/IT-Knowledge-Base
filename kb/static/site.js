"use strict";

(function () {
  const body = document.body;
  const searchForm = document.getElementById("search-form");
  const searchInput = document.getElementById("search-input");
  const searchClear = document.getElementById("search-clear");
  const resultsCount = document.getElementById("results-count");

  function normalize(value) {
    return String(value || "")
      .normalize("NFKD")
      .replace(/[\u0300-\u036f]/g, "")
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, " ")
      .trim();
  }

  function updateThemeIcon() {
    const icon = document.getElementById("theme-icon");
    const toggle = document.getElementById("theme-toggle");
    const light = document.documentElement.dataset.theme === "light";
    if (icon) icon.textContent = light ? "☀" : "☾";
    if (toggle) toggle.setAttribute("aria-label", light ? "Switch to dark theme" : "Switch to light theme");
  }

  const themeToggle = document.getElementById("theme-toggle");
  if (themeToggle) {
    themeToggle.addEventListener("click", function () {
      const next = document.documentElement.dataset.theme === "light" ? "dark" : "light";
      document.documentElement.dataset.theme = next;
      localStorage.setItem("kb-theme", next);
      updateThemeIcon();
    });
    updateThemeIcon();
  }

  const navToggle = document.getElementById("nav-toggle");
  const sidebar = document.getElementById("sidebar");
  if (navToggle && sidebar) {
    navToggle.addEventListener("click", function () {
      const open = sidebar.classList.toggle("is-open");
      navToggle.setAttribute("aria-expanded", String(open));
      navToggle.setAttribute("aria-label", open ? "Close article navigation" : "Open article navigation");
    });
  }

  document.querySelectorAll(".nav-group-button").forEach(function (button) {
    button.addEventListener("click", function () {
      const expanded = button.getAttribute("aria-expanded") === "true";
      button.setAttribute("aria-expanded", String(!expanded));
    });
  });

  document.querySelectorAll(".article-body pre").forEach(function (pre) {
    if (pre.closest(".codehilite") && pre.parentElement.querySelector(":scope > .copy-button")) return;
    const container = pre.closest(".codehilite") || pre;
    const button = document.createElement("button");
    button.type = "button";
    button.className = "copy-button";
    button.textContent = "Copy";
    button.setAttribute("aria-label", "Copy code block");
    button.addEventListener("click", async function () {
      const code = pre.querySelector("code");
      if (!code) return;
      try {
        await navigator.clipboard.writeText(code.innerText);
        button.textContent = "Copied";
        window.setTimeout(function () { button.textContent = "Copy"; }, 1500);
      } catch (error) {
        button.textContent = "Select code";
      }
    });
    container.appendChild(button);
  });

  const articleActionStatus = document.getElementById("article-action-status");
  const copyTicketNote = document.getElementById("copy-ticket-note");
  if (copyTicketNote) {
    copyTicketNote.addEventListener("click", async function () {
      const heading = Array.from(document.querySelectorAll(".article-body h2, .article-body h3"))
        .find(function (item) { return normalize(item.textContent).includes("ticket note example"); });
      const note = heading ? heading.nextElementSibling : null;
      if (!note) {
        articleActionStatus.textContent = "This article does not include a ticket-note example.";
        return;
      }
      try {
        await navigator.clipboard.writeText(note.innerText.trim());
        articleActionStatus.textContent = "Simulated ticket note copied. Review it before using it in a real ticket.";
      } catch (error) {
        articleActionStatus.textContent = "Copy is unavailable. Select the ticket-note example manually.";
      }
    });
  }

  document.querySelectorAll(".feedback-button").forEach(function (button) {
    button.addEventListener("click", function () {
      const value = button.dataset.feedback;
      localStorage.setItem("kb-feedback:" + window.location.pathname, value);
      document.querySelectorAll(".feedback-button").forEach(function (item) {
        item.classList.toggle("is-selected", item === button);
        item.setAttribute("aria-pressed", String(item === button));
      });
      articleActionStatus.textContent = value === "yes"
        ? "Marked helpful in this browser demonstration."
        : "Marked for improvement in this browser demonstration.";
    });
  });

  document.addEventListener("keydown", function (event) {
    if (event.key === "/" && searchInput && document.activeElement !== searchInput) {
      event.preventDefault();
      searchInput.focus();
    }
    if (event.key === "Escape" && sidebar && sidebar.classList.contains("is-open")) {
      sidebar.classList.remove("is-open");
      navToggle.setAttribute("aria-expanded", "false");
    }
  });

  if (body.dataset.page !== "index") {
    if (searchClear) searchClear.style.display = "none";
    return;
  }

  const cards = Array.from(document.querySelectorAll(".article-card[data-slug]"));
  const sections = Array.from(document.querySelectorAll("[data-category-section]"));
  const noResults = document.getElementById("no-results");
  const categoryFilter = document.getElementById("filter-category");
  const typeFilter = document.getElementById("filter-type");
  const platformFilter = document.getElementById("filter-platform");
  const audienceFilter = document.getElementById("filter-audience");
  const resetFilters = document.getElementById("reset-filters");
  const searchRecords = new Map();

  async function loadSearchIndex() {
    try {
      const response = await fetch("search-index.json", { cache: "no-store" });
      if (!response.ok) throw new Error("Search index request failed");
      const records = await response.json();
      records.forEach(function (record) {
        searchRecords.set(record.slug, normalize([
          record.title,
          record.kb_id,
          record.category,
          record.article_type,
          (record.platforms || []).join(" "),
          (record.tags || []).join(" "),
          record.excerpt,
          record.plain_text
        ].join(" ")));
      });
    } catch (error) {
      console.warn("Using card metadata because search-index.json did not load.", error);
    }
  }

  function selectedValue(element) {
    return element ? element.value : "";
  }

  function updateUrl(query) {
    const url = new URL(window.location.href);
    if (query) url.searchParams.set("q", query);
    else url.searchParams.delete("q");
    window.history.replaceState({}, "", url);
  }

  function applyFilters(updateHistory) {
    const query = searchInput ? searchInput.value.trim() : "";
    const terms = normalize(query).split(" ").filter(Boolean);
    const category = selectedValue(categoryFilter);
    const articleType = selectedValue(typeFilter);
    const platform = selectedValue(platformFilter);
    const audience = selectedValue(audienceFilter);
    let visible = 0;

    cards.forEach(function (card) {
      const searchable = searchRecords.get(card.dataset.slug) || normalize(card.dataset.search);
      const queryMatch = terms.every(function (term) { return searchable.includes(term); });
      const categoryMatch = !category || card.dataset.category === category;
      const typeMatch = !articleType || card.dataset.type === articleType;
      const platforms = (card.dataset.platforms || "").split("|");
      const platformMatch = !platform || platforms.includes(platform);
      const audienceMatch = !audience || card.dataset.audience === audience;
      const show = queryMatch && categoryMatch && typeMatch && platformMatch && audienceMatch;
      card.hidden = !show;
      if (show) visible += 1;
    });

    sections.forEach(function (section) {
      section.hidden = !Array.from(section.querySelectorAll(".article-card")).some(function (card) {
        return !card.hidden;
      });
    });

    const active = Boolean(query || category || articleType || platform || audience);
    if (resultsCount) {
      resultsCount.textContent = active
        ? visible + " of " + cards.length + " articles"
        : cards.length + " articles";
    }
    if (noResults) noResults.hidden = visible !== 0;
    if (searchClear) searchClear.style.display = query ? "grid" : "none";
    if (updateHistory) updateUrl(query);
  }

  if (searchForm) {
    searchForm.addEventListener("submit", function (event) {
      event.preventDefault();
      applyFilters(true);
    });
  }

  if (searchInput) {
    searchInput.addEventListener("input", function () { applyFilters(true); });
    searchInput.addEventListener("keydown", function (event) {
      if (event.key === "Escape") {
        searchInput.value = "";
        applyFilters(true);
      }
    });
  }

  if (searchClear) {
    searchClear.addEventListener("click", function () {
      searchInput.value = "";
      searchInput.focus();
      applyFilters(true);
    });
  }

  [categoryFilter, typeFilter, platformFilter, audienceFilter].forEach(function (filter) {
    if (filter) filter.addEventListener("change", function () { applyFilters(false); });
  });

  if (resetFilters) {
    resetFilters.addEventListener("click", function () {
      if (searchInput) searchInput.value = "";
      if (categoryFilter) categoryFilter.value = "";
      if (typeFilter) typeFilter.value = "";
      if (platformFilter) platformFilter.value = "";
      if (audienceFilter) audienceFilter.value = "";
      applyFilters(true);
      if (searchInput) searchInput.focus();
    });
  }

  const initialQuery = new URLSearchParams(window.location.search).get("q") || "";
  if (searchInput) searchInput.value = initialQuery;
  loadSearchIndex().finally(function () { applyFilters(false); });
})();
