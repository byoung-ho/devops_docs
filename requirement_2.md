# 요구사항 #2: 가전 목록 조회 + 사용 현황 + 차트

## 목표

특정 구독자를 선택하면 해당 사용자의 가전 목록을 조회하고,
특정 가전을 선택하면 상세 사용 현황과 주간 사용량 Bar Chart를 표시합니다.

---

## 역할별 작업

| 역할 | 작업 내용 |
|------|----------|
| **PM** | 요구사항을 FE/BE에 배분, TE에 테스트 시나리오 작성 요청, feature 브랜치 관리 |
| **BE** | `GET /api/subscribers/{id}/devices` + `GET /api/devices/{id}/usage` API 구현 |
| **FE** | 가전 Table + 사용 현황 상세 + Bar Chart 구현 |
| **TE** | 테스트 시나리오 작성 → 검증 → Report 작성 |

---

## 완료 조건

### 가전 목록 (4.3 + 4.4)
- [ ] `GET /api/subscribers/{userId}/devices` API가 정상 동작한다
- [ ] 구독자 행 클릭 시 가전 목록이 Table에 표시된다
- [ ] 가전이 없는 사용자 선택 시 안내 메시지가 표시된다
- [ ] 모델명 / 타입 / 상태 / 위치 기준 검색이 동작한다
- [ ] Online / Offline / Standby / Error 상태 필터가 동작한다
- [ ] 존재하지 않는 사용자 ID 요청 시 404 에러를 반환한다

### 사용 현황 + 차트 (4.5 + 4.6)
- [ ] `GET /api/devices/{deviceId}/usage` API가 정상 동작한다
- [ ] 가전 행 클릭 시 사용 현황 정보가 표시된다
- [ ] 주간 사용량이 Bar Chart(요일 기준)로 표시된다
- [ ] 존재하지 않는 디바이스 ID 요청 시 404 에러를 반환한다

### 검증
- [ ] TE의 검증 Report가 작성되었다

---

## BE: Backend API 구현

### API 1: 사용자별 가전 목록

**파일:** `app/api/subscribers.py`

```python
@router.get("/subscribers/{user_id}/devices")
def get_devices_by_user(user_id: str):
    # 1. subscribers 리스트에서 user_id가 존재하는지 확인
    # 2. 존재하면 devices_by_user에서 해당 사용자의 디바이스 목록 반환
    # 3. 존재하지 않으면 HTTPException(status_code=404) 발생
    pass
```

**확인 방법:**
```bash
# 정상 케이스
curl http://localhost:8000/api/subscribers/U001/devices

# 가전 없는 사용자
curl http://localhost:8000/api/subscribers/U005/devices

# 존재하지 않는 사용자
curl http://localhost:8000/api/subscribers/U999/devices
```

### API 2: 가전 사용 현황

**파일:** `app/api/devices.py`

```python
@router.get("/devices/{device_id}/usage")
def get_device_usage(device_id: str):
    # 1. usage_by_device에서 device_id로 조회
    # 2. 존재하면 사용 현황 데이터 반환
    # 3. 존재하지 않으면 HTTPException(status_code=404) 발생
    pass
```

**확인 방법:**
```bash
# 정상 케이스
curl http://localhost:8000/api/devices/D001/usage

# 존재하지 않는 디바이스
curl http://localhost:8000/api/devices/D999/usage
```

---

## FE: Frontend 구현

**파일:** `app/static/app.js`

### Step 1: 사용자 선택 시 가전 조회

`selectSubscriber(userId)` 함수를 구현하세요.

```javascript
async function selectSubscriber(userId) {
    // 1. selectedUserId 업데이트, selectedDeviceId = null
    // 2. renderSubscribers() 호출 (선택 상태 반영)
    // 3. 이전 사용 현황 초기화:
    //    - usage-empty 표시, usage-detail 숨기기
    //    - usage-info 내용 비우기
    // 4. GET /api/subscribers/{userId}/devices 호출
    // 5. currentDevices에 저장
    // 6. renderDevices() 호출
}
```

### Step 2: 가전 Table 렌더링 + 검색/필터

`renderDevices()` 함수를 구현하세요.

```javascript
function renderDevices() {
    // 1. 검색어, 상태 필터 값 가져오기
    // 2. currentDevices 배열 필터링
    //    - 검색: type, model, status, deviceId, location 부분 매칭
    //    - 필터: status 일치
    // 3. 가전이 없으면 → "No registered devices" 메시지 표시
    //    필터 결과가 없으면 → "No devices matched" 메시지 표시
    //    결과 있으면 → device-table 표시
    // 4. <tbody>에 deviceId, type, model, location, status(badge) 렌더링
    // 5. 각 행 클릭 시 selectDevice(deviceId) 호출
}
```

이벤트 리스너 주석을 해제하세요:
```javascript
document.getElementById("device-search").addEventListener("input", renderDevices);
document.getElementById("device-status-filter").addEventListener("change", renderDevices);
```

### Step 3: 가전 선택 시 사용 현황 조회

`selectDevice(deviceId)` 함수를 구현하세요.

```javascript
async function selectDevice(deviceId) {
    // 1. selectedDeviceId 업데이트
    // 2. renderDevices() 호출 (선택 상태 반영)
    // 3. GET /api/devices/{deviceId}/usage 호출
    // 4. usage-empty 숨기기, usage-detail 표시
    // 5. usage-info에 상세 정보 렌더링:
    //    - Device ID, Device Name
    //    - Power Status (badge 스타일 적용)
    //    - Last Used, Total Usage Hours, Weekly Usage Count
    //    - Health Status (badge 스타일 적용)
    //    - Remark
    // 6. renderUsageChart(data.weeklyUsageTrend) 호출
}
```

**usage-info HTML 구조 예시:**
```html
<div class="label">Device ID</div><div class="value">D001</div>
<div class="label">Device Name</div><div class="value">LG OLED evo C4</div>
<div class="label">Power Status</div><div class="value"><span class="badge status-on">On</span></div>
<!-- ... -->
```

### Step 4: 주간 사용량 Bar Chart

`renderUsageChart(trend)` 함수를 구현하세요.

```javascript
function renderUsageChart(trend) {
    const ctx = document.getElementById("usageChart");

    // 1. 기존 차트 있으면 destroy()
    // 2. new Chart() 생성
    //    - type: "bar"
    //    - labels: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    //    - data: trend 배열
    //    - options: responsive, beginAtZero
}
```

**Chart.js 참고:**
```javascript
usageChart = new Chart(ctx, {
    type: "bar",
    data: {
        labels: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        datasets: [{
            label: "Weekly Usage Trend",
            data: trend,
            borderWidth: 1
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: true,
        scales: { y: { beginAtZero: true } }
    }
});
```

---

## TE: 테스트 시나리오 (예시)

### 가전 목록 (4.3 + 4.4)

| # | 테스트 시나리오 | 예상 결과 | 결과 | 비고 |
|---|----------------|----------|------|------|
| 1 | `/api/subscribers/U001/devices` 호출 | 2개 가전 JSON 반환 | | |
| 2 | `/api/subscribers/U005/devices` 호출 | 빈 배열 `[]` 반환 | | |
| 3 | `/api/subscribers/U999/devices` 호출 | 404 에러 반환 | | |
| 4 | U001 클릭 시 가전 Table 표시 | D001, D002 표시 | | |
| 5 | U005 클릭 시 안내 메시지 | "No registered devices" 표시 | | |
| 6 | 가전 검색 "TV" 입력 | TV 타입만 표시 | | |
| 7 | 가전 상태 필터 "Online" 선택 | Online 가전만 표시 | | |

### 사용 현황 + 차트 (4.5 + 4.6)

| # | 테스트 시나리오 | 예상 결과 | 결과 | 비고 |
|---|----------------|----------|------|------|
| 8 | `/api/devices/D001/usage` 호출 | 사용 현황 JSON 반환 | | |
| 9 | `/api/devices/D999/usage` 호출 | 404 에러 반환 | | |
| 10 | D001 클릭 시 사용 현황 표시 | 전원상태, 누적시간 등 표시 | | |
| 11 | D001 클릭 시 Bar Chart 표시 | 요일별 사용량 차트 | | |
| 12 | 다른 가전 클릭 시 차트 갱신 | 이전 차트 제거, 새 차트 표시 | | |

---

## 예상 결과 화면

### 가전 목록
```
Subscriber "Kim Minsoo (U001)" 선택 시:

┌────────────────────────────────────────────────────┐
│ Devices              [Search...] [All Status ▼]     │
├──────┬────────┬────────────────┬───────────┬───────┤
│ ID   │ Type   │ Model          │ Location  │Status │
├──────┼────────┼────────────────┼───────────┼───────┤
│ D001 │ TV     │ LG OLED evo C4 │ Dormitory │Online │
│ D002 │ Washer │ LG WashTower   │ Home      │Offline│
└──────┴────────┴────────────────┴───────────┴───────┘
```

### 사용 현황 + 차트
```
Device "LG OLED evo C4 (D001)" 선택 시:

┌─────────────────────────────────────┐
│ Usage Detail                         │
│                                      │
│ Device ID        D001                │
│ Device Name      LG OLED evo C4      │
│ Power Status     [On]                │
│ Last Used        2026-03-22 10:10    │
│ Total Usage      152 hrs             │
│ Weekly Count     18                  │
│ Health Status    [Normal]            │
│ Remark           Streaming active    │
│                                      │
│ ┌──────────────────────────────────┐ │
│ │  ■       ■              ■    ■   │ │
│ │  ■   ■   ■       ■     ■    ■   │ │
│ │  ■   ■   ■   ■   ■     ■    ■   │ │
│ │  Mon Tue Wed Thu Fri Sat Sun     │ │
│ └──────────────────────────────────┘ │
└─────────────────────────────────────┘
```

---

## DevOps 실습 포인트

### Feature 브랜치 워크플로우
```bash
# 1. 새 브랜치 생성
git checkout -b feature/devices-api

# 2. 구현 후 커밋
git add app/api/subscribers.py app/api/devices.py app/static/app.js
git commit -m "feat: add devices list, usage API and weekly chart"

# 3. GitHub에 Push
git push origin feature/devices-api

# 4. GitHub에서 Pull Request 생성
#    - base: main ← compare: feature/devices-api
#    - PR 제목, 설명 작성

# 5. PM: TE의 검증 Report 확인 후 Merge
```
