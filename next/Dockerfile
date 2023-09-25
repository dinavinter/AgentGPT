# Use the official Node.js image as the base image
FROM node:18-alpine AS entrypoint

COPY entrypoint.sh /
RUN chmod +x /entrypoint.sh

RUN apk add --no-cache dos2unix netcat-openbsd \
    && dos2unix /entrypoint.sh

# =========================entrypoint=========================

FROM node:18-alpine AS deps

ENV NODE_ENV production
ENV NEXT_TELEMETRY_DISABLED 1

RUN apk add --no-cache libc6-compat netcat-openbsd
RUN npm install -g npm@latest

WORKDIR /next

COPY package.json package-lock.json ./
RUN  npm install --production

# Copy the wait-for-db.sh script
COPY wait-for-db.sh /usr/local/bin/wait-for-db.sh
RUN chmod +x /usr/local/bin/wait-for-db.sh

RUN apk add --no-cache dos2unix netcat-openbsd

# FROM node:18-alpine as prepare
# # Copy the rest of the application code
# COPY . .
# COPY entrypoint.sh /

# RUN dos2unix /entrypoint.sh

# =========================deps=========================

FROM deps AS builder
# WORKDIR /next
# COPY --from=deps /next/node_modules ./node_modules
COPY . .

ENV NEXT_TELEMETRY_DISABLED 1

RUN npm install -g npm@latest

RUN npm run prepare
RUN npm run build --no-lint --production --output-path=./.next

# =========================builder=========================

FROM node:16-alpine AS runner
WORKDIR /app
ENV NODE_ENV production
RUN addgroup --system --gid 1001 nodejs && adduser --system --uid 1001 nextjs
COPY --from=builder /app/next.config.js ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static
USER nextjs
EXPOSE 3000
ENV PORT 3000
ENV NEXT_TELEMETRY_DISABLED 1
CMD ["node", "server.js"]


# =========================runner=========================

FROM builder AS production

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

# COPY --from=builder --chown=nextjs:nodejs /next/.next ./.next/
# COPY --from=builder /next/node_modules ./node_modules/
# COPY --from=builder /next/package.json ./package.json
COPY entrypoint.sh /
RUN chmod +x /entrypoint.sh

# COPY --from=entrypoint --chown=nextjs:nodejs /next/entrypoint.sh /
# RUN chmod +x /entrypoint.sh



# USER nextjs

# Expose the port the app will run on
EXPOSE 3000

ENTRYPOINT ["sh", "/entrypoint.sh"]


# Start the application
CMD ["npm", "run", "start"]

# =========================production=========================


FROM builder AS setuser

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=builder --chown=nextjs:nodejs /next/.next ./.next/
COPY --from=builder /next/node_modules ./node_modules/
COPY --from=builder /next/package.json ./package.json
COPY --from=builder /next/entrypoint.sh /
RUN chmod +x /entrypoint.sh



# Copy the rest of the application code
# COPY --from=builder /app /
# COPY --from=builder /app/.next ./.next
# COPY --from=builder /app/node_modules ./node_modules
# COPY --from=builder /app/package.json ./package.json
# COPY entrypoint.sh /

# Ensure correct line endings after these files are edited by windows
# RUN apk add --no-cache dos2unix netcat-openbsd \
#     && dos2unix /entrypoint.sh



# RUN npm install -g npm@latest

# RUN dos2unix /entrypoint.sh

# COPY --from=builder --chown=nextjs:nodejs /app/.next ./.next
# COPY --from=builder /app/node_modules ./node_modules
# COPY --from=builder /app/package.json ./package.json


# # ARG NODE_ENV

# # ENV NODE_ENV=$NODE_ENV

# # Needed for the wait-for-db script
# # RUN apk add --no-cache netcat-openbsd

# # RUN echo "$NODE_ENV"

# # RUN echo $NODE_ENV

# # Set the working directory
# WORKDIR /next

# # Copy package.json and package-lock.json to the working directory
# COPY package*.json ./

# # Install dependencies
# RUN npm ci


# FROM base as dev
# # Start the application
# COPY --from=base /next /next
# WORKDIR /next

# CMD ["npm", "run", "dev"]

# FROM base as prod
# COPY --from=base /next /next
# WORKDIR /next
# # Build the application
# RUN npm run prepare
# RUN npx next build --no-lint
# # Remove dev dependencies
# RUN npm prune --production
# # Remove the source code
# RUN rm -rf src

# # Start the application
# CMD ["npm", "run", "dev"]
