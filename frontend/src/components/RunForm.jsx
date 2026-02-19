import { useState } from "react";

function buildBranchName(teamName, leaderName) {
  const sanitize = (s) => s.toUpperCase().replace(/[^A-Z0-9 ]/g, "").trim().replace(/ +/g, "_");
  if (!teamName && !leaderName) return "TEAM_NAME_LEADER_NAME_AI_Fix";
  return `${sanitize(teamName) || "TEAM"}_${sanitize(leaderName) || "LEADER"}_AI_Fix`;
}

export default function RunForm({ onSubmit, loading }) {
  const [repoUrl, setRepoUrl] = useState("");
  const [teamName, setTeamName] = useState("");
  const [leaderName, setLeaderName] = useState("");
  const branchPreview = buildBranchName(teamName, leaderName);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!repoUrl || !teamName || !leaderName) return;
    onSubmit({ repoUrl, teamName, leaderName });
  };

  return (
    <div className="form-card card">
      <h2 className="form-title">Run Healing Agent</h2>
      <p className="form-subtitle">Enter your repository details to start the autonomous CI/CD fix pipeline</p>
      <form onSubmit={handleSubmit}>
        <div className="form-group full" style={{ marginBottom: 16 }}>
          <label className="form-label">GitHub Repository URL</label>
          <input className="form-input" type="url" placeholder="https://github.com/your-org/your-repo" value={repoUrl} onChange={(e) => setRepoUrl(e.target.value)} required disabled={loading} />
        </div>
        <div className="form-grid">
          <div className="form-group">
            <label className="form-label">Team Name</label>
            <input className="form-input" type="text" placeholder="RIFT ORGANISERS" value={teamName} onChange={(e) => setTeamName(e.target.value)} required disabled={loading} />
          </div>
          <div className="form-group">
            <label className="form-label">Team Leader Name</label>
            <input className="form-input" type="text" placeholder="Saiyam Kumar" value={leaderName} onChange={(e) => setLeaderName(e.target.value)} required disabled={loading} />
          </div>
        </div>
        <div className="branch-preview">
          <span className="branch-label">BRANCH THAT WILL BE CREATED</span>
          {branchPreview}
        </div>
        <button type="submit" className={`run-btn ${loading ? "loading" : ""}`} disabled={loading || !repoUrl || !teamName || !leaderName}>
          {loading ? <><span className="spinner" />Agent Running...</> : "⚡ Run Healing Agent"}
        </button>
      </form>
    </div>
  );
}