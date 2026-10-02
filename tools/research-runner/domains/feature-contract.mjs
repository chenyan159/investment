export function featureIdentityFromStem(value) {
  const cleaned = String(value || "")
    .trim()
    .replace(/\.md$/iu, "")
    .replace(/_研究方案$/u, "")
    .replace(/_量化评分_\d{4}-\d{2}-\d{2}$/u, "");
  const match = cleaned.match(/^([NG]\d{2})_(.+)$/u);
  return match ? { featureId: match[1], featureName: match[2], featureSubject: `${match[1]}_${match[2]}` } : null;
}
