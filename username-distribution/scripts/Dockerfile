FROM registry.access.redhat.com/ubi8/nodejs-12:latest

WORKDIR /opt/app-root/src

COPY package*.json ./

RUN npm install

COPY . .

EXPOSE 8080

CMD [ "npm", "start" ]


