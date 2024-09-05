FROM registry.access.redhat.com/ubi8/nodejs-18@sha256:27fe4270eb1ebd19a8e284ed5230fedd8a7075e69302b992636250f7d1ee9337

WORKDIR /usr/src/app

COPY --chown=1001:1001 package*.json ./

RUN npm ci --omit=dev

# Copy app source into the container
COPY --chown=1001:1001 . .

# Configure fastify port and host defaults
#ENV FASTIFY_PORT 8080
#ENV FASTIFY_ADDRESS 0.0.0.0

# Note that the container exposes services on 8080
EXPOSE 8080

CMD [ "npm", "start"]
