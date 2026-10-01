"""
requirement_1.md 검증 템플릿 스크립트  (학생용)

이 파일은 무엇인가요?
--------------------
여러분(TE 역할)이 requirement_1 을 "직접 검증"하고, 그 결과를
Markdown Report 파일로 만드는 방법을 익히기 위한 '템플릿'입니다.

이미 동작하는 예제 몇 개가 들어 있습니다. 실행하면 바로 Report 가 생깁니다.
그다음, 아래 `TODO` 부분을 채워서 나머지 TE 시나리오를 완성하세요.

실행 방법
--------
    # 프로젝트 루트에서
    python tests/req1_test_template.py

결과
----
    tests/reports/req1_report_template.md   (여러분이 만든 검증 Report)

필요 패키지: fastapi, uvicorn (requirements.txt 에 이미 포함)
             그 외에는 파이썬 표준 라이브러리만 사용합니다.

────────────────────────────────────────────────────────────────────────
검증 흐름 3단계 (requirement_1.md 기준)
  1) 개발자 테스트  : 코드가 문법적으로 올바르고 함수가 값을 반환하는가?
  2) API 테스트     : 서버를 켜고 /api/subscribers 가 실제로 동작하는가?
  3) TE 시나리오    : 검색/필터가 "기대 결과"대로 동작하는가?
────────────────────────────────────────────────────────────────────────
"""

import os
import sys
import time
import json
import socket
import subprocess
import urllib.request
import urllib.error
from datetime import datetime

# Windows 콘솔(cp949)에서도 한글/기호가 깨지지 않도록 출력 인코딩을 UTF-8 로 설정
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

# =============================================================================
# 경로 설정 (수정할 필요 없음)
# =============================================================================
THIS_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(THIS_DIR)
REPORT_DIR = os.path.join(THIS_DIR, "reports")
REPORT_PATH = os.path.join(REPORT_DIR, "req1_report_template.md")

os.chdir(PROJECT_ROOT)          # 상대경로(app/static 등)를 위해 루트로 이동
BASE_URL = None                 # 서버 기동 후 채워짐

# 검증 결과를 담는 리스트. 각 항목: (TC ID, 시나리오, 기대결과, 실제결과, 통과여부)
results = []


def check(tc_id, scenario, expected, actual, passed):
    """검증 결과 1건을 기록한다."""
    results.append((tc_id, scenario, expected, actual, passed))
    tag = "PASS" if passed else "FAIL"
    print(f"  [{tag}] {tc_id}  {scenario}")


# =============================================================================
# HTTP 유틸 (수정할 필요 없음)
# =============================================================================
def http_get(path, timeout=5):
    """(status_code, json_data) 반환. 실패 시 (None, None)."""
    try:
        with urllib.request.urlopen(BASE_URL + path, timeout=timeout) as resp:
            body = resp.read().decode("utf-8")
            try:
                return resp.status, json.loads(body)
            except json.JSONDecodeError:
                return resp.status, None
    except urllib.error.HTTPError as e:
        return e.code, None
    except Exception:
        return None, None


# 검색/필터 로직 (app.js renderSubscribers 와 동일한 규칙을 파이썬으로 재현)
def filter_subscribers(subs, search="", status=""):
    s = (search or "").lower()
    out = []
    for u in subs:
        matches_search = (
            s in u["name"].lower()
            or s in u["plan"].lower()
            or s in u["status"].lower()
            or s in u["userId"].lower()
        )
        matches_status = (not status) or u["status"] == status
        if matches_search and matches_status:
            out.append(u)
    return out


# =============================================================================
# 서버 기동 유틸 (수정할 필요 없음)
# =============================================================================
def find_free_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port


def start_server(port):
    proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app",
         "--host", "127.0.0.1", "--port", str(port)],
        cwd=PROJECT_ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
    )
    for _ in range(40):
        if proc.poll() is not None:
            return proc, False
        try:
            with urllib.request.urlopen(f"http://127.0.0.1:{port}/health", timeout=1) as r:
                if r.status == 200:
                    return proc, True
        except Exception:
            time.sleep(0.5)
    return proc, False


def stop_server(proc):
    if proc and proc.poll() is None:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()


# =============================================================================
# 검증 실행부  ★★★ 여기서부터 여러분이 채웁니다 ★★★
# =============================================================================
def run_tests():
    # -------------------------------------------------------------------------
    # [예제 1] 개발자 테스트 : get_subscribers() 함수가 5명을 반환하는가?
    #   서버 없이도 함수를 직접 불러서 확인할 수 있습니다.
    # -------------------------------------------------------------------------
    try:
        from app.api.subscribers import get_subscribers
        data = get_subscribers()
        passed = isinstance(data, list) and len(data) == 5
        actual = f"{len(data)}명 반환" if isinstance(data, list) else "list 아님/None"
    except Exception as e:
        passed, actual = False, f"예외: {e}"
    check("DEV-01", "get_subscribers() 함수 직접 호출", "5명 반환", actual, passed)

    # -------------------------------------------------------------------------
    # [예제 2] API 테스트 : GET /api/subscribers 가 200 을 반환하는가?
    # -------------------------------------------------------------------------
    status, body = http_get("/api/subscribers")
    check("API-01", "GET /api/subscribers 호출", "200 OK",
          f"status={status}", status == 200)

    # 이후 TE 시나리오에서 재사용하기 위해 목록을 확보
    subscribers = body if isinstance(body, list) else []

    # -------------------------------------------------------------------------
    # [예제 3] TE 시나리오 #1 : /api/subscribers 호출 → 5명 반환
    # -------------------------------------------------------------------------
    passed = len(subscribers) == 5
    check("TE-1", "/api/subscribers 호출", "5명의 사용자 목록 반환",
          f"{len(subscribers)}명", passed)

    # -------------------------------------------------------------------------
    # [예제 4] TE 시나리오 #3 : 검색 "Kim" → Kim Minsoo 만 표시
    #   filter_subscribers() 를 사용해 검색 결과를 계산합니다.
    # -------------------------------------------------------------------------
    r = filter_subscribers(subscribers, search="Kim")
    passed = len(r) == 1 and r and r[0]["name"] == "Kim Minsoo"
    check("TE-3", '검색창에 "Kim" 입력', "Kim Minsoo만 표시",
          f'{len(r)}명: {[u["name"] for u in r]}', passed)

    # =========================================================================
    # ★ TODO 1 : TE 시나리오 #4 
    # =========================================================================
    # =========================================================================
    # ★ TODO 2 : TE 시나리오 #... 
    # ...
    # ...


# =============================================================================
# Markdown Report 생성 (수정할 필요 없음)
# =============================================================================
def render_report():
    total = len(results)
    passed = sum(1 for *_, p in results if p)
    failed = total - passed
    rate = (passed / total * 100) if total else 0.0

    lines = []
    lines.append("# requirement_1 검증 Report (TE 실습)")
    lines.append("")
    lines.append("| 항목 | 내용 |")
    lines.append("|------|------|")
    lines.append("| **프로젝트** | webOS Subscription Management Dashboard |")
    lines.append("| **검증 대상** | requirement_1.md |")
    lines.append(f"| **검증 일시** | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} |")
    lines.append("| **작성자** | (여기에 이름을 적으세요) |")
    lines.append("")
    lines.append(f"**총 {total}건 중 PASS {passed} / FAIL {failed} — Pass Rate {rate:.1f}%**")
    lines.append("")
    lines.append("| TC ID | 테스트 시나리오 | 기대 결과 | 실제 결과 | 판정 |")
    lines.append("|:-----:|----------------|-----------|-----------|:----:|")
    for tc_id, scenario, expected, actual, passed_ in results:
        mark = "✅ PASS" if passed_ else "❌ FAIL"
        lines.append(f"| {tc_id} | {scenario} | {expected} | {actual} | {mark} |")
    lines.append("")
    lines.append("> 본 Report 는 `tests/req1_test_template.py` 로 생성되었습니다.")

    os.makedirs(REPORT_DIR, exist_ok=True)
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    return passed, failed, total, rate


# =============================================================================
# main (수정할 필요 없음)
# =============================================================================
def main():
    global BASE_URL
    print("=" * 60)
    print(" requirement_1 검증 (학생용 템플릿)")
    print("=" * 60)

    if PROJECT_ROOT not in sys.path:
        sys.path.insert(0, PROJECT_ROOT)

    port = find_free_port()
    print(f"[서버 기동] 127.0.0.1:{port} ...")
    proc, ok = start_server(port)
    if not ok:
        print("[오류] 서버 기동 실패. requirements 설치 및 app/main.py 를 확인하세요.")
        stop_server(proc)
        sys.exit(1)

    BASE_URL = f"http://127.0.0.1:{port}"
    print("[서버 기동] 성공\n")

    run_tests()

    stop_server(proc)

    passed, failed, total, rate = render_report()
    print("\n" + "=" * 60)
    print(f" 결과: PASS {passed} / FAIL {failed} (총 {total}) - {rate:.1f}%")
    print(f" Report 저장: {os.path.relpath(REPORT_PATH, PROJECT_ROOT)}")
    print("=" * 60)


if __name__ == "__main__":
    main()
