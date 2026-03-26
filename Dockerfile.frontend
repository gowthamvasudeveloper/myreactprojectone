# Frontend image using multi-stage build:
# 1) Build React app with Vite
# 2) Serve static files via nginx

FROM node:20-alpine AS build
WORKDIR /frontend

COPY package.json package-lock.json ./
RUN npm ci

COPY . .
RUN npm run build

FROM nginx:1.27-alpine AS runtime

# Custom nginx config for SPA routing and API proxying.
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy built app
COPY --from=build /frontend/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]

