# Stage 1
FROM node:16-alpine AS deps
LABEL org.opencontainers.image.source="https://github.com/dinavinter/AgentGPT"

RUN apk add --no-cache libc6-compat
WORKDIR /app
COPY package.json package-lock.json ./
COPY . .

RUN \
    --mount=type=cache,target=/var/cache/node_modules \
    npm install --omit=dev --production=true

# Stage 2
FROM node:16-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
COPY ./production.next.config.mjs ./next.config.mjs
ARG HOST_API
ENV NEXT_PUBLIC_HOST_API=${HOST_API}
RUN NODE_ENV=production
RUN \
    --mount=type=cache,target=/var/cache/build \
    npm run build

# Stage 3
FROM node:16-alpine AS production
WORKDIR /app
ENV NODE_ENV production
RUN addgroup --system --gid 1001 nodejs && adduser --system --uid 1001 nextjs
COPY --from=builder /app/production.next.config.mjs ./next.config.mjs
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static
COPY entrypoint.sh /
RUN chmod +x /entrypoint.sh
COPY wait-for-db.sh /
RUN chmod +x /wait-for-db.sh
COPY /prisma ./prisma/

USER nextjs
EXPOSE 3000
ENV PORT 3000
ENV NEXT_TELEMETRY_DISABLED 1
ENTRYPOINT [ "sh", "/entrypoint.sh" ]
CMD ["node", "server.js"]
