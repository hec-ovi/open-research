# =============================================================================
# Frontend Dockerfile - Vite + React + TypeScript
# =============================================================================

FROM node:20-slim

# Set working directory
WORKDIR /app

# Install curl for health checks
RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy project files (except node_modules which is in .dockerignore)
COPY . .

# Expose port
EXPOSE 5173

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:5173 || exit 1

# Default command (overridden in docker-compose for dev mode)
CMD ["npm", "run", "dev"]
