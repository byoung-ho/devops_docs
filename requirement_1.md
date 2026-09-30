# 요구사항 #1: 구독 사용자 조회 + 검색/필터

## 목표

전체 구독 사용자 목록을 API로 제공하고, 대시보드 Table에 표시합니다.
검색 및 상태 필터 기능을 구현합니다.

---

## 역할별 작업

| 역할 | 작업 내용 |
|------|----------|
| **PM** | 요구사항을 FE/BE에 배분, TE에 테스트 시나리오 작성 요청 |
| **BE** | `GET /api/subscribers` API 구현 |
| **FE** | Table 렌더링 + 검색/필터 구현 |
| **TE** | 테스트 시나리오 작성 → 검증 → Report 작성 |

---

## 완료 조건

- [ ] `GET /api/subscribers` API가 정상 동작한다
- [ ] 대시보드 진입 시 구독자 목록이 Table에 자동 표시된다
- [ ] 이름 / 플랜 / 상태 / ID 기준 검색이 동작한다
- [ ] Active / Paused / Expired 상태 필터가 동작한다
- [ ] 검색/필터 결과가 실시간 반영된다
- [ ] TE의 검증 Report가 작성되었다

---

## BE: Backend API 구현

**파일:** `app/api/subscribers.py`

`GET /api/subscribers` 엔드포인트를 구현하세요.

```python
@router.get("/subscribers")
def get_subscribers():
    # subscribers 리스트 전체를 반환
    pass
```

**확인 방법:**
```bash
# 서버 실행
uvicorn app.main:app --reload

# API 테스트 (브라우저 또는 터미널)
# http://localhost:8000/api/subscribers
```

---

## FE: Frontend 구현

**파일:** `app/static/app.js`

### Step 1: 데이터 조회

`fetchSubscribers()` 함수를 구현하세요.

```javascript
async function fetchSubscribers() {
    // 1. GET /api/subscribers 호출
    // 2. 응답을 subscribers 변수에 저장
    // 3. renderSubscribers() 호출
}
```

파일 하단의 `fetchSubscribers()` 주석을 해제하세요.

### Step 2: Table 렌더링 + 검색/필터

`renderSubscribers()` 함수를 구현하세요.

```javascript
function renderSubscribers() {
    // 1. 검색어와 상태 필터 값 가져오기
    // 2. subscribers 배열 필터링
    //    - 검색: name, plan, status, userId에 대해 부분 문자열 매칭
    //    - 필터: status가 선택된 값과 일치
    // 3. <tbody>에 <tr> 렌더링
    //    - 표시 컬럼: userId, name, plan, status, deviceCount
    //    - 각 행 클릭 시 selectSubscriber(userId) 호출
    //    - 선택된 행(selectedUserId)에 "selected" 클래스 추가
}
```

이벤트 리스너 주석을 해제하세요:
```javascript
document.getElementById("subscriber-search").addEventListener("input", renderSubscribers);
document.getElementById("subscriber-status-filter").addEventListener("change", renderSubscribers);
```

---

## TE: 테스트 시나리오 (예시)

| # | 테스트 시나리오 | 예상 결과 | 결과 | 비고 |
|---|----------------|----------|------|------|
| 1 | `/api/subscribers` 호출 | 5명의 사용자 목록 JSON 반환 | | |
| 2 | 대시보드 접속 시 Table 자동 표시 | 5명 목록 표시 | | |
| 3 | 검색창에 "Kim" 입력 | Kim Minsoo만 표시 | | |
| 4 | 검색창에 "Premium" 입력 | Premium 플랜 사용자만 표시 | | |
| 5 | 상태 필터 "Active" 선택 | Active 사용자만 표시 | | |
| 6 | 상태 필터 "Expired" 선택 | Jung Hyerin만 표시 | | |
| 7 | 검색 + 필터 동시 적용 | 두 조건 모두 만족하는 결과만 표시 | | |
| 8 | 검색어 삭제 시 | 전체 목록 복원 | | |

---

## 예상 결과 화면

```
┌─────────────────────────────────────────────────┐
│ Subscribers           [Search...] [All Status ▼] │
├──────┬────────────┬─────────┬────────┬──────────┤
│ ID   │ Name       │ Plan    │ Status │ Devices  │
├──────┼────────────┼─────────┼────────┼──────────┤
│ U001 │ Kim Minsoo │ Premium │ Active │ 2        │
│ U002 │ Lee Jiyoon │ Basic   │ Active │ 1        │
│ U003 │ Park Junho │ Family  │ Paused │ 3        │
│ ...  │ ...        │ ...     │ ...    │ ...      │
└──────┴────────────┴─────────┴────────┴──────────┘
```

---

## DevOps 실습 포인트

### 수동 CI (로컬 검증)
```bash
# 1. 서버가 정상 실행되는지 확인
uvicorn app.main:app --reload

# 2. API 응답 확인
curl http://localhost:8000/api/subscribers

# 3. 브라우저에서 대시보드 확인
# http://localhost:8000
```

### PM: 검증 후 Git + Render CD
```bash
# TE의 검증 Report 확인 후 진행

# 1. 변경사항 커밋
git add app/api/subscribers.py app/static/app.js
git commit -m "feat: add subscribers list API and table rendering"

# 2. GitHub에 Push
git push origin main

```
