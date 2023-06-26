FROM node:14-alpine


WORKDIR /app


COPY simulation_app/package.json ./
COPY package-lock.json ./
RUN npm install


COPY . .


RUN npm run build


FROM nginx:1.17.1-alpine
COPY --from=0 /app/build /usr/share/nginx/html
