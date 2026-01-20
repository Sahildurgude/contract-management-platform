import { useEffect, useState } from "react";
import { listBlueprints } from "../api/blueprints";
import type { Blueprint } from "../api/blueprints";

import { createContract } from "../api/contracts";
import { useNavigate } from "react-router-dom";

export default function CreateContract() {
  const [name, setName] = useState("");
  const [blueprints, setBlueprints] = useState<Blueprint[]>([]);
  const [selectedBlueprint, setSelectedBlueprint] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    listBlueprints().then(setBlueprints);
  }, []);

  async function handleSubmit() {
    await createContract({
      name,
      blueprint_id: selectedBlueprint,
    });

    navigate("/contracts");
  }

  return (
    <div style={{ padding: 24 }}>
      <h2>Create Contract</h2>

      <div>
        <label>Contract Name</label><br />
        <input value={name} onChange={(e) => setName(e.target.value)} />
      </div>

      <div style={{ marginTop: 12 }}>
        <label>Blueprint</label><br />
        <select
          value={selectedBlueprint}
          onChange={(e) => setSelectedBlueprint(e.target.value)}
        >
          <option value="">Select blueprint</option>
          {blueprints.map((bp) => (
            <option key={bp.id} value={bp.id}>
              {bp.name}
            </option>
          ))}
        </select>
      </div>

      <button
        style={{ marginTop: 16 }}
        disabled={!name || !selectedBlueprint}
        onClick={handleSubmit}
      >
        Create Contract
      </button>
    </div>
  );
}
