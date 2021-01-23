self.addEventListener("install", e => {
    e.waitUntill(
        caches.open("static").then(cache => {
            return cache.addAll(["./src/", "./src/static/", "./src/static/images/favicon.png"])
        })
    )
})

self.addEventListener("fetch", e => {
    console.log("Interceptando fetch desde :: " + e.request.url);
    e.respondWith(
        caches.match(e.request).then(response => {
            return response || fetch(e.response)
        })
    )
})
