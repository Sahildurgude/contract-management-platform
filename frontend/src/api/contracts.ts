import { apiRequest } from "./client";

export interface Contract {
  id: string;
  blueprint_id: string;
  state: string;
  values: Record<string, any>;
}

export function createContract(data: {
  name: string;
  blueprint_id: string;
}) {
  return apiRequest<Contract>("/contracts/", {
    method: "POST",
    body: JSON.stringify(data),
  });
}

export function listContracts(group?: string) {
  const query = group ? `?group=${group}` : "";
  return apiRequest<Contract[]>(`/contracts/${query}`);
}



export function transitionContract(
  contractId: string,
  to_status: string
) {
  return apiRequest(`/contracts/${contractId}/transition`, {
    method: "POST",
    body: JSON.stringify({ to_status }),
  });
}
