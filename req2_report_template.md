# requirement_2 검증 Report (TE 실습)

| 항목 | 내용 |
|------|------|
| **프로젝트** | webOS Subscription Management Dashboard |
| **검증 대상** | requirement_2.md (가전 목록 + 사용 현황 + 차트) |
| **검증 일시** | 2026-09-28 17:26:19 |
| **작성자** | (여기에 이름을 적으세요) |

**총 5건 중 PASS 5 / FAIL 0 - Pass Rate 100.0%**

| TC ID | 테스트 시나리오 | 기대 결과 | 실제 결과 | 판정 |
|:-----:|----------------|-----------|-----------|:----:|
| DEV-01 | get_devices_by_user('U001') 직접 호출 | 2개 가전 반환 | 2개 반환 | ✅ PASS |
| API-01 | GET /api/subscribers/U001/devices | 200 OK | status=200 | ✅ PASS |
| TE-1 | /api/subscribers/U001/devices 호출 | D001, D002 (2개) 반환 | ['D001', 'D002'] | ✅ PASS |
| TE-3 | /api/subscribers/U999/devices 호출 | 404 에러 반환 | status=404 | ✅ PASS |
| TE-6 | 가전 검색 "TV" 입력 | TV 타입만 표시 | 1개: ['D001'] | ✅ PASS |

> 본 Report 는 `tests/req2_test_template.py` 로 생성되었습니다.
