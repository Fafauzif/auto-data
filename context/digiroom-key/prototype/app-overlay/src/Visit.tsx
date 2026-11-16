import RoadBranchMap from "./RoadBranchMap";
import { tasiaDraftUrl, filterBriefForPowertrain } from "./whatsapp";
import { useLocale } from "./locale";
import { useEffect, useMemo, useRef, useState } from "react";
import QRCode from "qrcode";
import LZString from "lz-string";
const { compressToEncodedURIComponent, decompressFromEncodedURIComponent } =
  LZString;
import {
  MapPin,
  Navigation,
  Check,
  Download,
  Copy,
  X,
  ArrowRight,
  Zap,
  CarFront,
  MessageCircle,
  Link2,
} from "lucide-react";
import type { PurchaseVehicle } from "./commerce-types";
import {
  BRANCHES,
  branchList,
  distanceKm,
  demoAvailability,
  CHARGING_SOURCE,
  type Branch,
} from "./branches";
import "./visit.css";

export interface SharedVisit {
  v: 1;
  vehicle: PurchaseVehicle;
  brief: string;
  finance: string;
  branch: string;
  date: string;
  time: string;
  job: string;
}
const clean = (v: unknown, max: number) =>
  typeof v === "string"
    ? v.replace(/[\u0000-\u0008\u000b\u000c\u000e-\u001f]/g, "").slice(0, max)
    : "";
export function compactVisitBrief(brief: string) {
  return brief
    .split("\n")
    .filter((l) =>
      /^(Vehicle|Selected vehicle|Garage|Lateral|Motorcycle|Door envelope|Rear clearance|Passengers|Selected luggage|Stroller|Weekly distance|Fuel per|Pertamax|Electricity per|Public charger|Alternate trip plan|Estimated weekly|•)/i.test(
        l,
      ),
    )
    .join("\n")
    .slice(0, 800);
}
export function encodeVisitHash(payload: SharedVisit) {
  const p = payload;
  const wire = [
    1,
    [
      p.vehicle.id,
      p.vehicle.name,
      p.vehicle.variant,
      p.vehicle.powertrain,
      p.vehicle.otr,
      p.vehicle.region,
      p.vehicle.priceDate,
    ],
    filterBriefForPowertrain(p.brief, p.vehicle.powertrain),
    filterBriefForPowertrain(p.finance, p.vehicle.powertrain),
    p.branch,
    p.date,
    p.time,
    p.job,
  ];
  return "#visit=z." + compressToEncodedURIComponent(JSON.stringify(wire));
}
export function parseSharedVisitHash(hash: string): SharedVisit | null {
  if (!hash.startsWith("#visit=") || hash.length > 9000) return null;
  try {
    let decoded: string | null;
    if (hash.startsWith("#visit=z.")) {
      decoded = decompressFromEncodedURIComponent(hash.slice(9));
    } else {
      const value = hash.slice(7).replace(/-/g, "+").replace(/_/g, "/");
      decoded = new TextDecoder("utf-8", { fatal: true }).decode(
        Uint8Array.from(atob(value), (c) => c.charCodeAt(0)),
      );
    }
    if (!decoded || decoded.length > 10000) return null;
    const raw = JSON.parse(decoded);
    const x =
      Array.isArray(raw) && Array.isArray(raw[1])
        ? {
            v: raw[0],
            vehicle: {
              id: raw[1][0],
              name: raw[1][1],
              variant: raw[1][2],
              powertrain: raw[1][3],
              otr: raw[1][4],
              region: raw[1][5],
              priceDate: raw[1][6],
            },
            brief: raw[2],
            finance: raw[3],
            branch: raw[4],
            date: raw[5],
            time: raw[6],
            job: raw[7],
          }
        : raw;
    if (
      x.v !== 1 ||
      !x.vehicle ||
      !["HEV", "BEV", "PHEV"].includes(x.vehicle.powertrain) ||
      !BRANCHES.some((b) => b.id === x.branch)
    )
      return null;
    const vehicle: PurchaseVehicle = {
      id: clean(x.vehicle.id, 80),
      name: clean(x.vehicle.name, 100),
      variant: clean(x.vehicle.variant, 100),
      powertrain: x.vehicle.powertrain,
      otr:
        typeof x.vehicle.otr === "number" &&
        Number.isFinite(x.vehicle.otr) &&
        x.vehicle.otr >= 0 &&
        x.vehicle.otr <= 2e10
          ? x.vehicle.otr
          : null,
      region: clean(x.vehicle.region, 40),
      priceDate: clean(x.vehicle.priceDate, 50),
      source: "",
    };
    if (!vehicle.name || !vehicle.id) return null;
    return {
      v: 1,
      vehicle,
      brief: clean(x.brief, 800),
      finance: clean(x.finance, 1400),
      branch: x.branch,
      date: /^\d{4}-\d{2}-\d{2}$/.test(x.date) ? x.date : "",
      time: ["10:00", "13:00", "15:00"].includes(x.time) ? x.time : "10:00",
      job: [
        "Test drive",
        "Ownership consultation",
        "Scheduled service / THS enquiry",
      ].includes(x.job)
        ? x.job
        : "Test drive",
    };
  } catch {
    return null;
  }
}
export function isValidVisitDate(date: string, today: string) {
  if (!/^\d{4}-\d{2}-\d{2}$/.test(date) || date < today) return false;
  const d = new Date(date + "T12:00:00Z");
  return Number.isFinite(d.getTime()) && d.toISOString().slice(0, 10) === date;
}
function BranchMap({
  branches,
  selected,
  onSelect,
}: {
  branches: Branch[];
  selected: string;
  onSelect: (id: string) => void;
}) {
  const { t, lang } = useLocale();

  const box =
    branches[0]?.area === "Bandung" &&
    branches.every((b) => b.area === "Bandung")
      ? [107.55, 107.75, -6.97, -6.85]
      : branches.every((b) => b.area === "Jabodetabek")
        ? [106.56, 107.11, -6.35, -6.1]
        : [106.5, 107.8, -7.05, -6.05];
  const point = (lng: number, lat: number) => [
    45 + ((lng - box[0]) / (box[1] - box[0])) * 510,
    290 - ((lat - box[2]) / (box[3] - box[2])) * 240,
  ];
  return (
    <div className="branch-map">
      <svg
        viewBox="0 0 600 340"
        role="group"
        aria-label={t("Auto2000 branch geographic map")}
      >
        <rect width="600" height="340" rx="12" fill="#e9eee7" />
        <path d="M0 22C120 64 180 3 310 20S480 74 600 28V0H0Z" fill="#d1e2e3" />
        {[80, 160, 240].map((y) => (
          <path
            key={y}
            d={`M0 ${y}Q180 ${y - 25} 310 ${y + 15}T600 ${y}`}
            stroke="#d6dfd3"
            fill="none"
            strokeWidth="2"
          />
        ))}
        {[110, 250, 400, 530].map((x) => (
          <path
            key={x}
            d={`M${x} 0Q${x - 45} 160 ${x + 25} 340`}
            stroke="#dde5d8"
            fill="none"
            strokeWidth="2"
          />
        ))}
        <text x="565" y="30" textAnchor="middle" fontSize="11" fill="#617260">
          N ↑
        </text>
        {branches.map((b, i) => {
          const [x, y] = point(b.lng, b.lat);
          return (
            <g
              key={b.id}
              role="button"
              tabIndex={0}
              aria-label={`Select ${b.name} on map`}
              aria-pressed={selected === b.id}
              onClick={() => onSelect(b.id)}
              onKeyDown={(e) => {
                if (e.key === "Enter" || e.key === " ") {
                  e.preventDefault();
                  onSelect(b.id);
                }
              }}
              className="branch-pin"
            >
              <circle
                cx={x}
                cy={y}
                r={selected === b.id ? 18 : 14}
                fill={selected === b.id ? "#cf302b" : "#fff"}
                stroke={selected === b.id ? "#fff" : "#78917b"}
                strokeWidth="2"
              />
              <text
                x={x}
                y={y + 4}
                textAnchor="middle"
                fill={selected === b.id ? "white" : "#405b46"}
                fontSize="11"
                fontWeight="700"
              >
                {i + 1}
              </text>
            </g>
          );
        })}
        <text x="20" y="322" fill="#627263" fontSize="10">
          {t(
            "Geographic branch pins · regional reference map · not navigation",
          )}
        </text>
      </svg>
    </div>
  );
}
export default function Visit({
  vehicle,
  scenarioBrief,
  financeSummary,
  initialPurpose = "Test drive",
  onSaveToKey,
  onClose,
}: {
  vehicle: PurchaseVehicle;
  scenarioBrief: string;
  financeSummary: string;
  initialPurpose?: string;
  onSaveToKey?: (preferred: { branch: string; date: string }) => void;
  onClose: () => void;
}) {
  const { t, lang } = useLocale();

  const shared = useMemo(() => parseSharedVisitHash(window.location.hash), []);
  const current = shared?.vehicle || vehicle;
  const modal = useRef<HTMLDialogElement>(null),
    dateField = useRef<HTMLInputElement>(null);
  const closeRef = useRef(onClose);
  const requestRevision = useRef(0);
  closeRef.current = onClose;
  const [area, setArea] = useState(
    shared ? BRANCHES.find((b) => b.id === shared.branch)!.area : "Jabodetabek",
  );
  const [branchId, setBranchId] = useState(shared?.branch || "cempaka-putih");
  const [origin, setOrigin] = useState<{ lat: number; lng: number }>();
  const [gps, setGps] = useState(""),
    [locating, setLocating] = useState(false);
  const [date, setDate] = useState(shared?.date || ""),
    [time, setTime] = useState(shared?.time || "10:00"),
    [job, setJob] = useState(shared?.job || initialPurpose);
  const [error, setError] = useState(""),
    [prepared, setPrepared] = useState(false),
    [qr, setQr] = useState(""),
    [link, setLink] = useState(""),
    [feedback, setFeedback] = useState(""),
    [preview, setPreview] = useState(false),
    [includeFinance, setIncludeFinance] = useState(
      shared ? shared.finance.length > 0 : true,
    );
  const branch = BRANCHES.find((b) => b.id === branchId) || BRANCHES[0],
    branches = branchList(area, origin);
  const now = new Date(),
    today = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, "0")}-${String(now.getDate()).padStart(2, "0")}`;
  const brief = filterBriefForPowertrain(
      shared ? shared.brief : scenarioBrief,
      current.powertrain,
    ),
    finance = filterBriefForPowertrain(
      shared ? shared.finance : financeSummary,
      current.powertrain,
    );
  const message = `AUTO2000 DIGIROOM — VISIT ENQUIRY\n${current.name} · ${current.variant} · ${current.powertrain}\nBranch: ${branch.name}\nRequest: ${job}\nPreferred: ${date || t("Not selected")} at ${time} WIB\n\n${brief}\n\n${includeFinance ? finance : t("Finance simulation excluded from sharing.")}\n\nEnquiry only. Vehicle and appointment availability require branch confirmation.`;
  useEffect(() => {
    const d = modal.current,
      previous = document.activeElement as HTMLElement | null;
    if (d && !d.open) d.showModal();
    const cancel = (e: Event) => {
      e.preventDefault();
      closeRef.current();
    };
    d?.addEventListener("cancel", cancel);
    return () => {
      requestRevision.current++;
      d?.removeEventListener("cancel", cancel);
      d?.close();
      previous?.focus();
    };
  }, []);
  const invalidate = () => {
    requestRevision.current++;
    setPrepared(false);
    setPreview(false);
    setQr("");
    setLink("");
    setError("");
    setFeedback("");
  };
  const select = (id: string) => {
    setBranchId(id);
    invalidate();
  };
  const locate = () => {
    if (!navigator.geolocation) {
      setGps(t("Location is unavailable. Choose an area below."));
      return;
    }
    setLocating(true);
    setGps(t("Requesting location permission…"));
    navigator.geolocation.getCurrentPosition(
      (p) => {
        const pos = { lat: p.coords.latitude, lng: p.coords.longitude };
        setOrigin(pos);
        const near = branchList("All areas", pos)[0];
        setArea(near.area);
        setBranchId(near.id);
        invalidate();
        setGps(
          t(
            "Branches sorted by straight-line distance. Your coordinates stay in this session.",
          ),
        );
        setLocating(false);
      },
      () => {
        setGps(
          t(
            "Location was not available. Select Jabodetabek or Bandung manually.",
          ),
        );
        setLocating(false);
      },
      { timeout: 10000, maximumAge: 300000, enableHighAccuracy: false },
    );
  };
  const prepare = async () => {
    const revision = ++requestRevision.current;
    if (!isValidVisitDate(date, today)) {
      setError(t("Choose today or a future date for your preferred visit."));
      dateField.current?.focus();
      return;
    }
    setError("");
    const payload: SharedVisit = {
      v: 1,
      vehicle: { ...current, source: "" },
      brief: compactVisitBrief(brief) || brief.slice(0, 800),
      finance: includeFinance ? finance.slice(0, 1400) : "",
      branch: branchId,
      date,
      time,
      job,
    };
    const url =
      window.location.origin +
      window.location.pathname +
      encodeVisitHash(payload);
    setLink(url);
    setPrepared(true);
    setFeedback(t("Visit brief prepared. Nothing has been sent to a branch."));
    try {
      const dataUrl = await QRCode.toDataURL(url, {
        width: 320,
        margin: 4,
        errorCorrectionLevel: "L",
        color: { dark: "#253b2a", light: "#ffffff" },
      });
      if (requestRevision.current === revision) setQr(dataUrl);
    } catch {
      if (requestRevision.current !== revision) return;
      setQr("");
      setFeedback(
        t(
          "Brief prepared. The full link is available below; QR could not be generated.",
        ),
      );
    }
  };
  const copy = async (text: string) => {
    try {
      await navigator.clipboard.writeText(text);
      setFeedback(t("Copied. No message has been sent."));
    } catch {
      setFeedback(
        t("Copy is unavailable. Select the message or download your brief."),
      );
    }
  };
  const download = () => {
    const blob = new Blob(
        [t(message) + (link ? "\n\nShared brief: " + link : "")],
        { type: "text/plain;charset=utf-8" },
      ),
      url = URL.createObjectURL(blob),
      a = document.createElement("a");
    a.href = url;
    a.download = "Auto2000-Visit-Brief.txt";
    a.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
    setFeedback(t("Brief downloaded. No appointment has been sent."));
  };
  return (
    <dialog
      ref={modal}
      className="branch-dialog"
      aria-labelledby="branch-visit-title"
    >
      <div className="branch-dialog-head">
        <div>
          <span className="eyebrow">{t("BRANCH & VISIT")}</span>
          <h2 id="branch-visit-title">
            {t("Choose a branch. Prepare your test drive.")}
          </h2>
        </div>
        <button
          className="visit-icon"
          aria-label={t("Close visit brief")}
          onClick={onClose}
        >
          <X size={20} />
        </button>
      </div>
      <p className="branch-intro">
        {shared
          ? t(
              "Shared visit brief. Review the saved choices before arranging a visit.",
            )
          : t(
              "Take your vehicle choice, practical checks and purchase simulation into one branch conversation.",
            )}
      </p>
      <div className="visit-vehicle">
        <CarFront size={27} />
        <div>
          <strong>{current.name}</strong>
          <span>
            {current.variant} · {current.powertrain}
          </span>
        </div>
        <span className="demo-tag">{t("Demonstration")}</span>
      </div>
      <div className="branch-grid">
        <section aria-labelledby="branch-selection">
          <div className="branch-select-heading">
            <h3 id="branch-selection">{t("1. Select a branch")}</h3>
            <button onClick={locate} disabled={locating}>
              <Navigation size={14} />
              {locating ? t("Locating…") : t("Use my location")}
            </button>
          </div>
          <p className="gps-status" role="status">
            {t(gps) ||
              t(
                "Optional GPS, or select an area. Six sourced locations; sample demonstrator allocations.",
              )}
          </p>
          <label className="visit-field">
            {t("Area")}
            <select
              value={area}
              onChange={(e) => {
                const next = e.target.value as "Jabodetabek" | "Bandung";
                setArea(next);
                select(branchList(next, origin)[0].id);
              }}
            >
              <option>Jabodetabek</option>
              <option>Bandung</option>
            </select>
          </label>
          <RoadBranchMap
            branches={branches}
            selected={branchId}
            onSelect={select}
            fallback={
              <BranchMap
                branches={branches}
                selected={branchId}
                onSelect={select}
              />
            }
          />
          <div className="branch-list">
            {branches.map((b, i) => (
              <button
                key={b.id}
                className={`branch-option ${branchId === b.id ? "selected" : ""}`}
                aria-pressed={branchId === b.id}
                onClick={() => select(b.id)}
              >
                <span className="branch-number">{i + 1}</span>
                <span>
                  <strong>{b.name}</strong>
                  <small>{b.address}</small>
                  <span className="branch-badge">
                    {t(demoAvailability(b, current.powertrain))}
                  </span>
                </span>
                {origin && (
                  <small className="branch-distance">
                    {distanceKm(origin, b).toFixed(1)} km
                    <br />
                    {t("straight line")}
                  </small>
                )}
                {branchId === b.id && <Check size={17} />}
              </button>
            ))}
          </div>
          <div className="branch-facilities">
            <p>
              <Zap size={15} />
              <span>
                {branch.charging === "listed"
                  ? t(
                      "Charging station listed by Toyota. Access, connector and operation require confirmation.",
                    )
                  : t(
                      "Branch charging not verified. Ask the branch before planning a charging stop.",
                    )}
              </span>
            </p>
            <p>
              <MapPin size={15} />
              <span>
                {t(
                  "THS enquiry: scheduled maintenance scope and service area require branch confirmation. High-voltage repair is not assumed to be a home-service job.",
                )}
              </span>
            </p>
            <a href={branch.source} target="_blank" rel="noreferrer">
              {t("Official branch details ↗")}
            </a>
            {branch.charging === "listed" && (
              <a href={CHARGING_SOURCE} target="_blank" rel="noreferrer">
                {t("Toyota charging directory ↗")}
              </a>
            )}
          </div>
        </section>
        <section
          className="visit-preparation"
          aria-labelledby="visit-preparation-title"
        >
          <h3 id="visit-preparation-title">{t("2. Prepare the request")}</h3>
          <label className="visit-field">
            {t("Visit purpose")}
            <select
              value={job}
              onChange={(e) => {
                setJob(e.target.value);
                invalidate();
              }}
            >
              <option value="Test drive">{t("Test drive")}</option>
              <option value="Ownership consultation">
                {t("Ownership consultation")}
              </option>
              <option value="Scheduled service / THS enquiry">
                {t("Scheduled service / THS enquiry")}
              </option>
            </select>
          </label>
          <div className="visit-date-grid">
            <label className="visit-field">
              {t("Preferred day")}
              <input
                ref={dateField}
                type="date"
                min={today}
                value={date}
                aria-invalid={!!error}
                aria-describedby={error ? "visit-date-error" : undefined}
                onChange={(e) => {
                  setDate(e.target.value);
                  invalidate();
                }}
              />
            </label>
            <label className="visit-field">
              {t("Preferred time")}
              <select
                value={time}
                onChange={(e) => {
                  setTime(e.target.value);
                  invalidate();
                }}
              >
                <option value="10:00">10:00 WIB</option>
                <option value="13:00">13:00 WIB</option>
                <option value="15:00">15:00 WIB</option>
              </select>
            </label>
          </div>
          {error && (
            <p id="visit-date-error" role="alert" className="visit-error">
              {t(error)}
            </p>
          )}
          <div className="visit-brief-preview">
            <h4>{t("Checks to bring")}</h4>
            <pre>
              {t(compactVisitBrief(brief)) ||
                t(
                  "Vehicle introduction, passenger access and an explanation of the selected powertrain.",
                )}
            </pre>
          </div>
          <label className="visit-finance-check">
            <input
              type="checkbox"
              checked={includeFinance}
              onChange={(e) => {
                setIncludeFinance(e.target.checked);
                invalidate();
              }}
            />
            {t("Include my purchase simulation in the shared brief")}
          </label>
          {includeFinance && (
            <details className="visit-finance-preview">
              <summary>{t("Review purchase simulation")}</summary>
              <pre>
                {t(finance) ||
                  t(
                    "No purchase simulation yet. Ask the advisor for a model-specific quotation.",
                  )}
              </pre>
            </details>
          )}
          <p className="visit-demo-note">
            {t(
              "Preferred times are awaiting branch confirmation. The QR and copied message carry your visit brief.",
            )}
          </p>
          <button className="primary visit-prepare" onClick={prepare}>
            {prepared ? t("Update visit brief") : t("Generate visit brief")}
            <ArrowRight size={17} />
          </button>
          {prepared && (
            <div className="visit-share">
              <div className="visit-share-heading">
                <Check size={19} />
                <strong>{t("Visit brief ready to share")}</strong>
              </div>
              {qr && (
                <img
                  src={qr}
                  width="320"
                  height="320"
                  alt={t("QR code opening this saved visit brief")}
                />
              )}
              <p>
                {t(
                  "Scan to reopen the saved vehicle, branch and checks. Anyone with the link can read its contents. Exact GPS coordinates are excluded.",
                )}
              </p>
              <div className="visit-share-actions">
                {onSaveToKey && !shared && job === "Test drive" && (
                  <button
                    onClick={() => onSaveToKey({ branch: branch.name, date })}
                  >
                    <ArrowRight size={15} />
                    {lang === "id"
                      ? "Bawa ke Tes Keseharian KEY"
                      : "Continue in KEY Life Test"}
                  </button>
                )}
                <button onClick={() => copy(link)}>
                  <Link2 size={15} />
                  {t("Copy brief link")}
                </button>
                <button onClick={download}>
                  <Download size={15} />
                  {t("Download brief")}
                </button>
                <a
                  className="tasia-send"
                  href={tasiaDraftUrl(t(message) + (link ? "\n\n" + link : ""))}
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  <MessageCircle size={15} />
                  {lang === "id"
                    ? "Kirim Ringkasan ke WhatsApp Auto2000 (Tasia)"
                    : "Send Brief to Auto2000 WhatsApp (Tasia)"}
                </a>
                <button
                  onClick={() => setPreview((v) => !v)}
                  aria-expanded={preview}
                >
                  <MessageCircle size={15} />
                  {t("Preview WhatsApp handoff")}
                </button>
              </div>
              <p className="tasia-note">
                {lang === "id"
                  ? "Tasia resmi: 0822-8980-2000. Tombol membuka draf WhatsApp; periksa isinya dan kirim sendiri. Belum ada janji temu yang dikonfirmasi."
                  : "Official Tasia: 0822-8980-2000. The button opens a WhatsApp draft; review it and send it yourself. No appointment is confirmed."}
              </p>
              <label className="visit-field visit-share-link">
                {t("Shareable brief link")}
                <input
                  readOnly
                  value={link}
                  onFocus={(e) => e.currentTarget.select()}
                />
              </label>
              {preview && (
                <div className="whatsapp-preview">
                  <h4>{t("WhatsApp message preview")}</h4>
                  <p>
                    {lang === "id"
                      ? "Draf ditujukan ke Tasia resmi. Periksa pesan, lalu kirim sendiri melalui WhatsApp."
                      : "Draft addressed to official Tasia. Review the message, then send it yourself in WhatsApp."}
                  </p>
                  <pre>{t(message)}</pre>
                  <button onClick={() => copy(t(message))}>
                    <Copy size={15} />
                    {t("Copy message")}
                  </button>
                </div>
              )}
            </div>
          )}
          <p className="visit-feedback" role="status">
            {t(feedback)}
          </p>
        </section>
      </div>
    </dialog>
  );
}
