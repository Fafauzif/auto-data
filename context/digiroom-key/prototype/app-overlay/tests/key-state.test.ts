import { describe, expect, it } from "vitest";
import {
  approvalMatches,
  driveWindow,
  EMPTY,
  indonesiaDay,
  seedBrief,
  transition,
  type Action,
  type Actor,
  type KeyState,
  reservationOverlaps,
  tradeEquity,
  upgradeCashDue,
} from "../src/key/state";
describe("KEY transaction rules", () => {
  it("requires the authorized payer to approve the current work estimate", () => {
    expect(approvalMatches(3, 2, "payer")).toBe(false);
    expect(approvalMatches(3, 3, "customer")).toBe(false);
    expect(approvalMatches(3, 3, "payer")).toBe(true);
  });
  it("blocks reservations for the same demonstrator through turnaround", () => {
    const confirmed = [{ unit: "Z1", start: 100, end: 300, id: "K-1" }];
    expect(
      reservationOverlaps(confirmed, {
        unit: "Z1",
        start: 299,
        end: 400,
        id: "K-2",
      }),
    ).toBe(true);
    expect(
      reservationOverlaps(confirmed, {
        unit: "Z1",
        start: 300,
        end: 400,
        id: "K-2",
      }),
    ).toBe(false);
    expect(
      reservationOverlaps(confirmed, {
        unit: "Z2",
        start: 200,
        end: 400,
        id: "K-2",
      }),
    ).toBe(false);
  });
  it("handles a trade credit, zero equity and explicit shortfall without double-counting fees", () => {
    expect(tradeEquity(250, 100, 10)).toBe(140);
    expect(tradeEquity(110, 100, 10)).toBe(0);
    expect(tradeEquity(85, 100, 10)).toBe(-25);
    expect([140, 0, -25].map((equity) => upgradeCashDue(100, equity))).toEqual([
      0, 100, 125,
    ]);
  });
});
describe("KEY case handoffs", () => {
  const now = Date.parse("2026-11-16T04:00:00Z");
  function apply(state: KeyState, actor: Actor, action: Action, at = now) {
    const result = transition(state, actor, action, at);
    if ("error" in result) throw new Error(result.error);
    return result.state;
  }
  it("holds the seeded demonstrator until turnaround and sends an alternative for owner acceptance", () => {
    const state = apply(EMPTY, "customer", {
      type: "requestDrive",
      brief: seedBrief,
      kind: "life",
      branch: "Auto2000 Asia Afrika",
      requested: indonesiaDay(2, now),
      shortlist: true,
      firstToyota: false,
      firstXev: true,
      firstAuto2000: true,
    });
    const k = state.drive!;
    const w = driveWindow(
      k.id,
      k.branch,
      k.requested,
      "life",
      k.brief.powertrain,
      k.brief.variant,
    );
    expect(
      transition(
        state,
        "sales",
        { type: "confirmDrive", alternative: false, window: w },
        now,
      ),
    ).toEqual({ error: "overlap" });
    const other = driveWindow(
      k.id,
      k.branch,
      indonesiaDay(7, now),
      "standard",
      k.brief.powertrain,
      k.brief.variant,
    );
    const alternative = apply(state, "sales", {
      type: "confirmDrive",
      alternative: true,
      window: other,
    });
    expect(alternative.drive?.stage).toBe("alternative");
    expect(
      apply(alternative, "customer", { type: "acceptAlternative" }).drive
        ?.stage,
    ).toBe("confirmed");
  });
  it("separates covered base work from approved customer-paid work and blocks a stale payer approval", () => {
    let state = apply(EMPTY, "customer", {
      type: "requestService",
      details: {
        job: "hybrid",
        outlet: "Auto2000 Soekarno-Hatta",
        market: "Bandung",
        prior: "auto2000",
        funding: "covered",
        symptom: "",
        priorWork: "",
        scope: "Hybrid health check",
        base: 277500,
        priceParts: 0,
        labor: 250000,
        tax: 27500,
        day: indonesiaDay(2, now),
        checkIn: "09:00",
        collection: "11:00",
      },
    });
    state = apply(state, "workshop", { type: "confirmService" });
    state = apply(state, "workshop", { type: "checkIn" });
    state = apply(state, "workshop", {
      type: "estimate",
      amount: 55000,
      required: "Seal",
      deferred: "",
      option: "Decline",
    });
    state = apply(state, "workshop", {
      type: "estimate",
      amount: 66000,
      required: "Seal",
      deferred: "",
      option: "Decline",
    });
    expect(
      transition(
        state,
        "payer",
        { type: "approve", version: 2, accepted: true },
        now,
      ),
    ).toEqual({ error: "stale" });
    expect(
      transition(state, "workshop", { type: "readyService" }, now),
    ).toEqual({ error: "action" });
    state = apply(state, "payer", {
      type: "approve",
      version: 3,
      accepted: true,
    });
    state = apply(state, "workshop", { type: "readyService" });
    state = apply(state, "workshop", { type: "closeService" });
    expect(state.service?.payment).toEqual({
      paid: 66000,
      covered: 277500,
      reimbursed: 0,
    });
  });
  it("lets a returning owner buy without trading in and rejects acceptance after a reservation expires", () => {
    let state = apply(EMPTY, "customer", {
      type: "requestUpgrade",
      trade: false,
      consent: true,
      replacement: "bz4x",
    });
    state = apply(state, "upgrade", {
      type: "upgradeTerms",
      payoff: 9000000,
      fee: 300000,
    });
    expect(state.upgrade).toMatchObject({
      payoff: 0,
      fee: 0,
      consent: false,
      unit: "BZ-BDG-021",
    });
    const action = {
      type: "acceptUpgrade",
      revision: state.upgrade!.revision,
    } as const;
    expect(
      transition(state, "customer", action, state.upgrade!.reservedUntil),
    ).toEqual({ error: "expired" });
    state = apply(state, "customer", action);
    state = apply(state, "upgrade", { type: "settleUpgrade" });
    expect(
      apply(state, "upgrade", { type: "deliverUpgrade" }).upgrade?.stage,
    ).toBe("delivered");
  });
});
