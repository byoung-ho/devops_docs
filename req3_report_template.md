# requirement_3 검증 Report (TE 실습)

| 항목 | 내용 |
|------|------|
| **프로젝트** | webOS Subscription Management Dashboard |
| **검증 대상** | requirement_3.md (상태 Badge + GitHub Actions CI) |
| **검증 일시** | 2026-09-28 17:38:32 |
| **작성자** | (여기에 이름을 적으세요) |

**총 4건 중 PASS 4 / FAIL 0 - Pass Rate 100.0%**

| TC ID | 테스트 시나리오 | 기대 결과 | 실제 결과 | 판정 |
|:-----:|----------------|-----------|-----------|:----:|
| TE-1 | Active 상태 구독자 확인 | 초록 badge (status-active) | status-active | ✅ PASS |
| TE-5 | Offline 상태 가전 확인 | 회색 badge (status-offline) | status-offline | ✅ PASS |
| CI-01 | .github/workflows/ci.yml 존재 | 파일 존재 | 존재 | ✅ PASS |
| TE-11 | CI health 체크 (로컬 재현) | 200 OK | status=200 | ✅ PASS |

> TE-10(실제 CI 실행), TE-13(Render 배포)은 GitHub Actions 탭과 배포 URL 에서 직접 확인하세요.
> 본 Report 는 `tests/req3_test_template.py` 로 생성되었습니다.
