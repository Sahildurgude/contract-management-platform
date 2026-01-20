import { useState } from "react";
import { createBlueprint } from "../api/blueprints";
import { useNavigate } from "react-router-dom";

type FieldType = "text" | "date" | "signature" | "checkbox";

interface BlueprintFieldDraft {
  field_type: FieldType;
  label: string;
  position_x: number;
  position_y: number;
}

export default function CreateBlueprint() {
  const [name, setName] = useState("");
  const [fields, setFields] = useState<BlueprintFieldDraft[]>([]);
  const [loading, setLoading] = useState(false);

  const navigate = useNavigate();

  function addField() {
    setFields([
      ...fields,
      {
        field_type: "text",
        label: "",
        position_x: fields.length + 1,
        position_y: 1,
      },
    ]);
  }

  function updateField(index: number, key: keyof BlueprintFieldDraft, value: any) {
    const updated = [...fields];
    updated[index] = { ...updated[index], [key]: value };
    setFields(updated);
  }

  async function handleSubmit() {
    if (!name.trim()) {
      alert("Blueprint name is required");
      return;
    }

    setLoading(true);

    try {
      await createBlueprint({
        name,
        fields,
      });

      navigate("/blueprints");
    } catch (e: any) {
      alert(e.message || "Failed to create blueprint");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={{ padding: 24 }}>
      <h2>Create Blueprint</h2>

      <div style={{ marginBottom: 16 }}>
        <label>Blueprint Name</label>
        <br />
        <input
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
      </div>

      <h3>Fields</h3>

      {fields.map((field, index) => (
        <div key={index} style={{ marginBottom: 12 }}>
          <select
            value={field.field_type}
            onChange={(e) =>
              updateField(index, "field_type", e.target.value as FieldType)
            }
          >
            <option value="text">Text</option>
            <option value="date">Date</option>
            <option value="signature">Signature</option>
            <option value="checkbox">Checkbox</option>
          </select>

          <input
            placeholder="Label"
            value={field.label}
            onChange={(e) =>
              updateField(index, "label", e.target.value)
            }
            style={{ marginLeft: 8 }}
          />
        </div>
      ))}

      <button onClick={addField}>+ Add Field</button>

      <br /><br />

      <button onClick={handleSubmit} disabled={loading}>
        {loading ? "Creating..." : "Create Blueprint"}
      </button>
    </div>
  );
}
