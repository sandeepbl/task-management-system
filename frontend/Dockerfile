# Use an official Node.js runtime as a parent image
FROM node:14 as build-stage

WORKDIR /app

COPY package.json ./
RUN npm install

COPY . .

RUN npm run build

# Use an official Nginx runtime as a parent image
FROM nginx:stable-alpine as production-stage

COPY --from=build-stage /app/dist /usr/share/nginx/html

# Copy custom nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
