<?php

/*
 * Bu dosyayi config.local.php olarak kopyalayin ve yalnizca sunucudaki
 * gercek MySQL bilgilerini yazin. config.local.php Git tarafindan izlenmez.
 */
return [
    'database' => [
        'host' => 'localhost',
        'port' => 3306,
        'name' => 'macera_akademi',
        'user' => 'macera_user',
        'password' => 'BURAYA_GUCLU_PAROLA_YAZIN',
        'charset' => 'utf8mb4',
    ],

    /* Mobil uygulamalar API'ye bu origin'lerle ulasir. */
    'allowed_origins' => [
        'https://maceraakademi.com.tr',
        'https://www.maceraakademi.com.tr',
        'https://appassets.androidplatform.net',
        'null',
    ],

    /* Cihaz oturumunun kac gun gecerli kalacagi. */
    'token_ttl_days' => 90,
    'debug' => false,
];
