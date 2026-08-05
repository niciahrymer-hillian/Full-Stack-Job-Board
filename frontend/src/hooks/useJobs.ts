// React Query hooks — the server-state layer. Components call these instead of
// useEffect+useState. A successful mutation invalidates the "jobs" key, so every
// list re-renders with fresh data automatically.
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { api } from "../api/client";

export interface Job {
  id: number;
  title: string;
  description: string;
  location: string;
  owner_id: number;
  created_at: string;
}

export function useJobs() {
  return useQuery({
    queryKey: ["jobs"],
    queryFn: async () => (await api.get<Job[]>("/jobs")).data,
  });
}

export function useCreateJob() {
  const qc = useQueryClient();
  return useMutation({
    // TODO: type the input with a JobCreate interface
    mutationFn: async (job: Omit<Job, "id" | "owner_id" | "created_at">) =>
      (await api.post<Job>("/jobs", job)).data,
    onSuccess: () => qc.invalidateQueries({ queryKey: ["jobs"] }),
  });
}
