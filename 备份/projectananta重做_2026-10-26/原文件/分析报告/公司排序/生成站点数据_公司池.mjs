export function selectEvaluatedCompanies(indexCompanies, evaluatedTickers, expectedCount) {
  const cohort = new Set(evaluatedTickers);
  if (cohort.size !== expectedCount) {
    throw new Error(`评估公司池数量不符：expected=${expectedCount}, actual=${cohort.size}`);
  }
  const byTicker = new Map(indexCompanies.map((company) => [company.ticker, company]));
  if (byTicker.size !== indexCompanies.length) throw new Error("公司索引存在重复证券身份");
  const missing = [...cohort].filter((ticker) => !byTicker.has(ticker));
  if (missing.length) throw new Error(`历史评估公司缺少索引身份：${missing.join(", ")}`);
  return indexCompanies.filter((company) => cohort.has(company.ticker));
}
