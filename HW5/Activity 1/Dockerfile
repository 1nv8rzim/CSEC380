FROM php:apache

COPY ./armbook_packaged /var/www/html/
RUN docker-php-ext-install mysqli
RUN a2enmod ssl
COPY ./apache-selfsigned.key /etc/ssl/private/apache-selfsigned.key
COPY ./apache-selfsigned.crt /etc/ssl/certs/apache-selfsigned.crt
RUN echo PFZpcnR1YWxIb3N0ICo6NDQzPgogICBEb2N1bWVudFJvb3QgL3Zhci93d3cvaHRtbAoKICAgU1NMRW5naW5lIG9uCiAgIFNTTENlcnRpZmljYXRlRmlsZSAvZXRjL3NzbC9jZXJ0cy9hcGFjaGUtc2VsZnNpZ25lZC5jcnQKICAgU1NMQ2VydGlmaWNhdGVLZXlGaWxlIC9ldGMvc3NsL3ByaXZhdGUvYXBhY2hlLXNlbGZzaWduZWQua2V5CjwvVmlydHVhbEhvc3Q+ | base64 -d >> /etc/apache2/sites-enabled/000-default.conf
EXPOSE 80
EXPOSE 443