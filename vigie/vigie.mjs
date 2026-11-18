#!/usr/bin/env node
// Vigie — status line pour Claude Code.
// Claude Code envoie un JSON sur stdin ; on affiche une ligne compacte.
// Aucune dépendance, aucun appel réseau, aucun jeton lu.

import { pathToFileURL } from "node:url";

const C = {
  dim: (s) => `\x1b[2m${s}\x1b[0m`,
  cyan: (s) => `\x1b[36m${s}\x1b[0m`,
  green: (s) => `\x1b[32m${s}\x1b[0m`,
  yellow: (s) => `\x1b[33m${s}\x1b[0m`,
  red: (s) => `\x1b[31m${s}\x1b[0m`,
};

const WEEK_MS = 7 * 24 * 3600 * 1000;

function pct(limit) {
  if (!limit) return null;
  const v = limit.used_percentage ?? limit.utilization;
  return typeof v === "number" ? Math.max(0, Math.min(100, v)) : null;
}

function resetMs(limit) {
  const r = limit?.resets_at;
  if (r == null) return null;
  const t = typeof r === "number" ? (r < 1e12 ? r * 1000 : r) : Date.parse(r);
  return Number.isFinite(t) ? t : null;
}

function bar(p, width = 8) {
  const filled = Math.round((p / 100) * width);
  const s = "━".repeat(filled) + C.dim("─".repeat(width - filled));
  const color = p >= 85 ? C.red : p >= 60 ? C.yellow : C.green;
  return color(s);
}

// Avance = part de la semaine écoulée − part du quota consommée.
// Positif : tu consommes moins vite que le rythme régulier.
export function pace(usedPct, resetsAt, now = Date.now()) {
  if (usedPct == null || resetsAt == null) return null;
  const elapsed = 1 - (resetsAt - now) / WEEK_MS;
  if (elapsed < 0 || elapsed > 1) return null;
  return elapsed * 100 - usedPct;
}

export function render(input, now = Date.now()) {
  const parts = [];
  const model = input?.model?.display_name;
  if (model) parts.push(C.cyan(`›_ ${model}`));

  const cost = input?.cost?.total_cost_usd;
  if (typeof cost === "number") parts.push(`$${cost.toFixed(2)}`);

  const ctx = input?.context_window?.used_percentage;
  if (typeof ctx === "number") parts.push(`ctx ${Math.round(ctx)}%`);

  const rl = input?.rate_limits;
  const five = pct(rl?.five_hour);
  if (five != null) parts.push(`5h ${bar(five)} ${Math.round(five)}%`);
  const week = pct(rl?.seven_day);
  if (week != null) parts.push(`Sem ${bar(week)} ${Math.round(week)}%`);

  const ahead = pace(week, resetMs(rl?.seven_day), now);
  if (ahead != null) {
    const txt = `${ahead >= 0 ? "+" : ""}${ahead.toFixed(1).replace(".", ",")} %`;
    parts.push(ahead >= 0 ? C.green(`${txt} d'avance`) : C.red(`${txt} de retard`));
  }

  return parts.join(C.dim("  │  "));
}

async function main() {
  let raw = "";
  for await (const chunk of process.stdin) raw += chunk;
  let input = {};
  try {
    input = JSON.parse(raw || "{}");
  } catch {
    // entrée illisible : on affiche une ligne vide plutôt que de planter
  }
  process.stdout.write(render(input) + "\n");
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) main();
