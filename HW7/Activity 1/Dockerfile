FROM  php:apache

RUN docker-php-ext-install mysqli && docker-php-ext-enable mysqli

COPY armbook/ /var/www/html/

EXPOSE 80