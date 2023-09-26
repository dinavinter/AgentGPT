# Stage 1
FROM node:16-alpine AS deps
RUN apk add --no-cache libc6-compat
WORKDIR /app
COPY package.json package-lock.json ./
COPY . .
RUN npm install --omit=dev --production=true

# Stage 2
FROM node:16-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
COPY ./production.next.config.mjs ./next.config.mjs
ARG HOST_API
ENV NEXT_PUBLIC_HOST_API=${HOST_API}
RUN NODE_ENV=production npm run build && npm prune --production

# Stage 3
FROM node:16-alpine AS production
WORKDIR /app
ENV NODE_ENV production
RUN addgroup --system --gid 1001 nodejs && adduser --system --uid 1001 nextjs
COPY --from=builder /app/production.next.config.mjs ./next.config.mjs
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static
USER nextjs
EXPOSE 3000
ENV PORT 3000
ENV NEXT_TELEMETRY_DISABLED 1
CMD ["node", "server.js"]
