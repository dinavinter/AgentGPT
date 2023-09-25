# Use the official Node.js image as the base image
FROM node:18-alpine as base

ARG NODE_ENV

ENV NODE_ENV=$NODE_ENV

# Needed for the wait-for-db script
RUN apk add --no-cache netcat-openbsd

RUN echo "$NODE_ENV"

RUN echo $NODE_ENV

RUN npm install -g npm@10.1.0
# Set the working directory
WORKDIR /next

# Copy package.json and package-lock.json to the working directory
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy the wait-for-db.sh script
COPY wait-for-db.sh /usr/local/bin/wait-for-db.sh
RUN chmod +x /usr/local/bin/wait-for-db.sh

# Copy the rest of the application code
COPY . .
COPY entrypoint.sh /

# Ensure correct line endings after these files are edited by windows
RUN apk add --no-cache dos2unix netcat-openbsd \
    && dos2unix /entrypoint.sh

# Expose the port the app will run on
EXPOSE 3000

ENTRYPOINT ["sh", "/entrypoint.sh"]

FROM base as dev
# Start the application
CMD ["npm", "run", "dev"]

FROM base as prod
# Build the application
RUN npm run build
CMD ["npm", "run", "start"]
