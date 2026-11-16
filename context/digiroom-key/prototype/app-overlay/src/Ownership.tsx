import { useLocale } from "./locale";
import { useEffect, useMemo, useRef, useState } from "react";
import {
  ArrowUpRight,
  ArrowRight,
  Check,
  ChevronDown,
  Fuel,
  PlugZap,
  ShieldCheck,
  Wrench,
} from "lucide-react";
import type { PurchaseVehicle } from "./commerce-types";
import { moneyIDR as money } from "./commerce-types";
import {
  financeEstimate,
  ownershipDefaults,
  ownershipEstimate,
  validateOwnership,
  type OwnershipInputs,
} from "./ownership-model";
import "./ownership.css";
interface Props {
  vehicle: PurchaseVehicle;
  kmWeek: number;
  fuelPrice: number;
  electricityPrice: number;
  onSummaryChange?: (summary: string) => void;
  onVisit?: () => void;
  onServiceVisit?: () => void;
  onTrade?: (marketTrade: number) => void;
}
function NumberField({
  label,
  value,
  onChange,
  min = 0,
  max = 6e9,
  step = 100000,
  unit = "Rp",
}: {
  label: string;
  value: number;
  onChange: (n: number) => void;
  min?: number;
  max?: number;
  step?: number;
  unit?: string;
}) {
  const { t, lang } = useLocale();

  return (
    <label className="own-field">
      <span>{label}</span>
      <span className="own-input">
        <span>{unit}</span>
        <input
          type="number"
          min={min}
          max={max}
          step={step}
          value={value || ""}
          placeholder="0"
          onChange={(e) => onChange(Number(e.target.value))}
        />
      </span>
    </label>
  );
}
function Slider({
  label,
  value,
  min,
  max,
  step = 1,
  onChange,
  unit,
}: {
  label: string;
  value: number;
  min: number;
  max: number;
  step?: number;
  onChange: (n: number) => void;
  unit: string;
}) {
  const { t, lang } = useLocale();

  return (
    <label className="own-slider">
      <span>
        {label}
        <strong>
          {value}
          {unit}
        </strong>
      </span>
      <input
        type="range"
        min={min}
        max={max}
        step={step}
        value={value}
        onChange={(e) => onChange(Number(e.target.value))}
      />
      <small>
        {min}
        {unit}
        <span>
          {max}
          {unit}
        </span>
      </small>
    </label>
  );
}
function Owner({
  vehicle,
  kmWeek,
  fuelPrice,
  electricityPrice,
  onSummaryChange,
  onVisit,
  onServiceVisit,
  onTrade,
}: Props) {
  const { t, lang } = useLocale();

  const storageKey = `digiroom-ownership-v2:${vehicle.id}:${vehicle.variant}`;
  const [input, setInput] = useState<OwnershipInputs>(() => {
    try {
      return validateOwnership(
        JSON.parse(localStorage.getItem(storageKey) || "null"),
        vehicle,
      );
    } catch {
      return ownershipDefaults(vehicle);
    }
  });
  const [tab, setTab] = useState<"finance" | "cost" | "service">("finance"),
    [notice, setNotice] = useState("");
  const changedPrice = useRef(false),
    callback = useRef(onSummaryChange);
  callback.current = onSummaryChange;
  const patch = (v: Partial<OwnershipInputs>) =>
    setInput((prev) => validateOwnership({ ...prev, ...v }, vehicle));
  const finance = useMemo(() => financeEstimate(input), [input]);
  const estimate = useMemo(
    () =>
      ownershipEstimate(vehicle, input, kmWeek, fuelPrice, electricityPrice),
    [vehicle, input, kmWeek, fuelPrice, electricityPrice],
  );
  const ev = vehicle.powertrain === "BEV",
    valid = input.price > 0;
  const referencePrice =
    input.region === "Jakarta" &&
    vehicle.otr !== null &&
    !changedPrice.current &&
    input.price === vehicle.otr;
  const summary = [
    `PURCHASE SIMULATION: ${vehicle.name} — ${vehicle.variant}`,
    valid
      ? `Region: ${input.region}; ${referencePrice ? "dated reference" : "user planning"} OTR: ${money(input.price)}`
      : `Region: ${input.region}; OTR not supplied. Finance and TCO totals are unavailable.`,
    valid
      ? `DP ${input.dp}%: ${money(finance.downPayment)}; term ${input.years} years; assumed flat rate ${input.flatRate}% per year.`
      : `Requested simulation: DP ${input.dp}%; term ${input.years} years; OTR required.`,
    `Lender quotation to request: ${input.quoteRequest}. No application is submitted.`,
    `Monthly repayment: ${valid ? money(finance.monthly) : "OTR required"}; vehicle initial cash: ${valid ? money(finance.initialCash) : "OTR required"}.`,
    `Trade-in estimate: ${money(input.tradeValue)}; outstanding settlement: ${money(input.settlement)}; net equity: ${money(finance.netEquity)}.`,
    `Five-year scenario: ${valid ? money(estimate.total) : "OTR required"} including estimated resale ${input.resale}% of OTR.`,
    `Energy assumptions: ${ev ? "12.13 kWh/100 km + 10% charging overhead" : "5.5 L/100 km; Pertamax RON92"}; ${kmWeek} km/week; petrol ${money(fuelPrice)}/L${ev ? `; electricity ${money(electricityPrice)}/kWh` : ""}.`,
    `Planning scenario only. Not an ACC/TAF approval, KINTO subscription quote or OLXmobbi valuation.`,
  ].join("\n");
  useEffect(() => {
    callback.current?.(summary);
  }, [summary]);
  useEffect(() => {
    try {
      localStorage.setItem(storageKey, JSON.stringify(input));
    } catch {
      setNotice(
        t(
          "These changes cannot be saved in this browser. Copy or download the visit brief.",
        ),
      );
    }
  }, [input, storageKey]);
  const changeRegion = (region: "Jakarta" | "Bandung") => {
    changedPrice.current = false;
    patch({ region, price: region === "Jakarta" ? (vehicle.otr ?? 0) : 0 });
  };
  const rows: [string, number][] = [
    [t("Depreciation after resale"), estimate.rows.depreciation],
    [t("Fuel / charging"), estimate.rows.energy],
    ["Insurance", estimate.rows.insurance],
    [t("Annual vehicle tax"), estimate.rows.tax],
    [t("Service & wear budget"), estimate.rows.service],
    [t("Charging installation"), estimate.rows.installation],
    [t("Loan interest"), estimate.rows.interest],
    [t("Administration"), estimate.rows.fees],
  ];
  return (
    <section className="ownership-panel" aria-labelledby="ownership-title">
      <header className="own-header">
        <div>
          <span className="own-kicker">{t("PURCHASE & OWNERSHIP")}</span>
          <h2 id="ownership-title">
            {t("Calculate your Toyota ownership costs.")}
          </h2>
          <p>
            {vehicle.name}{" "}
            <span>
              · {vehicle.variant} · {vehicle.powertrain}
            </span>
          </p>
        </div>
        <button className="own-visit" onClick={onVisit}>
          {t("Prepare a visit brief")}
          <ArrowUpRight size={17} />
        </button>
      </header>
      <div
        className="own-tabs"
        role="group"
        aria-label={t("Ownership sections")}
      >
        {(
          [
            ["finance", t("DP & instalments")],
            ["cost", t("Five-year costs")],
            ["service", t("Service & benefits")],
          ] as const
        ).map(([id, label]) => (
          <button key={id} aria-pressed={tab === id} onClick={() => setTab(id)}>
            {label}
          </button>
        ))}
      </div>
      {notice && (
        <p className="own-status" role="status">
          {t(notice)}
        </p>
      )}
      {tab === "finance" && (
        <div className="own-finance-layout">
          <div className="own-form">
            <div className="own-two">
              <label className="own-field">
                <span>{t("Registration region")}</span>
                <select
                  value={input.region}
                  onChange={(e) =>
                    changeRegion(e.target.value as "Jakarta" | "Bandung")
                  }
                >
                  <option>Jakarta</option>
                  <option>Bandung</option>
                </select>
              </label>
              <NumberField
                label={t("Vehicle OTR")}
                value={input.price}
                step={1000000}
                onChange={(n) => {
                  changedPrice.current = true;
                  patch({ price: n });
                }}
              />
            </div>
            <p className="own-note">
              {referencePrice ? (
                <>
                  {t("Jakarta reference ·")}
                  {vehicle.priceDate}.{" "}
                  <a href={vehicle.source} target="_blank" rel="noreferrer">
                    {t("View source")}
                    <ArrowUpRight size={11} />
                  </a>
                </>
              ) : (
                <>
                  {t(
                    "Enter an OTR amount for this region. Changes are your planning inputs, not a live dealer price.",
                  )}
                </>
              )}
            </p>
            <Slider
              label={t("Down payment")}
              value={input.dp}
              min={15}
              max={50}
              unit="%"
              onChange={(n) => patch({ dp: n })}
            />
            <Slider
              label={t("Loan term")}
              value={input.years}
              min={1}
              max={5}
              unit=" yr"
              onChange={(n) => patch({ years: n })}
            />
            <details className="own-details">
              <summary>
                {t("Adjust finance assumptions")}
                <ChevronDown size={15} />
              </summary>
              <div className="own-two">
                <label className="own-field">
                  <span>{t("Lender quotation to request")}</span>
                  <select
                    value={input.quoteRequest}
                    onChange={(e) =>
                      patch({
                        quoteRequest: e.target
                          .value as OwnershipInputs["quoteRequest"],
                      })
                    }
                  >
                    <option>ACC &amp; TAF</option>
                    <option>ACC</option>
                    <option>TAF</option>
                  </select>
                </label>
                <NumberField
                  label={t("Annual flat interest")}
                  value={input.flatRate}
                  min={0}
                  max={20}
                  step={0.1}
                  unit="%"
                  onChange={(n) => patch({ flatRate: n })}
                />
                <NumberField
                  label={t("Administration fee")}
                  value={input.fees}
                  max={1e8}
                  onChange={(n) => patch({ fees: n })}
                />
                <NumberField
                  label={t("Annual insurance allowance")}
                  value={input.insuranceRate}
                  max={10}
                  step={0.1}
                  unit="% OTR"
                  onChange={(n) => patch({ insuranceRate: n })}
                />
              </div>
              <p className="own-note">
                {t("Team assumptions:")} {input.flatRate}
                {t(
                  "% flat interest per year; administration paid upfront; first-year insurance paid upfront. Instalments start after handover. No advance instalment or lender promotion is assumed.",
                )}
              </p>
            </details>
            <details className="own-details">
              <summary>
                {t("Apply a trade-in estimate")}
                <ChevronDown size={15} />
              </summary>
              <p className="own-note">
                {t(
                  "Use your own estimate until a physical appraisal and loan-settlement statement are available.",
                )}
              </p>
              <div className="own-two">
                <NumberField
                  label={t("Estimated current-car value")}
                  value={input.tradeValue}
                  onChange={(n) => patch({ tradeValue: n })}
                />
                <NumberField
                  label={t("Outstanding settlement")}
                  value={input.settlement}
                  onChange={(n) => patch({ settlement: n })}
                />
              </div>
              <div className="own-equity">
                <span>{t("Net equity after settlement")}</span>
                <strong>{money(finance.netEquity)}</strong>
              </div>
              {finance.settlementGap > 0 && (
                <p className="own-caution">
                  {t("Settlement exceeds the trade-in estimate by")}{" "}
                  {money(finance.settlementGap)}
                  {t(
                    ". This gap is added to planned initial cash, not rolled into the new loan.",
                  )}
                </p>
              )}
              {finance.excessEquity > 0 && (
                <p className="own-note">
                  {money(finance.excessEquity)}{" "}
                  {t(
                    "remains above the selected DP. Its treatment requires an agreed transaction; it does not reduce this loan automatically.",
                  )}
                </p>
              )}
              <p className="own-note">
                {t(
                  "OLXmobbi appraisal is a next step, not an instant valuation from these inputs.",
                )}
              </p>
              {onTrade && (
                <button
                  type="button"
                  className="primary"
                  onClick={() => onTrade(input.tradeValue)}
                >
                  {lang === "id"
                    ? "Bawa estimasi ke inspeksi KEY"
                    : "Take estimate to KEY inspection"}
                </button>
              )}
            </details>
            <details className="own-details">
              <summary>
                {t("Compare a KINTO subscription scenario")}
                <ChevronDown size={15} />
              </summary>
              <div className="own-two">
                <NumberField
                  label={t("Monthly subscription quote")}
                  value={input.subscription}
                  max={1e8}
                  onChange={(n) => patch({ subscription: n })}
                />
                <NumberField
                  label={t("Initial subscription fees")}
                  value={input.subscriptionInitial}
                  max={3e8}
                  onChange={(n) => patch({ subscriptionInitial: n })}
                />
              </div>
              <p className="own-note">
                {t(
                  "Enter a quote applicable to this model. KINTO availability, mileage limits, insurance, maintenance and contract length require confirmation. This illustration assumes the entered monthly amount stays constant for 60 months, includes insurance, tax and service, and returns the car with no resale proceeds.",
                )}
              </p>
              {estimate.subscriptionTotal !== null && (
                <p className="own-equity">
                  <span>{t("60-month subscription + energy")}</span>
                  <strong>{money(estimate.subscriptionTotal)}</strong>
                </p>
              )}
              <p className="own-note">
                {t(
                  "No KINTO tariff is prefilled. Charging installation and excess-mileage/damage charges are excluded from this subscription subtotal.",
                )}
              </p>
            </details>
          </div>
          <aside className="own-quote" aria-live="polite">
            <span className="own-kicker">
              {t("ESTIMATED MONTHLY INSTALMENT")}
            </span>
            <strong className="own-monthly">
              {valid ? money(finance.monthly) : t("Enter OTR")}
            </strong>
            <p>
              {input.years * 12} {t("monthly payments ·")} {input.dp}
              {t("% down payment")}
            </p>
            <dl>
              <div>
                <dt>{t("Down payment")}</dt>
                <dd>{valid ? money(finance.downPayment) : "—"}</dd>
              </div>
              <div>
                <dt>{t("Trade-in credit toward DP")}</dt>
                <dd>{money(finance.tradeCredit)}</dd>
              </div>
              <div>
                <dt>{t("Administration")}</dt>
                <dd>{money(input.fees)}</dd>
              </div>
              <div>
                <dt>{t("First-year insurance")}</dt>
                <dd>{valid ? money(finance.firstInsurance) : "—"}</dd>
              </div>
              {finance.settlementGap > 0 && (
                <div>
                  <dt>{t("Old-loan settlement gap")}</dt>
                  <dd>{money(finance.settlementGap)}</dd>
                </div>
              )}
              <div className="own-total">
                <dt>{t("Vehicle initial cash")}</dt>
                <dd>{valid ? money(finance.initialCash) : "—"}</dd>
              </div>
              <div>
                <dt>{t("Total loan repayment")}</dt>
                <dd>{valid ? money(finance.totalRepayment) : "—"}</dd>
              </div>
            </dl>
            <p className="own-note">
              {t(
                "No lender connection. ACC and TAF quotation requests must confirm rate method, eligibility, insurance, fees and payment timing. This result is not an offer or credit approval.",
              )}
            </p>
            <button className="primary" onClick={onVisit}>
              {t("Add simulation to visit brief")}
              <ArrowRight size={16} />
            </button>
          </aside>
        </div>
      )}
      {tab === "cost" && (
        <div className="own-cost-layout">
          <div>
            <div className="own-cost-intro">
              <span className="own-kicker">
                {t("FIVE YEARS ·")}{" "}
                {Math.round(estimate.annualKm * 5).toLocaleString("en-ID")} KM
              </span>
              <h3>
                {valid
                  ? money(estimate.total)
                  : t("Set an OTR in DP & instalments")}
              </h3>
              <p>
                {t(
                  "Estimated ownership cost after resale, including interest. All amounts below are editable planning assumptions.",
                )}
              </p>
            </div>
            <div className="own-breakdown">
              {rows.map(([label, value]) => (
                <div key={label}>
                  <span>{label}</span>
                  <div className="own-bar">
                    <i
                      style={{
                        width: `${estimate.total > 0 ? Math.min(100, (value / estimate.total) * 100) : 0}%`,
                      }}
                    />
                  </div>
                  <strong>{valid ? money(value) : "—"}</strong>
                </div>
              ))}
            </div>
            <div className="own-comparison">
              <h4>{t("Same-price petrol reference")}</h4>
              <div>
                <span>
                  {t("Selected")}
                  {vehicle.powertrain}
                </span>
                <strong>{valid ? money(estimate.total) : "—"}</strong>
              </div>
              <div>
                <span>{t("Petrol scenario · 8 L/100 km")}</span>
                <strong>{valid ? money(estimate.referenceTotal) : "—"}</strong>
              </div>
              <p>
                {t(
                  "Same OTR, resale percentage, insurance, service allowance and financing. Petrol reference uses the full tax allowance and no charger installation. This isolates scenario differences; it does not compare two actual vehicle quotations.",
                )}
              </p>
            </div>
          </div>
          <div className="own-cost-inputs">
            <h3>{t("Adjust five-year assumptions")}</h3>
            <Slider
              label={t("Resale value after five years")}
              value={input.resale}
              min={20}
              max={80}
              unit="% of OTR"
              onChange={(n) => patch({ resale: n })}
            />
            <p className="own-note">
              {t(
                "Residual value is an assumption, not a resale guarantee. A 10-point change moves this result by",
              )}
              {money(input.price * 0.1)}.
            </p>
            <div className="own-two">
              <NumberField
                label={t("Service & wear over five years")}
                value={input.serviceBudget}
                max={3e8}
                onChange={(n) => patch({ serviceBudget: n })}
              />
              <NumberField
                label={t("Annual vehicle-tax allowance")}
                value={input.annualTax}
                max={1e8}
                onChange={(n) => patch({ annualTax: n })}
              />
            </div>
            {ev && (
              <>
                <NumberField
                  label={t("Charging installation allowance")}
                  value={input.installation}
                  max={1e8}
                  onChange={(n) => patch({ installation: n })}
                />
                <Slider
                  label={t("Eligible overnight charging share")}
                  value={input.nightShare}
                  min={0}
                  max={100}
                  unit="%"
                  onChange={(n) => patch({ nightShare: n })}
                />
                <div className="own-two">
                  <NumberField
                    label={t("Years with charging discount")}
                    value={input.discountYears}
                    max={5}
                    step={1}
                    unit="years"
                    onChange={(n) => patch({ discountYears: n })}
                  />
                  <NumberField
                    label={t("Years with PKB exemption")}
                    value={input.taxExemptYears}
                    max={input.region === "Jakarta" ? 5 : 0}
                    step={1}
                    unit="years"
                    onChange={(n) => patch({ taxExemptYears: n })}
                  />
                </div>
                <p className="own-note">
                  30% discount applies only to the selected eligible charging
                  share during 22:00–05:00. Default: no discount. Confirm
                  activation, terms and expiry; extending it across years is
                  your scenario. Jakarta's BEV incentive is not projected
                  forward by default. A future exemption period is your
                  assumption, not a five-year policy guarantee. Bandung tax
                  relief is not assumed.
                </p>
              </>
            )}
            <div className="own-energy-basis">
              {ev ? <PlugZap size={18} /> : <Fuel size={18} />}
              <p>
                <strong>
                  {ev
                    ? "12.13 kWh/100 km + 10% charging overhead"
                    : "5.5 L/100 km · Pertamax RON92"}
                </strong>
                <br />
                {kmWeek}
                {t("km/week ·")}{" "}
                {ev
                  ? `${money(electricityPrice)}/kWh`
                  : `${money(fuelPrice)}/L`}
                {t(
                  ". Change distance and energy prices in the driving-cost test. These are planning assumptions, not measured model efficiency.",
                )}
              </p>
            </div>
            <p className="own-note">
              {t("Insurance uses")}
              {input.insuranceRate}
              {t(
                "% of the initial OTR annually. Service budget includes customer-paid scheduled work after entitlement, wear and exclusions. Loan principal is already represented by depreciation and is not counted again. Time value of money and inflation are excluded.",
              )}
            </p>
          </div>
        </div>
      )}
      {tab === "service" && (
        <div className="own-service-layout">
          <article>
            <ShieldCheck size={25} />
            <h3>{t("Included scheduled service")}</h3>
            <p>
              {t(
                "T-CARE covers eligible scheduled-service labour and parts up to the seventh service, within 3 years or 60,000 km, whichever limit is reached first.",
              )}
            </p>
            <p>
              {t(
                "Confirm the selected model, purchase cohort, service record and covered items. Repairs, wear and optional work are not automatically included.",
              )}
            </p>
            <a
              href="https://aftersales.toyota.astra.co.id/t-care/program-info"
              target="_blank"
              rel="noreferrer"
            >
              {t("Toyota programme terms")}
              <ArrowUpRight size={14} />
            </a>
          </article>
          <article>
            <ShieldCheck size={25} />
            <h3>{t("xEV battery protection")}</h3>
            <p>
              {t(
                "Relevant Toyota hybrid and bZ4X battery programmes provide 8 years or 160,000 km, whichever comes first, subject to model-specific warranty terms.",
              )}
            </p>
            <p>
              {t(
                "Have the advisor confirm coverage for this exact variant. Warranty coverage does not establish battery condition or promise a replacement for normal degradation.",
              )}
            </p>
            <a
              href="https://auto2000.co.id/berita-dan-tips/aftersales-mobil-listrik"
              target="_blank"
              rel="noreferrer"
            >
              {t("Battery-service information")}
              <ArrowUpRight size={14} />
            </a>
          </article>
          {ev ? (
            <article>
              <PlugZap size={25} />
              <h3>{t("Prepare home charging")}</h3>
              <p>
                {t(
                  "Check parking rights, electrical capacity, charger compatibility, cable routing and installation scope before committing.",
                )}
              </p>
              <p>
                {t(
                  "PLN has offered 30% off eligible home charging at 22:00–05:00. Availability, activation and expiry need confirmation. The cost model starts with no charging discount.",
                )}
              </p>
              <a
                href="https://www.pln.co.id/informasi-kendaraan-listrik-id"
                target="_blank"
                rel="noreferrer"
              >
                {t("PLN charging information")}
                <ArrowUpRight size={14} />
              </a>
            </article>
          ) : (
            <article>
              <Fuel size={25} />
              <h3>{t("Hybrid ownership")}</h3>
              <p>
                {t(
                  "An HEV does not need plug-in charging. Its energy calculation uses petrol consumption, not a household electricity tariff.",
                )}
              </p>
              <p>
                {t(
                  "Bring questions about servicing, driving conditions and battery coverage to the branch. Do not use BEV charging assumptions for a hybrid.",
                )}
              </p>
            </article>
          )}
          <article>
            <Wrench size={25} />
            <h3>{t("Plan the first paid service")}</h3>
            <p>
              {t(
                "As the included-service period ends, ask for an itemised scope, customer-paid price and a suitable appointment.",
              )}
            </p>
            <p>
              {t(
                "THS may suit eligible routine work at home. High-voltage diagnosis, equipment needs and repair scope must be checked with the branch.",
              )}
            </p>
            <button onClick={onServiceVisit || onVisit}>
              {t("Discuss service options")}
              <ArrowRight size={14} />
            </button>
          </article>
          {ev && (
            <article className="own-policy">
              <Check size={25} />
              <h3>{t("Jakarta BEV incentives")}</h3>
              <p>
                {t(
                  "Jakarta confirmed PKB/BBNKB incentives and ganjil-genap exemption for battery-electric vehicles on 5 May 2026. This is not a nationwide HEV benefit or a five-year policy guarantee. Other registration charges can still apply.",
                )}
              </p>
              <a
                href="https://www.jakarta.go.id/siaran-pers/6676-SP-HMS-05-2026"
                target="_blank"
                rel="noreferrer"
              >
                {t("Jakarta policy statement")}
                <ArrowUpRight size={14} />
              </a>
            </article>
          )}
        </div>
      )}
    </section>
  );
}
export default function Ownership(props: Props) {
  const { t, lang } = useLocale();

  return (
    <Owner key={`${props.vehicle.id}:${props.vehicle.variant}`} {...props} />
  );
}
