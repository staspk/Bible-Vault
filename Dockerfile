FROM node:24.4

RUN npm install -g npm@latest tsx pm2


WORKDIR /bible

COPY . .

RUN npm install

