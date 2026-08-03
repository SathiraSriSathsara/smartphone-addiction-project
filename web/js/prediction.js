"use strict";

const FIELD_PRESENTATION = Object.freeze({
  age: { label: "Age", unit: "years", helper: "Observed range: 18–35", min: 18, max: 35, step: 1 },
  daily_screen_time_hours: { label: "Daily screen time", unit: "hours/day", helper: "Typical weekday total", min: 0.5, max: 15, step: 0.01 },
  social_media_hours: { label: "Social media use", unit: "hours/day", helper: "Time across social platforms", min: 0, max: 8, step: 0.01 },
  gaming_hours: { label: "Gaming time", unit: "hours/day", helper: "Mobile or connected gaming", min: 0, max: 4, step: 0.01 },
  work_study_hours: { label: "Work or study time", unit: "hours/day", helper: "Phone-supported productive time", min: 0, max: 6, step: 0.01 },
  sleep_hours: { label: "Sleep duration", unit: "hours/night", helper: "Typical nightly sleep", min: 4.5, max: 9, step: 0.01 },
  notifications_per_day: { label: "Notifications", unit: "per day", helper: "Approximate alerts received", min: 20, max: 250, step: 1 },
  app_opens_per_day: { label: "App opens", unit: "per day", helper: "Approximate app-opening count", min: 15, max: 180, step: 1 },
  weekend_screen_time: { label: "Weekend screen time", unit: "hours/day", helper: "Typical Saturday or Sunday", min: 0.51, max: 17.56, step: 0.01 },
  gender: { label: "Gender", helper: "Select the matching dataset category" },
  stress_level: { label: "Stress level", helper: "Your typical self-reported level" },
  academic_work_impact: { label: "Academic or work impact", helper: "Does phone use affect work or study?" },
});

const state = {
  schemaFields: [],
  submitting: false,
};

const elements = {};

document.addEventListener("DOMContentLoaded", async () => {
  elements.form = document.querySelector("#prediction-form");
  elements.grid = document.querySelector("#field-grid");
  elements.schemaStatus = document.querySelector("#schema-status");
  elements.formError = document.querySelector("#form-error");
  elements.submit = document.querySelector("#submit-button");
  elements.reset = document.querySelector("#reset-button");
  elements.result = document.querySelector("#result-card");
  elements.placeholder = document.querySelector("#result-placeholder");
  elements.newAssessment = document.querySelector("#new-assessment-button");

  elements.form.addEventListener("submit", handleSubmit);
  elements.form.addEventListener("reset", handleReset);
  elements.newAssessment.addEventListener("click", startNewAssessment);

  const api = new window.SmartHabitApiClient(window.SmartHabitConfig.apiBaseUrl);
  window.smartHabitApi = api;

  try {
    const schema = await api.getModelSchema();
    state.schemaFields = schema.fields.filter((field) => field.name !== "id");
    renderFields(state.schemaFields);
    elements.schemaStatus.textContent = `${state.schemaFields.length} required fields`;
    elements.submit.disabled = false;
    elements.reset.disabled = false;
  } catch (error) {
    elements.grid.replaceChildren();
    elements.grid.setAttribute("aria-busy", "false");
    showFormError(error.message);
    elements.schemaStatus.textContent = "Schema unavailable";
  }
});

function renderFields(fields) {
  const fragment = document.createDocumentFragment();
  for (const field of fields) {
    const presentation = FIELD_PRESENTATION[field.name] || {
      label: humanize(field.name),
      helper: "Required model input",
    };
    const wrapper = document.createElement("div");
    wrapper.className = "field";

    const label = document.createElement("label");
    label.htmlFor = field.name;
    label.append(document.createTextNode(presentation.label));
    if (presentation.unit) {
      const unit = document.createElement("span");
      unit.className = "field__unit";
      unit.textContent = presentation.unit;
      label.append(unit);
    }

    const control = field.allowed_categories?.length
      ? createSelect(field)
      : createNumberInput(field, presentation);
    const helper = document.createElement("span");
    helper.id = `${field.name}-helper`;
    helper.className = "field__helper";
    helper.textContent = presentation.helper;
    const error = document.createElement("span");
    error.id = `${field.name}-error`;
    error.className = "field__error";
    error.setAttribute("aria-live", "polite");
    control.setAttribute("aria-describedby", `${helper.id} ${error.id}`);

    wrapper.append(label, control, helper, error);
    fragment.append(wrapper);
  }
  elements.grid.replaceChildren(fragment);
  elements.grid.setAttribute("aria-busy", "false");
}

function createNumberInput(field, presentation) {
  const input = document.createElement("input");
  input.type = "number";
  input.id = field.name;
  input.name = field.name;
  input.required = Boolean(field.required);
  input.inputMode = "decimal";
  input.autocomplete = "off";
  if (Number.isFinite(presentation.min)) input.min = String(presentation.min);
  if (Number.isFinite(presentation.max)) input.max = String(presentation.max);
  input.step = String(presentation.step ?? "any");
  return input;
}

function createSelect(field) {
  const select = document.createElement("select");
  select.id = field.name;
  select.name = field.name;
  select.required = Boolean(field.required);
  const placeholder = document.createElement("option");
  placeholder.value = "";
  placeholder.textContent = "Select an option";
  placeholder.disabled = true;
  placeholder.selected = true;
  select.append(placeholder);
  for (const category of field.allowed_categories) {
    const option = document.createElement("option");
    option.value = category;
    option.textContent = category;
    select.append(option);
  }
  return select;
}

async function handleSubmit(event) {
  event.preventDefault();
  if (state.submitting) return;

  clearErrors();
  if (!elements.form.checkValidity()) {
    elements.form.reportValidity();
    return;
  }

  const payload = {};
  for (const field of state.schemaFields) {
    const control = elements.form.elements.namedItem(field.name);
    payload[field.name] = field.type === "number"
      ? Number(control.value)
      : control.value;
  }

  setSubmitting(true);
  try {
    const result = await window.smartHabitApi.predict(payload);
    renderResult(result);
  } catch (error) {
    applyServerErrors(error.details);
    showFormError(error.message);
  } finally {
    setSubmitting(false);
  }
}

function applyServerErrors(details) {
  let firstInvalidControl = null;
  for (const detail of details || []) {
    const fieldName = detail.loc?.at(-1);
    if (!state.schemaFields.some((field) => field.name === fieldName)) continue;
    const control = elements.form.elements.namedItem(fieldName);
    const message = document.querySelector(`#${CSS.escape(fieldName)}-error`);
    if (!control || !message) continue;
    control.setAttribute("aria-invalid", "true");
    message.textContent = detail.msg || "Please check this value.";
    firstInvalidControl ||= control;
  }
  firstInvalidControl?.focus();
}

function renderResult(result) {
  const view = createResultViewModel(result);
  const gauge = document.querySelector("#probability-gauge");
  const gaugeProgress = document.querySelector("#probability-gauge-progress");
  const badge = document.querySelector("#result-risk-badge");
  badge.textContent = view.riskLabel;
  badge.dataset.risk = view.riskLevel;
  elements.result.dataset.risk = view.riskLevel;
  document.querySelector("#result-probability").textContent = view.percentageLabel;
  document.querySelector("#result-gauge-risk").textContent = view.riskLabel;
  gauge.setAttribute("aria-valuenow", String(view.percentage));
  gauge.setAttribute("aria-valuetext", view.gaugeText);
  gaugeProgress.style.strokeDashoffset = String(view.strokeDashoffset);
  document.querySelector("#result-message").textContent = view.message;
  document.querySelector("#result-class").textContent = view.predictedClass;
  document.querySelector("#result-non-addiction").textContent = view.nonAddictionLabel;
  document.querySelector("#result-model-version").textContent = view.modelVersion;
  document.querySelector("#result-disclaimer").textContent = result.disclaimer;
  for (const card of document.querySelectorAll(".risk-info-card")) {
    const isCurrent = card.dataset.risk === view.riskLevel;
    card.classList.toggle("is-current", isCurrent);
    if (isCurrent) {
      card.setAttribute("aria-current", "true");
    } else {
      card.removeAttribute("aria-current");
    }
  }
  elements.placeholder.hidden = true;
  elements.result.hidden = false;
  elements.result.focus();
  elements.result.scrollIntoView({ behavior: reducedMotion() ? "auto" : "smooth", block: "nearest" });
}

function createResultViewModel(result) {
  const percentage = Math.round(result.addiction_probability * 1000) / 10;
  const nonAddiction = Math.round(result.non_addiction_probability * 1000) / 10;
  return Object.freeze({
    percentage,
    percentageLabel: `${percentage}%`,
    nonAddictionLabel: `${nonAddiction}%`,
    predictedClass: String(result.predicted_class),
    riskLevel: result.risk_level,
    riskLabel: `${result.risk_level} risk`,
    message: result.risk_message,
    modelVersion: result.model_version ?? "Not recorded",
    gaugeText: `${percentage} percent, ${result.risk_level} risk display band`,
    strokeDashoffset: 100 - percentage,
    currentRiskCards: Object.freeze({
      Low: result.risk_level === "Low",
      Moderate: result.risk_level === "Moderate",
      High: result.risk_level === "High",
    }),
  });
}

function handleReset() {
  window.setTimeout(() => {
    clearErrors();
    elements.result.hidden = true;
    elements.placeholder.hidden = false;
    const firstControl = elements.form.querySelector("input, select");
    firstControl?.focus();
  }, 0);
}

function startNewAssessment() {
  elements.form.reset();
  elements.form.scrollIntoView({
    behavior: reducedMotion() ? "auto" : "smooth",
    block: "start",
  });
}

function setSubmitting(submitting) {
  state.submitting = submitting;
  elements.form.classList.toggle("is-submitting", submitting);
  elements.submit.disabled = submitting;
  elements.reset.disabled = submitting;
  elements.submit.querySelector(".button__label").textContent = submitting
    ? "Calculating…"
    : "Predict Your Risk";
  elements.grid.setAttribute("aria-busy", String(submitting));
}

function clearErrors() {
  elements.formError.hidden = true;
  elements.formError.textContent = "";
  for (const control of elements.form.querySelectorAll("[aria-invalid]")) {
    control.removeAttribute("aria-invalid");
  }
  for (const message of elements.form.querySelectorAll(".field__error")) {
    message.textContent = "";
  }
}

function showFormError(message) {
  elements.formError.textContent = message;
  elements.formError.hidden = false;
}

function humanize(name) {
  return name.replaceAll("_", " ").replace(/^./, (letter) => letter.toUpperCase());
}

function reducedMotion() {
  return window.matchMedia("(prefers-reduced-motion: reduce)").matches;
}

window.SmartHabitPredictionDashboard = Object.freeze({ createResultViewModel });
