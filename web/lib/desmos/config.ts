// Calculator options meant to match the College Board (Bluebook) build.
//
// UNVERIFIED: no official list of the Bluebook feature set was found during
// research. Before students use this, compare it side by side with
// desmos.com/testing/collegeboard/graphing and with Bluebook practice mode
// (Phase 0 audit), and fix this file to match. The headless verification
// service must import these same options so the AI never relies on a feature
// students don't have.
export const COLLEGE_BOARD_OPTIONS = {
  // Reported disabled in the College Board build.
  images: false,
  folders: false,
  notes: false,
  // Keep students on the item: no sharing or pasting graph links.
  links: false,
  pasteGraphLink: false,
  // Reported enabled in the College Board build: tables, regressions with ~,
  // sliders, lists, statistics. These are Desmos defaults; listed so the audit
  // has one place to check them.
  sliders: true,
  expressions: true,
  settingsMenu: true,
  zoomButtons: true,
  // Radians is the Desmos default. Confirm what Bluebook opens in.
  degreeMode: false,
} as const;

export function desmosScriptUrl(): string | null {
  const key = process.env.NEXT_PUBLIC_DESMOS_API_KEY;
  if (!key) return null;
  const version = process.env.NEXT_PUBLIC_DESMOS_API_VERSION || "v1.11";
  return `https://www.desmos.com/api/${version}/calculator.js?apiKey=${encodeURIComponent(key)}`;
}

let loading: Promise<void> | null = null;

/** Loads the Desmos API script once per page. */
export function loadDesmos(src: string): Promise<void> {
  if (typeof window === "undefined") return Promise.reject(new Error("Desmos only loads in the browser"));
  if (window.Desmos) return Promise.resolve();
  loading ??= new Promise<void>((resolve, reject) => {
    const script = document.createElement("script");
    script.src = src;
    script.async = true;
    script.onload = () => resolve();
    script.onerror = () => {
      loading = null;
      reject(new Error("Couldn't load the Desmos calculator"));
    };
    document.head.appendChild(script);
  });
  return loading;
}
