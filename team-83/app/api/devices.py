from fastapi import APIRouter, HTTPException
from app.data.dummy_data import usage_by_device

router = APIRouter()


# =============================================================================
# TODO [요구사항 #2]: GET /api/devices/{device_id}/usage
# =============================================================================
# 특정 가전의 상세 사용 현황을 반환하는 엔드포인트를 구현하세요.
# - HTTP Method: GET
# - Path: /devices/{device_id}/usage
# - Path Parameter: device_id (str)
# - 정상 응답: 해당 디바이스의 사용 현황 데이터를 JSON으로 반환
# - 디바이스가 존재하지 않는 경우: HTTPException(status_code=404) 반환
# - 참고: usage_by_device 딕셔너리를 활용하세요.
# =============================================================================
@router.get("/devices/{device_id}/usage")
def get_device_usage(device_id: str):
    usage = usage_by_device.get(device_id)
    if usage is None:
        raise HTTPException(status_code=404, detail="Device not found")
    return usage