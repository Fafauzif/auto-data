import { lazy, Suspense, useRef, useState } from "react";
import {
  Building2,
  CircleHelp,
  MapPin,
  ReceiptText,
  Share2,
} from "lucide-react";
import {
  flags,
  gapCounts,
  geo,
  markets,
  serviceEligible,
  servicePackage,
  type Market,
  type Outlet,
  type Origin,
} from "./geography";
import { type Funding, type JobId, type Prior, type Service } from "./state";
import {
  ActionButton,
  Field,
  History,
  Metric,
  Panel,
  Steps,
  downloadText,
  useKey,
  type Send,
  type Text,
} from "./ui";
const ServiceMap = lazy(() => import("./ServiceMap"));
const jobLabels = (t: Text): Record<JobId, string> => ({
  oil: t("Oil & filter · Avanza 2019 1.3", "Oli & filter · Avanza 2019 1.3"),
  fault: t("Brake noise diagnosis · Avanza", "Diagnosis bunyi rem · Avanza"),
  hybrid: t(
    "Hybrid health check · Yaris Cross",
    "Pemeriksaan sistem hybrid · Yaris Cross",
  ),
  home: t(
    "Toyota Home Service · Avanza oil & filter",
    "Toyota Home Service · Oli & filter Avanza",
  ),
});
const priorLabels = (t: Text): Record<Prior, string> => ({
  independent: t("Independent workshop", "Bengkel independen"),
  auto2000: "Auto2000",
  first: t("First comparable service", "Servis sejenis pertama"),
});
const fundingLabels = (t: Text): Record<Funding, string> => ({
  paid: t("Customer-paid", "Dibayar pelanggan"),
  covered: t("Eligible covered service", "Servis tercakup"),
  reimbursement: t("Reimbursement-funded", "Dibiayai melalui penggantian"),
});
export const serviceStatus = (t: Text): Record<Service["stage"], string> => ({
  requested: t(
    "Awaiting parts and slot confirmation",
    "Menunggu konfirmasi suku cadang dan jadwal",
  ),
  confirmed: t(
    "Parts reserved · Slot confirmed",
    "Suku cadang disiapkan · Jadwal dikonfirmasi",
  ),
  checkedIn: t("Vehicle in workshop", "Kendaraan di bengkel"),
  approval: t("Awaiting payer approval", "Menunggu persetujuan pembayar"),
  authorized: t("Payer decision recorded", "Keputusan pembayar tercatat"),
  ready: t("Ready for collection", "Siap diambil"),
  closed: t("Service completed", "Servis selesai"),
});
const scopeLabels = (t: Text): Record<JobId, string> => ({
  oil: t(
    "4 L engine oil, model-matched filter, washer replacement and leak check",
    "Oli mesin 4 L, filter sesuai model, ring baut, dan pemeriksaan kebocoran",
  ),
  fault: t(
    "Road test and brake inspection, recorded diagnosis before any repair",
    "Uji jalan dan inspeksi rem, diagnosis tertulis sebelum perbaikan",
  ),
  hybrid: t(
    "Hybrid health check, scan and written result for Yaris Cross Hybrid",
    "Pemeriksaan sistem hybrid, pemindaian, dan hasil tertulis untuk Yaris Cross Hybrid",
  ),
  home: t(
    "Avanza oil and filter at a qualifying Bandung address, with post-service leak check",
    "Oli dan filter Avanza di alamat Bandung yang memenuhi syarat, disertai pemeriksaan kebocoran",
  ),
});
function initialOrigin(market: Market) {
  const origins = geo.markets[market].origins;
  return origins.find((o) => o.before > 5 && o.after <= 5) ?? origins[0];
}
export function ServiceRequest({ send }: { send: Send }) {
  const offers = useRef<HTMLDivElement>(null);
  const { t, decimal, money, date } = useKey();
  const [market, setMarket] = useState<Market>("Bandung");
  const [network, setNetwork] = useState(false);
  const [originId, setOriginId] = useState(initialOrigin("Bandung").id);
  const [outletId, setOutletId] = useState("");
  const [job, setJob] = useState<JobId>("oil");
  const [prior, setPrior] = useState<Prior>("independent");
  const [funding, setFunding] = useState<Funding>("paid");
  const [symptom, setSymptom] = useState("");
  const [priorWork, setPriorWork] = useState("");
  const [addressInScope, setAddressInScope] = useState(false);
  const [offline, setOffline] = useState(false);
  const [listView, setListView] = useState(false);
  const [filter, setFilter] = useState("");
  const [layers, setLayers] = useState({
    origins: true,
    dealer: true,
    owned: true,
    comparison: false,
  });
  const data = geo.markets[market];
  const origin = data.origins.find((o) => o.id === originId) ?? data.origins[0];
  const counts = gapCounts(data.origins);
  const total = gapCounts(markets.flatMap((city) => geo.markets[city].origins));
  const destination = (id: string) =>
    data.outlets.find((outlet) => outlet.id === id);
  const routeTarget = destination(network ? origin.owned : origin.dealer);
  const options = data.outlets
    .filter((outlet) => serviceEligible(outlet, market, job, network))
    .sort((a, b) => a.name.localeCompare(b.name));
  const preferred = job === "home" ? flags.Bandung : routeTarget?.id;
  const offered =
    options.find((outlet) => outlet.id === outletId) ??
    options.find((outlet) => outlet.id === preferred) ??
    options[0];
  const selected = destination(outletId) ?? offered;
  const quote = offered ? servicePackage(job, offered) : undefined;
  const setOrigin = (item: Origin) => {
    setOriginId(item.id);
    setOutletId("");
  };
  const setOutlet = (item: Outlet) => setOutletId(item.id);
  const dates = quote && date(Date.parse(quote.day + "T12:00:00+07:00"));
  const searchQuery = filter.trim().toLocaleLowerCase();
  const outlets = data.outlets.filter(
    (o) => !searchQuery || o.name.toLocaleLowerCase().includes(searchQuery),
  );
  const filteredOptions = options.filter((outlet) => outlets.includes(outlet));
  const selectedIsEligible =
    !outletId || options.some((outlet) => outlet.id === outletId);
  return (
    <>
      <div
        className="key-market-bar"
        aria-label={t("Study market", "Wilayah studi")}
      >
        {markets.map((city) => (
          <button
            key={city}
            className={market === city ? "active" : ""}
            aria-pressed={market === city}
            onClick={() => {
              setMarket(city);
              setOrigin(initialOrigin(city));
              setFilter("");
            }}
          >
            {city}
          </button>
        ))}
      </div>
      <div className="key-service-jump">
        <ActionButton
          minor
          onClick={() => {
            offers.current?.focus({ preventScroll: true });
            offers.current?.scrollIntoView({ block: "start" });
          }}
        >
          {t("Jump to service offers", "Lihat penawaran servis")}
        </ActionButton>
      </div>
      <div className="key-access-grid">
        <section
          className="key-panel key-map-card"
          aria-label={t("Workshop access map", "Peta akses bengkel")}
        >
          <div className="key-map-heading">
            <div>
              <span className="key-kicker">
                {t("OIL SERVICE ACCESS", "AKSES SERVIS OLI")}
              </span>
              <h2>{market}</h2>
            </div>
            <div className="key-actions">
              <ActionButton minor onClick={() => setListView(!listView)}>
                {listView
                  ? t("Show map", "Tampilkan peta")
                  : t("List view", "Tampilan daftar")}
              </ActionButton>
              {!listView && (
                <ActionButton minor onClick={() => setOffline(!offline)}>
                  {offline
                    ? t("Use street tiles", "Gunakan peta jalan")
                    : t("Use local atlas", "Gunakan atlas lokal")}
                </ActionButton>
              )}
            </div>
          </div>
          <div
            className="key-map-scenarios"
            aria-label={t("Routing scenario", "Skenario rute")}
          >
            <button
              aria-pressed={!network}
              onClick={() => {
                setNetwork(false);
                setOutletId("");
              }}
            >
              {t("Dealer workshops", "Bengkel dealer")}
            </button>
            <button
              aria-pressed={network}
              onClick={() => {
                setNetwork(true);
                setOutletId("");
                setLayers((l) => ({ ...l, owned: true }));
              }}
            >
              {t(
                "With eligible OtoXpert",
                "Dengan OtoXpert yang memenuhi syarat",
              )}
            </button>
          </div>
          {listView ? (
            <div className="key-map-list">
              <table>
                <thead>
                  <tr>
                    <th>{t("Modeled origin", "Titik asal")}</th>
                    <th>{t("Dealer gap", "Selisih dealer")}</th>
                    <th>{t("With OtoXpert", "Dengan OtoXpert")}</th>
                  </tr>
                </thead>
                <tbody>
                  {data.origins.map((o) => (
                    <tr
                      key={o.id}
                      className={o.id === origin.id ? "selected" : ""}
                    >
                      <td>
                        <button
                          aria-pressed={o.id === origin.id}
                          onClick={() => setOrigin(o)}
                        >
                          {o.id}
                        </button>
                      </td>
                      <td>{decimal(o.before)} min</td>
                      <td>{decimal(o.after)} min</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <Suspense
              fallback={
                <div className="key-map-frame key-atlas-loading">
                  {t("Opening the local map…", "Membuka peta lokal…")}
                </div>
              }
            >
              <ServiceMap
                market={market}
                origins={data.origins}
                outlets={outlets}
                layers={layers}
                network={network}
                selected={origin.id}
                outletId={selected?.id ?? ""}
                offline={offline}
                onOrigin={setOrigin}
                onOutlet={setOutlet}
              />
            </Suspense>
          )}
          <div className="key-map-legend">
            <span className="key-origin-legend">
              <span className="key-dot" /> ≤5 min{" "}
              <span className="key-dot gap" /> &gt;5 min
            </span>
            {(
              [
                ["origins", t("Origins", "Titik asal")],
                ["dealer", "Auto2000"],
                [
                  "owned",
                  t("Auto2000-operated OtoXpert", "OtoXpert dikelola Auto2000"),
                ],
                [
                  "comparison",
                  t("Oil comparison network", "Jaringan pembanding oli"),
                ],
              ] as const
            ).map(([key, name]) => (
              <label key={key}>
                <input
                  type="checkbox"
                  checked={layers[key]}
                  onChange={(e) =>
                    setLayers({ ...layers, [key]: e.target.checked })
                  }
                />
                <span className={"key-dot " + key} />
                {name}
              </label>
            ))}
          </div>
        </section>
        <Panel
          title={t("Oil-service access gap", "Selisih akses servis oli")}
          eyebrow={t("MODELED ORIGINS", "TITIK ASAL MODEL")}
          className="key-access-summary"
        >
          <div className="key-access-number" data-testid="market-gap">
            {network ? counts.after : counts.before}
            <span> / {counts.points}</span>
          </div>
          <p>
            {t(
              "origins more than five minutes behind the collected oil-service comparison network",
              "titik asal lebih dari lima menit di belakang jaringan pembanding servis oli",
            )}
          </p>
          <dl className="key-atlas-counts">
            {markets.map((city) => {
              const c = gapCounts(geo.markets[city].origins);
              return (
                <div key={city} data-testid={"gap-" + city}>
                  <dt>
                    {city} <small>· {c.points}</small>
                  </dt>
                  <dd>
                    {c.before} → {c.after}
                  </dd>
                </div>
              );
            })}
            <div>
              <dt>
                {t("Four markets", "Empat wilayah")}{" "}
                <small>· {total.points}</small>
              </dt>
              <dd>
                {total.before} → {total.after}
              </dd>
            </div>
          </dl>
          <Field label={t("Modeled origin", "Titik asal model")}>
            <select
              value={origin.id}
              onChange={(e) =>
                setOrigin(data.origins.find((o) => o.id === e.target.value)!)
              }
            >
              {data.origins.map((o) => (
                <option key={o.id}>{o.id}</option>
              ))}
            </select>
          </Field>
          <dl className="key-timings">
            <Metric label={t("Dealer only", "Dealer saja")}>
              {decimal(origin.dealerSeconds / 60)} min
            </Metric>
            <Metric
              label={t("Eligible network", "Jaringan yang memenuhi syarat")}
            >
              {decimal(origin.ownedSeconds / 60)} min
            </Metric>
            <Metric label={t("Oil comparison", "Pembanding oli")}>
              {decimal(origin.comparatorSeconds / 60)} min
            </Metric>
          </dl>
          <p className="key-muted" data-testid="origin-detail">
            {routeTarget?.name} · {t("gap", "selisih")}{" "}
            {decimal(network ? origin.after : origin.before)} min
            <br />
            {t("Comparison", "Pembanding")} ·{" "}
            {destination(origin.comparator)?.name}
            {origin.ties.length > 1 && (
              <>
                <br />
                {t("Tied dealer endpoints", "Bengkel dengan waktu sama")}:{" "}
                {origin.ties
                  .map((id) => destination(id)?.name ?? id)
                  .join(" / ")}
              </>
            )}
          </p>
          <details className="key-details">
            <summary>
              <CircleHelp size={15} aria-hidden="true" />
              {t("About this map", "Tentang peta ini")}
            </summary>
            <p>
              {t(
                "One-way OSRM times at regular grid origins. The threshold applies to the defined oil job. Eight remaining origins are assigned to Soekarno-Hatta. Modeled time excludes live traffic. Offers and operating windows below are competition fixtures.",
                "Waktu satu arah OSRM dari titik grid. Ambang berlaku untuk pekerjaan oli. Delapan titik tersisa terhubung ke Soekarno-Hatta. Waktu model tidak mencakup lalu lintas saat ini. Penawaran dan jadwal di bawah menggunakan data kompetisi.",
              )}
            </p>
            <a
              href={
                "https://github.com/Fafauzif/auto-data/blob/" +
                geo.revision +
                "/analysis/geography/GEOGRAPHY_INTEGRATION_REPORT.md"
              }
              target="_blank"
              rel="noreferrer"
            >
              {t(
                "Geography report · 14 Nov 2026",
                "Laporan geografi · 14 Nov 2026",
              )}
            </a>
          </details>
        </Panel>
      </div>
      <div className="key-split key-service-offers" ref={offers} tabIndex={-1}>
        <Panel
          title={t(
            "Find an offer for your job",
            "Cari penawaran sesuai pekerjaan",
          )}
          eyebrow={t("VEHICLE AND JOB", "KENDARAAN DAN PEKERJAAN")}
        >
          <Field label={t("Workshop job", "Pekerjaan bengkel")}>
            <select
              value={job}
              onChange={(e) => {
                const next = e.target.value as JobId;
                setJob(next);
                setFunding(next === "hybrid" ? "covered" : "paid");
                setOutletId("");
              }}
            >
              {Object.entries(jobLabels(t)).map(([id, label]) => (
                <option key={id} value={id}>
                  {label}
                </option>
              ))}
            </select>
          </Field>
          <Field
            label={t(
              "Search outlets in " + market,
              "Cari bengkel di " + market,
            )}
          >
            <input
              type="search"
              value={filter}
              onChange={(e) => setFilter(e.target.value)}
            />
          </Field>
          <Field label={t("Eligible outlet", "Bengkel yang memenuhi syarat")}>
            <select
              value={
                selectedIsEligible &&
                offered &&
                filteredOptions.includes(offered)
                  ? offered.id
                  : ""
              }
              onChange={(e) => setOutletId(e.target.value)}
            >
              <option value="" disabled>
                {t(
                  "Choose an eligible outlet",
                  "Pilih bengkel yang memenuhi syarat",
                )}
              </option>
              {filteredOptions.map((outlet) => (
                <option key={outlet.id} value={outlet.id}>
                  {outlet.name}
                </option>
              ))}
            </select>
          </Field>
          {selected && (
            <p className="key-callout">
              <MapPin size={19} aria-hidden="true" />
              <span>
                <strong>{selected.name}</strong> · {selected.operator}
                <br />
                {selected.hours ||
                  t(
                    "Published directory location",
                    "Lokasi dalam direktori publik",
                  )}
                {selected.url && (
                  <>
                    {" "}
                    ·{" "}
                    <a href={selected.url} target="_blank" rel="noreferrer">
                      {t("Directory", "Direktori")}
                    </a>
                  </>
                )}
              </span>
            </p>
          )}
          {!selectedIsEligible && (
            <p className="key-muted">
              {t(
                "This outlet is shown for comparison. Choose an eligible Auto2000-operated outlet to request service.",
                "Bengkel ini ditampilkan sebagai pembanding. Pilih bengkel yang dikelola Auto2000 untuk meminta servis.",
              )}
            </p>
          )}
          {!options.length && (
            <p>
              {t(
                "No offer for this job in the selected market. Toyota Home Service is available in the Bandung route shown here.",
                "Tidak ada penawaran pekerjaan ini di wilayah terpilih. Toyota Home Service tersedia pada rute Bandung yang ditampilkan.",
              )}
            </p>
          )}
          <details className="key-details" open={job === "fault" || undefined}>
            <summary>
              {t("Service and payer details", "Rincian servis dan pembayar")}
            </summary>
            <Field
              label={t(
                "Provider last used for comparable work",
                "Bengkel sebelumnya untuk pekerjaan sejenis",
              )}
            >
              <select
                value={prior}
                onChange={(e) => setPrior(e.target.value as Prior)}
              >
                {Object.entries(priorLabels(t)).map(([id, label]) => (
                  <option key={id} value={id}>
                    {label}
                  </option>
                ))}
              </select>
            </Field>
            <Field label={t("Funding", "Pembiayaan servis")}>
              <select
                value={funding}
                onChange={(e) => setFunding(e.target.value as Funding)}
              >
                {Object.entries(fundingLabels(t))
                  .filter(([id]) => job === "hybrid" || id !== "covered")
                  .map(([id, label]) => (
                    <option key={id} value={id}>
                      {label}
                    </option>
                  ))}
              </select>
            </Field>
            {job === "fault" && (
              <>
                <Field
                  label={t(
                    "Symptoms for the technician",
                    "Gejala untuk teknisi",
                  )}
                >
                  <textarea
                    value={symptom}
                    onChange={(e) => setSymptom(e.target.value)}
                    rows={2}
                    placeholder={t(
                      "Rattle when braking at low speed",
                      "Bunyi saat mengerem pelan",
                    )}
                  />
                </Field>
                <Field
                  label={t(
                    "Prior inspection or work",
                    "Pemeriksaan atau pekerjaan sebelumnya",
                  )}
                >
                  <input
                    value={priorWork}
                    onChange={(e) => setPriorWork(e.target.value)}
                  />
                </Field>
              </>
            )}
          </details>
          {job === "home" && (
            <label className="key-check">
              <input
                type="checkbox"
                checked={addressInScope}
                onChange={(e) => setAddressInScope(e.target.checked)}
              />
              {t(
                "Service address qualifies in the Soekarno-Hatta coverage area",
                "Alamat servis masuk cakupan Soekarno-Hatta",
              )}
            </label>
          )}
        </Panel>
        <Panel
          title={t(
            "Installed price and collection",
            "Harga terpasang dan pengambilan",
          )}
          eyebrow={
            offered?.operator ?? t("WORKSHOP OFFER", "PENAWARAN BENGKEL")
          }
        >
          {quote &&
          offered &&
          selectedIsEligible &&
          filteredOptions.includes(offered) ? (
            <>
              <p>{scopeLabels(t)[job]}</p>
              <dl className="key-metrics">
                <Metric label={t("Parts", "Suku cadang")}>
                  {money(quote.priceParts)}
                </Metric>
                <Metric label={t("Labor", "Jasa")}>{money(quote.labor)}</Metric>
                <Metric label={t("Tax", "Pajak")}>{money(quote.tax)}</Metric>
                <Metric
                  label={
                    funding === "covered"
                      ? t("Your initial cost", "Biaya awal Anda")
                      : t("Installed total", "Total terpasang")
                  }
                >
                  {money(funding === "covered" ? 0 : quote.base)}
                </Metric>
              </dl>
              <p className="key-callout">
                <Building2 size={20} aria-hidden="true" />
                <span>
                  {dates} · {t("Check-in", "Datang")} {quote.checkIn} WIB ·{" "}
                  {t("Collection", "Ambil")} {quote.collection} WIB
                </span>
              </p>
              <p className="key-muted">
                {t(
                  "Additional repairs or parts require a separate estimate. Slot and parts are confirmed by the workshop adviser.",
                  "Pekerjaan dan suku cadang tambahan memerlukan estimasi terpisah. Jadwal dan parts dikonfirmasi penasihat bengkel.",
                )}
              </p>
              <ActionButton
                disabled={
                  (job === "fault" && !symptom.trim()) ||
                  (job === "home" && !addressInScope)
                }
                onClick={() =>
                  send({
                    type: "requestService",
                    details: {
                      ...quote,
                      job,
                      outlet: offered.name,
                      market,
                      prior,
                      funding,
                      symptom,
                      priorWork,
                    },
                  })
                }
              >
                {t("Request this service", "Ajukan servis ini")}
              </ActionButton>
            </>
          ) : (
            <p>
              {t(
                "Select an eligible outlet to see a price and a collection window.",
                "Pilih bengkel yang memenuhi syarat untuk melihat harga dan waktu pengambilan.",
              )}
            </p>
          )}
        </Panel>
      </div>
    </>
  );
}
export function ServiceRecord({
  record,
  adviser,
  payerVersion,
  send,
  openPayer,
}: {
  record: Service;
  adviser: boolean;
  payerVersion?: number;
  send: Send;
  openPayer: (version: number) => void;
}) {
  const { t, money, date } = useKey();
  const [amount, setAmount] = useState(166500);
  const [required, setRequired] = useState(
    t(
      record.job === "fault"
        ? "Clean and reseat the brake hardware"
        : "Replace the split drain-plug seal and recheck for leaks",
      record.job === "fault"
        ? "Bersihkan dan pasang kembali perangkat rem"
        : "Ganti seal baut pembuangan yang retak dan periksa kebocoran",
    ),
  );
  const [deferred, setDeferred] = useState(
    t(
      "Cabin filter can wait until the next visit",
      "Filter kabin dapat diganti pada kunjungan berikutnya",
    ),
  );
  const [option, setOption] = useState(
    t(
      "Complete the originally agreed work only",
      "Kerjakan lingkup awal yang telah disepakati",
    ),
  );
  const [link, setLink] = useState("");
  const estimate = record.estimate,
    payment = record.payment,
    stage = record.stage;
  const payer =
    !adviser &&
    !!estimate &&
    payerVersion === estimate.version &&
    stage === "approval";
  const stale = !!payerVersion && !payer;
  const progress = [
    "requested",
    "confirmed",
    "checkedIn",
    "approval",
    "authorized",
    "ready",
    "closed",
  ].indexOf(stage);
  const initialCustomer = record.funding === "paid" ? record.base : 0;
  const quoteLines = [
    record.id + " · " + record.outlet,
    jobLabels(t)[record.job],
    date(Date.parse(record.day + "T12:00:00+07:00")),
    scopeLabels(t)[record.job],
    t("Customer-paid", "Dibayar pelanggan") + ": " + money(payment?.paid ?? 0),
    t("Covered", "Tercakup") + ": " + money(payment?.covered ?? 0),
    t("Reimbursement-funded", "Diganti") +
      ": " +
      money(payment?.reimbursed ?? 0),
    t("Approved scope version", "Versi pekerjaan disetujui") +
      ": " +
      (record.approval?.accepted ? record.approval.version : 1),
    ...(record.approval?.accepted && estimate ? [estimate.required] : []),
  ];
  return (
    <>
      <Steps
        items={[
          t("Request", "Permintaan"),
          t("Slot", "Jadwal"),
          t("Workshop", "Bengkel"),
          t("Payer", "Pembayar"),
          t("Collection", "Pengambilan"),
        ]}
        active={progress > 4 ? 4 : Math.min(3, progress)}
      />
      <div className="key-split">
        <Panel title={jobLabels(t)[record.job]} eyebrow={record.id}>
          <p>
            {record.outlet} · {record.market}
          </p>
          <p>{scopeLabels(t)[record.job]}</p>
          <dl className="key-metrics">
            <Metric label={t("Installed price v1", "Harga terpasang v1")}>
              {money(record.base)}
            </Metric>
            <Metric label={t("Funding", "Pembiayaan")}>
              {fundingLabels(t)[record.funding]}
            </Metric>
            <Metric label={t("Check-in", "Datang")}>
              {date(Date.parse(record.day + "T12:00:00+07:00"))} ·{" "}
              {record.checkIn} WIB
            </Metric>
            <Metric label={t("Collection", "Pengambilan")}>
              {record.collection} WIB
            </Metric>
          </dl>
          <p>
            {t("Prior provider", "Bengkel sebelumnya")} ·{" "}
            {priorLabels(t)[record.prior]}
          </p>
          {record.symptom && (
            <p>
              <strong>
                {t("Technician handoff", "Serah terima untuk teknisi")}
              </strong>
              <br />
              {record.symptom}
              <br />
              {t("Prior work", "Pekerjaan sebelumnya")} ·{" "}
              {record.priorWork || t("None recorded", "Belum tercatat")}
            </p>
          )}
          <History events={record.history} />
        </Panel>
        <Panel
          title={serviceStatus(t)[stage]}
          eyebrow={t("WORK ORDER", "PERINTAH KERJA")}
        >
          {adviser && stage === "requested" && (
            <>
              <p>
                {t(
                  "Fitment, job and operator match. Check workshop hours, reserve the listed parts and accept the collection window.",
                  "Suku cadang, pekerjaan, dan operator sesuai. Periksa jam bengkel, siapkan suku cadang, dan konfirmasi waktu pengambilan.",
                )}
              </p>
              <ActionButton onClick={() => send({ type: "confirmService" })}>
                {t(
                  "Reserve parts and confirm slot",
                  "Siapkan suku cadang dan konfirmasi jadwal",
                )}
              </ActionButton>
            </>
          )}
          {adviser && stage === "confirmed" && (
            <ActionButton onClick={() => send({ type: "checkIn" })}>
              {t("Check in vehicle", "Terima kendaraan")}
            </ActionButton>
          )}
          {estimate && (adviser || payer || stage !== "approval") && (
            <>
              <h3>
                {t("Additional work estimate", "Estimasi pekerjaan tambahan")} ·
                v{estimate.version}
              </h3>
              <p>
                <strong>{t("Required", "Diperlukan")}</strong> ·{" "}
                {estimate.required}
                <br />
                <strong>{t("Can wait", "Bisa ditunda")}</strong> ·{" "}
                {estimate.deferred}
                <br />
                <strong>{t("Option", "Opsi")}</strong> · {estimate.option}
              </p>
              <dl className="key-metrics">
                <Metric
                  label={t(
                    "Additional installed amount",
                    "Biaya tambahan terpasang",
                  )}
                >
                  {money(estimate.amount)}
                </Metric>
                <Metric
                  label={t(
                    "Revised customer payment",
                    "Revisi pembayaran pelanggan",
                  )}
                >
                  {money(initialCustomer + estimate.amount)}
                </Metric>
              </dl>
              {record.approval && (
                <p className="key-callout">
                  {record.approval.accepted
                    ? t(
                        "Authorized payer accepted added work.",
                        "Pembayar menyetujui pekerjaan tambahan.",
                      )
                    : t(
                        "Authorized payer chose the original scope only.",
                        "Pembayar memilih lingkup awal saja.",
                      )}{" "}
                  · v{record.approval.version}
                </p>
              )}
            </>
          )}
          {!adviser && stage === "approval" && estimate && !payer && (
            <>
              {stale && (
                <p role="alert">
                  {t(
                    "This approval link has expired. Open the current estimate.",
                    "Tautan persetujuan kedaluwarsa. Buka estimasi terbaru.",
                  )}
                </p>
              )}
              <p>
                {t(
                  "Share the scoped estimate with the authorized payer. The approval records the exact version and total.",
                  "Bagikan estimasi kepada pembayar berwenang. Persetujuan mencatat versi dan total tersebut.",
                )}
              </p>
              <div className="key-actions">
                <button
                  className="key-btn key-btn-minor"
                  onClick={() => {
                    const url = new URL(location.href);
                    url.hash = "payer=" + record.id + ":" + estimate.version;
                    setLink(url.href);
                    navigator.clipboard?.writeText(url.href).catch(() => {});
                  }}
                >
                  <Share2 size={16} aria-hidden="true" />
                  {t("Share approval link", "Bagikan tautan persetujuan")}
                </button>
                <ActionButton onClick={() => openPayer(estimate.version)}>
                  {t(
                    "Open authorized payer view",
                    "Buka tampilan pembayar berwenang",
                  )}
                </ActionButton>
              </div>
              {link && (
                <Field
                  label={t(
                    "Scoped approval link for this demo account on this device",
                    "Tautan untuk akun pembayar di perangkat ini",
                  )}
                >
                  <input
                    value={link}
                    readOnly
                    onFocus={(e) => e.target.select()}
                  />
                </Field>
              )}
            </>
          )}
          {payer && estimate && (
            <div className="key-actions">
              <ActionButton
                onClick={() =>
                  send(
                    {
                      type: "approve",
                      accepted: true,
                      version: estimate.version,
                    },
                    "payer",
                  )
                }
              >
                {t("Approve estimate v", "Setujui estimasi v")}
                {estimate.version}
              </ActionButton>
              <ActionButton
                minor
                onClick={() =>
                  send(
                    {
                      type: "approve",
                      accepted: false,
                      version: estimate.version,
                    },
                    "payer",
                  )
                }
              >
                {t("Keep the original scope", "Lanjutkan lingkup awal")}
              </ActionButton>
            </div>
          )}
          {adviser &&
            ["checkedIn", "approval", "authorized"].includes(stage) && (
              <details
                className="key-details"
                open={stage === "checkedIn" || undefined}
              >
                <summary>
                  {t(
                    "Write additional work estimate",
                    "Tulis estimasi pekerjaan tambahan",
                  )}
                </summary>
                <Field
                  label={t(
                    "Required work and reason",
                    "Pekerjaan wajib dan alasannya",
                  )}
                >
                  <input
                    value={required}
                    onChange={(e) => setRequired(e.target.value)}
                  />
                </Field>
                <Field
                  label={t("Deferrable work", "Pekerjaan yang dapat ditunda")}
                >
                  <input
                    value={deferred}
                    onChange={(e) => setDeferred(e.target.value)}
                  />
                </Field>
                <Field label={t("Available option", "Pilihan tersedia")}>
                  <input
                    value={option}
                    onChange={(e) => setOption(e.target.value)}
                  />
                </Field>
                <Field
                  label={t(
                    "Additional installed price (IDR)",
                    "Harga tambahan terpasang (IDR)",
                  )}
                >
                  <input
                    type="number"
                    min="1"
                    value={amount}
                    onChange={(e) => setAmount(e.target.valueAsNumber)}
                  />
                </Field>
                <ActionButton
                  onClick={() =>
                    send({
                      type: "estimate",
                      required,
                      deferred,
                      option,
                      amount,
                    })
                  }
                >
                  {t("Issue estimate v", "Terbitkan estimasi v")}
                  {record.revision + 1}
                </ActionButton>
              </details>
            )}
          {adviser && (stage === "checkedIn" || stage === "authorized") && (
            <ActionButton minor onClick={() => send({ type: "readyService" })}>
              {t("Mark ready for collection", "Tandai siap diambil")}
            </ActionButton>
          )}
          {adviser && stage === "ready" && (
            <ActionButton onClick={() => send({ type: "closeService" })}>
              {t(
                "Record handover and issue receipt",
                "Catat serah terima dan terbitkan bukti bayar",
              )}
            </ActionButton>
          )}
          {payment && (
            <>
              <dl className="key-metrics">
                <Metric label={t("Customer paid", "Dibayar pelanggan")}>
                  {money(payment.paid)}
                </Metric>
                <Metric label={t("Covered", "Tercakup")}>
                  {money(payment.covered)}
                </Metric>
                <Metric label={t("Reimbursement", "Penggantian")}>
                  {money(payment.reimbursed)}
                </Metric>
              </dl>
              {record.symptom && !record.approval?.accepted && (
                <p>
                  {t(
                    "Next step: book the recommended repair if the reported symptom persists.",
                    "Langkah berikutnya: jadwalkan perbaikan bila gejala masih terasa.",
                  )}
                </p>
              )}
              <p className="key-callout">
                <ReceiptText size={19} aria-hidden="true" />
                {record.funding === "paid" && record.prior === "independent"
                  ? t(
                      "Comparable independent-workshop job recovered.",
                      "Pekerjaan sejenis dari bengkel independen kembali ke Auto2000.",
                    )
                  : record.prior === "auto2000"
                    ? t(
                        "Returning Auto2000 customer.",
                        "Pelanggan kembali ke Auto2000.",
                      )
                    : t(
                        "Vehicle service record updated.",
                        "Riwayat servis kendaraan diperbarui.",
                      )}
              </p>
              <ActionButton
                minor
                onClick={() =>
                  downloadText(record.id + "-receipt.txt", quoteLines)
                }
              >
                {t("Download service receipt", "Unduh bukti servis")}
              </ActionButton>
            </>
          )}
        </Panel>
      </div>
    </>
  );
}
