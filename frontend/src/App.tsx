// Minimal job list wired to React Query. The point is the data flow, not the CSS.
// TODO: add login form, <ProtectedRoute>, and a create-job form (see LESSON_PLAN).
import { useJobs } from "./hooks/useJobs";

export default function App() {
  const { data: jobs, isLoading, error } = useJobs();

  if (isLoading) return <p>Loading jobs…</p>;
  if (error) return <p>Failed to load jobs.</p>;

  return (
    <main style={{ maxWidth: 640, margin: "2rem auto", fontFamily: "system-ui" }}>
      <h1>Open Roles</h1>
      <ul>
        {jobs?.map((job) => (
          <li key={job.id}>
            <strong>{job.title}</strong> — {job.location}
          </li>
        ))}
      </ul>
    </main>
  );
}
