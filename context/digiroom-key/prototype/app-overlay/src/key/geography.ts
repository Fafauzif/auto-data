import raw from "./data/geo-v1.json";
import { indonesiaDay, type Funding, type JobId, type Service } from "./state";
export const markets = ["Bandung", "Surabaya", "Medan", "Palembang"] as const;
export type Market = (typeof markets)[number];
export type Origin = {
  id: string;
  position: [number, number];
  dealer: string;
  owned: string;
  comparator: string;
  ties: string[];
  dealerSeconds: number;
  ownedSeconds: number;
  comparatorSeconds: number;
  before: number;
  after: number;
};
export type Outlet = {
  id: string;
  name: string;
  position: [number, number];
  kind: "dealer" | "owned" | "comparison";
  oilComparator: boolean;
  operator: string;
  url: string;
  hours: string;
  residual: number;
};
export const geo = raw as {
  version: number;
  revision: string;
  cutoff: string;
  markets: Record<Market, { origins: Origin[]; outlets: Outlet[] }>;
};
export function gapCounts(origins: Origin[]) {
  return {
    points: origins.length,
    before: origins.filter((o) => o.before > 5).length,
    after: origins.filter((o) => o.after > 5).length,
  };
}
export const flags = {
  Bandung: "auto2000:dba10a500b6d",
  Surabaya: "auto2000:a16d56442a39",
  Medan: "Pancing",
  Palembang: "Tanjung Api",
};
export function serviceEligible(
  outlet: Outlet,
  market: Market,
  job: JobId,
  network: boolean,
) {
  if (job === "oil")
    return outlet.kind === "dealer" || (network && outlet.kind === "owned");
  if (outlet.kind !== "dealer") return false;
  if (job === "home")
    return market === "Bandung" && outlet.id === flags.Bandung;
  if (job === "hybrid")
    return (
      [flags.Bandung, flags.Surabaya].includes(outlet.id) ||
      outlet.name.includes(flags[market]) ||
      (market === "Bandung" && outlet.name.includes("Pasteur"))
    );
  return true;
}
type Price = {
  priceParts: number;
  labor: number;
  tax: number;
  scope: string;
  checkIn: string;
  collection: string;
  funding: Funding;
};
const packages: Record<JobId, Price> = {
  oil: {
    priceParts: 465000,
    labor: 130000,
    tax: 65450,
    scope:
      "4 L engine oil, model-matched filter, washer replacement and leak check",
    checkIn: "09:00",
    collection: "10:30–11:00",
    funding: "paid",
  },
  fault: {
    priceParts: 0,
    labor: 300000,
    tax: 33000,
    scope:
      "Road test and brake inspection, recorded diagnosis before any repair",
    checkIn: "10:00",
    collection: "12:00–12:30",
    funding: "paid",
  },
  hybrid: {
    priceParts: 0,
    labor: 250000,
    tax: 27500,
    scope:
      "Hybrid health check, scan and written result for Yaris Cross Hybrid",
    checkIn: "08:30",
    collection: "10:00–10:30",
    funding: "covered",
  },
  home: {
    priceParts: 465000,
    labor: 170000,
    tax: 69850,
    scope:
      "Avanza oil and filter at a qualifying Bandung address, with post-service leak check",
    checkIn: "09:00–10:00",
    collection: "10:30–11:30",
    funding: "paid",
  },
};
export function servicePackage(job: JobId, outlet: Outlet) {
  const price = packages[job];
  const labor = outlet.kind === "owned" && job === "oil" ? 110000 : price.labor;
  const tax = Math.round((price.priceParts + labor) * 0.11);
  let daysAhead = 2;
  while (
    [0, 6].includes(
      new Date(indonesiaDay(daysAhead) + "T12:00:00+07:00").getUTCDay(),
    )
  )
    daysAhead++;
  return {
    ...price,
    labor,
    tax,
    base: price.priceParts + labor + tax,
    day: indonesiaDay(daysAhead),
  } satisfies Pick<
    Service,
    | "priceParts"
    | "labor"
    | "tax"
    | "base"
    | "day"
    | "checkIn"
    | "collection"
    | "funding"
    | "scope"
  >;
}
