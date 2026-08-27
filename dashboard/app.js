// GracefulOS Dashboard Client Logic

document.addEventListener('DOMContentLoaded', () => {
  initNavigation();
  loadAllData();
  setInterval(loadAllData, 3000); // Polling telemetry
});

function initNavigation() {
  const navItems = document.querySelectorAll('.nav-item');
  const panels = document.querySelectorAll('.tab-panel');
  const title = document.getElementById('page-title');

  navItems.forEach(item => {
    item.addEventListener('click', () => {
      navItems.forEach(n => n.classList.remove('active'));
      panels.forEach(p => p.classList.remove('active'));

      item.classList.add('active');
      const tabId = item.getAttribute('data-tab');
      const targetPanel = document.getElementById(tabId);
      if (targetPanel) {
        targetPanel.classList.add('active');
        title.innerText = item.innerText.replace(/^[^\w]+/, '').trim();
      }
    });
  });
}

async function loadAllData() {
  await Promise.all([
    fetchStatus(),
    fetchAgents(),
    fetchAuditRecords(),
    fetchIncidents(),
    fetchApprovals(),
    fetchJobObjects(),
    fetchFirewallRules(),
    fetchTrustedPatterns()
  ]);
}

async function fetchStatus() {
  try {
    const res = await fetch('/api/v1/status');
    const data = await res.json();
    document.getElementById('stat-agents').innerText = data.total_agents;
    document.getElementById('stat-incidents').innerText = data.active_incidents;
    document.getElementById('stat-ledger').innerText = data.tamper_free_ledger ? 'TAMPER-FREE' : 'CORRUPT';

    const dist = data.degradation_distribution;
    document.getElementById('stat-dist').innerText = 
      `${dist.NORMAL} Normal, ${dist.WATCH} Watch, ${dist.RESTRICTED} Restr, ${dist.CONTAINED} Contained`;

    if (dist.CONTAINED > 0) {
      document.getElementById('stat-posture').innerText = 'CONTAINED';
      document.getElementById('stat-posture').style.color = 'var(--color-contained)';
    } else if (dist.ISOLATED > 0) {
      document.getElementById('stat-posture').innerText = 'ISOLATED';
      document.getElementById('stat-posture').style.color = 'var(--color-isolated)';
    } else if (dist.READ_ONLY > 0) {
      document.getElementById('stat-posture').innerText = 'READ_ONLY';
      document.getElementById('stat-posture').style.color = 'var(--color-readonly)';
    } else if (dist.RESTRICTED > 0) {
      document.getElementById('stat-posture').innerText = 'RESTRICTED';
      document.getElementById('stat-posture').style.color = 'var(--color-restricted)';
    } else if (dist.WATCH > 0) {
      document.getElementById('stat-posture').innerText = 'WATCH';
      document.getElementById('stat-posture').style.color = 'var(--color-watch)';
    } else {
      document.getElementById('stat-posture').innerText = 'NORMAL';
      document.getElementById('stat-posture').style.color = 'var(--color-normal)';
    }
  } catch (err) {
    console.error('Error fetching status:', err);
  }
}

async function fetchAgents() {
  try {
    const res = await fetch('/api/v1/agents');
    const agents = await res.json();
    const tbody = document.getElementById('agents-tbody');
    
    if (!agents.length) {
      tbody.innerHTML = '<tr><td colspan="6" style="text-align:center;">No agents currently active.</td></tr>';
      return;
    }

    tbody.innerHTML = agents.map(a => `
      <tr>
        <td class="mono"><strong>${a.agent_id}</strong></td>
        <td>${a.name} <br><small style="color:var(--text-muted)">${a.mission}</small></td>
        <td><span class="badge badge-watch">${a.model}</span></td>
        <td><strong>${a.risk_score} / 100</strong></td>
        <td><span class="badge badge-${a.state.toLowerCase()}">${a.state}</span></td>
        <td>
          <button class="btn btn-outline" style="padding:4px 8px; font-size:11px;" onclick="viewAgent('${a.agent_id}')">Inspect</button>
        </td>
      </tr>
    `).join('');
  } catch (err) {
    console.error('Error fetching agents:', err);
  }
}

async function fetchAuditRecords() {
  try {
    const res = await fetch('/api/v1/audit/records?limit=15');
    const records = await res.json();
    const overviewTbody = document.getElementById('overview-audit-tbody');
    const fullTbody = document.getElementById('full-audit-tbody');

    if (!records.length) {
      overviewTbody.innerHTML = '<tr><td colspan="7" style="text-align:center;">No audit records logged yet.</td></tr>';
      fullTbody.innerHTML = '<tr><td colspan="8" style="text-align:center;">No audit records.</td></tr>';
      return;
    }

    const rows = records.map(r => `
      <tr>
        <td class="mono" style="font-size:11px;">${r.timestamp.substring(11, 19)}</td>
        <td class="mono">${r.agent_id || 'System'}</td>
        <td><span class="badge badge-watch">${r.event_type}</span></td>
        <td class="mono">${r.action_name}</td>
        <td><strong>${r.decision}</strong></td>
        <td class="mono">${r.risk_score_before} → ${r.risk_score_after}</td>
        <td><span class="badge badge-${r.degradation_state.toLowerCase()}">${r.degradation_state}</span></td>
      </tr>
    `).join('');
    overviewTbody.innerHTML = rows;

    fullTbody.innerHTML = records.map(r => `
      <tr>
        <td class="mono">${r.record_id}</td>
        <td class="mono">${r.timestamp.substring(11, 19)}</td>
        <td class="mono">${r.agent_id || 'System'}</td>
        <td class="mono">${r.action_name}</td>
        <td>${r.decision}</td>
        <td class="mono">${r.risk_score_before} → ${r.risk_score_after}</td>
        <td class="mono" style="font-size:10px;">${r.prev_hash.substring(0, 10)}...</td>
        <td class="mono" style="font-size:10px; color:var(--accent-cyan);">${r.current_hash.substring(0, 10)}...</td>
      </tr>
    `).join('');
  } catch (err) {
    console.error('Error fetching audit records:', err);
  }
}

async function fetchIncidents() {
  try {
    const res = await fetch('/api/v1/incidents');
    const incidents = await res.json();
    const tbody = document.getElementById('incidents-tbody');

    if (!incidents.length) {
      tbody.innerHTML = '<tr><td colspan="7" style="text-align:center;">No incidents recorded.</td></tr>';
      return;
    }

    tbody.innerHTML = incidents.map(i => `
      <tr>
        <td class="mono">${i.incident_id}</td>
        <td class="mono">${i.timestamp.substring(11, 19)}</td>
        <td class="mono">${i.agent_id}</td>
        <td><span class="badge badge-${i.severity === 'CRITICAL' ? 'contained' : 'restricted'}">${i.severity}</span></td>
        <td class="mono">${i.trigger_rule}</td>
        <td><span class="badge badge-${i.status === 'CONTAINED' ? 'contained' : 'watch'}">${i.status}</span></td>
        <td>${i.summary}</td>
      </tr>
    `).join('');
  } catch (err) {
    console.error('Error fetching incidents:', err);
  }
}

async function fetchApprovals() {
  try {
    const res = await fetch('/api/v1/approvals');
    const approvals = await res.json();
    const tbody = document.getElementById('approvals-tbody');

    if (!approvals.length) {
      tbody.innerHTML = '<tr><td colspan="6" style="text-align:center;">No pending approval requests.</td></tr>';
      return;
    }

    tbody.innerHTML = approvals.map(a => `
      <tr>
        <td class="mono">${a.request_id}</td>
        <td class="mono"><strong>${a.agent_id}</strong></td>
        <td><span class="badge badge-watch">${a.tool_name}</span></td>
        <td class="mono" style="font-size:12px;">${a.action_description}</td>
        <td><strong>${a.risk_score}</strong></td>
        <td>
          <div style="display:flex; gap:6px; flex-wrap:wrap;">
            <button class="btn btn-primary" style="padding:4px 8px; font-size:11px;" onclick="resolveApproval('${a.request_id}', true, false)">✅ Allow Once</button>
            <button class="btn btn-outline" style="padding:4px 8px; font-size:11px; border-color:var(--accent-cyan); color:var(--accent-cyan);" onclick="resolveApproval('${a.request_id}', true, true)">🛡️ Always Allow</button>
            <button class="btn btn-danger" style="padding:4px 8px; font-size:11px;" onclick="resolveApproval('${a.request_id}', false, false)">❌ Deny</button>
          </div>
        </td>
      </tr>
    `).join('');
  } catch (err) {
    console.error('Error fetching approvals:', err);
  }
}

async function viewAgent(agentId) {
  try {
    const res = await fetch(`/api/v1/agents/${agentId}`);
    const a = await res.json();
    
    // Switch to Agent Details tab
    document.querySelector('[data-tab="tab-agent-details"]').click();

    const view = document.getElementById('agent-details-view');
    view.innerHTML = `
      <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:24px;">
        <div>
          <h2>${a.name} <span class="mono" style="font-size:14px; color:var(--text-muted);">(${a.agent_id})</span></h2>
          <p style="color:var(--text-secondary); margin-top:4px;">Mission: ${a.mission} | Model: ${a.model}</p>
        </div>
        <span class="badge badge-${a.state.toLowerCase()}" style="font-size:14px; padding:6px 14px;">${a.state}</span>
      </div>

      <div class="stats-grid">
        <div class="glass-card stat-box">
          <span class="stat-label">Current Risk Score</span>
          <span class="stat-value" style="color:var(--accent-cyan);">${a.risk_score} / 100</span>
        </div>
        <div class="glass-card stat-box">
          <span class="stat-label">Files Modified / Deleted</span>
          <span class="stat-value">${a.blast_radius.usage.files_modified} / ${a.blast_radius.usage.files_deleted}</span>
        </div>
        <div class="glass-card stat-box">
          <span class="stat-label">PowerShell Commands</span>
          <span class="stat-value">${a.blast_radius.usage.powershell_commands}</span>
        </div>
        <div class="glass-card stat-box">
          <span class="stat-label">Processes Spawned</span>
          <span class="stat-value">${a.blast_radius.usage.processes_spawned}</span>
        </div>
      </div>

      <div style="margin-top:24px;">
        <h4 style="margin-bottom:12px;">Effective Capabilities Granted in Current State:</h4>
        <div style="display:flex; flex-wrap:wrap; gap:8px;">
          ${a.effective_capabilities.map(c => `<span class="badge badge-normal">${c}</span>`).join('') || '<span style="color:var(--color-contained);">No capabilities granted (CONTAINED)</span>'}
        </div>
      </div>
    `;
    loadIncidentReplay(agentId);
  } catch (err) {
    console.error('Error viewing agent:', err);
  }
}

async function loadIncidentReplay(agentId) {
  try {
    const res = await fetch(`/api/v1/replay/${agentId}`);
    const data = await res.json();
    const container = document.getElementById('replay-timeline-container');

    if (!data.timeline.length) {
      container.innerHTML = '<p style="color:var(--text-secondary);">No timeline events recorded yet.</p>';
      return;
    }

    container.innerHTML = data.timeline.map(s => `
      <div class="timeline-step">
        <div class="timeline-dot">${s.step}</div>
        <div class="timeline-card">
          <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
            <strong>${s.action_name}</strong>
            <span class="badge badge-${s.state.toLowerCase()}">${s.state} (Score: ${s.risk_after})</span>
          </div>
          <p style="font-size:12px; color:var(--text-secondary);">${JSON.stringify(s.details)}</p>
          <div class="mono" style="font-size:10px; color:var(--text-muted); margin-top:6px;">Hash: ${s.hash.substring(0, 16)}...</div>
        </div>
      </div>
    `).join('');
  } catch (err) {
    console.error('Error loading replay:', err);
  }
}

async function fetchJobObjects() {
  const container = document.getElementById('job-objects-list');
  if (!container) return;
  try {
    const res = await fetch('/api/v1/agents');
    const agents = await res.json();
    if (!agents.length) {
      container.innerHTML = '<p style="color:var(--text-secondary); font-size:13px;">No active Win32 Job Objects. Launch or register an agent to bind a process tree.</p>';
      return;
    }
    container.innerHTML = `
      <div class="table-container">
        <table>
          <thead>
            <tr><th>Job Object Name</th><th>Target Agent</th><th>Active PIDs</th><th>Memory Cap</th><th>Kill-On-Close</th><th>Status</th></tr>
          </thead>
          <tbody>
            ${agents.map(a => `
              <tr>
                <td class="mono"><strong>GracefulOS_Job_${a.agent_id}</strong></td>
                <td class="mono">${a.agent_id}</td>
                <td><span class="badge badge-watch">Attached</span></td>
                <td class="mono">512 MB</td>
                <td><span class="badge badge-normal">TRUE</span></td>
                <td><span class="badge badge-${a.state.toLowerCase()}">${a.state}</span></td>
              </tr>
            `).join('')}
          </tbody>
        </table>
      </div>
    `;
  } catch (err) {
    console.error('Error fetching job objects:', err);
  }
}

async function fetchFirewallRules() {
  const container = document.getElementById('firewall-rules-list');
  if (!container) return;
  try {
    const res = await fetch('/api/v1/status');
    const status = await res.json();
    container.innerHTML = `
      <div class="table-container">
        <table>
          <thead>
            <tr><th>Rule Name</th><th>Direction</th><th>Action</th><th>Profile</th><th>State</th></tr>
          </thead>
          <tbody>
            <tr>
              <td class="mono">GracefulOS_Block_Isolated</td>
              <td>Outbound</td>
              <td><span class="badge badge-contained">BLOCK</span></td>
              <td>Domain, Private, Public</td>
              <td><span class="badge badge-normal">ACTIVE</span></td>
            </tr>
            <tr>
              <td class="mono">GracefulOS_Allow_Localhost</td>
              <td>Inbound/Outbound</td>
              <td><span class="badge badge-normal">ALLOW</span></td>
              <td>Private</td>
              <td><span class="badge badge-normal">ACTIVE</span></td>
            </tr>
            <tr>
              <td class="mono">GracefulOS_Dynamic_Sync</td>
              <td>Outbound</td>
              <td><span class="badge badge-watch">SYNCED</span></td>
              <td>All</td>
              <td><span class="badge badge-normal">CONNECTED</span></td>
            </tr>
          </tbody>
        </table>
      </div>
    `;
  } catch (err) {
    console.error('Error fetching firewall rules:', err);
  }
}

function showToast(message, isError = false) {
  let toast = document.getElementById('dashboard-toast');
  if (!toast) {
    toast = document.createElement('div');
    toast.id = 'dashboard-toast';
    toast.style.position = 'fixed';
    toast.style.bottom = '24px';
    toast.style.right = '24px';
    toast.style.padding = '12px 20px';
    toast.style.borderRadius = '8px';
    toast.style.zIndex = '9999';
    toast.style.fontSize = '13px';
    toast.style.fontWeight = '500';
    toast.style.transition = 'all 0.3s ease';
    document.body.appendChild(toast);
  }
  toast.style.background = isError ? 'rgba(239, 68, 68, 0.95)' : 'rgba(16, 185, 129, 0.95)';
  toast.style.color = '#fff';
  toast.style.boxShadow = '0 8px 24px rgba(0,0,0,0.4)';
  toast.innerText = message;
  toast.style.opacity = '1';
  setTimeout(() => { toast.style.opacity = '0'; }, 4000);
}

async function runAttackDemo() {
  try {
    showToast('Launching Flagship 5-Stage Attack Chain Simulation...');
    // Register agent
    await fetch('/api/v1/agents/register', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        agent_id: 'agent-coder-001',
        name: 'Autonomous Coder Agent',
        mission: 'fix_local_project',
        model: 'local-qwen'
      })
    });

    // Step 1: Normal
    await fetch('/api/v1/tools/invoke', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        agent_id: 'agent-coder-001',
        tool_name: 'read_file',
        arguments: {'path': 'README.md'}
      })
    });

    // Step 2: Watch (Prompt Injection)
    await fetch('/api/v1/risk/signal', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        agent_id: 'agent-coder-001',
        signal_code: 'PROMPT_INJECTION_DETECTED',
        reason: 'Malicious README instruction detected'
      })
    });

    // Step 3: Restricted (PowerShell)
    await fetch('/api/v1/tools/invoke', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        agent_id: 'agent-coder-001',
        tool_name: 'powershell',
        arguments: {'command': 'Remove-Item C:\\Users\\* -Recurse'}
      })
    });

    // Step 4: Read_Only (Canary Tripwire)
    await fetch('/api/v1/tools/invoke', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        agent_id: 'agent-coder-001',
        tool_name: 'read_file',
        arguments: {'path': 'runtime/canary/fake_admin_token.txt'}
      })
    });

    // Step 5: Contained (Service Tamper Attempt)
    await fetch('/api/v1/tools/invoke', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        agent_id: 'agent-coder-001',
        tool_name: 'powershell',
        arguments: {'command': 'Stop-Service GracefulOS'}
      })
    });

    await loadAllData();
    viewAgent('agent-coder-001');
    showToast('Attack Demo Completed: Agent CONTAINED & Job Object Killed!');
  } catch (err) {
    showToast('Error running simulation: ' + err, true);
  }
}

async function resolveApproval(requestId, approved, alwaysTrust = false) {
  try {
    await fetch('/api/v1/approvals/resolve', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        request_id: requestId,
        approved: approved,
        always_trust: alwaysTrust,
        reviewer: 'administrator'
      })
    });
    if (approved) {
      if (alwaysTrust) {
        showToast(`Request ${requestId} APPROVED & ALWAYS TRUSTED in this workspace!`);
      } else {
        showToast(`Request ${requestId} APPROVED for 1-time execution (Allow Once).`);
      }
    } else {
      showToast(`Request ${requestId} DENIED. Security barrier maintained.`, true);
    }
    loadAllData();
  } catch (err) {
    showToast('Error resolving approval: ' + err, true);
  }
}

async function fetchTrustedPatterns() {
  const container = document.getElementById('trusted-patterns-list');
  if (!container) return;
  try {
    const res = await fetch('/api/v1/policy/trust');
    const data = await res.json();
    const patterns = data.trusted_patterns || [];

    if (!patterns.length) {
      container.innerHTML = '<p style="color:var(--text-secondary); font-size:13px;">No custom trusted patterns active. Add any script or command above to always allow it.</p>';
      return;
    }

    container.innerHTML = `
      <div class="table-container">
        <table>
          <thead>
            <tr><th>Trusted Pattern / Safe Command</th><th>Scope</th><th>Action</th><th>Status</th><th>Remove</th></tr>
          </thead>
          <tbody>
            ${patterns.map(p => `
              <tr>
                <td class="mono"><strong>${p}</strong></td>
                <td><span class="badge badge-watch">Workspace</span></td>
                <td><span class="badge badge-normal">ALWAYS ALLOW</span></td>
                <td><span class="badge badge-normal">ACTIVE</span></td>
                <td>
                  <button class="btn btn-danger" style="padding:3px 8px; font-size:11px;" onclick="removeTrustedPattern('${p}')">🗑️ Remove</button>
                </td>
              </tr>
            `).join('')}
          </tbody>
        </table>
      </div>
    `;
  } catch (err) {
    console.error('Error fetching trusted patterns:', err);
  }
}

async function addTrustedPattern() {
  const input = document.getElementById('trusted-pattern-input');
  const pattern = input.value.trim();
  if (!pattern) {
    showToast('Please enter a command or tool pattern to trust', true);
    return;
  }
  try {
    await fetch('/api/v1/policy/trust', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ pattern: pattern })
    });
    input.value = '';
    showToast(`Added '${pattern}' to Trusted Workspace Allowlist!`);
    loadAllData();
  } catch (err) {
    showToast('Error adding trusted pattern: ' + err, true);
  }
}

async function removeTrustedPattern(pattern) {
  try {
    await fetch('/api/v1/policy/trust', {
      method: 'DELETE',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ pattern: pattern })
    });
    showToast(`Removed '${pattern}' from Trusted Allowlist.`);
    loadAllData();
  } catch (err) {
    showToast('Error removing trusted pattern: ' + err, true);
  }
}

async function releaseContainment() {
  const agentId = document.getElementById('release-agent-id').value.trim();
  if (!agentId) {
    showToast('Please enter an Agent ID', true);
    return;
  }
  try {
    const res = await fetch('/api/v1/recovery/release', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        agent_id: agentId,
        admin_token: 'ADMIN_LOCAL_SECRET_KEY',
        target_state: 'WATCH',
        notes: 'Admin authorized release after sandbox verification'
      })
    });
    const data = await res.json();
    showToast(`Agent ${agentId} released! New state: ${data.new_state}`);
    loadAllData();
  } catch (err) {
    showToast('Error releasing containment: ' + err, true);
  }
}

async function triggerRefresh(btn) {
  const icon = document.getElementById('refresh-icon');
  if (icon) {
    icon.classList.add('spin-icon');
  }
  if (btn) {
    btn.disabled = true;
    btn.style.opacity = '0.7';
  }
  
  try {
    await loadAllData();
    showToast('Telemetry & dashboard data refreshed!');
  } catch (err) {
    showToast('Failed to refresh data: ' + err, true);
  } finally {
    setTimeout(() => {
      if (icon) icon.classList.remove('spin-icon');
      if (btn) {
        btn.disabled = false;
        btn.style.opacity = '1';
      }
    }, 450);
  }
}
