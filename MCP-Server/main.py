from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

# ======================================================================================
# 1. ĐỊNH NGHĨA CÁC CẤU TRÚC DỮ LIỆU (PYDANTIC MODELS)
# ======================================================================================

# Các model này ánh xạ trực tiếp tới cấu trúc JSON trong tài liệu API
# Giúp FastAPI tự động validate dữ liệu nhận được và serialize dữ liệu trả về.

# --- Cấu trúc cho Request Body ---

class ApplicationRequest(BaseModel):
    version: str
    elf_sha256: str

class BoardRequest(BaseModel):
    type: str
    name: str
    ssid: str
    rssi: int

class OtaRequest(BaseModel):
    application: ApplicationRequest
    mac_address: Optional[str] = None
    uuid: Optional[str] = None
    chip_model_name: Optional[str] = None
    flash_size: Optional[int] = None
    psram_size: Optional[int] = None
    partition_table: Optional[List[Any]] = None
    board: BoardRequest

# --- Cấu trúc cho Response Body ---

class ActivationResponse(BaseModel):
    code: str
    message: str

class MqttResponse(BaseModel):
    endpoint: str
    client_id: str
    username: str
    password: str

class WebsocketResponse(BaseModel):
    url: str
    token: str

class ServerTimeResponse(BaseModel):
    timestamp: int
    timezone: str
    timezone_offset: int

class FirmwareResponse(BaseModel):
    version: str
    url: str

class OtaResponse(BaseModel):
    activation: ActivationResponse
    mqtt: MqttResponse
    websocket: WebsocketResponse
    server_time: ServerTimeResponse
    firmware: FirmwareResponse

# ======================================================================================
# 2. KHỞI TẠO ỨNG DỤNG FASTAPI
# ======================================================================================

app = FastAPI(
    title="MiMi Control Protocol Server",
    description="Máy chủ trung tâm cho dự án MiMi, xử lý OTA và giao tiếp thiết bị.",
    version="0.2.0",
)

# ======================================================================================
# 3. ĐỊNH NGHĨA CÁC ENDPOINTS
# ======================================================================================

@app.get("/")
def read_root():
    """
    Endpoint gốc, dùng để kiểm tra xem máy chủ có đang hoạt động hay không.
    """
    return {"message": "Chào mừng đến với MiMi Control Protocol Server! Endpoint /api/ota/ đã sẵn sàng."}

@app.post("/api/ota/", response_model=OtaResponse)
def handle_ota_request(
    request_body: OtaRequest,
    device_id: str = Header(..., description="Mã định danh duy nhất của thiết bị"),
    user_agent: str = Header(..., description="Tên và phiên bản phần mềm client, ví dụ: esp-box-3/1.5.6"),
    client_id: Optional[str] = Header(None, description="Mã định danh duy nhất của client"),
    accept_language: Optional[str] = Header(None, description="Ngôn ngữ hiện tại của client")
):
    """
    Xử lý yêu cầu nâng cấp OTA (Over-The-Air) của thiết bị.

    Endpoint này nhận thông tin về phiên bản firmware hiện tại của thiết bị 
    và trả về thông tin phiên bản mới nhất cùng các cấu hình khác.
    """
    print(f"Nhận được yêu cầu OTA từ Device-Id: {device_id}")
    print(f"User-Agent: {user_agent}")
    print(f"Client-Id: {client_id}")
    print(f"Firmware hiện tại: {request_body.application.version}")
    print(f"Thông tin bo mạch: {request_body.board.name}")

    # --- LOGIC GIẢ (MOCK LOGIC) ---
    # Trong thực tế, bạn sẽ cần:
    # 1. Tra cứu `device_id` hoặc `user_agent` trong cơ sở dữ liệu.
    # 2. Dựa vào phiên bản và loại thiết bị, quyết định xem có bản cập nhật không.
    # 3. Lấy thông tin phiên bản mới nhất và URL tải xuống từ cơ sở dữ liệu.
    # 4. Tạo mã kích hoạt, thông tin MQTT/WebSocket.
    #
    # Hiện tại, chúng ta sẽ trả về một phản hồi mẫu được hard-coded.
    
    # Tạo một phản hồi mẫu
    mock_response = OtaResponse(
        activation=ActivationResponse(
            code="MIM123",
            message="Vui lòng kích hoạt trên màn hình thiết bị của bạn."
        ),
        mqtt=MqttResponse(
            endpoint="mqtt.mimi-protocol.dev",
            client_id=f"GID_test@@@{device_id}@@@{request_body.uuid}",
            username="device_user",
            password="secure_password"
        ),
        websocket=WebsocketResponse(
            url="wss://api.mimi-protocol.dev/v1/ws",
            token="a-very-secure-websocket-token"
        ),
        server_time=ServerTimeResponse(
            timestamp=1678886400000,
            timezone="Asia/Ho_Chi_Minh",
            timezone_offset=25200
        ),
        firmware=FirmwareResponse(
            version="1.0.2", # Giả sử đây là phiên bản mới hơn
            url=f"https://storage.googleapis.com/mimi-firmware/esp-box-3/1.0.2.bin"
        )
    )

    return mock_response

# ======================================================================================
# Lệnh để chạy máy chủ (chỉ dành cho môi trường dev):
# uvicorn MCP-Server.main:app --reload --host 0.0.0.0 --port 8000
# ======================================================================================
