import { describe, expect, it, vi } from "vitest";

vi.mock("server-only", () => ({}));

import { resolveProviderKind } from "./provider";

describe("tutor provider selection", () => {
  it("prefers the endpoint, then Anthropic, then the stub", () => {
    expect(resolveProviderKind({})).toBe("stub");
    expect(resolveProviderKind({ ANTHROPIC_API_KEY: "k" })).toBe("anthropic");
    expect(resolveProviderKind({ ANTHROPIC_API_KEY: "k", TUTOR_ENDPOINT_URL: "http://x", TUTOR_ENDPOINT_MODEL: "m" })).toBe("endpoint");
    // Both endpoint vars are required; a URL alone is not a configured endpoint.
    expect(resolveProviderKind({ ANTHROPIC_API_KEY: "k", TUTOR_ENDPOINT_URL: "http://x" })).toBe("anthropic");
  });

  it("honours TUTOR_PROVIDER as an override and rejects unknown values", () => {
    const all = { ANTHROPIC_API_KEY: "k", TUTOR_ENDPOINT_URL: "http://x", TUTOR_ENDPOINT_MODEL: "m" };
    expect(resolveProviderKind({ ...all, TUTOR_PROVIDER: "anthropic" })).toBe("anthropic");
    expect(resolveProviderKind({ ...all, TUTOR_PROVIDER: "stub" })).toBe("stub");
    expect(resolveProviderKind({ ...all, TUTOR_PROVIDER: " Endpoint " })).toBe("endpoint");
    expect(() => resolveProviderKind({ TUTOR_PROVIDER: "gemini" })).toThrow(/TUTOR_PROVIDER/);
  });
});
