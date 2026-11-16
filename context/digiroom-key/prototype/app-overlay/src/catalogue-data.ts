import type { PurchaseVehicle } from "./commerce-types";
import type { CarId } from "./types";
export interface CatalogueVariant {
  id: string;
  name: string;
  otr: number;
  source: string;
  priceDate: string;
}
export interface CatalogueProduct {
  id: string;
  name: string;
  powertrain: "HEV" | "BEV";
  category: "MPV" | "SUV" | "Sedan" | "Pickup";
  variants: CatalogueVariant[];
  source: string;
  heroCar?: CarId;
  dimensions?: { length: number; width: number; height: number; seats: number };
  note?: string;
}
const INDEX = "https://itstimeforeveryone.toyota.astra.co.id/";
const product = (slug: string) =>
  `https://www.toyota.astra.co.id/product/${slug}`;
const variant = (
  id: string,
  name: string,
  otr: number,
  source = INDEX,
  priceDate = "15 November 2026 reference check",
): CatalogueVariant => ({ id, name, otr, source, priceDate });
const ZENIX =
  "https://auto2000.co.id/dealer-toyota/jakarta-selatan/auto2000lentengagung/sales-advisor/maysantika-intan-sari-00053734/berita-dan-tips/harga-innova-zenix-hybrid-facelift-jakarta-barat";
const VELOZ =
  "https://www.toyota.astra.co.id/corporate-information/news-promo/read/daftar-fitur-dan-teknologi-pada-new-veloz-hybrid-ev-berapa-harganya-di-dealer-resmi-toyota";
export const CATALOGUE: CatalogueProduct[] = [
  {
    id: "zenix",
    name: "Kijang Innova Zenix",
    powertrain: "HEV",
    category: "MPV",
    heroCar: "zenix",
    source: product("kijang-innova-zenix-hybrid-ev"),
    dimensions: { length: 4.755, width: 1.85, height: 1.795, seats: 7 },
    variants: [
      variant(
        "g-hv",
        "G HV CVT",
        475400000,
        ZENIX,
        "12 November 2026 dealer reference",
      ),
      variant(
        "v-hv",
        "V HV Non Modellista · Non RSE",
        517000000,
        ZENIX,
        "12 November 2026 dealer reference",
      ),
      variant(
        "v-mod",
        "V HV Modellista · Non RSE",
        539500000,
        ZENIX,
        "12 November 2026 dealer reference",
      ),
      variant(
        "q-hv",
        "Q HV Modellista TSS · Non RSE",
        618400000,
        ZENIX,
        "12 November 2026 dealer reference",
      ),
    ],
    note: "The interactive model illustrates a seven-position reference layout. It does not reproduce each grade’s seats or equipment.",
  },
  {
    id: "veloz",
    name: "Veloz Hybrid EV",
    powertrain: "HEV",
    category: "MPV",
    source: product("veloz-hybrid-ev"),
    variants: [
      variant(
        "v",
        "V Hybrid CVT · non-premium colour",
        303000000,
        VELOZ,
        "1 July 2026 published reference",
      ),
      variant(
        "q",
        "Q Hybrid CVT · non-premium colour",
        325000000,
        VELOZ,
        "1 July 2026 published reference",
      ),
      variant(
        "q-mod",
        "Q Hybrid CVT Modellista · one tone",
        350000000,
        VELOZ,
        "1 July 2026 published reference",
      ),
      variant(
        "q-tss",
        "Q Hybrid CVT TSS Modellista · one tone",
        385000000,
        VELOZ,
        "1 July 2026 published reference",
      ),
    ],
    note: "Published pricing includes a special V-grade reference. Offer eligibility and spot-order lead time need dealer confirmation.",
  },
  {
    id: "yaris-cross",
    name: "Yaris Cross Hybrid EV",
    powertrain: "HEV",
    category: "SUV",
    source: product("new-yaris-cross-g-hybrid-ev"),
    variants: [
      variant("g", "G Hybrid EV · starting reference", 399000000),
      variant("s", "S Hybrid EV · starting reference", 448800000),
    ],
  },
  {
    id: "corolla-cross",
    name: "Corolla Cross Hybrid EV",
    powertrain: "HEV",
    category: "SUV",
    source: product("corolla-cross-hev"),
    variants: [
      variant("hybrid", "Hybrid EV · starting reference", 606400000),
      variant("gr", "Hybrid EV GR Sport · starting reference", 646500000),
    ],
  },
  {
    id: "corolla-altis",
    name: "Corolla Altis Hybrid EV",
    powertrain: "HEV",
    category: "Sedan",
    source: product("corolla-hybrid"),
    variants: [
      variant("hybrid", "Hybrid EV · starting reference", 639900000),
      variant("gr", "Hybrid EV GR Sport · starting reference", 646600000),
    ],
  },
  {
    id: "vios",
    name: "Vios Hybrid EV",
    powertrain: "HEV",
    category: "Sedan",
    source: product("vios-hybrid-ev"),
    variants: [variant("hybrid", "Hybrid EV · starting reference", 460500000)],
    note: "Toyota’s product page identifies spot-order supply. Branch and delivery timing require confirmation.",
  },
  {
    id: "camry",
    name: "Camry Hybrid EV",
    powertrain: "HEV",
    category: "Sedan",
    source: product("camry-hev"),
    variants: [variant("hybrid", "Hybrid EV · starting reference", 977200000)],
  },
  {
    id: "alphard",
    name: "Alphard Hybrid EV",
    powertrain: "HEV",
    category: "MPV",
    source: product("alphard-hev"),
    variants: [
      variant("xe", "XE Hybrid EV · starting reference", 1388000000),
      variant("hybrid", "Hybrid EV · electrified-list reference", 1737400000),
    ],
    note: "Toyota’s general price list and electrified list show different starting figures for the non-XE model. The figure follows the electrified price list. Request a quote for the exact grade.",
  },
  {
    id: "vellfire",
    name: "Vellfire Hybrid EV",
    powertrain: "HEV",
    category: "MPV",
    source: product("vellfire-hev"),
    variants: [variant("hybrid", "Hybrid EV · starting reference", 1872800000)],
  },
  {
    id: "land-cruiser",
    name: "Land Cruiser Hybrid EV",
    powertrain: "HEV",
    category: "SUV",
    source: product("lc300-hybrid-ev"),
    variants: [variant("hybrid", "Hybrid EV · starting reference", 2716000000)],
  },
  {
    id: "bz4x",
    name: "Toyota bZ4X",
    powertrain: "BEV",
    category: "SUV",
    heroCar: "bz4x",
    source: product("bz4x-battery-ev"),
    dimensions: { length: 4.69, width: 1.86, height: 1.65, seats: 5 },
    variants: [variant("bev", "Battery EV · starting reference", 799000000)],
    note: "The stylized 3D asset is a reference bZ4X silhouette, not a model-year or equipment configurator.",
  },
  {
    id: "bz4x-touring",
    name: "bZ4X Touring Battery EV",
    powertrain: "BEV",
    category: "SUV",
    source: product("bz4x-touring-battery-ev"),
    variants: [variant("bev", "Battery EV · starting reference", 889000000)],
  },
  {
    id: "urban-cruiser",
    name: "Urban Cruiser Battery EV",
    powertrain: "BEV",
    category: "SUV",
    source: product("urban-cruiser-battery-ev"),
    variants: [variant("bev", "Battery EV · starting reference", 759000000)],
  },
  {
    id: "hilux",
    name: "Hilux Battery EV",
    powertrain: "BEV",
    category: "Pickup",
    source: product("hilux-battery-ev"),
    variants: [variant("bev", "Battery EV · starting reference", 1019000000)],
  },
];
export function toPurchaseVehicle(
  p: CatalogueProduct,
  v: CatalogueVariant = p.variants[0],
): PurchaseVehicle {
  return {
    id: p.id,
    name: p.name,
    variant: v.name,
    powertrain: p.powertrain,
    otr: v.otr,
    region: "Jakarta reference",
    priceDate: v.priceDate,
    source: v.source,
    heroCar: p.heroCar,
  };
}
export const HERO_VEHICLES: Record<CarId, PurchaseVehicle> = {
  zenix: toPurchaseVehicle(CATALOGUE.find((p) => p.id === "zenix")!),
  bz4x: toPurchaseVehicle(CATALOGUE.find((p) => p.id === "bz4x")!),
};
export function filterCatalogue(
  query: string,
  powertrain: string = "all",
  category: string = "all",
) {
  const q = query.trim().toLowerCase();
  return CATALOGUE.filter(
    (p) =>
      (powertrain === "all" || p.powertrain === powertrain) &&
      (category === "all" || p.category === category) &&
      `${p.name} ${p.category} ${p.powertrain}`.toLowerCase().includes(q),
  );
}

export function resolveVehicle(
  id: string,
  variantName?: string,
): PurchaseVehicle | null {
  const p = CATALOGUE.find((v) => v.id === id);
  if (!p) return null;
  const v =
    p.variants.find((v) => v.name === variantName || v.id === variantName) ||
    p.variants[0];
  return toPurchaseVehicle(p, v);
}
