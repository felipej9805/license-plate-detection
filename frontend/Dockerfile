FROM node:alpine
WORKDIR /app
COPY package.json ./
COPY package-lock.json ./
COPY ./ ./
RUN npm i
ENV REACT_APP_DETECTION="localhost:5000"
EXPOSE 3000
CMD ["npm", "run", "start"]