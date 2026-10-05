FROM node:24.21.0-bookworm-slim@sha256:0e0ff40c39bc087845bfb27465a0df4ea419520094bc35842ff83dd8cbe6f9b6 AS node
FROM mcr.microsoft.com/playwright:v1.63.0-noble@sha256:eff16c30e6f3f4af0a03fa4b706120d5e9b0891c344a27d64559aff5900a4a27
COPY --from=node /usr/local/bin/node /usr/local/bin/node
COPY --from=node /usr/local/lib/node_modules/npm /usr/local/lib/node_modules/npm
RUN ln -sf /usr/local/lib/node_modules/npm/bin/npm-cli.js /usr/local/bin/npm \
 && groupadd -g 10001 perfdev && useradd -u 10001 -g 10001 -M perfdev
# Only human-reviewed manifests are present during the networked download step.
# No repository lifecycle/build/test script runs with network access.
WORKDIR /opt/gcreation-deps
COPY package.json package-lock.json ./
RUN npm ci --ignore-scripts --no-audit --no-fund --cache=/tmp/reviewed-npm-cache \
 && rm -rf /tmp/reviewed-npm-cache
WORKDIR /opt/gcreation-trusted
COPY trusted-source/ ./
RUN --network=none ln -s /opt/gcreation-deps/node_modules node_modules \
 && /usr/local/bin/node /opt/gcreation-deps/node_modules/typescript/bin/tsc -p ops/dev/trusted/tsconfig.json
ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright NODE_ENV=development
USER 10001:10001
WORKDIR /app
