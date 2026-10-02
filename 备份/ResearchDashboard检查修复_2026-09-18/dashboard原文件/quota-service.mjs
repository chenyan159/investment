import { evaluateCodexQuota, readCodexQuota } from "../quota-control.mjs";
import { QUOTA_REFRESH_MS } from "./config.mjs";

export class QuotaService {
  #value = null;
  #checkedAtMs = 0;
  #pending = null;

  current() {
    if (!this.#value || Date.now() - this.#checkedAtMs >= QUOTA_REFRESH_MS) {
      void this.refresh();
    }
    return this.#value;
  }

  async refresh({ force = false } = {}) {
    if (!force && this.#value && Date.now() - this.#checkedAtMs < QUOTA_REFRESH_MS) {
      return this.#value;
    }
    if (this.#pending) return this.#pending;
    this.#pending = this.#load();
    try {
      return await this.#pending;
    } finally {
      this.#pending = null;
    }
  }

  async #load() {
    const checkedAt = new Date();
    try {
      const raw = await readCodexQuota();
      const evaluated = evaluateCodexQuota(raw);
      const limits = raw?.rateLimits || raw?.rateLimitsByLimitId?.codex || {};
      const resetsAtSeconds = Number(limits?.primary?.resetsAt);
      this.#value = {
        ...evaluated,
        resetsAt: Number.isFinite(resetsAtSeconds)
          ? new Date(resetsAtSeconds * 1000).toISOString()
          : null,
        resetCredits: raw?.rateLimitResetCredits?.availableCount ?? null,
        checkedAt: checkedAt.toISOString(),
      };
    } catch (error) {
      this.#value = {
        error: error?.message || String(error),
        checkedAt: checkedAt.toISOString(),
      };
    }
    this.#checkedAtMs = checkedAt.getTime();
    return this.#value;
  }
}
