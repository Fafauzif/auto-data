import { lazy, Suspense, useEffect, useRef, useState } from "react";
import {
  ArrowRight,
  ArrowUpRight,
  CarFront,
  ChevronDown,
  ClipboardList,
  KeyRound,
  MapPin,
  RotateCcw,
  Wrench,
} from "lucide-react";
import type { Language } from "../types";
import { DriveRecord, DriveRequest, driveStatus } from "./DriveFlow";
import {
  EMPTY,
  KEY_STORAGE,
  readKey,
  responsible,
  transition,
  type Brief,
  type Journey,
  type Role,
} from "./state";
import {
  ActionButton,
  errorLabels,
  journeyNames,
  KeyLanguage,
  Panel,
  roles,
  useKey,
  type Send,
  type Text,
} from "./ui";
import "./key.css";
const Studio = lazy(() => import("../App"));
const ServiceView = lazy(() => import("./pages/ServicePage"));
const UpgradeView = lazy(() => import("./pages/UpgradePage"));
const keyRoles = ["customer", "sales", "workshop", "upgrade"] as const;
const roleJourney = { sales: "K", workshop: "E", upgrade: "Y" } as const;
const journeyRole = { K: "sales", E: "workshop", Y: "upgrade" } as const;
const icon = { K: CarFront, E: Wrench, Y: KeyRound };
const accounts = {
  customer: "Nadia & Arif",
  sales: "Raka · Bandung",
  workshop: "Dewi · Workshop",
  upgrade: "Dimas · Bandung",
};
function currentPage(hash: string) {
  return hash.slice(1).toLowerCase();
}
function language(): Language {
  try {
    return localStorage.getItem("digiroom-language-v3") === "id" ? "id" : "en";
  } catch {
    return "en";
  }
}
function readDraft(): {
  brief?: Brief;
  preferred?: { branch: string; date: string };
  marketTrade?: number;
} {
  try {
    return JSON.parse(sessionStorage.getItem("digiroom-key-draft") || "{}");
  } catch {
    return {};
  }
}
export default function KeyApp() {
  const [lang, setLang] = useState(language);
  const [hash, setHash] = useState(() => location.hash);
  const [state, setState] = useState(readKey);
  const [draft, setDraft] = useState(readDraft);
  const [error, setError] = useState("");
  const dialog = useRef<HTMLDialogElement>(null);
  const top = useRef<HTMLElement>(null);
  const previousHash = useRef(hash);
  const page = currentPage(hash);
  const studio =
    page.startsWith("studio") ||
    page.startsWith("visit=") ||
    new URLSearchParams(location.search).has("inspect");
  const payer = hash.match(/^#payer=(KEY-E-[A-Z0-9]+):(\d+)$/);
  const role: Role =
    page === "sales" || page === "workshop" || page === "upgrade"
      ? page
      : "customer";
  const routeJourney: Journey | undefined =
    page === "k"
      ? "K"
      : page === "e" || payer
        ? "E"
        : page === "y"
          ? "Y"
          : undefined;
  const journey = role === "customer" ? routeJourney : roleJourney[role];
  const t: Text = (en, id) => (lang === "id" ? id : en);
  const names = journeyNames(t);
  const labels = roles(t);
  const go = (route: string) => {
    if (location.hash !== route) location.hash = route;
    setHash(route);
    setError("");
    window.scrollTo(0, 0);
  };
  useEffect(() => {
    const follow = () => {
      setHash(location.hash);
      setError("");
    };
    const sync = (event: StorageEvent) => {
      if (event.key === KEY_STORAGE || event.key === null) setState(readKey());
    };
    addEventListener("hashchange", follow);
    addEventListener("storage", sync);
    return () => {
      removeEventListener("hashchange", follow);
      removeEventListener("storage", sync);
    };
  }, []);
  useEffect(() => {
    if (previousHash.current !== hash && !studio)
      top.current?.focus({ preventScroll: true });
    previousHash.current = hash;
  }, [hash, studio]);
  useEffect(() => {
    document.documentElement.lang = lang;
  }, [lang]);
  useEffect(() => {
    if (!studio) document.title = "Digiroom KEY | Auto2000";
  }, [studio]);
  const changeLanguage = (value: Language) => {
    setLang(value);
    try {
      localStorage.setItem("digiroom-language-v3", value);
    } catch {
      /* Language remains available in this session. */
    }
  };
  const saveDraft = (data: ReturnType<typeof readDraft>) => {
    setDraft(data);
    try {
      sessionStorage.setItem("digiroom-key-draft", JSON.stringify(data));
    } catch {
      /* Draft remains in memory. */
    }
  };
  const persist = (data: typeof state) => {
    setState(data);
    try {
      localStorage.setItem(KEY_STORAGE, JSON.stringify(data));
      setError("");
    } catch {
      setError(
        t(
          "Browser storage is unavailable. Changes last until this page closes.",
          "Penyimpanan peramban tidak tersedia. Perubahan bertahan sampai halaman ditutup.",
        ),
      );
    }
  };
  const send: Send = (action, actor) => {
    const result = transition(state, actor ?? role, action);
    if ("error" in result) {
      setError(errorLabels(t)[result.error]);
      return false;
    }
    persist(result.state);
    if (actor === "payer") go("#e");
    return true;
  };
  const backToKey = () => go("#k");
  const openStudio = () => go("#studio/garage");
  const journeyLink = (item: Journey) => "#" + item.toLowerCase();
  const record =
    journey === "K"
      ? state.drive
      : journey === "E"
        ? state.service
        : journey === "Y"
          ? state.upgrade
          : undefined;
  const queueOwner = journey && responsible(journey, state);
  const emptyName = {
    K: t("No drive requests yet", "Belum ada permintaan uji"),
    E: t("No service requests yet", "Belum ada permintaan servis"),
    Y: t("No upgrade requests yet", "Belum ada permintaan tukar tambah"),
  };
  const stateName =
    journey === "K" && state.drive
      ? driveStatus(t)[state.drive.stage]
      : undefined;
  if (studio)
    return (
      <Suspense
        fallback={
          <p className="key-loading">
            {t("Opening Life Test studio…", "Membuka studio Tes Keseharian…")}
          </p>
        }
      >
        <Studio
          key={page}
          keyNavigation={{
            garage: page === "studio/garage",
            trade: page === "studio/ownership",
            language: lang,
            onLanguage: changeLanguage,
            onBack: backToKey,
            onBrief: (brief, preferred) => {
              saveDraft({ ...draft, brief, preferred });
              backToKey();
            },
            onTrade: (marketTrade) => {
              saveDraft({ ...draft, marketTrade });
              go("#y");
            },
          }}
        />
      </Suspense>
    );
  return (
    <KeyLanguage.Provider value={lang}>
      <div className="key-app">
        <a
          className="key-skip"
          href="#key-main"
          onClick={(event) => {
            event.preventDefault();
            top.current?.focus();
          }}
        >
          {t("Skip to content", "Lewati ke isi")}
        </a>
        <header className="key-header">
          <div className="key-bound key-header-inner">
            <a
              className="key-brand"
              href={role === "customer" ? "#home" : "#" + role}
              aria-label="Auto2000 Digiroom KEY"
            >
              <span className="key-brand-auto">
                AUTO<span>2000</span>
              </span>
              <span className="key-brand-title">
                digiroom<span>KEY</span>
              </span>
            </a>
            <div className="key-header-controls">
              <div
                className="key-language"
                aria-label={t("Language", "Bahasa")}
              >
                <button
                  onClick={() => changeLanguage("en")}
                  aria-pressed={lang === "en"}
                >
                  EN
                </button>
                <button
                  onClick={() => changeLanguage("id")}
                  aria-pressed={lang === "id"}
                >
                  ID
                </button>
              </div>
              <label className="key-role">
                <span className="key-role-avatar">
                  {accounts[role].slice(0, 1)}
                </span>
                <span className="key-role-name">
                  <small>{t("WORKSPACE", "RUANG KERJA")}</small>
                  <span>{labels[role]}</span>
                </span>
                <ChevronDown size={15} aria-hidden="true" />
                <select
                  aria-label={t("Switch workspace", "Ganti ruang kerja")}
                  value={role}
                  onChange={(event) => {
                    const value = event.target.value as Role;
                    go(
                      value === "customer"
                        ? journey
                          ? journeyLink(journey)
                          : "#home"
                        : "#" + value,
                    );
                  }}
                >
                  {keyRoles.map((item) => (
                    <option key={item} value={item}>
                      {labels[item]} · {accounts[item]}
                    </option>
                  ))}
                </select>
              </label>
            </div>
          </div>
        </header>
        <nav
          className="key-nav"
          aria-label={t("Digiroom KEY navigation", "Navigasi Digiroom KEY")}
        >
          <div className="key-bound key-nav-inner">
            {role === "customer" ? (
              <>
                <a
                  href="#home"
                  aria-current={page === "home" || !page ? "page" : undefined}
                >
                  {t("Overview", "Ringkasan")}
                </a>
                {(["K", "E", "Y"] as const).map((item) => (
                  <a
                    key={item}
                    href={journeyLink(item)}
                    aria-current={journey === item ? "page" : undefined}
                  >
                    {names[item]}
                  </a>
                ))}
                <div className="key-nav-spacer" />
                <a
                  href="#requests"
                  aria-current={page === "requests" ? "page" : undefined}
                >
                  <ClipboardList size={15} aria-hidden="true" />
                  {t("My requests", "Permintaan saya")}
                </a>
                <a
                  href="#records"
                  aria-current={page === "records" ? "page" : undefined}
                >
                  {t("Vehicle records", "Riwayat kendaraan")}
                </a>
              </>
            ) : (
              <>
                <a href={"#" + role} aria-current="page">
                  {t("Work queue", "Antrean kerja")}
                </a>
                <span className="key-nav-account">{accounts[role]}</span>
              </>
            )}
          </div>
        </nav>
        <main
          className="key-bound key-main"
          id="key-main"
          tabIndex={-1}
          ref={top}
        >
          {role === "customer" &&
            !journey &&
            page !== "records" &&
            page !== "requests" && <Home go={go} />}
          {!!journey && (
            <div className="key-page-heading">
              <div className="key-letter">{journey}</div>
              <div>
                <p className="key-kicker">
                  {role === "customer" ? "DIGIROOM KEY" : labels[role]}
                </p>
                <h1>{names[journey]}</h1>
              </div>
              {role === "customer" && journey === "K" && record && (
                <button
                  className="key-btn key-btn-minor key-heading-action"
                  onClick={openStudio}
                >
                  <ArrowUpRight size={17} aria-hidden="true" />
                  {t("Open 3D Life Test", "Buka Tes Keseharian 3D")}
                </button>
              )}
            </div>
          )}
          {role !== "customer" && journey && (
            <div
              className="key-queue"
              aria-label={t("Work queue", "Antrean kerja")}
            >
              <div>
                <span className="key-kicker">
                  {t("WORK QUEUE", "ANTREAN KERJA")}
                </span>
                <strong>{record ? record.id : emptyName[journey]}</strong>
              </div>
              <div>
                <span>
                  {record
                    ? queueOwner
                      ? t("Next action", "Tindakan berikutnya")
                      : t("Status", "Status")
                    : t("Open requests", "Permintaan aktif")}
                </span>
                <strong>
                  {record
                    ? queueOwner
                      ? labels[queueOwner]
                      : t("Completed", "Selesai")
                    : "0"}
                </strong>
              </div>
              <div>
                <span>
                  {record
                    ? t("Quote version", "Versi penawaran")
                    : t("Workspace", "Ruang kerja")}
                </span>
                <strong>
                  {record
                    ? record.revision
                      ? "v" + record.revision
                      : "—"
                    : labels[role]}
                </strong>
              </div>
            </div>
          )}
          {error && (
            <p className="key-error" role="alert">
              {error}
            </p>
          )}
          {role !== "customer" && journey && !record && (
            <Panel title={emptyName[journey]}>
              <p>
                {t(
                  "A customer request appears here with its vehicle and next action.",
                  "Permintaan pelanggan muncul dengan kendaraan dan tindakan berikutnya.",
                )}
              </p>
              <ActionButton minor onClick={() => go(journeyLink(journey))}>
                {t("Open customer journey", "Buka perjalanan pelanggan")}
              </ActionButton>
            </Panel>
          )}
          {journey === "K" &&
            (state.drive ? (
              <DriveRecord
                key={role + state.drive.id}
                record={state.drive}
                adviser={role === "sales"}
                send={send}
              />
            ) : (
              role === "customer" && (
                <DriveRequest
                  brief={draft.brief}
                  preferred={draft.preferred}
                  onStudio={openStudio}
                  send={send}
                />
              )
            ))}
          {journey === "E" && (state.service || role === "customer") && (
            <Suspense
              fallback={
                <p className="key-loading">
                  {t("Opening workshop services…", "Membuka layanan bengkel…")}
                </p>
              }
            >
              <ServiceView
                state={state.service}
                role={role}
                payerVersion={
                  payer && state.service?.id === payer[1]
                    ? Number(payer[2])
                    : undefined
                }
                openPayer={(version) =>
                  go("#payer=" + state.service?.id + ":" + version)
                }
                send={send}
              />
            </Suspense>
          )}
          {journey === "Y" && (state.upgrade || role === "customer") && (
            <Suspense
              fallback={
                <p className="key-loading">
                  {t(
                    "Opening upgrade workspace…",
                    "Membuka ruang tukar tambah…",
                  )}
                </p>
              }
            >
              <UpgradeView
                state={state.upgrade}
                role={role}
                onPlanner={() => go("#studio/ownership")}
                marketTrade={draft.marketTrade}
                send={send}
              />
            </Suspense>
          )}
          {role === "customer" &&
            (page === "requests" || page === "records") && (
              <>
                <div className="key-page-heading">
                  <div className="key-letter">
                    <ClipboardList size={27} aria-hidden="true" />
                  </div>
                  <div>
                    <p className="key-kicker">DIGIROOM KEY</p>
                    <h1>
                      {page === "records"
                        ? t("Vehicle records", "Riwayat kendaraan")
                        : t("My requests", "Permintaan saya")}
                    </h1>
                  </div>
                </div>
                <div className="key-records">
                  {page === "records" && (
                    <Panel
                      title="Yaris Cross Hybrid"
                      eyebrow={t("CURRENT VEHICLE", "KENDARAAN SAAT INI")}
                    >
                      <p>2024 · HEV · 24.800 km</p>
                      <p>
                        {t(
                          "Scheduled-service receipts and hybrid health record are available to share with your permission.",
                          "Bukti servis berkala dan riwayat hybrid dapat dibagikan dengan izin Anda.",
                        )}
                      </p>
                      <ActionButton minor onClick={() => go("#y")}>
                        {t("Open upgrade journey", "Buka perjalanan pembelian")}
                      </ActionButton>
                    </Panel>
                  )}
                  {(
                    [
                      ["K", state.drive, stateName],
                      ["E", state.service, undefined],
                      ["Y", state.upgrade, undefined],
                    ] as const
                  )
                    .filter(
                      ([item, value]) =>
                        value &&
                        (page === "requests" ||
                          (item === "K" &&
                            state.drive?.stage === "delivered") ||
                          (item === "E" && state.service?.stage === "closed") ||
                          (item === "Y" &&
                            state.upgrade?.stage === "delivered")),
                    )
                    .map(([item, value, status]) => (
                      <Panel title={names[item]} key={item} eyebrow={value!.id}>
                        <p>
                          {status ??
                            (responsible(item, state)
                              ? t("In progress", "Berlangsung")
                              : t("Completed", "Selesai"))}
                        </p>
                        <p>
                          {t("Next action", "Tindakan berikutnya")} ·{" "}
                          {responsible(item, state)
                            ? labels[responsible(item, state)!]
                            : t(
                                "Vehicle record updated",
                                "Riwayat kendaraan diperbarui",
                              )}
                        </p>
                        <ActionButton
                          minor
                          onClick={() => go(journeyLink(item))}
                        >
                          {t("Open record", "Buka rincian")}
                        </ActionButton>
                      </Panel>
                    ))}
                  {page === "requests" &&
                    !state.drive &&
                    !state.service &&
                    !state.upgrade && (
                      <Panel
                        title={t("No requests yet", "Belum ada permintaan")}
                      >
                        <p>
                          {t(
                            "Your drives, service visits and upgrade requests appear here after you send them.",
                            "Uji kendara, kunjungan servis, dan permintaan pembelian muncul setelah dikirim.",
                          )}
                        </p>
                        <ActionButton onClick={() => go("#home")}>
                          {t("Explore Digiroom KEY", "Jelajahi Digiroom KEY")}
                        </ActionButton>
                      </Panel>
                    )}
                </div>
              </>
            )}
        </main>
        <footer className="key-footer">
          <div className="key-bound">
            <span>
              Digiroom KEY <span className="key-footer-separator">/</span>{" "}
              {t(
                "Competition accounts · records saved on this device",
                "Akun kompetisi · riwayat tersimpan di perangkat ini",
              )}
            </span>
            <button type="button" onClick={() => dialog.current?.showModal()}>
              <RotateCcw size={14} aria-hidden="true" />
              {t("Reset walkthrough", "Atur ulang alur demo")}
            </button>
          </div>
        </footer>
        <dialog
          ref={dialog}
          className="key-reset"
          aria-labelledby="key-reset-title"
        >
          <h2 id="key-reset-title">
            {t("Reset the walkthrough?", "Atur ulang alur demo?")}
          </h2>
          <p>
            {t(
              "Clear the three local transactions and restore the starting accounts.",
              "Hapus tiga transaksi lokal dan pulihkan akun awal.",
            )}
          </p>
          <div className="key-actions">
            <ActionButton minor onClick={() => dialog.current?.close()}>
              {t("Keep progress", "Simpan progres")}
            </ActionButton>
            <ActionButton
              onClick={() => {
                dialog.current?.close();
                persist(EMPTY);
                saveDraft({});
                go("#home");
              }}
            >
              {t("Reset walkthrough", "Atur ulang alur demo")}
            </ActionButton>
          </div>
        </dialog>
      </div>
    </KeyLanguage.Provider>
  );
}
function Home({ go }: { go: (route: string) => void }) {
  const { t } = useKey();
  const names = journeyNames(t);
  const descriptions = {
    K: t(
      "Check your garage and family setup in 3D. Take your checklist on a 48-Hour Life Test.",
      "Periksa garasi dan kebutuhan keluarga dalam 3D. Bawa daftar cek saat Tes Keseharian 48 Jam.",
    ),
    E: t(
      "Compare workshop access in Bandung. Confirm parts, approve any extras and collect your car.",
      "Bandingkan akses bengkel di Bandung. Konfirmasi suku cadang, setujui tambahan, dan ambil mobil.",
    ),
    Y: t(
      "Turn an inspected buy offer into a clear deal on your next Toyota.",
      "Ubah penawaran beli hasil inspeksi menjadi transaksi Toyota berikutnya.",
    ),
  };
  return (
    <>
      <section className="key-hero" aria-labelledby="key-home-title">
        <div className="key-hero-copy">
          <p className="key-kicker">
            <span />
            {t("AUTO2000 OWNERSHIP JOURNEY", "PERJALANAN KEPEMILIKAN AUTO2000")}
          </p>
          <h1 id="key-home-title">
            {t("Know your fit.", "Kenali kecocokan.")}
            <br />
            {t("Book your service.", "Jadwalkan servis.")}
            <br />
            <em>{t("Find your next Toyota.", "Temukan Toyota Anda.")}</em>
          </h1>
          <div className="key-hero-actions">
            <ActionButton onClick={() => go("#studio/garage")}>
              {t("Open 3D Life Test", "Buka Tes Keseharian 3D")}
            </ActionButton>
            <button onClick={() => go("#k")} className="key-link">
              {t("Open visit card", "Buka kartu kunjungan")}
              <ArrowUpRight size={15} aria-hidden="true" />
            </button>
          </div>
        </div>
        <div className="key-hero-art">
          <div className="key-hero-shadow" />
          <img
            src="/key/zenix-studio.webp"
            alt={t(
              "Silver Innova Zenix Hybrid viewed from the front and side",
              "Innova Zenix Hybrid perak dilihat dari depan dan samping",
            )}
            fetchPriority="high"
          />
          <div className="key-hero-spec">
            <span className="key-hero-model">
              INNOVA ZENIX <strong>HYBRID</strong>
            </span>
            <span>
              {t(
                "Garage · Family · Driving week",
                "Garasi · Keluarga · Rutinitas",
              )}
            </span>
          </div>
        </div>
      </section>
      <section
        className="key-journey-section"
        aria-labelledby="key-journey-title"
      >
        <div className="key-section-head">
          <h2 id="key-journey-title">
            {t("Choose your next step", "Pilih langkah berikutnya")}
          </h2>
          <span>
            <MapPin size={15} aria-hidden="true" />
            {t("Auto2000 · Indonesia", "Auto2000 · Indonesia")}
          </span>
        </div>
        <div className="key-journey-cards">
          {(["K", "E", "Y"] as const).map((item) => {
            const Icon = icon[item];
            return (
              <a
                key={item}
                href={"#" + item.toLowerCase()}
                className="key-journey-card"
              >
                <div>
                  <span className="key-journey-letter">{item}</span>
                  <Icon size={24} aria-hidden="true" />
                </div>
                <h3>{names[item]}</h3>
                <p>{descriptions[item]}</p>
                <span className="key-card-arrow">
                  <ArrowRight size={19} aria-hidden="true" />
                </span>
              </a>
            );
          })}
        </div>
      </section>
    </>
  );
}
