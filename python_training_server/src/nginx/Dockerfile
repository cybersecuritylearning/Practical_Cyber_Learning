FROM nginx:alpine

RUN rm /etc/nginx/nginx.conf /etc/nginx/conf.d/default.conf

COPY nginx.conf.template /nginx.conf.template

ENV DOLLAR=$
CMD ["/bin/sh" , "-c" , "envsubst < /nginx.conf.template > /etc/nginx/nginx.conf && exec nginx -g 'daemon off;'"]
RUN mkdir -p /var/www/html

RUN mkdir -p /nginx/logs