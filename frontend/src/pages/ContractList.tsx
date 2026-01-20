import { useEffect, useState } from "react";
import { listContracts, transitionContract } from "../api/contracts";
import type { Contract } from "../api/contracts";

const ALLOWED_TRANSITIONS: Record<string, string[]> = {
  created: ["approved", "revoked"],
  approved: ["sent"],
  sent: ["signed", "revoked"],
  signed: ["locked"],
  locked: [],
  revoked: [],
};

export default function ContractList() {
  const [contracts, setContracts] = useState<Contract[]>([]);
const [error, setError] = useState("");
const [group, setGroup] = useState<string>("active");

useEffect(() => {
  async function load() {
    try {
      const data = await listContracts(group);
      setContracts(data);
    } catch (e: any) {
      setError(e.message || "Failed to load contracts");
    }
  }

  load();
}, [group]);

async function changeState(contractId: string, toStatus: string) {
  try {
    await transitionContract(contractId, toStatus);
    const updated = await listContracts(group);
    setContracts(updated);
  } catch (e: any) {
    alert(e.message || "Transition failed");
  }
}


  return (
    <div style={{ padding: 24 }}>
      <h2>Contracts</h2>

      {error && <p style={{ color: "red" }}>{error}</p>}
      {contracts.length === 0 && <p>No contracts found</p>}

      <ul>
        {contracts.map((c) => (
          <li key={c.id} style={{ marginBottom: 12 }}>
            Contract {c.id.slice(0, 8)} — <b>{c.state}</b>

            <div style={{ marginTop: 4 }}>
              {ALLOWED_TRANSITIONS[c.state]?.map((next) => (
                <button
                  key={next}
                  style={{ marginRight: 8 }}
                  onClick={() => changeState(c.id, next)}
                >
                  {next}
                </button>
              ))}
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}
