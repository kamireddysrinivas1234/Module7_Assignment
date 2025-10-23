# QR Code Generator (Module 7 - Dockerized)

Dockerized Python CLI that generates QR codes as PNG images. Uses a non-root user, slim base image, volumes, and overrideable CMD.

## Quick Run (Local - VS Code / Windows)

```pwsh
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py --url https://www.njit.edu
```

## Docker

```pwsh
docker build -t qr-code-generator-app .
docker run -d --name qr-generator qr-code-generator-app
mkdir qr_codes
docker run -d --name qr-generator2 `
  -v "${PWD}/qr_codes:/app/qr_codes" `
  qr-code-generator-app --url https://www.njit.edu
docker logs qr-generator2
```

## GitHub Actions Workflow

Workflow file at `.github/workflows/ci.yml` installs deps and runs a smoke test that generates `qr_codes/ci_smoke.png`.

## Links to Submit

- GitHub Repo: https://github.com/kamireddysrinivas1234/Module7_Assignment
- DockerHub Image: https://hub.docker.com/r/srinivaskamireddy/qr-code-generator-app
