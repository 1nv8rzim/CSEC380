FROM  php:apache

RUN mkdir -p /etc/apache2/ssl
RUN a2enmod ssl
RUN a2enmod rewrite
RUN a2enmod http2
RUN a2enmod headers 
RUN docker-php-ext-install mysqli

COPY armbook_packaged/ /var/www/html/
COPY 000-default.conf /etc/apache2/sites-enabled/000-default.conf
COPY apache.crt /etc/apache2/ssl/apache.crt
COPY apache.key /etc/apache2/ssl/apache.key

RUN service apache2 restart

EXPOSE 80
EXPOSE 443