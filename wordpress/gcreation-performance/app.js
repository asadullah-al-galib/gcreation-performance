/* global gcpConfig */
(() => {
  const root = document.querySelector("#gcp-app");
  if (!root) return;
  const status = root.querySelector("#gcp-status");
  const report = root.querySelector("#gcp-report");
  const events = root.querySelector("#gcp-events");
  let credentials;
  const node = (tag, text, parent) => {
    const el = document.createElement(tag);
    if (text !== undefined) el.textContent = text;
    if (parent) parent.append(el);
    return el;
  };
  async function api(path, body) {
    const result = await fetch(gcpConfig.api + path, {
      method: body ? "POST" : "GET",
      credentials: "same-origin",
      headers: {
        "X-WP-Nonce": gcpConfig.nonce,
        "X-GCP-Session-Nonce": gcpConfig.sessionNonce,
        "Content-Type": "application/json",
      },
      body: body ? JSON.stringify(body) : undefined,
    });
    const data = await result.json();
    if (!result.ok)
      throw new Error(data.message || data.error || "Request failed");
    return data;
  }
  function issueCard(issue, paid) {
    const card = node("article", undefined, report);
    card.className = "gcp-issue";
    node("p", issue.severity, card);
    node("h3", issue.title, card);
    node("p", "Affected page: " + issue.affected_url, card);
    node(
      "p",
      "Measured: " +
        JSON.stringify(issue.measured_values) +
        " · Threshold: " +
        issue.threshold,
      card,
    );
    const evidence = node("ul", undefined, card);
    issue.evidence.forEach((item) => node("li", item, evidence));
    node("p", issue.impact, card);
    node("p", issue.recommendation, card);
    if (paid) {
      const steps = node("ol", undefined, card);
      issue.steps.forEach((step) => node("li", step, steps));
      node("p", "Verify: " + issue.verification_method, card);
      for (const [action, label] of [
        ["fixed", "Mark as Fixed"],
        ["retest", "Test Again"],
        ["expert", "Hire Expert"],
      ]) {
        const button = node("button", label, card);
        button.type = "button";
        button.onclick = async () => {
          button.disabled = true;
          try {
            const result = await api("report", {
              ...credentials,
              action,
              ruleId: issue.rule_id,
              url: issue.affected_url,
            });
            status.textContent =
              action === "fixed"
                ? "Marked by you. Technical verification is still pending."
                : action === "retest"
                  ? "Retest queued. Use Refresh report and comparisons to see measured results when complete."
                  : "Expert request received: " + result.state;
          } catch (error) {
            status.textContent = error.message;
          } finally {
            button.disabled = false;
          }
        };
      }
    }
  }
  function renderReport(data, paid, id) {
    report.replaceChildren();
    node(
      "h2",
      paid ? "Interactive Fix Center" : "Your free performance report",
      report,
    );
    node(
      "p",
      data.healthScore === null
        ? "Performance score unavailable for this scan."
        : "Performance Health Score: " + data.healthScore + "/100",
      report,
    );
    node("p", data.scoreBasis, report);
    data.incomplete.forEach((item) => node("p", item, report));
    const issues = paid ? data.issues : data.issues.slice(0, 5);
    if (!issues.length)
      node(
        "p",
        "No configured rule triggered on the measured pages. This is not a guarantee of a problem-free website.",
        report,
      );
    issues.forEach((issue) => issueCard(issue, paid));
    if (paid) {
      const refresh = node("button", "Refresh report and comparisons", report);
      refresh.type = "button";
      refresh.onclick = () => void loadPaidReport();
    }
    if (!paid) {
      node(
        "p",
        "Deep analysis covers more representative pages and provides step-by-step fixes. Scope and discovered URL count determine the price.",
        report,
      );
      const form = node("form", undefined, report);
      const scopeLabel = node("label", "Audit scope ", form);
      const scope = node("select", undefined, scopeLabel);
      for (const [value, label] of [
        ["major5", "Major 5 Pages Audit"],
        ["full", "Full Website Audit"],
      ]) {
        const option = node("option", label, scope);
        option.value = value;
      }
      const modeLabel = node("label", "Solution mode ", form);
      const mode = node("select", undefined, modeLabel);
      for (const [value, label] of [
        ["self", "I Will Fix It"],
        ["expert", "Hire gCreation Expert"],
      ]) {
        const option = node("option", label, mode);
        option.value = value;
      }
      const priceLabel = node("p", "Loading trusted price…", form);
      const checkoutButton = node("button", "Continue to checkout", form);
      const reviewForm = node("form", undefined, report);
      reviewForm.hidden = true;
      const reviewLabel = node(
        "label",
        "Contact email for expert review ",
        reviewForm,
      );
      const reviewEmail = node("input", undefined, reviewLabel);
      reviewEmail.type = "email";
      reviewEmail.required = true;
      node("button", "Request custom expert review", reviewForm);
      reviewForm.onsubmit = async (event) => {
        event.preventDefault();
        try {
          const result = await api("expert-review", {
            auditId: id,
            contact: reviewEmail.value,
          });
          status.textContent = "Expert review requested: " + result.state;
        } catch (error) {
          status.textContent = error.message;
        }
      };
      const updateQuote = async () => {
        checkoutButton.disabled = true;
        try {
          const pricing = await api("quote", {
            auditId: id,
            scope: scope.value,
            mode: mode.value,
          });
          priceLabel.textContent =
            pricing.amount === null
              ? "Custom / Expert Review required for this website size."
              : pricing.currency +
                " " +
                pricing.amount +
                " · " +
                pricing.count +
                " discovered URLs";
          reviewForm.hidden = pricing.amount !== null;
          checkoutButton.disabled = pricing.amount === null;
        } catch (error) {
          priceLabel.textContent = error.message;
        }
      };
      scope.onchange = updateQuote;
      mode.onchange = updateQuote;
      void updateQuote();
      form.onsubmit = async (event) => {
        event.preventDefault();
        try {
          const data = await api("checkout", {
            auditId: id,
            scope: scope.value,
            mode: mode.value,
          });
          window.location.assign(data.checkoutUrl);
        } catch (error) {
          status.textContent = error.message;
        }
      };
    }
  }
  root.querySelector("#gcp-scan").onsubmit = async (event) => {
    event.preventDefault();
    const form = event.currentTarget;
    const button = form.querySelector("button");
    button.disabled = true;
    events.replaceChildren();
    report.replaceChildren();
    status.textContent = "Submitting your scan…";
    try {
      const scan = await api("scan", { url: new FormData(form).get("url") });
      let offset = 0;
      for (let poll = 0; poll < 180; poll++) {
        const updates = await api("events/" + scan.id + "?after=" + offset);
        updates.forEach((item) => {
          offset = item.id;
          node(
            "li",
            item.type.replaceAll(".", " ") + " " + JSON.stringify(item.data),
            events,
          );
        });
        const state = await api("scan/" + scan.id);
        status.textContent = "Scan state: " + state.state.replaceAll("_", " ");
        if (state.state === "FAILED")
          throw new Error(state.error || "Scan failed");
        if (state.report) {
          renderReport(state.report, false, scan.id);
          await api("analytics", { auditId: scan.id });
          return;
        }
        await new Promise((resolve) => setTimeout(resolve, 2000));
      }
      status.textContent =
        "Your scan remains queued or running. Keep this session and try again later.";
    } catch (error) {
      status.textContent = error.message;
    } finally {
      button.disabled = false;
    }
  };
  async function loadPaidReport() {
    try {
      const result = await api("report", credentials);
      if (!result.audit.report) {
        status.textContent = "Paid audit state: " + result.audit.state;
        return;
      }
      renderReport(result.audit.report, true, result.audit.id);
      for (const retest of result.retests) {
        node("h3", "Retest: " + retest.state, report);
        if (retest.comparison)
          for (const comparison of retest.comparison) {
            node("p", comparison.url, report);
            node(
              "p",
              "TTFB before: " +
                (comparison.ttfbBefore ?? "unavailable") +
                " ms · after: " +
                (comparison.ttfbAfter ?? "unavailable") +
                " ms",
              report,
            );
            node(
              "pre",
              JSON.stringify(
                {
                  lighthouseBefore: comparison.before,
                  lighthouseAfter: comparison.after,
                },
                null,
                2,
              ),
              report,
            );
          }
      }
    } catch (error) {
      status.textContent = error.message;
    }
  }
  const token = new URLSearchParams(location.hash.slice(1)).get("report");
  if (token) {
    history.replaceState(null, "", location.pathname + location.search);
    root.querySelector("#gcp-scan").hidden = true;
    const form = node("form", undefined, report);
    node("h2", "Verify secure report access", form);
    const orderLabel = node("label", "Order number ", form);
    const order = node("input", undefined, orderLabel);
    order.required = true;
    order.inputMode = "numeric";
    const contactLabel = node("label", "Checkout email ", form);
    const contact = node("input", undefined, contactLabel);
    contact.required = true;
    contact.type = "email";
    node("button", "Open Fix Center", form);
    form.onsubmit = async (event) => {
      event.preventDefault();
      credentials = { token, orderId: order.value, contact: contact.value };
      await loadPaidReport();
    };
  }
})();
