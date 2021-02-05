const CACHE_NAME = 'static-cache';

// const FILES_TO_CACHE = [
//     '/src/web/static/',
//     'src/'
// ];

self.addEventListener('install', (evt) => {
    console.log('[ServiceWorker] Instalando');
    // evt.waitUntil(
    //     caches.open(CACHE_NAME).then((cache) => {
    //         console.log('[ServiceWorker] Pre-caching offline page');
    //         return cache.addAll(FILES_TO_CACHE);
    //     })
    // );

    // self.skipWaiting();
});

self.addEventListener('activate', (evt) => {
    console.log('[ServiceWorker] Activate');
    evt.waitUntil(
        caches.keys().then((keyList) => {
            return Promise.all(keyList.map((key) => {
                if (key !== CACHE_NAME) {
                    console.log('[ServiceWorker] Removiendo cache antiguo', key);
                    return caches.delete(key);
                }
            }));
        })
    );
    self.clients.claim();
});

self.addEventListener('fetch', function (event) {
    event.respondWith(
        caches.match(event.request).then(function (response) {
            return response || fetch(event.request);
        })
    );
});