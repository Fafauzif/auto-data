import { ServiceRecord, ServiceRequest } from "../ServiceFlow";
import type { Role, Service } from "../state";
import type { Send } from "../ui";
export default function ServicePage({
  state,
  role,
  payerVersion,
  send,
  openPayer,
}: {
  state?: Service;
  role: Role;
  payerVersion?: number;
  send: Send;
  openPayer: (version: number) => void;
}) {
  return state ? (
    <ServiceRecord
      key={role + state.id}
      record={state}
      adviser={role === "workshop"}
      payerVersion={payerVersion}
      send={send}
      openPayer={openPayer}
    />
  ) : (
    <ServiceRequest send={send} />
  );
}
