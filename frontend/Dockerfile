FROM node:18-alpine AS build 

WORKDIR /app

# ENV BACKEND_URL=${BACKEND_URL}

COPY package*.json ./

RUN npm install

RUN npm i -g serve

# Copy the rest of the application code to the container
COPY . .

RUN npm run build

ENV PORT 5173

EXPOSE $PORT



FROM nginx:alpine 

COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 5173/tcp

CMD ["/usr/sbin/nginx", "-g", "daemon off;"]