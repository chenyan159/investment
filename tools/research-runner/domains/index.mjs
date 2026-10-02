import fs from "node:fs";
import { companyComparisonDomain } from "./company-comparison.mjs";
import { companyInvestmentDecisionDomain } from "./company-investment-decision.mjs";
import { companyDomain } from "./company.mjs";
import { companySentimentDomain } from "./company-sentiment.mjs";
import { featureQuantizationDomain } from "./feature-quantization.mjs";
import { fileRunDomain } from "./file-run.mjs";
import { industryDomain } from "./industry.mjs";

export const DOMAIN_ADAPTERS = {
  company: companyDomain,
  "company-comparison": companyComparisonDomain,
  "company-investment-decision": companyInvestmentDecisionDomain,
  "company-sentiment": companySentimentDomain,
  industry: industryDomain,
  "feature-quantization": featureQuantizationDomain,
  "file-run": fileRunDomain,
};

export function getDomainAdapter(domain) {
  const adapter = DOMAIN_ADAPTERS[domain];
  if (!adapter) throw new Error(`Unsupported domain: ${domain}`);
  return adapter;
}

export function getDomainAdapters(domain = "") {
  return domain ? [getDomainAdapter(domain)] : Object.values(DOMAIN_ADAPTERS);
}

export function checkRequiredPaths(domain = "") {
  for (const adapter of getDomainAdapters(domain)) {
    for (const requiredPath of adapter.requiredPaths) {
      if (!fs.existsSync(requiredPath)) throw new Error(`Required file does not exist: ${requiredPath}`);
    }
    if (typeof adapter.checkRequired === "function") adapter.checkRequired();
  }
}
