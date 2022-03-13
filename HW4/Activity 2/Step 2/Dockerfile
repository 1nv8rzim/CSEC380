FROM php:apache

COPY ./armbook_packaged /var/www/html/
RUN docker-php-ext-install mysqli

EXPOSE 80