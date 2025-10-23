# Reflection: Dockerizing the QR Code Generator

Dockerization helped me package the QR app and its dependencies into a reproducible image. I focused on security by using `python:3.12-slim-bullseye`, running as a non-root user, and isolating writable paths (`/app/qr_codes`, `/app/logs`). Using `ENTRYPOINT ["python","main.py"]` with a default `CMD` lets me override the target URL at runtime without changing the image, which is helpful for testing and grading. The `.dockerignore` reduced context size and improved build speed.

A key challenge was logging configuration. Loguru’s `retention` argument initially failed when I used the string `"10 files"`; switching to an integer value `10` resolved it. I validated volume mounts on Windows by mapping a local `qr_codes` folder to `/app/qr_codes` and confirming that images were written to the host. The GitHub Actions workflow provides quick feedback by installing requirements and running a smoke test that ensures a PNG is generated in CI.

Overall, I’m confident building minimal images, tagging/pushing to DockerHub, and using volumes and environment variables to adjust runtime behavior. I’d like more practice with multi-stage builds, automated vulnerability scanning, and artifact uploads from CI, but this assignment solidified the fundamentals of containerizing Python apps and establishing a simple CI pipeline.
