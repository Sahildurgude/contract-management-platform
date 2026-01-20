import { apiRequest } from "./client";

export interface BlueprintField {
  id: string;
  field_type: "text" | "date" | "signature" | "checkbox";
  label: string;
  position_x: number;
  position_y: number;
}

export interface Blueprint {
  id: string;
  name: string;
  fields: BlueprintField[];
}

export async function listBlueprints(): Promise<Blueprint[]> {
  return apiRequest<Blueprint[]>("/blueprints/");
}

export async function createBlueprint(payload: {
  name: string;
  fields: {
    field_type: string;
    label: string;
    position_x: number;
    position_y: number;
  }[];
}) {
  return apiRequest("/blueprints/", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}
