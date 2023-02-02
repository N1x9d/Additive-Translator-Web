FROM node:10.1.0
MAINTAINER Dan Lynn <docker@danlynn.org>
WORKDIR /myapp
COPY . .
RUN npm run build
# run ember server on container start
CMD ["npm", "start"]
