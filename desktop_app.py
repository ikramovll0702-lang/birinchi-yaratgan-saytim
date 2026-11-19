"""
HEMIS Desktop Application Launcher
pywebview yordamida veb tizimni alohida Windows oynasi (desktop dastur) sifatida ishga tushirish.
"""
import os
import sys
import time
import socket
import threading
import urllib.request
import uvicorn
import webview

def find_free_port(preferred: int = 8000) -> int:
    """Belgilangan yoki bo'sh portni topish."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(("127.0.0.1", preferred))
            return preferred
        except OSError:
            s.bind(("127.0.0.1", 0))
            return s.getsockname()[1]

def run_uvicorn_server(port: int):
    """FastAPI serverini orqa fonda ishga tushirish."""
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=port,
        log_level="warning",
        access_log=False
    )

def wait_for_server(url: str, timeout: float = 25.0) -> bool:
    """Server ishga tushishini kutish."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "HEMIS-Desktop"})
            with urllib.request.urlopen(req, timeout=1.5) as resp:
                if resp.status in (200, 302, 307):
                    return True
        except Exception:
            time.sleep(0.3)
    return False

def main():
    port = find_free_port(8000)
    server_url = f"http://127.0.0.1:{port}"
    check_url = f"{server_url}/auth/login"

    # Serverni daemon ipda ishga tushirish
    server_thread = threading.Thread(
        target=run_uvicorn_server,
        args=(port,),
        daemon=True,
        name="HEMIS-Server-Thread"
    )
    server_thread.start()

    # Server tayyor bo'lishini kutish
    if not wait_for_server(check_url, timeout=25.0):
        print(f"[XATOLIK] Server {server_url} da o'z vaqtida javob bermadi.")
        sys.exit(1)

    # Alohida dastur oynasini ochish (Microsoft Edge WebView2 motorida)
    title = "HEMIS - Oliy Ta'lim Muassasasi Talabalar Boshqaruv Tizimi"
    window = webview.create_window(
        title=title,
        url=server_url,
        width=1280,
        height=820,
        min_size=(960, 640),
        confirm_close=False,
        text_select=True
    )

    webview.start(private_mode=False, debug=False)

if __name__ == "__main__":
    main()
