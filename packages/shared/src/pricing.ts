import type { Mode } from "../../contracts/src/index.js";
export const defaultPricing = {
  currency: "BDT",
  major5: 499,
  full: [
    { max: 25, amount: 699 },
    { max: 100, amount: 999 },
    { max: 500, amount: 1499 },
    { max: 2000, amount: 2499 },
  ],
};
export function pricingConfig(): typeof defaultPricing {
  if (!process.env.PRICING_JSON) return defaultPricing;
  const value = JSON.parse(process.env.PRICING_JSON) as typeof defaultPricing;
  if (
    value.currency !== "BDT" ||
    !Number.isSafeInteger(value.major5) ||
    value.major5 < 1 ||
    !Array.isArray(value.full) ||
    value.full.length !== 4 ||
    value.full.some(
      (tier, i) =>
        tier.max !== [25, 100, 500, 2000][i] ||
        !Number.isSafeInteger(tier.amount) ||
        tier.amount < 1,
    )
  )
    throw new Error("Invalid trusted pricing configuration");
  return value;
}
export function quote(
  scope: "major5" | "full",
  count: number,
  mode: Mode,
  config = pricingConfig(),
) {
  if (!Number.isSafeInteger(count) || count < 1)
    throw new Error("Verified URL count is required");
  if (!["major5", "full"].includes(scope) || !["self", "expert"].includes(mode))
    throw new Error("Invalid selection");
  const tier =
    scope === "major5"
      ? { max: 5, amount: config.major5 }
      : config.full.find((item) => count <= item.max);
  return {
    scope,
    mode,
    count,
    currency: config.currency,
    amount: tier?.amount ?? null,
    tier: scope === "major5" ? "major5" : tier ? `up-to-${tier.max}` : "custom",
    requiresExpertReview: !tier,
  };
}
