# Canonical environment for the heterogeneity validation:
# R 4.6.0 (rocker, built from source at that version) + metafor/metadat from the 2026-10-01 Posit Package Manager
# snapshot + Node 24.15.0 + Playwright 1.63.0 with its own Chromium + pinned Python packages.
#   docker build -t heterogeneity-reproducible .
#   docker run --rm -v "$PWD/outputs:/work/outputs" heterogeneity-reproducible           # full run (default)
#   docker run --rm heterogeneity-reproducible --quick
FROM node:24.15.0-bookworm-slim AS node
FROM rocker/r-ver:4.6.0
COPY --from=node /usr/local/bin/node /usr/local/bin/node
COPY --from=node /usr/local/lib/node_modules /usr/local/lib/node_modules
RUN ln -s /usr/local/lib/node_modules/npm/bin/npm-cli.js /usr/local/bin/npm && ln -s /usr/local/lib/node_modules/npm/bin/npx-cli.js /usr/local/bin/npx
ENV DEBIAN_FRONTEND=noninteractive PYTHONDONTWRITEBYTECODE=1 PIP_NO_CACHE_DIR=1 MPLBACKEND=Agg \
    OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PLAYWRIGHT_BROWSERS_PATH=/opt/ms-playwright
RUN apt-get update && apt-get install -y --no-install-recommends python3 python3-venv && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY bench/install_r_packages.R bench/install_r_packages.R
RUN Rscript bench/install_r_packages.R
COPY requirements.txt .
RUN python3 -m venv /opt/venv && /opt/venv/bin/pip install -r requirements.txt
ENV PATH="/opt/venv/bin:$PATH"
COPY package.json package-lock.json ./
RUN npm ci && npx playwright install --with-deps chromium && rm -rf /var/lib/apt/lists/*
COPY . .
ENTRYPOINT ["python", "reproduce.py"]
