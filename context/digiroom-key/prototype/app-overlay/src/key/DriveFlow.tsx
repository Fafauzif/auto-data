import { useState } from "react";
import {
  CalendarDays,
  CarFront,
  ClipboardCheck,
  Download,
  MoveUpRight,
} from "lucide-react";
import { BRANCHES } from "../branches";
import {
  driveWindow,
  indonesiaDay,
  seedBrief,
  type Brief,
  type CheckResult,
  type Drive,
  type DriveKind,
} from "./state";
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
const checkLabels = (t: Text): Record<CheckResult, string> => ({
  pass: t("Works for us", "Cocok untuk kami"),
  adjust: t("Needs an adjustment", "Perlu penyesuaian"),
  pending: t("Try again", "Coba lagi"),
});
const defaultBranch = "Auto2000 Asia Afrika";
const modes = (t: Text): Record<DriveKind, string> => ({
  life: t("48-Hour Life Test", "Tes Keseharian 48 Jam"),
  standard: t("Standard drive", "Uji kendara standar"),
});
export const driveStatus = (t: Text): Record<Drive["stage"], string> => ({
  requested: t("Awaiting branch confirmation", "Menunggu konfirmasi cabang"),
  alternative: t(
    "Alternative drive offered",
    "Alternatif uji kendara ditawarkan",
  ),
  confirmed: t("Drive confirmed", "Uji kendara dikonfirmasi"),
  out: t("On the Life Test", "Sedang menjalani uji kendara"),
  returned: t("Drive completed", "Uji kendara selesai"),
  quoted: t("Quote ready for buyer", "Penawaran siap untuk pembeli"),
  accepted: t("Awaiting lender decision", "Menunggu keputusan pembiayaan"),
  financed: t("Lender decision recorded", "Keputusan pembiayaan tercatat"),
  ordered: t("Preparing your Toyota", "Toyota Anda sedang disiapkan"),
  delivered: t("Toyota delivered", "Toyota telah diserahkan"),
});
const defaultChecks = (t: Text) => [
  t(seedBrief.checks[0], "Buka pintu bagasi di garasi 3,10 × 5,60 m"),
  t(seedBrief.checks[1], "Coba akses baris ketiga dengan kursi anak terpasang"),
  t(
    seedBrief.checks[2],
    "Muat dua tas untuk keluarga beranggotakan lima orang",
  ),
];
function CheckCard({
  brief,
  onStudio,
  results,
}: {
  brief: Brief;
  onStudio?: () => void;
  results?: CheckResult[];
}) {
  const { t } = useKey();
  const checks = brief === seedBrief ? defaultChecks(t) : brief.checks;
  return (
    <section className="key-visit-card">
      <div className="key-visit-head">
        <ClipboardCheck size={25} aria-hidden="true" />
        <div>
          <span>{t("HOUSEHOLD VISIT CARD", "KARTU KUNJUNGAN KELUARGA")}</span>
          <h2>{brief.model}</h2>
          <p>
            {brief.variant} · {brief.powertrain}
          </p>
        </div>
      </div>
      <ul>
        {checks.map((check, i) => (
          <li key={i}>
            {check}
            {results && (
              <small className="key-check-outcome">
                {checkLabels(t)[results[i]]}
              </small>
            )}
          </li>
        ))}
      </ul>
      <p className="key-visit-planning">
        {brief === seedBrief
          ? t(
              brief.planning,
              "250 km/minggu · Pertamax Rp15.950/L · asumsi 5,5 L/100 km · perkiraan Rp219.313/minggu",
            )
          : brief.planning}
      </p>
      <div className="key-actions">
        <button
          className="key-link"
          onClick={() =>
            downloadText("Digiroom-Life-Test.txt", [
              brief.model + " · " + brief.variant,
              ...checks,
              brief.planning,
            ])
          }
        >
          <Download size={16} aria-hidden="true" />
          {t("Download visit card", "Unduh kartu kunjungan")}
        </button>
        {onStudio && (
          <button className="key-link" onClick={onStudio}>
            <MoveUpRight size={16} aria-hidden="true" />
            {t("Edit in 3D studio", "Ubah di studio 3D")}
          </button>
        )}
      </div>
    </section>
  );
}
export function DriveRequest({
  brief = seedBrief,
  preferred,
  onStudio,
  send,
}: {
  brief?: Brief;
  preferred?: { branch: string; date: string };
  onStudio: () => void;
  send: Send;
}) {
  const { t } = useKey();
  const [kind, setKind] = useState<DriveKind>("life");
  const [branch, setBranch] = useState(
    preferred?.branch ??
      (brief.powertrain === "BEV" ? "Auto2000 Pasteur" : defaultBranch),
  );
  const [requested, setDate] = useState(() =>
    preferred?.date && preferred.date >= indonesiaDay()
      ? preferred.date
      : indonesiaDay(1),
  );
  const [shortlist, setShortlist] = useState(true);
  const [firstToyota, setFirstToyota] = useState(false);
  const [firstXev, setFirstXev] = useState(true);
  const [firstAuto2000, setFirstAuto2000] = useState(true);
  return (
    <div className="key-split">
      <CheckCard brief={brief} onStudio={onStudio} />
      <Panel
        title={t(
          "Take your checklist on the road",
          "Bawa daftar cek saat uji kendara",
        )}
        eyebrow={t("MATCH YOUR ROUTINE", "SESUAIKAN DENGAN RUTINITAS")}
      >
        <fieldset className="key-choice">
          <legend>{t("Drive format", "Format uji kendara")}</legend>
          {(["life", "standard"] as const).map((value) => (
            <label key={value}>
              <input
                type="radio"
                name="drive-format"
                checked={kind === value}
                onChange={() => setKind(value)}
              />
              {modes(t)[value]}
            </label>
          ))}
        </fieldset>
        <div className="key-form-grid">
          <Field label={t("Preferred branch", "Cabang pilihan")}>
            <select
              value={branch}
              onChange={(event) => setBranch(event.target.value)}
            >
              {BRANCHES.map((b) => (
                <option key={b.id}>{b.name}</option>
              ))}
            </select>
          </Field>
          <Field
            label={t("Preferred pickup date", "Tanggal pengambilan pilihan")}
          >
            <input
              type="date"
              min={indonesiaDay()}
              value={requested}
              onChange={(event) => setDate(event.target.value)}
            />
          </Field>
        </div>
        {kind === "life" && (
          <label className="key-check">
            <input
              type="checkbox"
              checked={shortlist}
              onChange={(event) => setShortlist(event.target.checked)}
            />
            {t(
              "Shortlisted buyer with a valid driving licence",
              "Calon pembeli terpilih dengan SIM aktif",
            )}
          </label>
        )}
        <details className="key-details">
          <summary>{t("Purchase history", "Riwayat pembelian")}</summary>
          <label className="key-check">
            <input
              type="checkbox"
              checked={firstToyota}
              onChange={(e) => setFirstToyota(e.target.checked)}
            />
            {t("First Toyota", "Toyota pertama")}
          </label>
          <label className="key-check">
            <input
              type="checkbox"
              checked={firstXev}
              onChange={(e) => setFirstXev(e.target.checked)}
            />
            {t("First xEV", "xEV pertama")}
          </label>
          <label className="key-check">
            <input
              type="checkbox"
              checked={firstAuto2000}
              onChange={(e) => setFirstAuto2000(e.target.checked)}
            />
            {t("First Auto2000 purchase", "Pembelian pertama di Auto2000")}
          </label>
        </details>
        <ActionButton
          onClick={() =>
            send({
              type: "requestDrive",
              brief,
              kind,
              branch,
              requested,
              shortlist,
              firstToyota,
              firstXev,
              firstAuto2000,
            })
          }
        >
          {t("Send to sales adviser", "Kirim ke penasihat penjualan")}
        </ActionButton>
        <p className="key-muted">
          {t(
            "The branch checks driver eligibility, exact variant and the demonstrator calendar.",
            "Cabang memeriksa kelayakan pengemudi, varian, dan kalender unit uji.",
          )}
        </p>
      </Panel>
    </div>
  );
}
export function DriveRecord({
  record,
  adviser,
  send,
}: {
  record: Drive;
  adviser: boolean;
  send: Send;
}) {
  const { t, date, money } = useKey();
  const [results, setResults] = useState(
    record.results ??
      t(
        "Tailgate clears at home. Third-row access works with the child seat in place.",
        "Bagasi bisa dibuka di rumah. Baris ketiga dapat diakses dengan kursi anak terpasang.",
      ),
  );
  const [checks, setChecks] = useState<CheckResult[]>(
    record.checkResults ?? record.brief.checks.map(() => "pass"),
  );
  const [condition, setCondition] = useState(
    t(
      "Clean exterior and cabin; no visible damage",
      "Bodi dan kabin bersih, tidak ada kerusakan terlihat",
    ),
  );
  const [odometer, setOdometer] = useState(1842);
  const [level, setLevel] = useState(82);
  const [checked, setChecked] = useState(false);
  const [buyer, setBuyer] = useState(false);
  const reference = record.brief.referencePrice ?? 0;
  const [cash, setCash] = useState(() => Math.round(reference * 0.24));
  const [monthly, setMonthly] = useState(() =>
    Math.round(((reference * 0.76) / 48) * 1.2),
  );
  const [term, setTerm] = useState(48);
  const [fees, setFees] = useState(4500000);
  const [altKind, setAltKind] = useState<DriveKind>("standard");
  const [altBranch, setAltBranch] = useState(record.branch);
  const [altDate, setAltDate] = useState(() => indonesiaDay(5));
  const stage = record.stage,
    w = record.window,
    q = record.quote;
  const recordDay = indonesiaDay(4, record.history[0].at);
  const blocked = driveWindow(
    "FLEET-BDG-01",
    defaultBranch,
    recordDay,
    "life",
    "HEV",
    seedBrief.variant,
  );
  const progress =
    stage === "delivered"
      ? 4
      : ["quoted", "accepted", "financed", "ordered"].includes(stage)
        ? 3
        : ["out", "returned"].includes(stage)
          ? 2
          : ["confirmed", "alternative"].includes(stage)
            ? 1
            : 0;
  const quoteLines = q
    ? [
        record.id + " · v" + record.revision,
        record.brief.model + " · " + record.brief.variant,
        date(q.issued),
        t("Cash due", "Dana awal") + ": " + money(q.cash),
        t("Monthly payment", "Cicilan bulanan") + ": " + money(q.monthly),
        t("Term", "Tenor") + ": " + q.term,
        t("Fees included in cash due", "Biaya termasuk dalam dana awal") +
          ": " +
          money(q.fees),
        record.brief.planning,
      ]
    : [];
  return (
    <>
      <Steps
        items={[
          t("Request", "Permintaan"),
          t("Drive booked", "Jadwal uji"),
          t("Try your routine", "Coba rutinitas"),
          t("Purchase quote", "Penawaran"),
          t("Delivery", "Serah terima"),
        ]}
        active={progress}
      />
      <div className="key-split">
        <CheckCard brief={record.brief} results={record.checkResults} />
        <Panel title={driveStatus(t)[stage]} eyebrow={record.id}>
          <dl className="key-metrics">
            <Metric label={t("Drive format", "Format uji")}>
              {modes(t)[w?.kind ?? record.kind]}
            </Metric>
            <Metric label={t("Branch", "Cabang")}>
              {w?.branch ?? record.branch}
            </Metric>
            <Metric
              label={
                w
                  ? t("Pickup", "Pengambilan")
                  : t("Requested", "Tanggal pilihan")
              }
            >
              {w
                ? date(w.start, true) + " WIB"
                : date(Date.parse(record.requested + "T12:00:00+07:00"))}
            </Metric>
            {w && (
              <Metric label={t("Return by", "Kembali sebelum")}>
                {date(w.returnAt, true)} WIB
              </Metric>
            )}
          </dl>
          {w && (
            <details className="key-details">
              <summary>
                {t(
                  "Driver terms and branch contact",
                  "Ketentuan pengemudi dan kontak cabang",
                )}
              </summary>
              <p>
                {w.kind === "life"
                  ? t(
                      "Bring your licence. The named driver has branch fleet coverage under the signed agreement. Stay within 250 km in Greater Bandung, use the car privately, and return it to the same desk. Contact Raka at the Life Test desk through this request.",
                      "Bawa SIM. Pengemudi terdaftar mendapat perlindungan armada sesuai perjanjian. Batas 250 km di Bandung Raya, penggunaan pribadi, dan kembali ke meja yang sama. Hubungi Raka di meja Tes Keseharian melalui permintaan ini.",
                    )
                  : t(
                      "Bring your licence and meet Raka at the sales desk. An adviser joins the drive and checks your household questions.",
                      "Bawa SIM dan temui Raka di meja penjualan. Penasihat mendampingi uji kendara dan memeriksa kebutuhan keluarga.",
                    )}
              </p>
              <p>
                {t("Demonstrator", "Unit uji")}: {w.unit}
              </p>
              {adviser && (
                <p>
                  {t(
                    "Available after turnaround",
                    "Tersedia setelah persiapan",
                  )}
                  : {date(w.end, true)} WIB
                </p>
              )}
            </details>
          )}
          {adviser && stage === "requested" && (
            <>
              <p className="key-callout">
                <CalendarDays size={21} aria-hidden="true" />
                <span>
                  {t("Demonstrator calendar", "Kalender unit uji")} ·{" "}
                  {defaultBranch}
                  <br />
                  {seedBrief.variant} · {date(blocked.start, true)} –{" "}
                  {date(blocked.end, true)} WIB ·{" "}
                  {t(
                    "Reserved through turnaround",
                    "Dipesan hingga persiapan selesai",
                  )}
                </span>
              </p>
              <ActionButton
                onClick={() =>
                  send({
                    type: "confirmDrive",
                    alternative: false,
                    window: driveWindow(
                      record.id,
                      record.branch,
                      record.requested,
                      record.kind,
                      record.brief.powertrain,
                      record.brief.variant,
                    ),
                  })
                }
              >
                {t("Confirm requested drive", "Konfirmasi uji kendara")}
              </ActionButton>
              <details className="key-details">
                <summary>
                  {t(
                    "Offer a different branch, date or drive",
                    "Tawarkan cabang, tanggal, atau jenis uji lain",
                  )}
                </summary>
                <div className="key-form-grid">
                  <Field label={t("Alternative branch", "Cabang alternatif")}>
                    <select
                      value={altBranch}
                      onChange={(e) => setAltBranch(e.target.value)}
                    >
                      {BRANCHES.map((b) => (
                        <option key={b.id}>{b.name}</option>
                      ))}
                    </select>
                  </Field>
                  <Field label={t("Alternative date", "Tanggal alternatif")}>
                    <input
                      type="date"
                      value={altDate}
                      min={indonesiaDay()}
                      onChange={(e) => setAltDate(e.target.value)}
                    />
                  </Field>
                  <Field label={t("Alternative format", "Format alternatif")}>
                    <select
                      value={altKind}
                      onChange={(e) => setAltKind(e.target.value as DriveKind)}
                    >
                      {Object.entries(modes(t)).map(([value, label]) => (
                        <option key={value} value={value}>
                          {label}
                        </option>
                      ))}
                    </select>
                  </Field>
                </div>
                <ActionButton
                  onClick={() =>
                    send({
                      type: "confirmDrive",
                      alternative: true,
                      window: driveWindow(
                        record.id,
                        altBranch,
                        altDate,
                        altKind,
                        record.brief.powertrain,
                        record.brief.variant,
                      ),
                    })
                  }
                >
                  {t("Send alternative drive", "Kirim alternatif uji kendara")}
                </ActionButton>
              </details>
            </>
          )}
          {!adviser && stage === "alternative" && (
            <ActionButton onClick={() => send({ type: "acceptAlternative" })}>
              {t("Accept alternative drive", "Terima alternatif uji kendara")}
            </ActionButton>
          )}
          {adviser && stage === "confirmed" && (
            <>
              <div className="key-form-grid">
                <Field label={t("Odometer (km)", "Odometer (km)")}>
                  <input
                    type="number"
                    min="0"
                    value={odometer}
                    onChange={(e) => setOdometer(e.target.valueAsNumber)}
                  />
                </Field>
                <Field
                  label={t("Fuel or charge (%)", "Bahan bakar atau daya (%)")}
                >
                  <input
                    type="number"
                    min="0"
                    max="100"
                    value={level}
                    onChange={(e) => setLevel(e.target.valueAsNumber)}
                  />
                </Field>
              </div>
              <Field label={t("Vehicle condition", "Kondisi kendaraan")}>
                <input
                  value={condition}
                  onChange={(e) => setCondition(e.target.value)}
                />
              </Field>
              <label className="key-check">
                <input
                  type="checkbox"
                  checked={checked}
                  onChange={(e) => setChecked(e.target.checked)}
                />
                {t(
                  "Licence, coverage, use limits and return procedure checked",
                  "SIM, perlindungan, batas penggunaan, dan prosedur kembali sudah diperiksa",
                )}
              </label>
              <ActionButton
                disabled={!checked}
                onClick={() =>
                  send({ type: "pickup", condition, odometer, level, checked })
                }
              >
                {t("Record vehicle pickup", "Catat pengambilan unit uji")}
              </ActionButton>
            </>
          )}
          {record.condition && (
            <p className="key-callout">
              <CarFront size={20} aria-hidden="true" />
              <span>
                {t("Pickup record", "Catatan pengambilan")} · {record.odometer}{" "}
                km · {record.level}%<br />
                {record.condition}
              </span>
            </p>
          )}
          {!adviser && stage === "out" && (
            <>
              <details className="key-details">
                <summary>
                  {t("Mark each household check", "Tandai setiap cek keluarga")}
                </summary>
                {record.brief.checks.map((check, index) => (
                  <Field key={index} label={check}>
                    <select
                      value={checks[index]}
                      onChange={(event) =>
                        setChecks(
                          checks.map((item, i) =>
                            i === index
                              ? (event.target.value as CheckResult)
                              : item,
                          ),
                        )
                      }
                    >
                      {Object.entries(checkLabels(t)).map(([value, label]) => (
                        <option key={value} value={value}>
                          {label}
                        </option>
                      ))}
                    </select>
                  </Field>
                ))}
              </details>
              <Field
                label={t(
                  "How did the car fit your routine?",
                  "Bagaimana mobil cocok dengan rutinitas Anda?",
                )}
              >
                <textarea
                  value={results}
                  rows={3}
                  onChange={(e) => setResults(e.target.value)}
                />
              </Field>
              <ActionButton
                disabled={
                  !results.trim() ||
                  (record.results === results.trim() &&
                    checks.every(
                      (flag, index) => record.checkResults?.[index] === flag,
                    ))
                }
                onClick={() => send({ type: "saveResult", results, checks })}
              >
                {t("Save household results", "Simpan hasil keluarga")}
              </ActionButton>
            </>
          )}
          {record.results && (
            <p>
              <strong>{t("Household results", "Hasil keluarga")}</strong>
              <br />
              {record.results}
            </p>
          )}
          {adviser && stage === "out" && (
            <ActionButton
              disabled={!record.results}
              onClick={() => send({ type: "returnDrive" })}
            >
              {t("Accept vehicle return", "Terima pengembalian kendaraan")}
            </ActionButton>
          )}
          {adviser && stage === "returned" && (
            <>
              <p>
                {t("Purchase terms for", "Ketentuan pembelian untuk")}{" "}
                <strong>{record.brief.variant}</strong>
              </p>
              <div className="key-form-grid">
                <Field label={t("Cash due (IDR)", "Dana awal (IDR)")}>
                  <input
                    type="number"
                    min="0"
                    value={cash}
                    onChange={(e) => setCash(e.target.valueAsNumber)}
                  />
                </Field>
                <Field
                  label={t("Monthly payment (IDR)", "Cicilan bulanan (IDR)")}
                >
                  <input
                    type="number"
                    min="0"
                    value={monthly}
                    onChange={(e) => setMonthly(e.target.valueAsNumber)}
                  />
                </Field>
                <Field label={t("Term in months", "Tenor dalam bulan")}>
                  <input
                    type="number"
                    min="1"
                    value={term}
                    onChange={(e) => setTerm(e.target.valueAsNumber)}
                  />
                </Field>
                <Field
                  label={t(
                    "Fees included in cash due (IDR)",
                    "Biaya termasuk dana awal (IDR)",
                  )}
                >
                  <input
                    type="number"
                    min="0"
                    value={fees}
                    onChange={(e) => setFees(e.target.valueAsNumber)}
                  />
                </Field>
              </div>
              <ActionButton
                onClick={() =>
                  send({
                    type: "quoteDrive",
                    terms: { cash, monthly, term, fees },
                  })
                }
              >
                {t(
                  "Issue dated purchase quote",
                  "Terbitkan penawaran pembelian bertanggal",
                )}
              </ActionButton>
            </>
          )}
          {q && !adviser && !buyer && (
            <ActionButton onClick={() => setBuyer(true)}>
              {t("Open household buyer view", "Buka tampilan pembeli keluarga")}
            </ActionButton>
          )}
          {q && (adviser || buyer) && (
            <>
              <h3>
                {t("Purchase quote", "Penawaran pembelian")} · v
                {record.revision} · {date(q.issued)}
              </h3>
              <p>
                {record.brief.variant} ·{" "}
                {["financed", "ordered", "delivered"].includes(stage)
                  ? t(
                      "Lender decision recorded",
                      "Keputusan pembiayaan tercatat",
                    )
                  : t(
                      "Awaiting lender decision",
                      "Menunggu keputusan pembiayaan",
                    )}
              </p>
              <dl className="key-metrics">
                <Metric label={t("Cash due", "Dana awal")}>
                  {money(q.cash)}
                </Metric>
                <Metric label={t("Monthly payment", "Cicilan bulanan")}>
                  {money(q.monthly)}
                </Metric>
                <Metric label={t("Term", "Tenor")}>
                  {q.term} {t("months", "bulan")}
                </Metric>
                <Metric
                  label={t(
                    "Fees included in cash due",
                    "Biaya termasuk dana awal",
                  )}
                >
                  {money(q.fees)}
                </Metric>
              </dl>
              <div className="key-actions">
                <ActionButton
                  minor
                  onClick={() =>
                    downloadText(record.id + "-purchase-quote.txt", quoteLines)
                  }
                >
                  {t("Download buyer copy", "Unduh salinan pembeli")}
                </ActionButton>
                {!adviser && stage === "quoted" && (
                  <ActionButton
                    onClick={() => send({ type: "acceptDriveQuote" })}
                  >
                    {t("Accept purchase quote", "Terima penawaran pembelian")}
                  </ActionButton>
                )}
              </div>
            </>
          )}
          {adviser && stage === "accepted" && (
            <ActionButton onClick={() => send({ type: "financeDrive" })}>
              {t(
                "Record lender decision",
                "Catat keputusan pemberi pembiayaan",
              )}
            </ActionButton>
          )}
          {adviser && stage === "financed" && (
            <ActionButton onClick={() => send({ type: "orderDrive" })}>
              {t("Record vehicle order", "Catat pesanan kendaraan")}
            </ActionButton>
          )}
          {adviser && stage === "ordered" && (
            <ActionButton onClick={() => send({ type: "deliverDrive" })}>
              {t("Confirm Toyota delivery", "Konfirmasi serah terima Toyota")}
            </ActionButton>
          )}
          {stage === "delivered" && (
            <p className="key-callout">
              {record.firstAuto2000
                ? t(
                    "First Auto2000 delivery recorded.",
                    "Serah terima Auto2000 pertama tercatat.",
                  )
                : t(
                    "Returning Auto2000 buyer took delivery.",
                    "Pembeli lama Auto2000 menerima kendaraan.",
                  )}{" "}
              {t("First Toyota", "Toyota pertama")}{" "}
              {record.firstToyota ? t("yes", "ya") : t("no", "tidak")} ·{" "}
              {t("First xEV", "xEV pertama")}{" "}
              {record.firstXev ? t("yes", "ya") : t("no", "tidak")}.
            </p>
          )}
          <History events={record.history} />
        </Panel>
      </div>
    </>
  );
}
