from pathlib import Path
import subprocess, sys, time

BASE_DIR = Path(__file__).parent.resolve()

SENDER_DIR = BASE_DIR / "error_sending"
RECEIVER_DIR = BASE_DIR / "error_receiving"


def popen(cmd: str, cwd: Path):
    return subprocess.Popen(
        cmd,
        cwd=str(cwd),
        shell=True,
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
    )

if __name__ == "__main__":
    receiver = popen(
        "uvicorn webhook_receiver:app --port 8000",
        cwd=RECEIVER_DIR
    )

    time.sleep(1)

    sender = popen(
        "uvicorn main:app --port 8001",
        cwd=SENDER_DIR
    )

    try:
        receiver.wait()
        sender.wait()
    except KeyboardInterrupt:
        subprocess.run(f"taskkill /PID {receiver.pid} /F /T", shell=True)
        subprocess.run(f"taskkill /PID {sender.pid} /F /T", shell=True)
        sys.exit(0)