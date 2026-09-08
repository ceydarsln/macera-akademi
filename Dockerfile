FROM php:8.2-apache

RUN docker-php-ext-install pdo_mysql \
    && a2enmod headers \
    && rm -rf /var/lib/apt/lists/*

COPY docker/apache-macera.conf /etc/apache2/conf-available/macera.conf
RUN a2enconf macera

COPY web/ /opt/macera/web/
COPY tools/aynala.sh /opt/macera/tools/aynala.sh
RUN chmod +x /opt/macera/tools/aynala.sh \
    && mkdir -p /opt/macera/app/src/main/assets \
    && /opt/macera/tools/aynala.sh \
    && cp -a /opt/macera/web/. /var/www/html/ \
    && rm -rf /opt/macera \
    && chown -R www-data:www-data /var/www/html

COPY docker/healthcheck.php /usr/local/bin/macera-healthcheck.php

EXPOSE 80

HEALTHCHECK --interval=30s --timeout=6s --start-period=20s --retries=3 \
    CMD ["php", "/usr/local/bin/macera-healthcheck.php"]
