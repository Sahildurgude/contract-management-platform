import { useEffect, useState } from "react";
import { listBlueprints } from "../api/blueprints";
import type { Blueprint } from "../api/blueprints";


export default function BlueprintList() {
  const [blueprints, setBlueprints] = useState<Blueprint[]>([]);
  const [error, setError] = useState<string>("");

  useEffect(() => {
    async function load() {
      try {
        const data = await listBlueprints();
        setBlueprints(data);
      } catch (e: any) {
        setError(e.message || "Failed to load blueprints");
      }
    }
    load();
  }, []);

  return (
    <div style={{ padding: 24 }}>
      <h2>Existing Blueprints</h2>

      {error && <p style={{ color: "red" }}>{error}</p>}
      {blueprints.length === 0 && <p>No blueprints found</p>}

      <ul>
        {blueprints.map((bp) => (
          <li key={bp.id}>{bp.name}</li>
        ))}
      </ul>
    </div>
  );
}
