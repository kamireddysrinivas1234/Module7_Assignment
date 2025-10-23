import argparse
import os
import sys
import re
from datetime import datetime
from pathlib import Path

from loguru import logger
from dotenv import load_dotenv
import qrcode

# Load .env if present
load_dotenv()

DEFAULT_URL = os.getenv("DEFAULT_URL", "https://github.com/kaw393939")
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "qr_codes")
LOG_DIR = os.getenv("LOG_DIR", "logs")
DEFAULT_FILENAME = os.getenv("FILENAME", "")  # if empty we auto-generate
DEFAULT_BOX_SIZE = int(os.getenv("QR_BOX_SIZE", "10"))
DEFAULT_BORDER = int(os.getenv("QR_BORDER", "4"))

# Very loose URL check (good enough for this tool)
_URL_RE = re.compile(r"^https?://", re.IGNORECASE)

def ensure_dirs():
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
    Path(LOG_DIR).mkdir(parents=True, exist_ok=True)

def configure_logger():
    ensure_dirs()
    log_file = Path(LOG_DIR) / "app.log"
    logger.remove()
    logger.add(sys.stderr, level="INFO")
    logger.add(log_file, rotation="1 MB", retention=10, level="INFO")

def build_filename(name_hint: str | None) -> str:
    if name_hint:
        base = name_hint.strip()
    elif DEFAULT_FILENAME:
        base = DEFAULT_FILENAME.strip()
    else:
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base = f"qr_{stamp}.png"

    if not base.lower().endswith(".png"):
        base += ".png"
    return base

def generate_qr(data: str, out_path: Path, box_size: int, border: int):
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=box_size,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(out_path)

def parse_args():
    parser = argparse.ArgumentParser(description="Generate a QR code PNG for a URL.")
    parser.add_argument("--url", "-u", default=DEFAULT_URL, help=f"Target URL (default: {DEFAULT_URL})")
    parser.add_argument("--filename", "-f", default="", help="Output filename (default: auto-named .png)")
    parser.add_argument("--box-size", type=int, default=DEFAULT_BOX_SIZE, help=f"QR box size (default: {DEFAULT_BOX_SIZE})")
    parser.add_argument("--border", type=int, default=DEFAULT_BORDER, help=f"QR border (default: {DEFAULT_BORDER})")
    parser.add_argument("--silent", action="store_true", help="Suppress stdout (logs still written)")
    return parser.parse_args()

def main():
    configure_logger()
    args = parse_args()

    url = args.url.strip()
    if not _URL_RE.match(url):
        logger.error("Invalid or missing URL. Must start with http:// or https://")
        sys.exit(2)

    filename = build_filename(args.filename)
    out_path = Path(OUTPUT_DIR) / filename

    logger.info(f"Generating QR for: {url}")
    logger.info(f"Writing to: {out_path}")

    ensure_dirs()
    try:
        generate_qr(url, out_path, args.box_size, args.border)
    except Exception as exc:
        logger.exception(f"Failed to generate QR code: {exc}")
        sys.exit(1)

    msg = f"✅ QR code saved: {out_path.resolve()}"
    logger.info(msg)
    if not args.silent:
        print(msg)

if __name__ == "__main__":
    main()
