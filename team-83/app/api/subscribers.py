from fastapi import APIRouter, HTTPException
from app.data.dummy_data import subscribers, devices_by_user

router = APIRouter()


# =============================================================================
# TODO [요구사항 #1]: GET /api/subscribers
# =============================================================================
# 전체 구독 사용자 목록을 반환하는 엔드포인트를 구현하세요.
#
# - HTTP Method: GET
# - Path: /subscribers
# - 응답: subscribers 리스트 전체를 JSON으로 반환
# - 참고: dummy_data.py의 subscribers 변수를 활용하세요.
# =============================================================================
@router.get("/subscribers")
def get_subscribers():
    return subscribers

# =============================================================================
# TODO [요구사항 #2]: GET /api/subscribers/{user_id}/devices
# =============================================================================
# 특정 사용자의 가전 목록을 반환하는 엔드포인트를 구현하세요.
#
# - HTTP Method: GET
# - Path: /subscribers/{user_id}/devices
# - Path Parameter: user_id (str)
# - 정상 응답: 해당 사용자의 디바이스 리스트 반환
# - 사용자가 존재하지 않는 경우: HTTPException(status_code=404) 반환
# - 가전이 없는 경우: 빈 리스트([]) 반환
# - 참고: devices_by_user 딕셔너리를 활용하세요.
# =============================================================================
@router.get("/subscribers/{user_id}/devices")
def get_devices_by_user(user_id: str):
    if not any(s["userId"] == user_id for s in subscribers):
        raise HTTPException(status_code=404, detail="User not found")
    return devices_by_user.get(user_id, [])