import { UpgradeRecord, UpgradeRequest } from "../UpgradeFlow";
import type { Role, Upgrade } from "../state";
import type { Send } from "../ui";
export default function UpgradePage({
  state,
  role,
  send,
  marketTrade,
  onPlanner,
}: {
  state?: Upgrade;
  role: Role;
  send: Send;
  marketTrade?: number;
  onPlanner: () => void;
}) {
  return state ? (
    <UpgradeRecord
      key={role + state.id}
      record={state}
      adviser={role === "upgrade"}
      send={send}
    />
  ) : (
    <UpgradeRequest
      marketTrade={marketTrade}
      onPlanner={onPlanner}
      send={send}
    />
  );
}
