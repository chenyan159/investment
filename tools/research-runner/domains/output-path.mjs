export function primarySubject(value) {
  return String(value || "").split("/")[0].trim();
}

export function safeOutputNamePart(value, fallback = "output") {
  const cleaned = String(value || "")
    .trim()
    .replace(/[<>:"/\\|?*／\x00-\x1f]/gu, "_")
    .replace(/\s+/gu, "_")
    .replace(/_+/gu, "_")
    .replace(/^_+|_+$/gu, "");
  return (cleaned || fallback).slice(0, 100);
}
