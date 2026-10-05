FROM node:24.21.0-bookworm-slim AS node
FROM mcr.microsoft.com/playwright:v1.63.0-noble
COPY --from=node /usr/local/bin/node /usr/local/bin/node
COPY --from=node /usr/local/lib/node_modules/npm /usr/local/lib/node_modules/npm
RUN ln -sf /usr/local/lib/node_modules/npm/bin/npm-cli.js /usr/local/bin/npm \
 && groupadd -g 10001 perfdev && useradd -u 10001 -g 10001 -M perfdev
ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright NODE_ENV=development
USER 10001:10001
WORKDIR /app
