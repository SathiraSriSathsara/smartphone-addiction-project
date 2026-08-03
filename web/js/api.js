"use strict";

class SmartHabitApiError extends Error {
  constructor(message, status = 0, details = []) {
    super(message);
    this.name = "SmartHabitApiError";
    this.status = status;
    this.details = Array.isArray(details) ? details : [];
  }
}

class SmartHabitApiClient {
  constructor(baseUrl) {
    this.baseUrl = baseUrl.replace(/\/$/, "");
  }

  async getModelSchema() {
    return this.#request("/api/model/schema");
  }

  async predict(payload) {
    return this.#request("/api/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
  }

  async #request(path, options = {}) {
    const controller = new AbortController();
    const timeoutId = window.setTimeout(
      () => controller.abort(),
      window.SmartHabitConfig.requestTimeoutMs,
    );

    try {
      const response = await fetch(`${this.baseUrl}${path}`, {
        ...options,
        headers: { Accept: "application/json", ...options.headers },
        signal: controller.signal,
      });
      const body = await response.json().catch(() => null);
      if (!response.ok) {
        const error = body?.error;
        throw new SmartHabitApiError(
          error?.message || "The server could not complete the request.",
          response.status,
          error?.details,
        );
      }
      return body;
    } catch (error) {
      if (error instanceof SmartHabitApiError) {
        throw error;
      }
      if (error.name === "AbortError") {
        throw new SmartHabitApiError("The request timed out. Please try again.");
      }
      throw new SmartHabitApiError(
        "SmartHabit could not reach the API. Check that the backend is running.",
      );
    } finally {
      window.clearTimeout(timeoutId);
    }
  }
}

window.SmartHabitApiError = SmartHabitApiError;
window.SmartHabitApiClient = SmartHabitApiClient;
