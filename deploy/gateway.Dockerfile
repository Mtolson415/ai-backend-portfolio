FROM nginx:stable-alpine@sha256:583b7f2fce1cdb8da5ad5c39ebd3c33b98b87d493190e548bdee1fa8c619c311
RUN apk add --no-cache --upgrade libxslt=1.1.43-r4
COPY deploy/nginx.conf /etc/nginx/nginx.conf
USER 10001:10001
ENTRYPOINT ["nginx"]
CMD ["-g", "daemon off;"]
