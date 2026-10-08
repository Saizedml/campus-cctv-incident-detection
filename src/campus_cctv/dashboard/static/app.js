"use strict";
(() => {
  const byId = (id) => document.getElementById(id);
  const seed = JSON.parse(byId("initialData").textContent);
  let notices = seed;
  let selectedId = notices[0].alert_id;
  let pendingOnly = false;
  let imported = false;
  const reviews = new Map();
  const timeLabel = (seconds) => `${String(Math.floor(seconds / 60)).padStart(2, "0")}:${(seconds % 60).toFixed(1).padStart(4, "0")}`;
  const setText = (id, text) => { byId(id).textContent = text; };
  function node(tag, className, text) {
    const element = document.createElement(tag);
    if (className) element.className = className;
    if (text !== undefined) element.textContent = text;
    return element;
  }
  function groups() {
    const result = new Map();
    for (const notice of notices) {
      const key = `${notice.q}:${notice.parent_alert_id}`;
      if (!result.has(key)) result.set(key, []);
      result.get(key).push(notice);
    }
    return [...result.values()].map((items) => {
      items.sort((a, b) => a.decision_time_s - b.decision_time_s);
      const root = items.find((item) => item.kind === "NEW") || items[0];
      return { ...root, items };
    });
  }
  function showMessage(text) {
    setText("message", text);
    byId("message").hidden = false;
  }
  function renderQueue() {
    const rootGroups = groups();
    const visible = pendingOnly ? rootGroups.filter((item) => !reviews.has(item.alert_id)) : rootGroups;
    setText("queueCount", `${rootGroups.length} incidents`);
    byId("queue").replaceChildren();
    for (const q of [2, 5]) {
      const heading = node("div", `queue-tier ${q === 5 ? "lower" : ""}`, q === 2 ? "ALERT NOW" : "CHECK WHEN FREE");
      heading.append(node("span", "", `q${q}`));
      byId("queue").append(heading);
      for (const item of visible.filter((row) => row.q === q)) {
        const button = node("button", `queue-card ${item.alert_id === selectedId ? "selected" : ""}`);
        button.dataset.id = item.alert_id;
        button.setAttribute("aria-pressed", String(item.alert_id === selectedId));
        const header = node("div", "queue-card-header");
        header.append(node("span", "queue-card-title", item.task === "falls" ? "Person down" : "Weapon"), node("span", "queue-time", timeLabel(item.decision_time_s)));
        button.append(header, node("div", "queue-source", item.source_id));
        const footer = node("div", "queue-card-footer");
        const updates = item.items.filter((n) => n.kind === "UPDATE").length;
        footer.append(node("span", "", reviews.get(item.alert_id)?.verdict || "Awaiting review"), node("span", "", updates ? `+${updates} UPDATE` : item.kind));
        button.append(footer);
        button.addEventListener("click", () => { selectedId = item.alert_id; render(); });
        byId("queue").append(button);
      }
    }
    if (!visible.length) byId("queue").append(node("p", "queue-empty", "No incidents awaiting review."));
  }
  function renderDetail() {
    const item = groups().find((row) => row.alert_id === selectedId);
    if (!item) return;
    const falls = item.task === "falls";
    setText("sourceLabel", item.source_id.toUpperCase());
    setText("sceneSource", item.source_id);
    setText("sceneTime", timeLabel(item.decision_time_s));
    setText("evidenceTitle", falls ? "Person-down alert" : "Weapon alert");
    setText("detailTitle", falls ? "Person down" : "Weapon");
    setText("modelLabel", falls ? "person down" : "weapon");
    setText("score", item.score.toFixed(2));
    setText("detailSummary", falls ? "A posture alert requests review of the person and the surrounding context. It does not establish a medical emergency." : "A model-generated alert would request review of the object and its context. It does not establish intent.");
    setText("noticeCount", `${item.items.filter((n) => n.kind === "NEW").length} NEW + ${item.items.filter((n) => n.kind === "UPDATE").length} UPDATE`);
    setText("tierBadge", item.q === 2 ? "ALERT NOW · q2" : "CHECK WHEN FREE · q5");
    byId("tierBadge").className = `pill ${item.q === 2 ? "urgent" : "lower"}`;
    byId("standing").style.display = falls ? "none" : "";
    byId("prone").style.display = falls ? "" : "none";
    byId("skeletonControl").hidden = !falls || imported;
    byId("zoomButton").hidden = falls || imported;
    byId("scene").classList.remove("zoomed");
    byId("zoomButton").setAttribute("aria-pressed", "false");
    setText("zoomButton", "Zoom hand region");
    setText("evidenceCaption", imported ? "Notice metadata only · source media remains outside this dashboard" : falls ? "Illustrated prone pose · skeleton is synthetic, not a model prediction" : "Person context and hand region · illustrative geometry");
    setText("syntheticBadge", imported ? "LOCAL NOTICE METADATA" : "SYNTHETIC EVIDENCE");
    byId("importMask").hidden = !imported;
    const review = reviews.get(item.alert_id);
    setText("verdict", review?.verdict || "Awaiting review");
    setText("reviewStatus", review ? `${review.verdict} · human observation saved in this session` : "Awaiting human review");
    byId("reviewNote").value = review?.note || "";
    document.querySelectorAll("[data-review]").forEach((button) => button.setAttribute("aria-pressed", String(button.dataset.review === review?.verdict)));
    byId("history").replaceChildren(...item.items.map((notice) => node("li", "", `${timeLabel(notice.decision_time_s)} · ${notice.kind} · ${notice.score.toFixed(2)}`)));
    setText("timelineStart", item.items[0].kind);
    setText("timelineEnd", item.items.length > 1 ? item.items[item.items.length - 1].kind : "Context review");
  }
  function render() { renderQueue(); renderDetail(); }
  function validate(value) {
    if (!Array.isArray(value) || value.length === 0 || value.length > 10000) throw new Error("Supply between one and 10,000 notices.");
    const seen = new Set();
    for (const notice of value) {
      if (!notice || typeof notice !== "object") throw new Error("Every notice must be an object.");
      for (const key of ["alert_id", "parent_alert_id", "source_id"]) if (typeof notice[key] !== "string" || !notice[key]) throw new Error(`Missing ${key}.`);
      if (seen.has(notice.alert_id)) throw new Error("Notice IDs must be unique.");
      seen.add(notice.alert_id);
      if (!["NEW", "UPDATE"].includes(notice.kind) || !["weapons", "falls"].includes(notice.task) || ![2, 5].includes(notice.q)) throw new Error("Invalid notice kind, task or tier.");
      if (![notice.score, notice.decision_time_s].every((v) => typeof v === "number" && Number.isFinite(v) && v >= 0) || notice.score > 1) throw new Error("Invalid confidence or decision time.");
    }
    return value;
  }
  document.querySelectorAll("[data-review]").forEach((button) => button.addEventListener("click", () => {
    reviews.set(selectedId, { alert_id: selectedId, verdict: button.dataset.review, note: byId("reviewNote").value, origin: "human", reviewed_at: new Date().toISOString() });
    render();
  }));
  byId("reviewNote").addEventListener("input", () => { const review = reviews.get(selectedId); if (review) review.note = byId("reviewNote").value; });
  byId("allFilter").addEventListener("click", () => { pendingOnly = false; byId("allFilter").classList.add("active"); byId("pendingFilter").classList.remove("active"); renderQueue(); });
  byId("pendingFilter").addEventListener("click", () => { pendingOnly = true; byId("pendingFilter").classList.add("active"); byId("allFilter").classList.remove("active"); renderQueue(); });
  byId("zoomButton").addEventListener("click", () => { const zoomed = byId("scene").classList.toggle("zoomed"); byId("zoomButton").setAttribute("aria-pressed", String(zoomed)); setText("zoomButton", zoomed ? "Show person context" : "Zoom hand region"); });
  byId("skeletonToggle").addEventListener("change", () => { byId("skeleton").style.display = byId("skeletonToggle").checked ? "" : "none"; });
  byId("importButton").addEventListener("click", () => byId("fileInput").click());
  byId("fileInput").addEventListener("change", async () => {
    const file = byId("fileInput").files[0];
    if (!file) return;
    try {
      if (file.size > 1048576) throw new Error("Please keep notice files below one megabyte.");
      const parsed = validate(JSON.parse(await file.text()));
      notices = parsed; selectedId = groups()[0].alert_id; imported = true; reviews.clear(); render();
      showMessage("Local metadata imported. Media is masked; human observations remain separate from model confidence.");
    } catch (error) { showMessage(`Import not completed: ${error.message}`); }
    byId("fileInput").value = "";
  });
  byId("exportButton").addEventListener("click", () => {
    const blob = new Blob([JSON.stringify({ synthetic: !imported, decisions: [...reviews.values()] }, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob); const link = node("a"); link.href = url; link.download = "review-decisions.json"; link.click(); URL.revokeObjectURL(url);
  });
  document.addEventListener("keydown", (event) => {
    if (["TEXTAREA", "INPUT", "BUTTON"].includes(event.target.tagName)) return;
    if (event.key === "ArrowDown" || event.key === "ArrowUp") {
      const rows = groups(); const current = rows.findIndex((r) => r.alert_id === selectedId);
      selectedId = rows[(current + (event.key === "ArrowDown" ? 1 : rows.length - 1)) % rows.length].alert_id;
      event.preventDefault(); render();
    }
  });
  render();
})();
