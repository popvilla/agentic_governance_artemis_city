# Stage 1: Builder - Install dependencies and build the application
FROM node:18-alpine AS builder

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json first to leverage Docker cache
# This ensures that npm install is only re-run if dependencies change
COPY package*.json ./

# Install application dependencies
# Using 'npm ci' for deterministic builds, which is ideal for CI/CD and Docker
RUN npm ci --omit=dev

# Copy the rest of the application code
COPY . .

# Build the TypeScript project
RUN npm run build

# Stage 2: Production - Create a lean image with only the necessary files
FROM node:18-alpine

# Set the working directory in the container
WORKDIR /app

# Set environment variables for production
ENV NODE_ENV production

# Copy only the compiled application and production node_modules from the builder stage
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/package.json ./package.json

# Expose the port the app runs on
EXPOSE 3000

# Run as a non-root user for security best practices
# The node:alpine image typically creates a 'node' user with appropriate permissions
USER node

# Run the compiled application
CMD ["npm", "start"]