export type Journey = "K" | "E" | "Y";
export type Role = "customer" | "sales" | "workshop" | "upgrade";
export type Actor = Role | "payer";
export type DriveKind = "life" | "standard";
export type JobId = "oil" | "fault" | "hybrid" | "home";
export type Prior = "independent" | "auto2000" | "first";
export type Funding = "paid" | "covered" | "reimbursement";
export type Brief = {
  model: string;
  variant: string;
  powertrain: string;
  referencePrice?: number;
  checks: string[];
  planning: string;
};
export type Window = {
  id: string;
  unit: string;
  start: number;
  end: number;
  returnAt: number;
  branch: string;
  kind: DriveKind;
};
export type Log = {
  at: number;
  actor: Actor;
  action: Action["type"];
  version?: number;
};
type RecordBase = { id: string; history: Log[]; revision: number };
export type Drive = RecordBase & {
  brief: Brief;
  kind: DriveKind;
  branch: string;
  requested: string;
  shortlist: boolean;
  firstToyota: boolean;
  firstXev: boolean;
  firstAuto2000: boolean;
  window?: Window;
  condition?: string;
  odometer?: number;
  level?: number;
  results?: string;
  checkResults?: CheckResult[];
  quote?: {
    issued: number;
    cash: number;
    monthly: number;
    term: number;
    fees: number;
  };
  stage:
    | "requested"
    | "alternative"
    | "confirmed"
    | "out"
    | "returned"
    | "quoted"
    | "accepted"
    | "financed"
    | "ordered"
    | "delivered";
};
export type Service = RecordBase & {
  job: JobId;
  outlet: string;
  market: string;
  prior: Prior;
  funding: Funding;
  symptom: string;
  priorWork: string;
  scope: string;
  base: number;
  priceParts: number;
  labor: number;
  tax: number;
  day: string;
  checkIn: string;
  collection: string;
  estimate?: {
    version: number;
    amount: number;
    required: string;
    deferred: string;
    option: string;
  };
  approval?: { version: number; accepted: boolean };
  payment?: { paid: number; covered: number; reimbursed: number };
  stage:
    | "requested"
    | "confirmed"
    | "checkedIn"
    | "approval"
    | "authorized"
    | "ready"
    | "closed";
};
export type Upgrade = RecordBase & {
  trade: boolean;
  consent: boolean;
  replacement: "zenix" | "bz4x";
  offer?: {
    amount: number;
    expires: number;
    conditions: string;
    evidence: string;
  };
  payoff: number;
  fee: number;
  reservedUntil?: number;
  unit?: string;
  acceptedRevision?: number;
  quoteAt?: number;
  depositPaid?: number;
  refund?: number;
  stage:
    | "inspection"
    | "offer"
    | "terms"
    | "accepted"
    | "settled"
    | "delivered"
    | "recovery";
};
export type KeyState = {
  v: 1;
  drive?: Drive;
  service?: Service;
  upgrade?: Upgrade;
};
export type CheckResult = "pass" | "adjust" | "pending";
export type Action =
  | {
      type: "requestDrive";
      brief: Brief;
      kind: DriveKind;
      branch: string;
      requested: string;
      shortlist: boolean;
      firstToyota: boolean;
      firstXev: boolean;
      firstAuto2000: boolean;
    }
  | { type: "confirmDrive"; alternative: boolean; window: Window }
  | { type: "quoteDrive"; terms: Omit<NonNullable<Drive["quote"]>, "issued"> }
  | {
      type:
        | "acceptAlternative"
        | "returnDrive"
        | "acceptDriveQuote"
        | "financeDrive"
        | "orderDrive"
        | "deliverDrive";
    }
  | {
      type: "pickup";
      condition: string;
      odometer: number;
      level: number;
      checked: boolean;
    }
  | { type: "saveResult"; results: string; checks: CheckResult[] }
  | {
      type: "requestService";
      details: Omit<
        Service,
        keyof RecordBase | "stage" | "estimate" | "approval" | "payment"
      >;
    }
  | { type: "confirmService" | "checkIn" | "readyService" | "closeService" }
  | {
      type: "estimate";
      amount: number;
      required: string;
      deferred: string;
      option: string;
    }
  | { type: "approve"; version: number; accepted: boolean }
  | {
      type: "requestUpgrade";
      trade: boolean;
      consent: boolean;
      replacement: Upgrade["replacement"];
    }
  | { type: "issueOffer"; amount: number; evidence: string; conditions: string }
  | { type: "upgradeTerms"; payoff: number; fee: number }
  | { type: "acceptUpgrade"; revision: number }
  | {
      type:
        | "settleUpgrade"
        | "deliverUpgrade"
        | "recoverUpgrade"
        | "reopenUpgrade";
    };
export const KEY_STORAGE = "digiroom-key-1";
export const EMPTY: KeyState = { v: 1 };
export const seedBrief: Brief = {
  model: "Toyota Innova Zenix Hybrid",
  variant: "V HV Non Modellista · Non RSE",
  powertrain: "HEV",
  referencePrice: 517000000,
  checks: [
    "Open the tailgate in a 3.10 × 5.60 m garage",
    "Reach row three with the child seat fitted",
    "Load two bags for a family of five",
  ],
  planning:
    "250 km/week · Pertamax Rp15.950/L · assumed 5.5 L/100 km · estimated Rp219.313/week",
};
export const replacements = {
  zenix: {
    model: "Innova Zenix Hybrid",
    variant: "V HV Non Modellista · Non RSE",
    unit: "ZX-BDG-017",
    otr: 491800000,
    cash: 121500000,
    monthly: 9845000,
    term: 48,
    fees: 4500000,
    deposit: 2000000,
    balloon: 0,
  },
  bz4x: {
    model: "Toyota bZ4X",
    variant: "FWD",
    unit: "BZ-BDG-021",
    otr: 799000000,
    cash: 199500000,
    monthly: 15750000,
    term: 48,
    fees: 6500000,
    deposit: 2000000,
    balloon: 0,
  },
};
const day = 86_400_000;
const hour = 3_600_000;
export function indonesiaDay(offset = 0, at = Date.now()) {
  return new Intl.DateTimeFormat("sv-SE", { timeZone: "Asia/Jakarta" }).format(
    new Date(at + offset * day),
  );
}
export function driveWindow(
  id: string,
  branch: string,
  requested: string,
  kind: DriveKind,
  powertrain: string,
  variant: string,
): Window {
  const start = Date.parse(requested + "T09:00:00+07:00");
  const returnAt = start + (kind === "life" ? 48 : 1) * hour;
  return {
    id,
    unit: [branch, powertrain, variant].join(" / "),
    start,
    returnAt,
    end: returnAt + (kind === "life" ? 3 * hour : hour / 2),
    branch,
    kind,
  };
}
export function reservations(block: Window, drive?: Drive) {
  return [
    block,
    ...(drive?.window && drive.stage === "out"
      ? [{ ...drive.window, end: Number.POSITIVE_INFINITY }]
      : drive?.window &&
          ["alternative", "confirmed", "returned"].includes(drive.stage)
        ? [drive.window]
        : []),
  ];
}
export function reservationOverlaps(
  existing: Pick<Window, "unit" | "start" | "end" | "id">[],
  candidate: Pick<Window, "unit" | "start" | "end" | "id">,
) {
  return existing.some(
    (entry) =>
      entry.id !== candidate.id &&
      entry.unit === candidate.unit &&
      candidate.start < entry.end &&
      candidate.end > entry.start,
  );
}
export function tradeEquity(offer: number, payoff: number, fees: number) {
  return offer - payoff - fees;
}
export function upgradeCashDue(cash: number, equity: number) {
  return Math.max(0, cash - equity);
}
export function approvalMatches(
  currentVersion: number,
  approvedVersion: number,
  actor: Actor,
) {
  return currentVersion === approvedVersion && actor === "payer";
}
export function isCurrentUpgrade(u: Upgrade, at: number) {
  return (
    !!u.unit &&
    (u.reservedUntil ?? 0) > at &&
    (!u.trade || (u.offer?.expires ?? 0) > at)
  );
}
export function readKey(): KeyState {
  try {
    const data = JSON.parse(localStorage.getItem(KEY_STORAGE) ?? "null");
    if (!data || data.v !== 1) return EMPTY;
    for (const field of ["drive", "service", "upgrade"]) {
      const record = data[field];
      if (
        record &&
        (typeof record.id !== "string" ||
          !Array.isArray(record.history) ||
          typeof record.stage !== "string")
      )
        return EMPTY;
    }
    return data;
  } catch {
    return EMPTY;
  }
}
export function responsible(
  journey: Journey,
  state: KeyState,
): Actor | undefined {
  if (journey === "K") {
    const k = state.drive;
    if (!k || k.stage === "delivered") return;
    return k.stage === "out" ||
      k.stage === "alternative" ||
      k.stage === "quoted"
      ? "customer"
      : "sales";
  }
  if (journey === "E") {
    const e = state.service;
    if (!e || e.stage === "closed") return;
    return e.stage === "approval" ? "payer" : "workshop";
  }
  const y = state.upgrade;
  if (y && y.stage !== "delivered")
    return y.stage === "terms" ? "customer" : "upgrade";
}
const roles: Record<Action["type"], Actor> = {
  requestDrive: "customer",
  confirmDrive: "sales",
  acceptAlternative: "customer",
  pickup: "sales",
  saveResult: "customer",
  returnDrive: "sales",
  quoteDrive: "sales",
  acceptDriveQuote: "customer",
  financeDrive: "sales",
  orderDrive: "sales",
  deliverDrive: "sales",
  requestService: "customer",
  confirmService: "workshop",
  checkIn: "workshop",
  estimate: "workshop",
  approve: "payer",
  readyService: "workshop",
  closeService: "workshop",
  requestUpgrade: "customer",
  issueOffer: "upgrade",
  upgradeTerms: "upgrade",
  acceptUpgrade: "customer",
  settleUpgrade: "upgrade",
  deliverUpgrade: "upgrade",
  recoverUpgrade: "upgrade",
  reopenUpgrade: "upgrade",
};
export type ErrorCode =
  | "action"
  | "overlap"
  | "terms"
  | "stale"
  | "expired"
  | "details";
type Result = { state: KeyState } | { error: ErrorCode };
export function transition(
  state: KeyState,
  actor: Actor,
  action: Action,
  at = Date.now(),
): Result {
  if (roles[action.type] !== actor) return { error: "action" };
  const k = state.drive,
    e = state.service,
    y = state.upgrade;
  const log = { actor, at, action: action.type };
  const next = <T extends RecordBase>(record: T, patch: Partial<T>): T => ({
    ...record,
    ...patch,
    history: [
      ...record.history,
      { ...log, version: patch.revision ?? record.revision },
    ],
  });
  const start = (prefix: Journey): RecordBase => ({
    id: `KEY-${prefix}-${at.toString(36).toUpperCase()}`,
    revision: 0,
    history: [log],
  });
  const drive = (patch: Partial<Drive>) => ({
    state: { ...state, drive: next(k!, patch) },
  });
  const service = (patch: Partial<Service>) => ({
    state: { ...state, service: next(e!, patch) },
  });
  const upgrade = (patch: Partial<Upgrade>) => ({
    state: { ...state, upgrade: next(y!, patch) },
  });
  switch (action.type) {
    case "requestDrive":
      if (k && k.stage !== "delivered") break;
      if (
        !action.branch ||
        !action.brief.variant ||
        !action.brief.checks.length ||
        !/^\d{4}-\d{2}-\d{2}$/.test(action.requested) ||
        action.requested < indonesiaDay(0, at)
      )
        return { error: "details" };
      return {
        state: {
          ...state,
          drive: {
            ...start("K"),
            brief: action.brief,
            kind: action.kind,
            branch: action.branch,
            requested: action.requested,
            shortlist: action.shortlist,
            firstToyota: action.firstToyota,
            firstXev: action.firstXev,
            firstAuto2000: action.firstAuto2000,
            stage: "requested",
          },
        },
      };
    case "confirmDrive": {
      if (k?.stage !== "requested") break;
      const w = action.window;
      if (w.id !== k.id || !Number.isFinite(w.start) || w.end <= w.start)
        return { error: "details" };
      if (w.start < at) return { error: "expired" };
      const lifeBranch =
        k.brief.powertrain === "BEV"
          ? "Auto2000 Pasteur"
          : "Auto2000 Asia Afrika";
      if (
        w.kind === "life" &&
        (!k.shortlist ||
          w.branch !== lifeBranch ||
          k.brief.powertrain === "PHEV" ||
          !/zenix|bz4x/i.test(k.brief.model))
      )
        return { error: "terms" };
      const block = driveWindow(
        "FLEET-BDG-01",
        "Auto2000 Asia Afrika",
        indonesiaDay(4, k.history[0].at),
        "life",
        "HEV",
        seedBrief.variant,
      );
      if (reservationOverlaps(reservations(block, k), w))
        return { error: "overlap" };
      return drive({
        window: w,
        stage: action.alternative ? "alternative" : "confirmed",
      });
    }
    case "acceptAlternative":
      if (k?.stage === "alternative" && k.window)
        return k.window.start > at
          ? drive({ stage: "confirmed" })
          : { error: "expired" };
      break;
    case "pickup":
      if (k?.stage !== "confirmed") break;
      if (
        !action.checked ||
        !action.condition.trim() ||
        !Number.isFinite(action.odometer) ||
        action.odometer < 0 ||
        !Number.isFinite(action.level) ||
        action.level < 0 ||
        action.level > 100
      )
        return { error: "details" };
      return drive({
        stage: "out",
        odometer: action.odometer,
        level: action.level,
        condition: action.condition.trim(),
      });
    case "saveResult":
      if (
        k?.stage === "out" &&
        action.results.trim() &&
        action.checks.length === k.brief.checks.length
      )
        return drive({
          results: action.results.trim(),
          checkResults: action.checks,
        });
      return { error: "details" };
    case "returnDrive":
      if (k?.stage === "out" && k.results) return drive({ stage: "returned" });
      return { error: "details" };
    case "quoteDrive":
      if (k?.stage === "returned") {
        const { cash, monthly, term, fees } = action.terms;
        if (
          ![cash, monthly, term, fees].every(Number.isSafeInteger) ||
          cash <= 0 ||
          monthly < 0 ||
          term <= 0 ||
          fees < 0 ||
          fees > cash
        )
          return { error: "details" };
        return drive({
          stage: "quoted",
          revision: k.revision + 1,
          quote: { ...action.terms, issued: at },
        });
      }
      break;
    case "acceptDriveQuote":
      if (k?.stage === "quoted") return drive({ stage: "accepted" });
      break;
    case "financeDrive":
      if (k?.stage === "accepted") return drive({ stage: "financed" });
      break;
    case "orderDrive":
      if (k?.stage === "financed") return drive({ stage: "ordered" });
      break;
    case "deliverDrive":
      if (k?.stage === "ordered") return drive({ stage: "delivered" });
      break;
    case "requestService":
      if (e && e.stage !== "closed") break;
      if (
        !action.details.outlet ||
        (action.details.job === "fault" && !action.details.symptom.trim())
      )
        return { error: "details" };
      return {
        state: {
          ...state,
          service: {
            ...action.details,
            ...start("E"),
            stage: "requested",
            revision: 1,
          },
        },
      };
    case "confirmService":
      if (e?.stage === "requested") return service({ stage: "confirmed" });
      break;
    case "checkIn":
      if (e?.stage === "confirmed") return service({ stage: "checkedIn" });
      break;
    case "estimate":
      if (!e || !["checkedIn", "approval", "authorized"].includes(e.stage))
        break;
      if (
        !Number.isSafeInteger(action.amount) ||
        action.amount <= 0 ||
        !action.required.trim()
      )
        return { error: "details" };
      return service({
        stage: "approval",
        revision: e.revision + 1,
        approval: undefined,
        estimate: {
          version: e.revision + 1,
          amount: action.amount,
          required: action.required.trim(),
          deferred: action.deferred.trim(),
          option: action.option.trim(),
        },
      });
    case "approve":
      if (!e || e.stage !== "approval" || !e.estimate) break;
      if (!approvalMatches(e.estimate.version, action.version, actor))
        return { error: "stale" };
      return service({
        stage: "authorized",
        approval: { version: action.version, accepted: action.accepted },
      });
    case "readyService":
      if (
        e?.stage === "checkedIn" ||
        (e?.stage === "authorized" &&
          e.approval?.version === e.estimate?.version)
      )
        return service({ stage: "ready" });
      break;
    case "closeService":
      if (e?.stage === "ready") {
        const extra = e.approval?.accepted ? (e.estimate?.amount ?? 0) : 0;
        const payment = {
          paid: e.funding === "paid" ? e.base + extra : extra,
          covered: e.funding === "covered" ? e.base : 0,
          reimbursed: e.funding === "reimbursement" ? e.base : 0,
        };
        return service({ stage: "closed", payment });
      }
      break;
    case "requestUpgrade":
      if (y && y.stage !== "delivered") break;
      return {
        state: {
          ...state,
          upgrade: {
            ...start("Y"),
            trade: action.trade,
            consent: action.trade && action.consent,
            replacement: action.replacement,
            payoff: 0,
            fee: 0,
            stage: action.trade ? "inspection" : "offer",
          },
        },
      };
    case "issueOffer":
      if (y?.stage !== "inspection" || !y.trade) break;
      if (
        !Number.isSafeInteger(action.amount) ||
        action.amount <= 0 ||
        !action.conditions.trim()
      )
        return { error: "details" };
      return upgrade({
        stage: "offer",
        revision: y.revision + 1,
        offer: {
          amount: action.amount,
          expires: at + 5 * day,
          conditions: action.conditions.trim(),
          evidence: y.consent ? action.evidence.trim() : "",
        },
      });
    case "upgradeTerms":
      if (y?.stage !== "offer") break;
      if (y.trade && (y.offer?.expires ?? 0) <= at) return { error: "expired" };
      if (
        ![action.payoff, action.fee].every(
          (value) => Number.isSafeInteger(value) && value >= 0,
        )
      )
        return { error: "details" };
      return upgrade({
        stage: "terms",
        revision: y.revision + 1,
        payoff: y.trade ? action.payoff : 0,
        fee: y.trade ? action.fee : 0,
        unit: replacements[y.replacement].unit,
        reservedUntil: at + 2 * day,
        quoteAt: at,
      });
    case "acceptUpgrade":
      if (y?.stage !== "terms") break;
      if (y.revision !== action.revision) return { error: "stale" };
      if (!isCurrentUpgrade(y, at)) return { error: "expired" };
      return upgrade({
        stage: "accepted",
        acceptedRevision: action.revision,
        depositPaid: Math.min(
          replacements[y.replacement].deposit,
          upgradeCashDue(
            replacements[y.replacement].cash,
            y.trade && y.offer
              ? tradeEquity(y.offer.amount, y.payoff, y.fee)
              : 0,
          ),
        ),
        refund: undefined,
      });
    case "settleUpgrade":
      if (y?.stage !== "accepted" || y.acceptedRevision !== y.revision) break;
      if (!isCurrentUpgrade(y, at)) return { error: "expired" };
      return upgrade({ stage: "settled" });
    case "deliverUpgrade":
      if (y?.stage === "settled" && y.acceptedRevision === y.revision)
        return upgrade({ stage: "delivered" });
      break;
    case "recoverUpgrade":
      if (y && ["offer", "terms", "accepted"].includes(y.stage))
        return upgrade({
          stage: "recovery",
          revision: y.revision + 1,
          offer: undefined,
          unit: undefined,
          reservedUntil: undefined,
          acceptedRevision: undefined,
          quoteAt: undefined,
          refund: y.depositPaid ?? 0,
          depositPaid: undefined,
        });
      break;
    case "reopenUpgrade":
      if (y?.stage === "recovery")
        return upgrade({ stage: y.trade ? "inspection" : "offer" });
      break;
  }
  return { error: "action" };
}
