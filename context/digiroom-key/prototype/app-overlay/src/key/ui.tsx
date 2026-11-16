import { createContext, useContext, type ReactNode } from "react";
import { ArrowRight, Check } from "lucide-react";
import type { Language } from "../types";
import {
  type Action,
  type Actor,
  type ErrorCode,
  type Journey,
  type Log,
} from "./state";
export type Text = (en: string, id: string) => string;
export const KeyLanguage = createContext<Language>("en");
export function useKey() {
  const lang = useContext(KeyLanguage);
  const t: Text = (en, id) => (lang === "id" ? id : en);
  const display = lang === "id" ? "id-ID" : "en-ID";
  const money = (amount: number) =>
    new Intl.NumberFormat(display, {
      style: "currency",
      currency: "IDR",
      maximumFractionDigits: 0,
    }).format(amount);
  const decimal = (amount: number, places = 1) =>
    new Intl.NumberFormat(display, {
      maximumFractionDigits: places,
      minimumFractionDigits: places,
    }).format(amount);
  const date = (at: number, time = false) =>
    new Intl.DateTimeFormat(display, {
      timeZone: "Asia/Jakarta",
      dateStyle: "medium",
      ...(time ? { timeStyle: "short" } : {}),
    }).format(at);
  return { lang, t, money, decimal, date };
}
export const journeyNames = (t: Text): Record<Journey, string> => ({
  K: t("Know Your Fit", "Kenali Kecocokan"),
  E: t("Easy Service", "Servis Mudah"),
  Y: t("Your Next Toyota", "Toyota Berikutnya"),
});
export const roles = (t: Text): Record<Actor, string> => ({
  customer: t("Customer", "Pelanggan"),
  sales: t("Sales adviser", "Penasihat penjualan"),
  workshop: t("Workshop adviser", "Penasihat bengkel"),
  upgrade: t("Upgrade adviser", "Penasihat tukar tambah"),
  payer: t("Authorized payer", "Pembayar berwenang"),
});
export const errorLabels = (t: Text): Record<ErrorCode, string> => ({
  action: t(
    "This action is unavailable at the current step. Refresh the request and check its status.",
    "Tindakan ini belum tersedia. Muat ulang permintaan dan periksa statusnya.",
  ),
  overlap: t(
    "The demonstrator is already reserved through its turnaround window. Offer another date or branch.",
    "Unit uji sudah dipesan hingga persiapan selesai. Tawarkan tanggal atau cabang lain.",
  ),
  terms: t(
    "This variant, branch or driver is ineligible for a take-home slot. Offer an eligible branch or a standard drive.",
    "Varian, cabang, atau pengemudi belum memenuhi syarat tes bawa pulang. Tawarkan cabang lain atau uji standar.",
  ),
  stale: t(
    "The terms have changed. Open the current version to continue.",
    "Ketentuan telah berubah. Buka versi terbaru untuk melanjutkan.",
  ),
  expired: t(
    "This window has expired. Ask the adviser to arrange a new one.",
    "Waktu berlaku habis. Minta penasihat mengatur jadwal atau penawaran baru.",
  ),
  details: t(
    "Please complete the required details before continuing.",
    "Lengkapi rincian wajib sebelum melanjutkan.",
  ),
});
export type Send = (action: Action, actor?: "payer") => boolean;
export function Panel({
  title,
  eyebrow,
  children,
  className = "",
}: {
  title: string;
  eyebrow?: string;
  children: ReactNode;
  className?: string;
}) {
  return (
    <section className={"key-panel " + className}>
      {eyebrow && <div className="key-kicker">{eyebrow}</div>}
      <h2>{title}</h2>
      {children}
    </section>
  );
}
export function ActionButton({
  children,
  onClick,
  minor = false,
  disabled = false,
}: {
  children: ReactNode;
  onClick?: () => void;
  minor?: boolean;
  disabled?: boolean;
}) {
  return (
    <button
      type="button"
      className={minor ? "key-btn key-btn-minor" : "key-btn key-btn-primary"}
      onClick={onClick}
      disabled={disabled}
    >
      {children}
      {!minor && <ArrowRight size={17} aria-hidden="true" />}
    </button>
  );
}
export function Field({
  label,
  children,
}: {
  label: string;
  children: ReactNode;
}) {
  return (
    <label className="key-field">
      {label}
      {children}
    </label>
  );
}
export function Metric({
  label,
  children,
}: {
  label: string;
  children: ReactNode;
}) {
  return (
    <div className="key-metric">
      <dt>{label}</dt>
      <dd>{children}</dd>
    </div>
  );
}
export function Steps({ items, active }: { items: string[]; active: number }) {
  const { t } = useKey();
  return (
    <ol
      className="key-steps"
      aria-label={t("Journey progress", "Progres perjalanan")}
    >
      {items.map((item, index) => (
        <li key={item} aria-current={index === active ? "step" : undefined}>
          <span>
            {index < active ? (
              <Check size={13} aria-hidden="true" />
            ) : (
              index + 1
            )}
          </span>
          {item}
        </li>
      ))}
    </ol>
  );
}
const eventLabels = (t: Text): Record<Action["type"], string> => ({
  requestDrive: t("Drive requested", "Uji kendara diminta"),
  confirmDrive: t(
    "Branch checked the demonstrator calendar",
    "Cabang memeriksa kalender unit uji",
  ),
  acceptAlternative: t("Alternative accepted", "Alternatif diterima"),
  pickup: t("Demonstrator handed over", "Unit uji diserahterimakan"),
  saveResult: t("Household checks recorded", "Catatan keluarga tersimpan"),
  returnDrive: t("Demonstrator returned", "Unit uji dikembalikan"),
  quoteDrive: t("Purchase quote issued", "Penawaran pembelian terbit"),
  acceptDriveQuote: t("Buyer accepted quote", "Pembeli menerima penawaran"),
  financeDrive: t(
    "Lender decision recorded",
    "Keputusan pemberi pembiayaan tercatat",
  ),
  orderDrive: t("Vehicle ordered", "Kendaraan dipesan"),
  deliverDrive: t("Vehicle delivered", "Kendaraan diserahkan"),
  requestService: t("Service requested", "Servis diminta"),
  confirmService: t(
    "Parts and time confirmed",
    "Suku cadang dan waktu dikonfirmasi",
  ),
  checkIn: t("Vehicle checked in", "Kendaraan diterima"),
  estimate: t(
    "Revised scope sent for approval",
    "Revisi pekerjaan dikirim untuk persetujuan",
  ),
  approve: t("Payer decision recorded", "Keputusan pembayar tercatat"),
  readyService: t("Ready for collection", "Siap diambil"),
  closeService: t("Receipt issued", "Bukti bayar terbit"),
  requestUpgrade: t("Upgrade request opened", "Permintaan tukar tambah dibuat"),
  issueOffer: t(
    "Inspected buy offer issued",
    "Penawaran beli hasil inspeksi terbit",
  ),
  upgradeTerms: t(
    "Lender conditions and unit confirmed",
    "Syarat pembiayaan dan unit dikonfirmasi",
  ),
  acceptUpgrade: t(
    "Owner accepted current terms",
    "Pemilik menerima ketentuan terbaru",
  ),
  settleUpgrade: t("Settlement recorded", "Pelunasan tercatat"),
  deliverUpgrade: t("Handover completed", "Serah terima selesai"),
  recoverUpgrade: t(
    "Expired or unavailable terms withdrawn",
    "Ketentuan kedaluwarsa atau tidak tersedia ditarik",
  ),
  reopenUpgrade: t(
    "Replacement terms requested",
    "Ketentuan pengganti diminta",
  ),
});
export function History({ events }: { events: Log[] }) {
  const { t, date } = useKey();
  return (
    <details className="key-history">
      <summary>
        {t("Transaction history", "Riwayat transaksi")} · {events.length}
      </summary>
      <ol>
        {[...events].reverse().map((event, index) => (
          <li key={index}>
            <strong>
              {eventLabels(t)[event.action]}
              {event.version ? " · v" + event.version : ""}
            </strong>
            <span>
              {roles(t)[event.actor]} · {date(event.at, true)} WIB
            </span>
          </li>
        ))}
      </ol>
    </details>
  );
}
export function downloadText(filename: string, lines: string[]) {
  const url = URL.createObjectURL(
    new Blob([lines.join("\n")], { type: "text/plain;charset=utf-8" }),
  );
  const link = document.createElement("a");
  link.download = filename;
  link.href = url;
  link.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}
