import type { Brief } from "./key/state";
import { LocaleProvider, translateText } from "./locale";
import {
  lazy,
  Suspense,
  useEffect,
  useRef,
  useState,
  Component,
  type ReactNode,
  type CSSProperties,
} from "react";
import {
  ArrowUpRight,
  ArrowRight,
  Check,
  ChevronDown,
  CarFront,
  Box,
  Users,
  Zap,
  RotateCcw,
  Plus,
  Bookmark,
  X,
  CheckCircle2,
  Layers,
  Info,
  DoorOpen,
  Loader2,
} from "lucide-react";
import {
  DEFAULT_SCENARIO,
  type Scenario,
  type CarId,
  type Mode,
  type Language,
  type Quality,
} from "./types";
import {
  CARS,
  garageResult,
  familyResult,
  energyResult,
  validateScenario,
  createBriefText,
  suggestMode,
} from "./domain";
import Catalogue from "./Catalogue";
import Ownership from "./Ownership";
import Visit from "./Visit";
import { HERO_VEHICLES, resolveVehicle } from "./catalogue-data";
import type { PurchaseVehicle } from "./commerce-types";
import "./revision.css";
const CONCERNS: Record<string, string> = {
  "Check my parking, door and tailgate clearance.":
    "Periksa ruang parkir, pintu, dan bagasi saya.",
  "Try passenger access and my luggage in the actual car.":
    "Coba akses penumpang dan barang saya pada mobil asli.",
  "Explain hybrid operation during my test drive.":
    "Jelaskan pengoperasian hybrid saat test drive.",
  "Discuss charging access and installation costs.":
    "Bahas akses pengisian dan biaya instalasi.",
};
const Scene = lazy(() => import("./Scene"));
const STORAGE = "digiroom-life-test-v2";
function load() {
  try {
    const modern = localStorage.getItem(STORAGE);
    const v = JSON.parse(
      modern || localStorage.getItem("digiroom-life-test-v1") || "null",
    );
    const scenario = validateScenario(v?.scenario);
    if (!modern && scenario.fuelPrice === 13000) scenario.fuelPrice = 15950;
    return {
      scenario,
      language:
        (localStorage.getItem("digiroom-language-v3") || v?.language) === "id"
          ? ("id" as const)
          : ("en" as const),
      purchase: resolveVehicle(v?.purchase?.id, v?.purchase?.variant),
      concerns: Array.isArray(v?.concerns)
        ? (v.concerns
            .filter((s: unknown) => typeof s === "string")
            .slice(0, 8) as string[])
        : [],
    };
  } catch {
    return {
      purchase: null,
      scenario: { ...DEFAULT_SCENARIO },
      language: "en" as const,
      concerns: [] as string[],
    };
  }
}
class SceneBoundary extends Component<
  { children: ReactNode; onError: () => void },
  { failed: boolean }
> {
  state = { failed: false };
  static getDerivedStateFromError() {
    return { failed: true };
  }
  componentDidCatch() {
    this.props.onError();
  }
  render() {
    return this.state.failed ? null : this.props.children;
  }
}
function RangeField({
  label,
  value,
  min,
  max,
  step = 1,
  unit,
  onChange,
}: {
  label: string;
  value: number;
  min: number;
  max: number;
  step?: number;
  unit: string;
  onChange: (v: number) => void;
}) {
  return (
    <label className="range-field">
      <span className="field-line">
        <span>{label}</span>
        <span className="number-wrap">
          <input
            aria-label={label}
            type="number"
            min={min}
            max={max}
            step={step}
            value={value}
            onChange={(e) => {
              if (e.target.value !== "")
                onChange(Math.min(max, Math.max(min, Number(e.target.value))));
            }}
          />
          <span>{unit}</span>
        </span>
      </span>
      <input
        aria-label={`${label} slider`}
        type="range"
        min={min}
        max={max}
        step={step}
        value={value}
        onChange={(e) => onChange(+e.target.value)}
      />
    </label>
  );
}
function Toggle({
  label,
  checked,
  onChange,
}: {
  label: string;
  checked: boolean;
  onChange: () => void;
}) {
  return (
    <button className="toggle-row" aria-pressed={checked} onClick={onChange}>
      <span>{label}</span>
      <span className={"switch " + (checked ? "on" : "")}>
        <span />
      </span>
    </button>
  );
}
function PlanView({
  s,
  t,
}: {
  s: Scenario;
  t: (a: string, b: string) => string;
}) {
  const c = CARS[s.car],
    g = garageResult(s),
    isGarage = s.mode === "garage",
    w = isGarage ? s.garageWidth : 6,
    d = isGarage ? s.garageDepth : 7;
  return (
    <div className="plan-view">
      <svg
        viewBox="0 0 700 550"
        role="img"
        aria-label={t("Overhead vehicle plan", "Denah kendaraan dari atas")}
      >
        <defs>
          <pattern
            id="tiles"
            width="35"
            height="35"
            patternUnits="userSpaceOnUse"
          >
            <path
              d="M35 0H0V35"
              fill="none"
              stroke="#d9ded8"
              strokeWidth=".6"
            />
          </pattern>
        </defs>
        <rect width="700" height="550" fill="#e8ede8" />
        <rect
          x="65"
          y="40"
          width="570"
          height="465"
          rx="8"
          fill="url(#tiles)"
        />
        <g transform="translate(350,280)">
          <rect
            x={-w * 30}
            y={-d * 30}
            width={w * 60}
            height={d * 60}
            fill="#fafbf9"
            stroke="#8b978d"
            strokeWidth="8"
          />
          <g transform={`translate(${isGarage ? s.offset * 60 : 0},0)`}>
            <rect
              x={-c.width * 30}
              y={-c.length * 30}
              width={c.width * 60}
              height={c.length * 60}
              rx="25"
              fill={s.paint}
              stroke="#4f5b55"
              strokeWidth="2"
            />
            <rect
              x={-c.width * 24}
              y={-c.length * 19}
              width={c.width * 48}
              height={c.length * 10}
              rx="9"
              fill="#354d58"
            />
            <rect
              x={-c.width * 24}
              y={c.length * 14}
              width={c.width * 48}
              height={c.length * 9}
              rx="8"
              fill="#354d58"
            />
            {s.doorOpen && (
              <path
                d={`M${-c.width * 30} -65l-39 32v53l39 -10`}
                fill="#cf302b"
                opacity=".65"
              />
            )}
            {s.tailgateOpen && (
              <rect
                x={-c.width * 30}
                y={c.length * 30}
                width={c.width * 60}
                height="42"
                fill="#cf302b"
                opacity=".3"
              />
            )}
            {s.mode === "family" && (
              <g>
                {Array.from({ length: familyResult(s).seatsAvailable }).map(
                  (_, i) => (
                    <rect
                      key={i}
                      x={i % 2 === 0 ? -38 : 10}
                      y={-75 + Math.floor(i / 2) * 43}
                      width="28"
                      height="30"
                      rx="8"
                      fill={i < s.passengers ? "#a47b60" : "#d8ded2"}
                      stroke="#ffffff"
                    />
                  ),
                )}
                {Array.from({
                  length: Math.min(
                    s.luggage,
                    Math.max(
                      0,
                      familyResult(s).luggageCapacity - (s.stroller ? 2 : 0),
                    ),
                  ),
                }).map((_, i) => (
                  <rect
                    key={i}
                    x={-35 + (i % 3) * 25}
                    y={85 + Math.floor(i / 3) * 20}
                    width="20"
                    height="17"
                    rx="3"
                    fill="#b19c76"
                  />
                ))}
                {s.stroller && (
                  <rect
                    x="-33"
                    y="110"
                    width="56"
                    height="18"
                    rx="4"
                    fill="#90a38c"
                  />
                )}
              </g>
            )}
            {s.mode === "family" && s.childSeat && (
              <g data-testid="child-seat-2d">
                <rect
                  x="-55"
                  y="-52"
                  width="110"
                  height="32"
                  rx="7"
                  fill="#243b50"
                />
                <text
                  x="0"
                  y="-31"
                  textAnchor="middle"
                  fill="white"
                  fontSize="12"
                >
                  {t("Child seat · Row 2", "Kursi anak · Baris 2")}
                </text>
              </g>
            )}
            {s.mode === "energy" && (
              <g>
                <rect
                  x="-26"
                  y="0"
                  width="52"
                  height="58"
                  rx="4"
                  fill="#6e9f8e"
                />
                <text
                  x="0"
                  y="35"
                  textAnchor="middle"
                  fill="white"
                  fontSize="10"
                >
                  {s.car === "zenix" ? "HEV" : "BEV"}
                </text>
              </g>
            )}
            <text
              x="0"
              y={s.mode === "family" ? -113 : 8}
              textAnchor="middle"
              fill="#fff"
              fontSize="13"
            >
              {s.car === "zenix" ? "ZENIX" : "bZ4X"}
            </text>
          </g>
          {s.obstacle && isGarage && (
            <rect
              x={-w * 30 + 5}
              y="-65"
              width="33"
              height="108"
              rx="12"
              fill="#56675c"
            />
          )}
        </g>
        {s.mode === "energy" && (
          <g>
            {[0, 1, 2].map((n) => (
              <g key={n}>
                <circle
                  cx={180 + n * 170}
                  cy="70"
                  r="20"
                  fill={n === s.energyStep ? "#476a52" : "#bac7b9"}
                />
                <text
                  x={180 + n * 170}
                  y="75"
                  textAnchor="middle"
                  fill="white"
                  fontSize="14"
                >
                  {n + 1}
                </text>
              </g>
            ))}
            <text
              x="350"
              y="490"
              textAnchor="middle"
              fill="#4d6655"
              fontSize="13"
            >
              {s.kmWeek} km / {t("week", "minggu")} ·{" "}
              {s.car === "zenix"
                ? t("Hybrid illustration", "Ilustrasi hybrid")
                : s.homeCharging
                  ? t("Home charging", "Pengisian rumah")
                  : t("Public charging", "Pengisian umum")}
            </text>
          </g>
        )}
        <text x="350" y="28" textAnchor="middle" fill="#4f5b55" fontSize="14">
          {isGarage
            ? `${w.toFixed(2)} m × ${d.toFixed(2)} m`
            : t("Your selected vehicle", "Kendaraan pilihan Anda")}
        </text>
        <text
          x="350"
          y="535"
          textAnchor="middle"
          fill={g.fits ? "#365f43" : "#aa302b"}
          fontSize="14"
        >
          {t(
            "Use the controls to change your test",
            "Gunakan kontrol untuk mengubah tes",
          )}
        </text>
      </svg>
      <span className="plan-label">
        {t("2D planning view", "Tampilan denah 2D")}
      </span>
    </div>
  );
}
type KeyNavigation = {
  garage: boolean;
  trade: boolean;
  language: Language;
  onLanguage: (language: Language) => void;
  onBack: () => void;
  onBrief: (brief: Brief, preferred?: { branch: string; date: string }) => void;
  onTrade: (marketTrade: number) => void;
};
export default function App({
  keyNavigation,
}: { keyNavigation?: KeyNavigation } = {}) {
  const initial = useRef(load());
  const [s, setS] = useState<Scenario>(() =>
      keyNavigation?.garage
        ? { ...initial.current.scenario, mode: "garage" }
        : initial.current.scenario,
    ),
    [lang, setLang] = useState<Language>(
      keyNavigation?.language ?? initial.current.language,
    ),
    [concerns, setConcerns] = useState<string[]>(initial.current.concerns),
    [quality, setQuality] = useState<Quality>("standard"),
    [flat, setFlat] = useState(false),
    [sceneError, setSceneError] = useState(false),
    [reset, setReset] = useState(0),
    [status, setStatus] = useState(""),
    [question, setQuestion] = useState(""),
    [assisted, setAssisted] = useState(false),
    [saved, setSaved] = useState(false),
    [reduced, setReduced] = useState(
      () => matchMedia("(prefers-reduced-motion: reduce)").matches,
    ),
    [stats, setStats] = useState({ fps: 0, drawCalls: 0, triangles: 0 });
  const [view, setView] = useState<"studio" | "catalogue" | "ownership">(() =>
    keyNavigation?.trade ||
    (!keyNavigation?.garage &&
      initial.current.purchase &&
      initial.current.purchase.heroCar !== initial.current.scenario.car)
      ? "ownership"
      : "studio",
  );
  const [purchase, setPurchase] = useState<PurchaseVehicle>(
    () =>
      (keyNavigation?.garage ? undefined : initial.current.purchase) ||
      HERO_VEHICLES[initial.current.scenario.car],
  );
  const financeKey = JSON.stringify([
    purchase.id,
    purchase.variant,
    s.kmWeek,
    s.fuelPrice,
    s.electricityPrice,
    s.homeCharging,
    s.publicChargePrice,
    s.publicChargeShare,
  ]);
  const [financeSnapshot, setFinanceSnapshot] = useState({ key: "", text: "" });
  const financeSummary =
    financeSnapshot.key === financeKey
      ? financeSnapshot.text
      : "Purchase simulation not current. Reopen Purchase & ownership to refresh it before sharing.";
  const setFinanceSummary = (text: string) =>
    setFinanceSnapshot({ key: financeKey, text });
  const enterStudio = () => {
    if (purchase.heroCar !== s.car) setPurchase(HERO_VEHICLES[s.car]);
    setView("studio");
  };
  const [visitOpen, setVisitOpen] = useState(() =>
    location.hash.startsWith("#visit="),
  );
  const [sceneAttempt, setSceneAttempt] = useState(0);
  const chooseLanguage = (value: Language) => {
    setLang(value);
    keyNavigation?.onLanguage(value);
  };
  const sendKeyBrief = (preferred?: { branch: string; date: string }) => {
    if (!keyNavigation) return;
    const fits = purchase.heroCar === s.car;
    const checks = concerns.map(displayConcern);
    if (fits) {
      checks.push(
        t(
          `Garage ${s.garageWidth.toFixed(2)} × ${s.garageDepth.toFixed(2)} m: check driver door and tailgate. Approximate rear clearance ${g.rearClearance.toFixed(2)} m.`,
          `Garasi ${s.garageWidth.toFixed(2)} × ${s.garageDepth.toFixed(2)} m: periksa pintu pengemudi dan bagasi. Perkiraan jarak di belakang ${g.rearClearance.toFixed(2)} m.`,
        ),
      );
      checks.push(
        t(
          `Try ${s.passengers} passengers and ${s.luggage} luggage items${s.childSeat ? " with the child seat fitted" : ""}.`,
          `Coba ${s.passengers} penumpang dan ${s.luggage} barang${s.childSeat ? " dengan kursi anak terpasang" : ""}.`,
        ),
      );
      if (s.car === "bz4x") {
        checks.push(
          t("Home charging", "Pengisian di rumah") +
            ": " +
            (s.homeCharging
              ? t("Available", "Tersedia")
              : t("Unavailable", "Tidak tersedia")),
        );
        if (s.publicCharger.trim())
          checks.push(
            t("Public charging", "Pengisian publik") +
              ": " +
              s.publicCharger.trim(),
          );
        if (s.backupTrip.trim())
          checks.push(
            t("Alternate trip plan", "Rencana perjalanan alternatif") +
              ": " +
              s.backupTrip.trim(),
          );
      }
    } else {
      checks.push(
        t(
          "Check parking access, seating and baggage on the exact variant.",
          "Periksa akses parkir, kursi, dan bagasi pada varian yang dipilih.",
        ),
      );
      if (purchase.powertrain === "PHEV")
        checks.push(
          t(
            "Check home charging and fuel use on an unplugged trip.",
            "Periksa pengisian rumah dan penggunaan bahan bakar saat perjalanan tanpa mengisi daya.",
          ),
        );
    }
    const planning = fits
      ? s.car === "zenix"
        ? t(
            `${s.kmWeek} km/week · Pertamax ${money(s.fuelPrice)}/L · assumed 5.5 L/100 km · estimated ${money(energy.weeklyCost)}/week`,
            `${s.kmWeek} km/minggu · Pertamax ${money(s.fuelPrice)}/L · asumsi 5,5 L/100 km · perkiraan ${money(energy.weeklyCost)}/minggu`,
          )
        : t(
            `${s.kmWeek} km/week · ${money(energy.averageChargePrice)}/kWh (${Math.round(energy.publicShare * 100)}% public) · assumed 12.13 kWh/100 km + 10% charging overhead · estimated ${money(energy.weeklyCost)}/week`,
            `${s.kmWeek} km/minggu · ${money(energy.averageChargePrice)}/kWh (${Math.round(energy.publicShare * 100)}% publik) · asumsi 12,13 kWh/100 km + 10% pengisian · perkiraan ${money(energy.weeklyCost)}/minggu`,
          )
      : t(
          "Plan energy costs in Purchase & ownership for the selected powertrain.",
          "Rencanakan biaya energi di Pembelian & Kepemilikan untuk jenis penggerak pilihan.",
        );
    save();
    keyNavigation.onBrief(
      {
        model: purchase.name,
        variant: purchase.variant,
        powertrain: purchase.powertrain,
        referencePrice: purchase.otr ?? undefined,
        checks,
        planning,
      },
      preferred,
    );
  };
  useEffect(() => {
    document.title =
      view === "catalogue"
        ? "Toyota xEV Models | Digiroom"
        : view === "ownership"
          ? `${purchase.name} Ownership | Digiroom`
          : "Toyota xEV Showroom | Digiroom";
  }, [view, purchase.name]);
  const choosePurchase = (v: PurchaseVehicle) => {
    if (v.heroCar) selectCar(v.heroCar);
    setPurchase(v);
    setFinanceSummary("Finance simulation not yet opened.");
    setView("ownership");
    window.scrollTo?.({ top: 0, behavior: "instant" });
  };
  const [visitPurpose, setVisitPurpose] = useState("Test drive");
  const openVisit = () => {
    setVisitPurpose(
      view === "ownership" ? "Ownership consultation" : "Test drive",
    );
    setVisitOpen(true);
  };
  const openServiceVisit = () => {
    setVisitPurpose("Scheduled service / THS enquiry");
    setVisitOpen(true);
  };
  const tx = (text: string) => translateText(text, lang);
  const t = (en: string, id: string) => (lang === "en" ? en : id),
    car = CARS[s.car],
    g = garageResult(s),
    f = familyResult(s),
    energy = energyResult(s);
  const money = (n: number) =>
    new Intl.NumberFormat(lang === "en" ? "en-ID" : "id-ID", {
      style: "currency",
      currency: "IDR",
      maximumFractionDigits: 0,
    }).format(n);
  const patch = (v: Partial<Scenario>) => {
    setS((prev) => validateScenario({ ...prev, ...v }));
    setSaved(false);
  };
  useEffect(() => {
    document.documentElement.lang = lang;
    try {
      localStorage.setItem("digiroom-language-v3", lang);
    } catch {
      /* Main saved-state effect reports unavailable storage. */
    }
    const timer = setTimeout(() => {
      try {
        localStorage.setItem(
          STORAGE,
          JSON.stringify({
            scenario: s,
            language: lang,
            concerns,
            purchase: { id: purchase.id, variant: purchase.variant },
          }),
        );
      } catch {
        setStatus(
          t(
            "Browser storage is unavailable. Download your brief to keep a copy.",
            "Penyimpanan tidak tersedia. Unduh ringkasan untuk menyimpannya.",
          ),
        );
      }
    }, 300);
    return () => clearTimeout(timer);
  }, [s, lang, concerns, purchase]);
  useEffect(() => {
    const m = matchMedia("(prefers-reduced-motion: reduce)"),
      cb = () => setReduced(m.matches);
    m.addEventListener("change", cb);
    return () => m.removeEventListener("change", cb);
  }, []);
  useEffect(() => {
    if (!status) return;
    const n = setTimeout(() => setStatus(""), 4500);
    return () => clearTimeout(n);
  }, [status]);
  const modeLabel = (m: Mode) =>
    ({
      showroom: t("Showroom", "Showroom"),
      garage: t("Your garage", "Garasi Anda"),
      family: t("Your family", "Keluarga Anda"),
      energy: t("Your week", "Rutinitas Anda"),
    })[m];
  const changeMode = (mode: Mode) => {
    patch({ mode });
    setReset((x) => x + 1);
  };
  const selectCar = (id: CarId) => {
    patch({ car: id, doorOpen: false, tailgateOpen: false, folded: false });
    setPurchase(HERO_VEHICLES[id]);
    setFinanceSummary("Finance simulation not yet opened.");
    setReset((x) => x + 1);
  };
  const displayConcern = (c: string) =>
    lang === "id"
      ? CONCERNS[c] || c
      : Object.entries(CONCERNS).find(([, id]) => id === c)?.[0] || c;
  const addConcern = (text: string) => {
    text = Object.entries(CONCERNS).find(([, id]) => id === text)?.[0] || text;
    setConcerns((prev) =>
      prev.includes(text) ? prev : [...prev, text].slice(-8),
    );
    setStatus(
      t("Added to your visit brief.", "Ditambahkan ke ringkasan kunjungan."),
    );
  };
  const save = () => {
    try {
      localStorage.setItem(
        STORAGE,
        JSON.stringify({
          scenario: s,
          language: lang,
          concerns,
          purchase: { id: purchase.id, variant: purchase.variant },
        }),
      );
      setSaved(true);
      setStatus(t("Saved on this browser.", "Disimpan di peramban ini."));
    } catch {
      setStatus(
        t(
          "Cannot save here. Download your brief instead.",
          "Tidak dapat menyimpan. Unduh ringkasan kunjungan.",
        ),
      );
    }
  };
  const icons = { showroom: CarFront, garage: Box, family: Users, energy: Zap };
  return (
    <LocaleProvider language={lang}>
      <>
        <header className="masthead">
          <a
            className="brand"
            href="#showroom"
            onClick={(e) => {
              e.preventDefault();
              enterStudio();
              changeMode("showroom");
            }}
            aria-label="Auto2000 Digiroom showroom"
          >
            <span className="brand-word">
              AUTO<span>2000</span>
            </span>
            <span className="brand-divider" />
            <span className="digiroom">
              digiroom<span>xEV Showroom</span>
            </span>
          </a>
          <div className="header-right">
            <span className="private-note">
              {t(
                "Your choices, kept on your device",
                "Pilihan tersimpan di perangkat Anda",
              )}
            </span>
            <div className="language-switch" aria-label="Language / Bahasa">
              <button
                aria-pressed={lang === "en"}
                onClick={() => chooseLanguage("en")}
              >
                EN
              </button>
              <button
                aria-pressed={lang === "id"}
                onClick={() => chooseLanguage("id")}
              >
                Indonesia
              </button>
            </div>
            <button
              className="save-button"
              aria-label={saved ? t("Saved", "Tersimpan") : t("Save", "Simpan")}
              onClick={save}
            >
              <Bookmark size={15} fill={saved ? "currentColor" : "none"} />
              <span>
                {saved ? t("Saved", "Tersimpan") : t("Save", "Simpan")}
              </span>
            </button>
          </div>
        </header>
        {keyNavigation && (
          <div className="key-studio-bar">
            <button type="button" onClick={keyNavigation.onBack}>
              ← {t("Back to Digiroom KEY", "Kembali ke Digiroom KEY")}
            </button>
            <button type="button" onClick={() => sendKeyBrief()}>
              {t("Save visit card to KEY", "Simpan kartu kunjungan ke KEY")}{" "}
              <ArrowUpRight size={15} />
            </button>
          </div>
        )}
        <nav className="journey-nav" aria-label={tx("Shopping journey")}>
          <div>
            <button
              className={view === "studio" ? "active" : ""}
              onClick={enterStudio}
            >
              {tx("Interactive showroom")}
            </button>
            <button
              className={view === "catalogue" ? "active" : ""}
              onClick={() => setView("catalogue")}
            >
              {tx("Explore all xEV")}
            </button>
            <button
              className={view === "ownership" ? "active" : ""}
              onClick={() => setView("ownership")}
            >
              {tx("Purchase & ownership")}
            </button>
          </div>
          <button className="journey-visit" onClick={openVisit}>
            {tx("Branch & visit")}
            <ArrowUpRight size={15} />
          </button>
        </nav>
        {view === "catalogue" && (
          <Catalogue
            selectedId={purchase.id}
            onChoose={choosePurchase}
            onClose={enterStudio}
          />
        )}
        {view === "ownership" && (
          <section className="ownership-shell">
            <div className="ownership-context">
              <button
                className="text-action"
                onClick={() => setView("catalogue")}
              >
                {tx("Change model")}
                <ArrowRight size={15} />
              </button>
              <p>
                {tx("Selected vehicle")} · {purchase.name} · {purchase.variant}
              </p>
            </div>
            <Ownership
              key={purchase.id + purchase.variant}
              vehicle={purchase}
              kmWeek={s.kmWeek}
              fuelPrice={s.fuelPrice}
              electricityPrice={
                s.car === "bz4x" && purchase.powertrain === "BEV"
                  ? energy.averageChargePrice
                  : s.electricityPrice
              }
              onSummaryChange={setFinanceSummary}
              onVisit={openVisit}
              onServiceVisit={openServiceVisit}
              onTrade={keyNavigation?.onTrade}
            />
          </section>
        )}
        <main className="workspace" hidden={view !== "studio"}>
          <div className="workspace-heading">
            <div className="breadcrumb">
              <span>DIGIROOM</span>
              <span>/</span>
              <span>
                {t(
                  "Compare vehicles. Check fit. Plan your purchase.",
                  "Kenali keseharian bersama Toyota",
                )}
              </span>
            </div>
            <nav
              className="modes"
              aria-label={t("Explore a scenario", "Jelajahi skenario")}
            >
              {(["showroom", "garage", "family", "energy"] as Mode[]).map(
                (m) => {
                  const Icon = icons[m];
                  return (
                    <button
                      key={m}
                      className={s.mode === m ? "active" : ""}
                      aria-current={s.mode === m ? "page" : undefined}
                      onClick={() => changeMode(m)}
                    >
                      <Icon size={16} />
                      {modeLabel(m)}
                    </button>
                  );
                },
              )}
            </nav>
          </div>
          <div className="experience">
            <section
              className="task-panel"
              aria-labelledby="task-title"
              key={s.mode}
            >
              <div className="eyebrow">
                <span className="short-line" />
                {s.mode === "showroom"
                  ? t("THE SHOWROOM", "SHOWROOM")
                  : t("LIFE TEST", "TES KESEHARIAN")}
              </div>
              <h1 id="task-title">
                {s.mode === "showroom"
                  ? t(
                      "Explore Toyota\nHybrid & Electric",
                      "Kenali Toyota\npilihan Anda.",
                    )
                  : s.mode === "garage"
                    ? t(
                        "Check your\ngarage clearance",
                        "Ruang untuk\nkeseharian.",
                      )
                    : s.mode === "family"
                      ? t(
                          "Configure seats\nand luggage",
                          "Ajak semua.\nBeserta barangnya.",
                        )
                      : t(
                          "Estimate your\ndriving costs",
                          "Rutinitas dengan\ncara berbeda.",
                        )}
              </h1>
              <p className="intro">
                {s.mode === "showroom"
                  ? t(
                      "Explore two vehicles in 3D. Check parking space, passenger needs and running costs before a branch visit.",
                      "Lihat lebih dekat. Buka pintunya. Coba kesesuaiannya dengan garasi, keluarga, dan rutinitas Anda.",
                    )
                  : s.mode === "garage"
                    ? t(
                        "A car can fit inside and still leave you little room to get out. Try your space.",
                        "Mobil bisa muat, tetapi ruang untuk keluar belum tentu cukup. Coba ruang Anda.",
                      )
                    : s.mode === "family"
                      ? t(
                          "Seats and luggage share the same space. Try the arrangement you actually travel with.",
                          "Kursi dan bagasi berbagi ruang. Coba susunan perjalanan Anda.",
                        )
                      : t(
                          "Explore the powertrain. Change your driving and energy assumptions to see the estimate.",
                          "Kenali penggeraknya. Ubah asumsi perjalanan dan energi untuk melihat estimasi.",
                        )}
              </p>
              {s.mode === "showroom" && (
                <>
                  <div className="selected-name">
                    <span className="powertrain">
                      {car.powertrain === "HEV"
                        ? "HYBRID ELECTRIC"
                        : "BATTERY ELECTRIC"}
                    </span>
                    <h2>{car.name}</h2>
                    <p>
                      {s.car === "zenix"
                        ? t(
                            "Seven-seat hybrid MPV. No plug-in charging required.",
                            "Fleksibilitas tujuh kursi dengan tenaga hybrid.",
                          )
                        : t(
                            "Five-seat battery-electric SUV. Plan home or public charging.",
                            "Lima kursi bertenaga listrik. Cara baru merencanakan rutinitas.",
                          )}
                    </p>
                  </div>
                  <div className="spec-strip">
                    <div>
                      <strong>
                        {car.length.toFixed(2)}
                        <small>m</small>
                      </strong>
                      <span>{t("Length", "Panjang")}</span>
                    </div>
                    <div>
                      <strong>
                        {car.width.toFixed(2)}
                        <small>m</small>
                      </strong>
                      <span>{t("Width", "Lebar")}</span>
                    </div>
                    <div>
                      <strong>{car.seats}</strong>
                      <span>{t("Seats", "Kursi")}</span>
                    </div>
                  </div>
                  <div className="paint-label">
                    {t("Exterior colour", "Warna eksterior")}
                    <span>
                      {s.paint === "#b1b7b8"
                        ? t("Silver", "Perak")
                        : s.paint === "#f0eeea"
                          ? t("Pearl white", "Putih mutiara")
                          : t("Graphite", "Grafit")}
                    </span>
                  </div>
                  <div className="swatches">
                    {["#b1b7b8", "#f0eeea", "#364442"].map((c) => (
                      <button
                        aria-label={
                          c === "#b1b7b8"
                            ? t("Silver", "Perak")
                            : c === "#f0eeea"
                              ? t("Pearl white", "Putih mutiara")
                              : t("Graphite", "Grafit")
                        }
                        aria-pressed={s.paint === c}
                        key={c}
                        style={{ "--paint": c } as CSSProperties}
                        onClick={() => patch({ paint: c })}
                      >
                        {s.paint === c && <Check size={17} />}
                      </button>
                    ))}
                  </div>
                  <div className="quick-controls">
                    <Toggle
                      label={t("Open driver's door", "Buka pintu pengemudi")}
                      checked={s.doorOpen}
                      onChange={() => patch({ doorOpen: !s.doorOpen })}
                    />
                    <Toggle
                      label={t("Open tailgate", "Buka bagasi")}
                      checked={s.tailgateOpen}
                      onChange={() => patch({ tailgateOpen: !s.tailgateOpen })}
                    />
                  </div>
                  <button
                    className="primary wide"
                    onClick={() => changeMode("garage")}
                  >
                    {t("Try it in your garage", "Coba di garasi Anda")}
                    <ArrowRight size={17} />
                  </button>
                </>
              )}
              {s.mode === "garage" && (
                <>
                  <div className="controls-block">
                    <RangeField
                      label={t("Garage width", "Lebar garasi")}
                      value={s.garageWidth}
                      min={2.2}
                      max={5}
                      step={0.05}
                      unit="m"
                      onChange={(v) => patch({ garageWidth: v })}
                    />
                    <RangeField
                      label={t("Garage depth", "Panjang garasi")}
                      value={s.garageDepth}
                      min={4}
                      max={8}
                      step={0.1}
                      unit="m"
                      onChange={(v) => patch({ garageDepth: v })}
                    />
                    <RangeField
                      label={t("Parking position", "Posisi parkir")}
                      value={s.offset}
                      min={-0.5}
                      max={0.5}
                      step={0.05}
                      unit="m"
                      onChange={(v) => patch({ offset: v })}
                    />
                  </div>
                  <Toggle
                    label={t("Open driver’s door", "Buka pintu pengemudi")}
                    checked={s.doorOpen}
                    onChange={() => patch({ doorOpen: !s.doorOpen })}
                  />
                  <Toggle
                    label={t("Open tailgate", "Buka bagasi")}
                    checked={s.tailgateOpen}
                    onChange={() => patch({ tailgateOpen: !s.tailgateOpen })}
                  />
                  <Toggle
                    label={t(
                      "Park a motorcycle beside it",
                      "Parkir motor di samping",
                    )}
                    checked={s.obstacle}
                    onChange={() => patch({ obstacle: !s.obstacle })}
                  />
                  <div
                    className={
                      "result " +
                      (g.fits &&
                      g.doorFits &&
                      g.tailgateFits &&
                      !g.obstacleConflict
                        ? "good"
                        : "caution")
                    }
                  >
                    <Info size={17} />
                    <div>
                      <strong>
                        {!g.fits
                          ? t(
                              "The footprint needs more room.",
                              "Ukuran mobil membutuhkan ruang lebih.",
                            )
                          : !g.doorFits
                            ? t(
                                "It fits. The door needs more space.",
                                "Mobil muat. Pintu perlu ruang lebih.",
                              )
                            : !g.tailgateFits
                              ? t(
                                  "The tailgate needs more room.",
                                  "Bagasi perlu ruang lebih.",
                                )
                              : g.obstacleConflict
                                ? t(
                                    "The motorcycle overlaps the car.",
                                    "Motor bertumpuk dengan mobil.",
                                  )
                                : t(
                                    "Body, door and tailgate clear this layout.",
                                    "Ada ruang pada susunan ini.",
                                  )}
                      </strong>
                      <p>
                        {t("Side space", "Ruang samping")}:{" "}
                        {(g.sideClearance * 100).toFixed(0)} cm ·{" "}
                        {t("Rear space", "Ruang belakang")}:{" "}
                        {(g.rearClearance * 100).toFixed(0)} cm
                      </p>
                      <ul className="clearance-checks">
                        <li>
                          Vehicle body: {g.fits ? "fits" : "needs more room"}
                        </li>
                        <li>
                          {t(
                            "Driver-door envelope:",
                            "Ruang bukaan pintu pengemudi:",
                          )}{" "}
                          {g.doorFits
                            ? t("clear", "cukup")
                            : t("restricted", "terbatas")}
                        </li>
                        <li>
                          {t("Tailgate envelope:", "Ruang bukaan bagasi:")}{" "}
                          {g.tailgateFits
                            ? t("clear", "cukup")
                            : t("restricted", "terbatas")}
                        </li>
                      </ul>
                    </div>
                  </div>
                  <button
                    className="text-action"
                    onClick={() =>
                      addConcern(
                        t(
                          "Check my parking, door and tailgate clearance.",
                          "Periksa ruang parkir, pintu, dan bagasi saya.",
                        ),
                      )
                    }
                  >
                    {t("Add a clearance check", "Tambahkan pemeriksaan ruang")}
                    <Plus size={16} />
                  </button>
                </>
              )}
              {s.mode === "family" && (
                <>
                  <div className="controls-block">
                    <RangeField
                      label={t("People travelling", "Jumlah penumpang")}
                      value={s.passengers}
                      min={1}
                      max={7}
                      unit={t("people", "orang")}
                      onChange={(v) => patch({ passengers: v })}
                    />
                    <RangeField
                      label={t("Large bags", "Tas besar")}
                      value={s.luggage}
                      min={0}
                      max={6}
                      unit={t("bags", "tas")}
                      onChange={(v) => patch({ luggage: v })}
                    />
                  </div>
                  <Toggle
                    label={
                      s.car === "zenix"
                        ? t("Fold the third row", "Lipat baris ketiga")
                        : t(
                            "Fold part of the rear bench",
                            "Lipat sebagian kursi belakang",
                          )
                    }
                    checked={s.folded}
                    onChange={() => patch({ folded: !s.folded })}
                  />
                  <Toggle
                    label={t(
                      "Bring a folded stroller",
                      "Bawa stroller terlipat",
                    )}
                    checked={s.stroller}
                    onChange={() => patch({ stroller: !s.stroller })}
                  />
                  <Toggle
                    label={t("Include a child seat", "Sertakan kursi anak")}
                    checked={s.childSeat}
                    onChange={() => patch({ childSeat: !s.childSeat })}
                  />
                  <Toggle
                    label={t("Open the tailgate", "Buka bagasi")}
                    checked={s.tailgateOpen}
                    onChange={() => patch({ tailgateOpen: !s.tailgateOpen })}
                  />
                  <div
                    className={
                      "result " +
                      (f.passengerFits && f.luggageFits ? "good" : "caution")
                    }
                  >
                    <Users size={18} />
                    <div>
                      <strong>
                        {!f.passengerFits
                          ? t(
                              "This arrangement has too few seats.",
                              "Kursi pada susunan ini tidak cukup.",
                            )
                          : !f.luggageFits
                            ? t(
                                "Your bags need another arrangement.",
                                "Barang Anda perlu susunan lain.",
                              )
                            : t(
                                "This arrangement works in the illustration.",
                                "Susunan ini sesuai dalam ilustrasi.",
                              )}
                      </strong>
                      <p>
                        {f.seatsAvailable}{" "}
                        {t("seats available", "kursi tersedia")} ·{" "}
                        {t("Illustrated capacity", "Kapasitas ilustrasi")}:{" "}
                        {f.luggageCapacity} {t("large bags", "tas besar")}
                      </p>
                    </div>
                  </div>
                  <p className="small-note">
                    {t(
                      "Bring your stroller or child seat to check the exact fit and access at the branch.",
                      "Bawa stroller atau kursi anak Anda untuk memeriksa kesesuaian di cabang.",
                    )}
                  </p>
                  <button
                    className="text-action"
                    onClick={() =>
                      addConcern(
                        t(
                          "Try passenger access and my luggage in the actual car.",
                          "Coba akses penumpang dan barang saya pada mobil asli.",
                        ),
                      )
                    }
                  >
                    {t(
                      "Add a family demonstration",
                      "Tambahkan demonstrasi keluarga",
                    )}
                    <Plus size={16} />
                  </button>
                </>
              )}
              {s.mode === "energy" && (
                <>
                  <div className="energy-selector">
                    <span>
                      {s.car === "zenix"
                        ? t(
                            "A hybrid traffic illustration",
                            "Ilustrasi hybrid di lalu lintas",
                          )
                        : t(
                            "An electric driving week",
                            "Rutinitas berkendara listrik",
                          )}
                    </span>
                    <div className="step-buttons">
                      {[0, 1, 2].map((n) => (
                        <button
                          key={n}
                          className={s.energyStep === n ? "active" : ""}
                          aria-label={`${t("Scene", "Adegan")} ${n + 1}`}
                          onClick={() => patch({ energyStep: n })}
                        >
                          {n + 1}
                        </button>
                      ))}
                    </div>
                    <p>
                      {s.car === "zenix"
                        ? [
                            t(
                              "Pull away: the motor can help at low speed.",
                              "Mulai bergerak: motor dapat membantu pada kecepatan rendah.",
                            ),
                            t(
                              "Accelerate: the engine and motor can work together.",
                              "Akselerasi: mesin dan motor dapat bekerja bersama.",
                            ),
                            t(
                              "Slow down: regenerative braking can recover energy.",
                              "Melambat: pengereman regeneratif dapat memulihkan energi.",
                            ),
                          ][s.energyStep]
                        : [
                            t(
                              "Start your week with a charging plan.",
                              "Awali minggu dengan rencana pengisian.",
                            ),
                            t(
                              "Include your commute and everyday trips.",
                              "Sertakan perjalanan rutin dan harian.",
                            ),
                            t(
                              "Leave room for a longer weekend journey.",
                              "Siapkan perjalanan akhir pekan yang lebih jauh.",
                            ),
                          ][s.energyStep]}
                    </p>
                  </div>
                  <RangeField
                    label={t("Weekly driving", "Jarak per minggu")}
                    value={s.kmWeek}
                    min={50}
                    max={1000}
                    step={10}
                    unit="km"
                    onChange={(v) => patch({ kmWeek: v })}
                  />
                  {s.car === "bz4x" && (
                    <Toggle
                      label={t(
                        "I can charge at home",
                        "Saya bisa mengisi di rumah",
                      )}
                      checked={s.homeCharging}
                      onChange={() => patch({ homeCharging: !s.homeCharging })}
                    />
                  )}
                  {s.car === "bz4x" && (
                    <details className="assumptions">
                      <summary>
                        {t(
                          "Plan charging for a regular trip",
                          "Rencanakan pengisian untuk perjalanan rutin",
                        )}
                        <ChevronDown size={14} />
                      </summary>
                      <div className="key-studio-charging">
                        <label>
                          {t(
                            "Usable public charger",
                            "Pengisian publik yang dapat digunakan",
                          )}
                          <input
                            value={s.publicCharger}
                            maxLength={140}
                            onChange={(e) =>
                              patch({ publicCharger: e.target.value })
                            }
                          />
                        </label>
                        <label>
                          {t(
                            "Alternate plan if the usual charger is unavailable",
                            "Rencana bila pengisian biasa tidak tersedia",
                          )}
                          <input
                            value={s.backupTrip}
                            maxLength={140}
                            onChange={(e) =>
                              patch({ backupTrip: e.target.value })
                            }
                          />
                        </label>
                        <RangeField
                          label={t(
                            "Public charging share",
                            "Porsi pengisian publik",
                          )}
                          value={s.publicChargeShare}
                          min={0}
                          max={100}
                          step={5}
                          unit="%"
                          onChange={(v) => patch({ publicChargeShare: v })}
                        />
                        <RangeField
                          label={t(
                            "Public charging price",
                            "Tarif pengisian publik",
                          )}
                          value={s.publicChargePrice}
                          min={1000}
                          max={10000}
                          step={100}
                          unit="Rp/kWh"
                          onChange={(v) => patch({ publicChargePrice: v })}
                        />
                      </div>
                    </details>
                  )}
                  <div className="cost-line">
                    <span>
                      {t(
                        "Estimated weekly energy cost",
                        "Estimasi biaya energi mingguan",
                      )}
                    </span>
                    <strong>{money(energy.weeklyCost)}</strong>
                    <small>
                      {t(
                        "Under the assumptions below",
                        "Dengan asumsi di bawah",
                      )}
                    </small>
                  </div>
                  <div className="energy-basis">
                    <strong>
                      {s.car === "zenix"
                        ? "Pertamax RON92"
                        : "Electricity consumption"}
                    </strong>
                    <span>
                      {s.car === "zenix"
                        ? `${money(s.fuelPrice)}/L · 5.5 L/100 km`
                        : t(
                            "12.13 kWh/100 km + 10% charging overhead",
                            "12,13 kWh/100 km + 10% rugi pengisian",
                          )}
                    </span>
                    <small>
                      {s.car === "zenix"
                        ? s.fuelPrice === 15950
                          ? "Jabodetabek price reference: Rp15,950/L, 9 Nov 2026. Consumption is a planning assumption."
                          : "Your edited planning price. Published reference: Rp15,950/L, 9 Nov 2026. Consumption is a planning assumption."
                        : t(
                            `Planning assumption. Applied charging tariff ${money(energy.averageChargePrice)}/kWh. Adjust it below.`,
                            `Asumsi perencanaan. Tarif gabungan ${money(energy.averageChargePrice)}/kWh. Ubah tarif di bawah.`,
                          )}
                    </small>
                  </div>
                  <button
                    className="primary ownership-link"
                    onClick={() => {
                      setPurchase(HERO_VEHICLES[s.car]);
                      setView("ownership");
                    }}
                  >
                    {tx("Simulate DP & instalments")}
                    <ArrowRight size={16} />
                  </button>
                  <details className="assumptions">
                    <summary>
                      {t("Adjust the assumptions", "Ubah asumsi")}
                      <ChevronDown size={14} />
                    </summary>
                    <RangeField
                      label={t("Petrol price", "Harga bensin")}
                      value={s.fuelPrice}
                      min={9000}
                      max={20000}
                      step={100}
                      unit="Rp/L"
                      onChange={(v) => patch({ fuelPrice: v })}
                    />
                    {s.car === "bz4x" && (
                      <RangeField
                        label={t("Electricity price", "Harga listrik")}
                        value={s.electricityPrice}
                        min={1000}
                        max={4000}
                        step={100}
                        unit="Rp/kWh"
                        onChange={(v) => patch({ electricityPrice: v })}
                      />
                    )}
                    <p>
                      {t(
                        "Planning assumptions: hybrid 5.5 L/100 km; BEV 12.13 kWh/100 km plus 10% charging overhead. Energy cost only. Purchase, installation, service and finance are excluded. Not measured Toyota efficiency figures.",
                        "Asumsi perencanaan: hybrid 5,5 L/100 km; BEV 12,13 kWh/100 km ditambah rugi pengisian 10%. Hanya biaya energi, tidak termasuk pembelian, instalasi, servis, atau kredit. Bukan hasil pengujian Toyota.",
                      )}
                    </p>
                  </details>
                  <button
                    className="text-action"
                    onClick={() =>
                      addConcern(
                        s.car === "zenix"
                          ? t(
                              "Explain hybrid operation during my test drive.",
                              "Jelaskan pengoperasian hybrid saat test drive.",
                            )
                          : t(
                              "Discuss charging access and installation costs.",
                              "Bahas akses pengisian dan biaya instalasi.",
                            ),
                      )
                    }
                  >
                    {t(
                      "Add an ownership question",
                      "Tambahkan pertanyaan kepemilikan",
                    )}
                    <Plus size={16} />
                  </button>
                </>
              )}
              {s.mode !== "showroom" && (
                <details className="method">
                  <summary>
                    {t("About this test", "Tentang tes ini")}
                    <Info size={13} />
                  </summary>
                  <p>
                    {s.mode === "garage"
                      ? t(
                          "Published reference dimensions set vehicle length and width. Door swing (65 cm), tailgate reach (70 cm) and obstacles use authored planning geometry. Garage height and turning paths are not tested. Confirm measurements in person.",
                          "Panjang dan lebar mengikuti dimensi referensi. Bukaan pintu 65 cm, jangkauan bagasi 70 cm, dan rintangan adalah geometri perencanaan. Tidak menguji tinggi garasi atau jalur belok. Periksa langsung.",
                        )
                      : s.mode === "family"
                        ? t(
                            "Take your seating, baggage and child-seat checks to the vehicle.",
                            "Susunan kursi dan kapasitas tas bersifat ilustratif. Keamanan muatan, kenyamanan, dan kursi anak perlu diperiksa langsung.",
                          )
                        : t(
                            "Power-flow scenes explain a principle, not a prediction. Traffic, weather and driving style change consumption. An HEV does not require plug-in charging.",
                            "Adegan aliran tenaga menjelaskan prinsip, bukan prediksi. Lalu lintas, cuaca, dan gaya berkendara memengaruhi konsumsi. HEV tidak membutuhkan pengisian eksternal.",
                          )}
                  </p>
                </details>
              )}
            </section>
            <section
              className="stage-column"
              aria-label={t("Vehicle experience", "Pengalaman kendaraan")}
            >
              <div className="stage">
                <div className="stage-top">
                  <span className="studio-label">
                    <span className="live-dot" />
                    {s.mode === "showroom"
                      ? "Digiroom Studio"
                      : modeLabel(s.mode)}
                    <span className="studio-sub">
                      {t("An interactive showroom", "Showroom interaktif")}
                    </span>
                  </span>
                  <button
                    className="icon-button"
                    aria-label={t("Reset camera", "Atur ulang kamera")}
                    title={t("Reset camera", "Atur ulang kamera")}
                    onClick={() => setReset((x) => x + 1)}
                  >
                    <RotateCcw size={16} />
                  </button>
                </div>
                {flat || sceneError ? (
                  <PlanView s={s} t={t} />
                ) : (
                  <SceneBoundary
                    key={sceneAttempt}
                    onError={() => setSceneError(true)}
                  >
                    <Suspense
                      fallback={
                        <div className="scene-loading">
                          <Loader2 className="spin" size={26} />
                          <span>
                            {t("Preparing the showroom", "Menyiapkan showroom")}
                          </span>
                        </div>
                      }
                    >
                      {view === "studio" && (
                        <Scene
                          language={lang}
                          scenario={s}
                          quality={quality}
                          reducedMotion={reduced}
                          resetKey={reset}
                          onSelectCar={selectCar}
                          onError={() => setSceneError(true)}
                          onStats={setStats}
                        />
                      )}
                    </Suspense>
                  </SceneBoundary>
                )}
                {sceneError && (
                  <div className="scene-recovery" role="status">
                    {t(
                      "3D is unavailable in this browser. Your controls still work in the 2D plan.",
                      "Tampilan 3D tidak tersedia di peramban ini. Kontrol tetap berfungsi pada denah 2D.",
                    )}
                    <button
                      onClick={() => {
                        setSceneError(false);
                        setFlat(false);
                        setQuality("lite");
                        setSceneAttempt((x) => x + 1);
                      }}
                    >
                      {t("Retry 3D in Lite", "Coba kembali 3D Ringan")}
                    </button>
                  </div>
                )}
                <div className="stage-bottom">
                  <span className="camera-hint">
                    {flat || sceneError
                      ? t(
                          "Adjust your test with the controls",
                          "Atur tes melalui kontrol",
                        )
                      : t(
                          "Drag to orbit · Scroll to look closer",
                          "Geser untuk memutar · Gulir untuk mendekat",
                        )}
                  </span>
                  <div className="stage-tools">
                    <button
                      onClick={() => {
                        if (flat || sceneError) {
                          setFlat(false);
                          setSceneError(false);
                          setSceneAttempt((x) => x + 1);
                        } else setFlat(true);
                      }}
                      aria-pressed={flat || sceneError}
                      className="view-button"
                    >
                      <Layers size={14} />
                      {flat || sceneError
                        ? t("3D view", "Tampilan 3D")
                        : t("2D plan", "Denah 2D")}
                    </button>
                    <label className="quality-label">
                      <select
                        aria-label={t("Graphics quality", "Kualitas grafis")}
                        value={quality}
                        onChange={(e) => setQuality(e.target.value as Quality)}
                      >
                        <option value="lite">{t("Lite", "Ringan")}</option>
                        <option value="standard">
                          {t("Standard", "Standar")}
                        </option>
                        <option value="high">{t("High", "Tinggi")}</option>
                      </select>
                    </label>
                  </div>
                </div>
              </div>
              <div
                className="vehicle-picker"
                aria-label={t("Choose your Toyota", "Pilih Toyota Anda")}
              >
                {(["zenix", "bz4x"] as CarId[]).map((id) => (
                  <button
                    key={id}
                    onClick={() => selectCar(id)}
                    className={
                      "vehicle-option " + (s.car === id ? "selected" : "")
                    }
                    aria-pressed={s.car === id}
                  >
                    <span className="car-line-art">
                      <CarFront size={29} strokeWidth={1} />
                    </span>
                    <span className="vehicle-option-text">
                      <strong>{CARS[id].name}</strong>
                      <span>
                        {CARS[id].powertrain === "HEV"
                          ? t(
                              "Hybrid electric · 7 seats",
                              "Hybrid electric · 7 kursi",
                            )
                          : t(
                              "Battery electric · 5 seats",
                              "Battery electric · 5 kursi",
                            )}
                      </span>
                    </span>
                    <span className="select-circle">
                      {s.car === id ? (
                        <Check size={13} />
                      ) : (
                        <ArrowUpRight size={15} />
                      )}
                    </span>
                  </button>
                ))}
              </div>
              <div className="product-links">
                <button
                  onClick={() => {
                    setPurchase(HERO_VEHICLES[s.car]);
                    setView("catalogue");
                  }}
                >
                  {tx("Product details")}
                  <ArrowUpRight size={15} />
                </button>
                <button onClick={() => setView("catalogue")}>
                  {tx("View all Toyota xEV models")}
                  <ArrowRight size={15} />
                </button>
              </div>
              <form
                className="question-bar"
                noValidate
                onSubmit={(e) => {
                  e.preventDefault();
                  if (!question.trim()) return;
                  changeMode(suggestMode(question));
                  setAssisted(true);
                }}
              >
                <span className="question-mark">?</span>
                <label className="sr-only" htmlFor="question">
                  {t(
                    "What would you like to try?",
                    "Apa yang ingin Anda coba?",
                  )}
                </label>
                <input
                  id="question"
                  value={question}
                  onChange={(e) => {
                    setQuestion(e.target.value);
                    setAssisted(false);
                  }}
                  placeholder={t(
                    "Try “a narrow garage” or “six people and bags”",
                    "Coba “garasi sempit” atau “enam orang dan tas”",
                  )}
                />
                {question && (
                  <button
                    type="button"
                    aria-label={t("Clear question", "Hapus pertanyaan")}
                    onClick={() => {
                      setQuestion("");
                      setAssisted(false);
                    }}
                  >
                    <X size={15} />
                  </button>
                )}
                <button
                  type="submit"
                  aria-label={t(
                    "Open suggested test",
                    "Buka tes yang disarankan",
                  )}
                >
                  <ArrowRight size={18} />
                </button>
              </form>
              {assisted && (
                <p className="assist-result" role="status">
                  {s.mode === "showroom"
                    ? t(
                        "Choose a test above: garage, family or weekly driving.",
                        "Pilih tes di atas: garasi, keluarga, atau perjalanan mingguan.",
                      )
                    : t(
                        `Opened ${modeLabel(s.mode).toLowerCase()}. Adjust the controls to match your situation.`,
                        `Tes ${modeLabel(s.mode).toLowerCase()} dibuka. Sesuaikan kontrol dengan kondisi Anda.`,
                      )}
                </p>
              )}
            </section>
          </div>
          <footer className="visit-footer">
            <div className="footer-copy">
              <span className="footer-symbol">
                <DoorOpen size={23} strokeWidth={1.5} />
              </span>
              <div>
                <strong>
                  {t(
                    "Request a test drive with your vehicle checks.",
                    "Bawa pertanyaan Anda ke mobil aslinya.",
                  )}
                </strong>
                <p>
                  {concerns.length
                    ? t(
                        `${concerns.length} ${concerns.length === 1 ? "check" : "checks"} in your visit brief.`,
                        `${concerns.length} pemeriksaan dalam ringkasan Anda.`,
                      )
                    : t(
                        "Choose a branch and carry your requirements into the visit brief.",
                        "Simpan kebutuhan Anda. Siapkan hal yang ingin Anda coba.",
                      )}
                </p>
              </div>
            </div>
            <button className="primary" onClick={openVisit}>
              {t("Prepare my visit", "Siapkan kunjungan")}
              <ArrowUpRight size={18} />
            </button>
          </footer>
          {new URLSearchParams(location.search).has("inspect") && (
            <output className="diagnostics">
              RAF {stats.fps.toFixed(0)} fps · {stats.drawCalls} calls ·{" "}
              {stats.triangles} tris
            </output>
          )}
        </main>
        <div className="toast" role="status" aria-live="polite">
          {status && (
            <>
              <CheckCircle2 size={16} />
              {status}
            </>
          )}
        </div>
        {visitOpen && (
          <Visit
            initialPurpose={visitPurpose}
            vehicle={purchase}
            scenarioBrief={
              purchase.heroCar === s.car
                ? createBriefText(s, "en", concerns)
                : `Selected vehicle: ${purchase.name} ${purchase.variant}. Garage and seating checks have not been performed for this model. Interactive 3D checks are available for Zenix and bZ4X.`
            }
            financeSummary={financeSummary}
            onSaveToKey={keyNavigation ? sendKeyBrief : undefined}
            onClose={() => {
              setVisitOpen(false);
              if (location.hash.startsWith("#visit="))
                history.replaceState(
                  null,
                  "",
                  location.pathname + location.search,
                );
            }}
          />
        )}
      </>
    </LocaleProvider>
  );
}
