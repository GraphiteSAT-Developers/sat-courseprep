import { describe, expect, it } from "vitest";
import { acceptedEntries, gradeSpr, validateSprEntry } from "./spr";

const twoThirds = { num: 2, den: 3 };
const eightNinths = { num: 8, den: 9 };

describe("validateSprEntry", () => {
  it("enforces 5 characters for positive and 6 for negative answers", () => {
    expect(validateSprEntry("12345").ok).toBe(true);
    expect(validateSprEntry("123456").ok).toBe(false);
    expect(validateSprEntry("-12345").ok).toBe(true);
    expect(validateSprEntry("-123456").ok).toBe(false);
  });

  it("rejects mixed numbers, symbols and junk", () => {
    for (const bad of ["3 1/2", "50%", "$5", "1,000", "1/2/3", "--1", "1/0", "", "x"]) {
      expect(validateSprEntry(bad).ok, bad).toBe(false);
    }
  });
});

describe("gradeSpr", () => {
  it("accepts the 8/9 entries from the official answer table and rejects .88", () => {
    for (const ok of ["8/9", ".8888", ".8889", "0.888", "0.889"]) {
      expect(gradeSpr(ok, [eightNinths]).status, ok).toBe("correct");
    }
    expect(gradeSpr(".88", [eightNinths])).toMatchObject({ status: "incorrect", hint: "rounded-too-early" });
  });

  it("rejects 0.67 for 2/3 and flags it as rounded too early", () => {
    expect(gradeSpr("0.67", [twoThirds])).toMatchObject({ status: "incorrect", hint: "rounded-too-early" });
    expect(gradeSpr("0.667", [twoThirds]).status).toBe("correct");
  });

  it("accepts unreduced fractions and exact decimals", () => {
    expect(gradeSpr("4/6", [twoThirds]).status).toBe("correct");
    expect(gradeSpr("2.5", [{ num: 5, den: 2 }]).status).toBe("correct");
    expect(gradeSpr("2.50", [{ num: 5, den: 2 }]).status).toBe("correct");
    expect(gradeSpr("5/2", [{ num: 5, den: 2 }]).status).toBe("correct");
  });

  it("handles negatives, including truncation toward zero", () => {
    const key = { num: -2, den: 3 };
    for (const ok of ["-2/3", "-.6666", "-.6667", "-0.666", "-0.667"]) {
      expect(gradeSpr(ok, [key]).status, ok).toBe("correct");
    }
    expect(gradeSpr(".6666", [key]).status).toBe("incorrect");
    expect(gradeSpr("-1", [{ num: -1, den: 1 }]).status).toBe("correct");
  });

  it("accepts any of several keys", () => {
    const keys = [{ num: 3, den: 1 }, { num: -1, den: 2 }];
    expect(gradeSpr("3", keys).status).toBe("correct");
    expect(gradeSpr("-.5", keys).status).toBe("correct");
    expect(gradeSpr("2", keys).status).toBe("incorrect");
  });

  it("returns invalid, not incorrect, for entries Bluebook wouldn't take", () => {
    expect(gradeSpr("0.6667", [twoThirds]).status).toBe("invalid");
  });
});

describe("acceptedEntries", () => {
  it("lists the official 8/9 forms", () => {
    expect(acceptedEntries(eightNinths).sort()).toEqual(["0.888", "0.889", ".8888", ".8889", "8/9"].sort());
  });

  it("lists fraction and decimal for a terminating answer", () => {
    expect(acceptedEntries({ num: 41, den: 8 })).toEqual(["41/8", "5.125"]);
  });

  it("lists every entry it returns as correct", () => {
    for (const key of [twoThirds, eightNinths, { num: -7, den: 3 }, { num: 100, den: 7 }, { num: 3, den: 1 }]) {
      for (const e of acceptedEntries(key)) expect(gradeSpr(e, [key]).status, `${e} for ${key.num}/${key.den}`).toBe("correct");
    }
  });
});
