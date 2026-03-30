// =============================================================================
// 전역 변수
// =============================================================================
let subscribers = [];
let currentDevices = [];
let selectedUserId = null;
let selectedDeviceId = null;
let usageChart = null;

// =============================================================================
// [요구사항 #3] 상태 기반 Badge 스타일
// =============================================================================
function badgeClass(value) {
  const v = (value || "").toLowerCase();

  if (["active", "online", "normal"].includes(v)) return "badge status-active";
  if (["paused", "standby"].includes(v)) return "badge status-paused";
  if (["expired", "error", "warning"].includes(v))
    return "badge status-expired";
  if (v === "offline") return "badge status-offline";
  if (["on", "cleaning"].includes(v)) return "badge status-on";
  if (v === "off") return "badge status-off";
  return "badge";
}

// =============================================================================
// [요구사항 #1] 구독 사용자 조회 + 검색/필터
// =============================================================================

async function fetchSubscribers() {
  const res = await fetch("/api/subscribers");
  subscribers = await res.json();
  renderSubscribers();
}

function renderSubscribers() {
  const tbody = document.getElementById("subscriber-body");
  const search = document
    .getElementById("subscriber-search")
    .value.toLowerCase();
  const statusFilter = document.getElementById(
    "subscriber-status-filter"
  ).value;

  const filtered = subscribers.filter((s) => {
    const matchSearch =
      s.name.toLowerCase().includes(search) ||
      s.plan.toLowerCase().includes(search) ||
      s.status.toLowerCase().includes(search) ||
      s.userId.toLowerCase().includes(search);
    const matchStatus = statusFilter === "" || s.status === statusFilter;
    return matchSearch && matchStatus;
  });

  tbody.innerHTML = "";
  filtered.forEach((s) => {
    const tr = document.createElement("tr");
    tr.className =
      "clickable" + (s.userId === selectedUserId ? " selected" : "");
    tr.innerHTML = `
            <td>${s.userId}</td>
            <td>${s.name}</td>
            <td>${s.plan}</td>
            <td><span class="${badgeClass(s.status)}">${s.status}</span></td>
            <td>${s.deviceCount}</td>
        `;
    tr.addEventListener("click", () => selectSubscriber(s.userId));
    tbody.appendChild(tr);
  });
}

// =============================================================================
// [요구사항 #2] 사용자별 가전 목록 + 사용 현황 + 차트
// =============================================================================

async function selectSubscriber(userId) {
  selectedUserId = userId;
  selectedDeviceId = null;
  renderSubscribers();

  document.getElementById("usage-detail").classList.add("hidden");
  document.getElementById("usage-empty").classList.remove("hidden");

  const res = await fetch(`/api/subscribers/${userId}/devices`);
  currentDevices = await res.json();
  renderDevices();
}

function renderDevices() {
  const emptyEl = document.getElementById("device-empty");
  const tableEl = document.getElementById("device-table");
  const tbody = document.getElementById("device-body");
  const search = document.getElementById("device-search").value.toLowerCase();
  const statusFilter = document.getElementById("device-status-filter").value;

  tbody.innerHTML = "";

  if (currentDevices.length === 0) {
    emptyEl.textContent = "No registered devices.";
    emptyEl.classList.remove("hidden");
    tableEl.classList.add("hidden");
    return;
  }

  const filtered = currentDevices.filter((d) => {
    const matchSearch =
      d.type.toLowerCase().includes(search) ||
      d.model.toLowerCase().includes(search) ||
      d.status.toLowerCase().includes(search) ||
      d.deviceId.toLowerCase().includes(search) ||
      d.location.toLowerCase().includes(search);
    const matchStatus = statusFilter === "" || d.status === statusFilter;
    return matchSearch && matchStatus;
  });

  if (filtered.length === 0) {
    emptyEl.textContent = "No devices matched your filter.";
    emptyEl.classList.remove("hidden");
    tableEl.classList.add("hidden");
    return;
  }

  emptyEl.classList.add("hidden");
  tableEl.classList.remove("hidden");

  filtered.forEach((d) => {
    const tr = document.createElement("tr");
    tr.className =
      "clickable" + (d.deviceId === selectedDeviceId ? " selected" : "");
    tr.innerHTML = `
            <td>${d.deviceId}</td>
            <td>${d.type}</td>
            <td>${d.model}</td>
            <td>${d.location}</td>
            <td><span class="${badgeClass(d.status)}">${d.status}</span></td>
        `;
    tr.addEventListener("click", () => selectDevice(d.deviceId));
    tbody.appendChild(tr);
  });
}

async function selectDevice(deviceId) {
  selectedDeviceId = deviceId;
  renderDevices();

  const res = await fetch(`/api/devices/${deviceId}/usage`);
  const data = await res.json();

  document.getElementById("usage-empty").classList.add("hidden");
  document.getElementById("usage-detail").classList.remove("hidden");

  document.getElementById("usage-info").innerHTML = `
        <span class="label">Device ID</span>     <span class="value">${
          data.deviceId
        }</span>
        <span class="label">Device Name</span>   <span class="value">${
          data.deviceName
        }</span>
        <span class="label">Power Status</span>  <span class="value"><span class="${badgeClass(
          data.powerStatus
        )}">${data.powerStatus}</span></span>
        <span class="label">Last Used</span>     <span class="value">${
          data.lastUsedAt
        }</span>
        <span class="label">Total Hours</span>   <span class="value">${
          data.totalUsageHours
        } hrs</span>
        <span class="label">Weekly Count</span>  <span class="value">${
          data.weeklyUsageCount
        }</span>
        <span class="label">Health</span>        <span class="value"><span class="${badgeClass(
          data.healthStatus
        )}">${data.healthStatus}</span></span>
        <span class="label">Remark</span>        <span class="value">${
          data.remark
        }</span>
    `;

  renderUsageChart(data.weeklyUsageTrend);
}

function renderUsageChart(trend) {
  const ctx = document.getElementById("usageChart");

  if (usageChart) {
    usageChart.destroy();
  }

  usageChart = new Chart(ctx, {
    type: "bar",
    data: {
      labels: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
      datasets: [
        {
          label: "Weekly Usage",
          data: trend,
          backgroundColor: "rgba(59, 130, 246, 0.6)",
          borderColor: "rgba(59, 130, 246, 1)",
          borderWidth: 1,
          borderRadius: 4,
        },
      ],
    },
    options: {
      responsive: true,
      scales: {
        y: { beginAtZero: true },
      },
    },
  });
}

// =============================================================================
// 이벤트 바인딩 + 초기화
// =============================================================================
function bindEvents() {
  document
    .getElementById("subscriber-search")
    .addEventListener("input", renderSubscribers);
  document
    .getElementById("subscriber-status-filter")
    .addEventListener("change", renderSubscribers);

  document
    .getElementById("device-search")
    .addEventListener("input", renderDevices);
  document
    .getElementById("device-status-filter")
    .addEventListener("change", renderDevices);
}

bindEvents();
fetchSubscribers();
