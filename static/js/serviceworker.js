const staticCacheName = "djangopwa-v1";

self.addEventListener("install", (event) => {
    event.waitUntil(
        caches.open(staticCacheName).then((cache) => {
            return cache.addAll([
                '/offline',
                '/css/django-pwa-app.css',
            ]);
        })
    );
});

self.addEventListener("fetch", (event) => {
    const requestUrl = new URL(event.request.url);
    if (requestUrl.origin === location.origin) {
        if ((requestUrl.pathname === "/")) {
            event.respondWith(caches.match(""));
            return;
        }
    }
    event.respondWith(
        caches.match(event.request).then((response) => {
            return response || fetch(event.request);
        })
    );
});
