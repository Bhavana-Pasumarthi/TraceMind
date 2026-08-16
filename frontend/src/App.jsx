import { useEffect, useState } from "react";
import { checkHealth } from "./services/api";

/**
 * Phase 1 placeholder. This intentionally does nothing but prove the
 * frontend can reach the backend and the backend can reach Postgres.
 * The real dashboard (filters, summary cards, charts, incident table)
 * is built in Phase 6, once there's real data to show.
 */
export default function App() {
  const [status, setStatus] = useState("checking...");

  useEffect(() => {
    checkHealth()
      .then((data) => setStatus(`backend: ${data.status}, database: ${data.database}`))
      .catch((err) => setStatus(`error: ${err.message}`));
  }, []);

  return (
    <div style={{ fontFamily: "system-ui, sans-serif", padding: "2rem" }}>
      <h1>TraceMind</h1>
      <p>Agentic Software Reliability &amp; Root-Cause Analysis Platform</p>
      <p>
        <strong>System status:</strong> {status}
      </p>
    </div>
  );
}
