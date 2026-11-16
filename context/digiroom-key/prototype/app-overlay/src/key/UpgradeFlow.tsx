import { useEffect, useState } from "react";
import {
  BadgeCheck,
  CircleDollarSign,
  FileCheck2,
  KeyRound,
} from "lucide-react";
import {
  isCurrentUpgrade,
  replacements,
  tradeEquity,
  upgradeCashDue,
  type Upgrade,
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
export const upgradeStatus = (t: Text): Record<Upgrade["stage"], string> => ({
  inspection: t("Awaiting vehicle inspection", "Menunggu inspeksi kendaraan"),
  offer: t(
    "Upgrade terms in preparation",
    "Ketentuan pembelian sedang disiapkan",
  ),
  terms: t("Ready for owner acceptance", "Siap disetujui pemilik"),
  accepted: t(
    "Preparing settlement and handover",
    "Menyiapkan pelunasan dan serah terima",
  ),
  settled: t("Settlement recorded", "Pelunasan tercatat"),
  delivered: t(
    "Replacement Toyota delivered",
    "Toyota pengganti telah diserahkan",
  ),
  recovery: t("Replacement terms requested", "Ketentuan pengganti diminta"),
});
const marketLow = 237000000,
  marketHigh = 255000000;
export function UpgradeRequest({
  send,
  marketTrade,
  onPlanner,
}: {
  send: Send;
  marketTrade?: number;
  onPlanner: () => void;
}) {
  const { t, money } = useKey();
  const [trade, setTrade] = useState(true);
  const [consent, setConsent] = useState(true);
  const [replacement, setReplacement] =
    useState<Upgrade["replacement"]>("zenix");
  return (
    <div className="key-split">
      <Panel
        title="Yaris Cross Hybrid"
        eyebrow={t("YOUR VEHICLE RECORD", "RIWAYAT KENDARAAN ANDA")}
      >
        <div className="key-vehicle-symbol">
          <KeyRound size={38} aria-hidden="true" />
        </div>
        <p>2024 · HEV · 24.800 km</p>
        <dl className="key-metrics">
          <Metric label={t("Current market estimate", "Perkiraan nilai pasar")}>
            {marketTrade ? (
              money(marketTrade)
            ) : (
              <>
                {money(marketLow)}–{money(marketHigh)}
              </>
            )}
          </Metric>
        </dl>
        <button type="button" className="key-link" onClick={onPlanner}>
          {t(
            "Open ownership and trade-in planner",
            "Buka perencana kepemilikan dan tukar tambah",
          )}
        </button>
        <p>
          {t(
            "A vehicle inspection confirms condition. The appraiser then issues a written buy offer with an expiry date.",
            "Inspeksi memastikan kondisi kendaraan. Penilai kemudian menerbitkan penawaran beli tertulis dengan tanggal berlaku.",
          )}
        </p>
        <p className="key-callout">
          <FileCheck2 size={20} aria-hidden="true" />
          <span>
            {t(
              "Available to share by consent",
              "Bisa dibagikan dengan persetujuan",
            )}
            <br />
            {t(
              "Scheduled-service receipts and hybrid health record",
              "Bukti servis berkala dan riwayat kondisi hybrid",
            )}
          </span>
        </p>
      </Panel>
      <Panel
        title={t("Choose your replacement Toyota", "Pilih Toyota pengganti")}
        eyebrow={t("EXISTING AUTO2000 CUSTOMER", "PELANGGAN AUTO2000")}
      >
        <Field label={t("Replacement vehicle", "Kendaraan pengganti")}>
          <select
            value={replacement}
            onChange={(e) =>
              setReplacement(e.target.value as Upgrade["replacement"])
            }
          >
            {Object.entries(replacements).map(([id, v]) => (
              <option key={id} value={id}>
                {v.model} · {v.variant}
              </option>
            ))}
          </select>
        </Field>
        <fieldset className="key-choice">
          <legend>
            {t("How would you like to buy?", "Bagaimana Anda ingin membeli?")}
          </legend>
          <label>
            <input
              type="radio"
              name="upgrade-type"
              checked={trade}
              onChange={() => setTrade(true)}
            />
            {t("Trade in my Yaris Cross", "Tukar tambah Yaris Cross")}
          </label>
          <label>
            <input
              type="radio"
              name="upgrade-type"
              checked={!trade}
              onChange={() => setTrade(false)}
            />
            {t("Buy without a trade-in", "Beli tanpa tukar tambah")}
          </label>
        </fieldset>
        {trade && (
          <label className="key-check">
            <input
              type="checkbox"
              checked={consent}
              onChange={(e) => setConsent(e.target.checked)}
            />
            {t(
              "Share service and hybrid health records with the appraiser",
              "Bagikan riwayat servis dan kondisi hybrid kepada penilai",
            )}
          </label>
        )}
        <ActionButton
          onClick={() =>
            send({ type: "requestUpgrade", trade, consent, replacement })
          }
        >
          {trade
            ? t("Request an inspection", "Ajukan inspeksi")
            : t(
                "Request a replacement quote",
                "Minta penawaran kendaraan pengganti",
              )}
        </ActionButton>
      </Panel>
    </div>
  );
}
export function UpgradeRecord({
  record,
  adviser,
  send,
}: {
  record: Upgrade;
  adviser: boolean;
  send: Send;
}) {
  const { t, money, date } = useKey();
  const vehicle = replacements[record.replacement];
  const [offer, setOffer] = useState(248000000);
  const [conditions, setConditions] = useState(
    t(
      "Original documents and both keys. Condition must match the inspector’s report at handover.",
      "Dokumen asli dan kedua kunci. Kondisi saat serah terima harus sesuai laporan inspeksi.",
    ),
  );
  const [evidence, setEvidence] = useState(
    t(
      "Inspection sheet IC-YC-041, scheduled-service receipts and hybrid health result",
      "Lembar inspeksi IC-YC-041, bukti servis berkala, dan hasil pemeriksaan hybrid",
    ),
  );
  const [payoff, setPayoff] = useState(record.trade ? 174000000 : 0);
  const [fee, setFee] = useState(record.trade ? 2500000 : 0);
  const [verified, setVerified] = useState(false);
  const [now, setNow] = useState(Date.now);
  useEffect(() => {
    const timer = window.setInterval(() => setNow(Date.now()), 15000);
    return () => clearInterval(timer);
  }, []);
  const stage = record.stage;
  const offerExpired = !!record.offer && record.offer.expires <= now;
  const expired =
    (stage === "offer" && offerExpired) ||
    (["terms", "accepted"].includes(stage) && !isCurrentUpgrade(record, now));
  const equity =
    record.trade && record.offer
      ? tradeEquity(record.offer.amount, record.payoff, record.fee)
      : 0;
  const cash = upgradeCashDue(vehicle.cash, equity);
  const extraEquity = Math.max(0, equity - vehicle.cash);
  const deposit = Math.min(vehicle.deposit, cash);
  const haveTerms = !!record.quoteAt;
  const stageLabels = [
    t("Inspection", "Inspeksi"),
    t("Buy offer", "Penawaran beli"),
    t("Unit and financing", "Unit dan pembiayaan"),
    t("Settlement", "Pelunasan"),
    t("Delivery", "Serah terima"),
  ];
  const step =
    stage === "delivered"
      ? 4
      : ["accepted", "settled"].includes(stage)
        ? 3
        : stage === "terms"
          ? 2
          : stage === "offer"
            ? 1
            : 0;
  const equityLabel =
    equity < 0
      ? t("Trade-in shortfall", "Kekurangan tukar tambah")
      : equity === 0
        ? t("Net trade-in equity", "Nilai bersih tukar tambah")
        : t("Trade-in equity credit", "Kredit nilai tukar tambah");
  const share = () =>
    downloadText(record.id + "-upgrade-terms.txt", [
      record.id + " · v" + record.revision,
      vehicle.model + " · " + vehicle.variant,
      t("Quote issued", "Penawaran terbit") + ": " + date(record.quoteAt!),
      ...(record.trade && record.offer
        ? [
            t("Appraised buy offer", "Penawaran beli") +
              ": " +
              money(record.offer.amount),
            t("Official old-loan payoff", "Pelunasan kredit lama") +
              ": " +
              money(record.payoff),
            t("Trade-in fees", "Biaya tukar tambah") + ": " + money(record.fee),
            equityLabel + ": " + money(Math.abs(equity)),
            t("Offer expires", "Penawaran berakhir") +
              ": " +
              date(record.offer.expires, true) +
              " WIB",
            record.offer.conditions,
          ]
        : []),
      t("Total cash due", "Total dana awal") + ": " + money(cash),
      t("Deposit applied to cash due", "Uang tanda jadi diperhitungkan") +
        ": " +
        money(deposit),
      t("Monthly instalment", "Cicilan bulanan") +
        ": " +
        money(vehicle.monthly) +
        " × " +
        vehicle.term,
      t(
        "Replacement fees in cash due",
        "Biaya kendaraan pengganti termasuk dana awal",
      ) +
        ": " +
        money(vehicle.fees),
      t("Unit reservation expires", "Reservasi unit berakhir") +
        ": " +
        date(record.reservedUntil!, true) +
        " WIB",
    ]);
  return (
    <>
      <Steps
        items={record.trade ? stageLabels : stageLabels.slice(2)}
        active={record.trade ? step : Math.max(0, step - 2)}
      />
      <div className="key-split">
        <Panel
          title={
            record.trade
              ? t("Your Yaris Cross appraisal", "Penilaian Yaris Cross Anda")
              : t("Direct repurchase", "Pembelian langsung")
          }
          eyebrow={record.id}
        >
          {record.trade && !record.offer && (
            <dl className="key-metrics">
              <Metric label={t("Market estimate", "Perkiraan nilai pasar")}>
                {money(marketLow)}–{money(marketHigh)}
              </Metric>
            </dl>
          )}
          {record.trade && (
            <p>
              {record.consent
                ? t(
                    "Service and hybrid health records shared with appraiser by consent.",
                    "Riwayat servis dan hybrid dibagikan kepada penilai atas persetujuan.",
                  )
                : t(
                    "Appraiser uses the inspection and ownership documents.",
                    "Penilai menggunakan hasil inspeksi dan dokumen kepemilikan.",
                  )}
            </p>
          )}
          {record.offer && (
            <>
              <dl className="key-metrics">
                <Metric
                  label={t(
                    "Inspected buy offer",
                    "Penawaran beli hasil inspeksi",
                  )}
                >
                  {money(record.offer.amount)}
                </Metric>
                <Metric label={t("Offer expires", "Penawaran berakhir")}>
                  {date(record.offer.expires, true)} WIB
                </Metric>
              </dl>
              <p>{record.offer.conditions}</p>
              <p>
                <strong>{t("Evidence accepted", "Bukti diterima")}</strong>
                <br />
                {record.offer.evidence ||
                  t(
                    "Physical inspection and ownership documents",
                    "Inspeksi fisik dan dokumen kepemilikan",
                  )}
              </p>
            </>
          )}
          {adviser && stage === "inspection" && (
            <>
              <p className="key-callout">
                <FileCheck2 size={19} aria-hidden="true" />
                {t(
                  "Inspection bay · Auto2000 Asia Afrika · Yaris Cross Hybrid",
                  "Ruang inspeksi · Auto2000 Asia Afrika · Yaris Cross Hybrid",
                )}
              </p>
              <Field
                label={t(
                  "Appraiser buy offer (IDR)",
                  "Penawaran beli penilai (IDR)",
                )}
              >
                <input
                  type="number"
                  min="1"
                  value={offer}
                  onChange={(e) => setOffer(e.target.valueAsNumber)}
                />
              </Field>
              {record.consent && (
                <Field
                  label={t(
                    "Evidence accepted by the appraiser",
                    "Bukti yang diterima penilai",
                  )}
                >
                  <input
                    value={evidence}
                    onChange={(e) => setEvidence(e.target.value)}
                  />
                </Field>
              )}
              <Field label={t("Offer conditions", "Syarat penawaran")}>
                <textarea
                  rows={2}
                  value={conditions}
                  onChange={(e) => setConditions(e.target.value)}
                />
              </Field>
              <ActionButton
                onClick={() =>
                  send({
                    type: "issueOffer",
                    amount: offer,
                    conditions,
                    evidence,
                  })
                }
              >
                {t(
                  "Issue inspected buy offer",
                  "Terbitkan penawaran beli hasil inspeksi",
                )}
              </ActionButton>
            </>
          )}
          <History events={record.history} />
        </Panel>
        <Panel
          title={
            expired
              ? t(
                  "Deal needs a new offer or unit",
                  "Transaksi memerlukan penawaran atau unit baru",
                )
              : upgradeStatus(t)[stage]
          }
          eyebrow={vehicle.model + " · " + vehicle.variant}
        >
          {record.refund !== undefined && (
            <p className="key-callout">
              {t(
                "Deposit refund recorded",
                "Pengembalian uang tanda jadi tercatat",
              )}{" "}
              · {money(record.refund)}
            </p>
          )}
          {adviser && stage === "offer" && !expired && (
            <>
              {record.trade && (
                <>
                  <p>
                    {t(
                      "Lender payoff statement",
                      "Surat pelunasan pemberi pembiayaan",
                    )}{" "}
                    · PAYOFF-YC-041
                  </p>
                  <div className="key-form-grid">
                    <Field
                      label={t(
                        "Official old-loan payoff (IDR)",
                        "Pelunasan kredit lama resmi (IDR)",
                      )}
                    >
                      <input
                        type="number"
                        min="0"
                        value={payoff}
                        onChange={(e) => setPayoff(e.target.valueAsNumber)}
                      />
                    </Field>
                    <Field
                      label={t(
                        "Trade-in fees (IDR)",
                        "Biaya tukar tambah (IDR)",
                      )}
                    >
                      <input
                        type="number"
                        min="0"
                        value={fee}
                        onChange={(e) => setFee(e.target.valueAsNumber)}
                      />
                    </Field>
                  </div>
                </>
              )}
              <p>
                <strong>
                  {t(
                    "Unit available to reserve",
                    "Unit tersedia untuk dipesan",
                  )}
                </strong>{" "}
                · {vehicle.unit} ·{" "}
                {t("Auto2000 Bandung stock", "Stok Auto2000 Bandung")}
              </p>
              <label className="key-check">
                <input
                  type="checkbox"
                  checked={verified}
                  onChange={(e) => setVerified(e.target.checked)}
                />
                {t(
                  "Lender conditions, exact unit and refundable deposit confirmed",
                  "Syarat pembiayaan, unit, dan pengembalian tanda jadi dikonfirmasi",
                )}
              </label>
              <ActionButton
                disabled={!verified}
                onClick={() => send({ type: "upgradeTerms", payoff, fee })}
              >
                {t(
                  "Reserve unit and issue upgrade terms",
                  "Pesan unit dan terbitkan ketentuan",
                )}
              </ActionButton>
            </>
          )}
          {haveTerms && !expired && (
            <>
              <p>
                <strong>{record.unit}</strong> · {t("Quote", "Penawaran")} v
                {record.revision} · {date(record.quoteAt!)}
                {record.reservedUntil && (
                  <>
                    <br />
                    {t("Reserved until", "Dipesan hingga")}{" "}
                    {date(record.reservedUntil, true)} WIB
                  </>
                )}
              </p>
              {record.trade && (
                <dl className="key-metrics">
                  <Metric label={t("Official payoff", "Pelunasan resmi")}>
                    {money(record.payoff)}
                  </Metric>
                  <Metric label={t("Trade-in fees", "Biaya tukar tambah")}>
                    {money(record.fee)}
                  </Metric>
                  <Metric label={equityLabel}>{money(Math.abs(equity))}</Metric>
                </dl>
              )}
              <dl className="key-metrics key-finance-metrics">
                <Metric
                  label={t(
                    "Replacement on-road price",
                    "Harga on-road kendaraan pengganti",
                  )}
                >
                  {money(vehicle.otr)}
                </Metric>
                <Metric
                  label={t(
                    "Cash due before trade-in",
                    "Dana awal sebelum tukar tambah",
                  )}
                >
                  {money(vehicle.cash)}
                </Metric>
                <Metric label={t("Total cash due", "Total dana awal")}>
                  {money(cash)}
                </Metric>
                <Metric label={t("Monthly instalment", "Cicilan bulanan")}>
                  {money(vehicle.monthly)}
                </Metric>
                <Metric label={t("Term", "Tenor")}>
                  {vehicle.term} {t("months", "bulan")}
                </Metric>
                <Metric
                  label={t(
                    "Replacement fees included in cash",
                    "Biaya kendaraan pengganti termasuk dana awal",
                  )}
                >
                  {money(vehicle.fees)}
                </Metric>
                <Metric
                  label={t(
                    "Deposit included in cash due",
                    "Tanda jadi termasuk dana awal",
                  )}
                >
                  {money(deposit)}
                </Metric>
                {vehicle.balloon > 0 && (
                  <Metric label={t("Balloon payment", "Pembayaran balon")}>
                    {money(vehicle.balloon)}
                  </Metric>
                )}
              </dl>
              {extraEquity > 0 && (
                <p>
                  {t(
                    "Equity remaining after cash due",
                    "Sisa nilai tukar tambah setelah dana awal",
                  )}
                  : {money(extraEquity)}
                </p>
              )}
              <p className="key-callout">
                <CircleDollarSign size={20} aria-hidden="true" />
                {t(
                  "Lender approved with signed documents and deposit. Deposit refundable if the reserved unit becomes unavailable.",
                  "Pembiayaan disetujui dengan dokumen bertanda tangan dan tanda jadi. Tanda jadi dikembalikan jika unit tidak tersedia.",
                )}
              </p>
              <div className="key-actions">
                <ActionButton minor onClick={share}>
                  {t("Download upgrade terms", "Unduh ketentuan pembelian")}
                </ActionButton>
                {!adviser && stage === "terms" && (
                  <ActionButton
                    onClick={() =>
                      send({ type: "acceptUpgrade", revision: record.revision })
                    }
                  >
                    {t(
                      "Accept current upgrade terms",
                      "Setujui ketentuan pembelian",
                    )}
                  </ActionButton>
                )}
              </div>
            </>
          )}
          {adviser && stage === "accepted" && !expired && (
            <>
              <p>
                {t("Deposit recorded", "Tanda jadi tercatat")} ·{" "}
                {money(record.depositPaid ?? 0)}.{" "}
                {record.trade
                  ? t(
                      "Send payoff to the old lender and match its release to the incoming Yaris Cross.",
                      "Lunasi kredit lama dan cocokkan surat pelepasan dengan Yaris Cross yang diterima.",
                    )
                  : t(
                      "Confirm deposit allocation to the replacement order.",
                      "Konfirmasi tanda jadi untuk pesanan kendaraan pengganti.",
                    )}
              </p>
              <ActionButton onClick={() => send({ type: "settleUpgrade" })}>
                {t("Record settlement", "Catat pelunasan")}
              </ActionButton>
            </>
          )}
          {adviser && stage === "settled" && (
            <ActionButton onClick={() => send({ type: "deliverUpgrade" })}>
              {record.trade
                ? t("Confirm both handovers", "Konfirmasi kedua serah terima")
                : t(
                    "Confirm replacement delivery",
                    "Konfirmasi serah terima kendaraan",
                  )}
            </ActionButton>
          )}
          {adviser && ["offer", "terms", "accepted"].includes(stage) && (
            <details className="key-details" open={expired || undefined}>
              <summary>
                {t(
                  "Offer expired or unit unavailable",
                  "Penawaran berakhir atau unit tidak tersedia",
                )}
              </summary>
              <p>
                {t(
                  "Release the unit, withdraw the stale terms and record any refund before reopening.",
                  "Lepaskan unit, tarik ketentuan lama, dan catat pengembalian sebelum membuka kembali.",
                )}
              </p>
              <ActionButton
                minor
                onClick={() => send({ type: "recoverUpgrade" })}
              >
                {t(
                  "Withdraw terms and record refund",
                  "Tarik ketentuan dan catat pengembalian",
                )}
              </ActionButton>
            </details>
          )}
          {adviser && stage === "recovery" && (
            <ActionButton onClick={() => send({ type: "reopenUpgrade" })}>
              {t("Arrange new terms", "Siapkan ketentuan baru")}
            </ActionButton>
          )}
          {stage === "delivered" && (
            <p className="key-callout">
              <BadgeCheck size={23} aria-hidden="true" />
              {record.trade
                ? t(
                    "Old-loan settlement, trade-in and replacement handovers recorded.",
                    "Pelunasan kredit lama, tukar tambah, dan serah terima kendaraan pengganti tercatat.",
                  )
                : t(
                    "Replacement delivered to an existing Auto2000 customer.",
                    "Kendaraan pengganti diserahkan kepada pelanggan Auto2000.",
                  )}
            </p>
          )}
        </Panel>
      </div>
    </>
  );
}
