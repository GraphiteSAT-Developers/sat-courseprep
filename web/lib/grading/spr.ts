// Student-produced response (SPR) entry rules, following the Bluebook directions:
// - up to 5 characters for a positive answer, 6 for a negative one (minus sign counts)
// - fractions and decimals are both accepted; mixed numbers and symbols are not
// - a decimal that doesn't terminate must fill the available space, either
//   truncated or rounded (for 2/3: .6666, .6667, 0.666, 0.667 are right; 0.67 is wrong)
//
// Everything here is exact rational arithmetic with BigInt so a float can never
// mark a right answer wrong (or the reverse).

/** An exact rational answer key. `den` must be positive. */
export interface Rational {
  num: number;
  den: number;
}

export type SprResult =
  | { status: "correct"; entry: string }
  | { status: "incorrect"; entry: string; hint?: SprHint }
  | { status: "invalid"; entry: string; reason: string };

/** Why a numerically close answer was still marked wrong. */
export type SprHint = "rounded-too-early";

export const MAX_POSITIVE_LENGTH = 5;
export const MAX_NEGATIVE_LENGTH = 6;

const ENTRY_PATTERN = /^-?(\d+\/\d+|\d+\.?\d*|\.\d+)$/;

interface ParsedEntry {
  negative: boolean;
  kind: "fraction" | "decimal";
  /** |value| = num / den */
  num: bigint;
  den: bigint;
  /** Digits after the decimal point (decimals only). */
  places: number;
}

/** Checks the entry against Bluebook's character rules without grading it. */
export function validateSprEntry(raw: string): { ok: true } | { ok: false; reason: string } {
  const entry = raw.trim();
  if (entry === "") return { ok: false, reason: "Enter an answer." };
  if (/\s/.test(entry)) return { ok: false, reason: "Mixed numbers like 3 1/2 aren't accepted. Enter 7/2 or 3.5." };
  if (/[,%$]/.test(entry)) return { ok: false, reason: "Don't include commas, %, or $." };
  if (!ENTRY_PATTERN.test(entry)) return { ok: false, reason: "Use digits, one decimal point or one fraction bar, and an optional leading minus sign." };
  const limit = entry.startsWith("-") ? MAX_NEGATIVE_LENGTH : MAX_POSITIVE_LENGTH;
  if (entry.length > limit) {
    return { ok: false, reason: `Too long: ${entry.startsWith("-") ? "negative answers fit 6 characters" : "positive answers fit 5 characters"}, including the decimal point and fraction bar.` };
  }
  if (/\/0+$/.test(entry)) return { ok: false, reason: "A fraction can't have a denominator of 0." };
  return { ok: true };
}

function parseEntry(entry: string): ParsedEntry {
  const negative = entry.startsWith("-");
  const body = negative ? entry.slice(1) : entry;
  if (body.includes("/")) {
    const [n, d] = body.split("/");
    return { negative, kind: "fraction", num: BigInt(n), den: BigInt(d), places: 0 };
  }
  const [whole, frac = ""] = body.split(".");
  const digits = (whole || "0") + frac;
  return { negative, kind: "decimal", num: BigInt(digits), den: 10n ** BigInt(frac.length), places: frac.length };
}

function abs(n: bigint): bigint {
  return n < 0n ? -n : n;
}

/** |key| scaled to `places` decimals, truncated and rounded half up. */
function scaledCandidates(key: Rational, places: number): { truncated: bigint; rounded: bigint } {
  const n = abs(BigInt(key.num)) * 10n ** BigInt(places);
  const d = BigInt(key.den);
  return { truncated: n / d, rounded: (2n * n + d) / (2n * d) };
}

/** True when the exact decimal form of |key| fits the box (so no truncation is allowed). */
function exactDecimalFits(key: Rational): boolean {
  if (!terminates(key)) return false;
  const negative = key.num < 0;
  const limit = negative ? MAX_NEGATIVE_LENGTH : MAX_POSITIVE_LENGTH;
  const g = gcd(abs(BigInt(key.num)), BigInt(key.den));
  const n = abs(BigInt(key.num)) / g;
  const d = BigInt(key.den) / g;
  if (d === 1n) return true;
  const whole = n / d;
  const exact = exactDecimal(n, d, whole === 0n ? "" : whole.toString());
  return exact !== null && (negative ? "-" : "").length + exact.length <= limit;
}

function terminates(key: Rational): boolean {
  let d = BigInt(key.den) / gcd(abs(BigInt(key.num)), BigInt(key.den));
  while (d % 2n === 0n) d /= 2n;
  while (d % 5n === 0n) d /= 5n;
  return d === 1n;
}

function gcd(a: bigint, b: bigint): bigint {
  while (b !== 0n) [a, b] = [b, a % b];
  return a;
}

function matchesExactly(p: ParsedEntry, key: Rational): boolean {
  const keyNegative = key.num < 0;
  const keyIsZero = key.num === 0;
  if (!keyIsZero && p.negative !== keyNegative) return false;
  return p.num * BigInt(key.den) === abs(BigInt(key.num)) * p.den;
}

/** Grades one entry against one or more acceptable answers (some SPR items have several). */
export function gradeSpr(raw: string, keys: Rational[]): SprResult {
  const entry = raw.trim();
  const valid = validateSprEntry(entry);
  if (!valid.ok) return { status: "invalid", entry, reason: valid.reason };

  const parsed = parseEntry(entry);
  let closeButShort = false;

  for (const key of keys) {
    if (matchesExactly(parsed, key)) return { status: "correct", entry };
    if (parsed.kind !== "decimal" || exactDecimalFits(key)) continue;
    if (key.num !== 0 && parsed.negative !== key.num < 0) continue;

    const { truncated, rounded } = scaledCandidates(key, parsed.places);
    const hitsValue = parsed.num === truncated || parsed.num === rounded;
    const limit = parsed.negative ? MAX_NEGATIVE_LENGTH : MAX_POSITIVE_LENGTH;
    if (hitsValue && entry.length === limit) return { status: "correct", entry };
    if (hitsValue) closeButShort = true;
  }

  return closeButShort
    ? { status: "incorrect", entry, hint: "rounded-too-early" }
    : { status: "incorrect", entry };
}

/**
 * Every short canonical entry Bluebook would accept for a key, for showing after
 * an attempt. Lists the reduced fraction (when it fits) plus the exact decimal,
 * or the full-width truncated and rounded decimals for a repeating one.
 */
export function acceptedEntries(key: Rational): string[] {
  const out = new Set<string>();
  const negative = key.num < 0;
  const sign = negative ? "-" : "";
  const limit = negative ? MAX_NEGATIVE_LENGTH : MAX_POSITIVE_LENGTH;
  const g = gcd(abs(BigInt(key.num)), BigInt(key.den));
  const n = abs(BigInt(key.num)) / g;
  const d = BigInt(key.den) / g;

  const fraction = d === 1n ? `${sign}${n}` : `${sign}${n}/${d}`;
  if (fraction.length <= limit) out.add(fraction);

  const whole = n / d;
  const wholePart = whole === 0n ? "" : whole.toString();
  for (const lead of whole === 0n ? ["", "0"] : [wholePart]) {
    const room = limit - sign.length - lead.length - 1;
    if (room < 1) continue;
    if (exactDecimalFits(key)) {
      const exact = exactDecimal(n, d, lead);
      if (exact && `${sign}${exact}`.length <= limit) out.add(`${sign}${exact}`);
      continue;
    }
    const { truncated, rounded } = scaledCandidates(key, room);
    for (const v of [truncated, rounded]) {
      const frac = (v - whole * 10n ** BigInt(room)).toString().padStart(room, "0");
      out.add(`${sign}${lead}.${frac}`);
    }
  }
  return [...out].filter((e) => validateSprEntry(e).ok);
}

function exactDecimal(n: bigint, d: bigint, lead: string): string | null {
  if (n % d === 0n) return null;
  let rem = n % d;
  let frac = "";
  while (rem !== 0n && frac.length < 12) {
    rem *= 10n;
    frac += (rem / d).toString();
    rem %= d;
  }
  return `${lead}.${frac}`;
}
