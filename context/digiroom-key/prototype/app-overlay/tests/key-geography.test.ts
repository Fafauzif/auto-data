import { expect, it } from "vitest";
import {
  gapCounts,
  geo,
  markets,
  serviceEligible,
  type Market,
} from "../src/key/geography";
import { energyResult } from "../src/domain";
import { DEFAULT_SCENARIO } from "../src/types";
it("reconciles every mapped market, both timing differences, and operator boundaries", () => {
  const expected = {
    Bandung: [78, 17, 14],
    Surabaya: [59, 10, 6],
    Medan: [78, 3, 0],
    Palembang: [69, 9, 0],
  } satisfies Record<Market, number[]>;
  let remainingSoekarnoHatta = 0;
  for (const market of markets) {
    const { origins, outlets } = geo.markets[market];
    const { points, before, after } = gapCounts(origins);
    expect([points, before, after]).toEqual(expected[market]);
    const byId = new Map(outlets.map((outlet) => [outlet.id, outlet]));
    for (const origin of origins) {
      expect(origin.before).toBeCloseTo(
        (origin.dealerSeconds - origin.comparatorSeconds) / 60,
        10,
      );
      expect(origin.after).toBeCloseTo(
        (origin.ownedSeconds - origin.comparatorSeconds) / 60,
        10,
      );
      expect(byId.get(origin.comparator)?.oilComparator).toBe(true);
      expect(byId.get(origin.owned)?.kind).not.toBe("comparison");
      if (
        origin.after > 5 &&
        byId.get(origin.dealer)?.name.includes("Soekarno-Hatta")
      )
        remainingSoekarnoHatta++;
    }
    for (const outlet of outlets) {
      if (outlet.kind === "comparison")
        expect(serviceEligible(outlet, market, "oil", true)).toBe(false);
      if (outlet.kind === "owned") expect(outlet.operator).toBe("Auto2000");
    }
  }
  expect(remainingSoekarnoHatta).toBe(8);
});
it("prices an explicit public charging mix with charging overhead applied once", () => {
  const energy = energyResult({
    ...DEFAULT_SCENARIO,
    car: "bz4x",
    publicChargeShare: 40,
    publicChargePrice: 2700,
    electricityPrice: 1700,
  });
  expect(energy.averageChargePrice).toBe(2100);
  expect(energy.weeklyCost).toBeCloseTo(250 * 0.1213 * 1.1 * 2100);
});
