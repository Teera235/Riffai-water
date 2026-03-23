FROM node:20-alpine

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm ci --only=production

# Copy app files
COPY . .

# Build app
ARG NEXT_PUBLIC_API_URL=https://riffai-backend-715107904640.asia-southeast1.run.app
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL
ENV NODE_ENV=production

RUN npm run build

# Expose port
EXPOSE 3000

# Start app
CMD ["npm", "start"]
