const CACHE_NAME = 'healthos-v3';
const ASSETS = [
    './',
    './index.html',
    './app.js',
    './manifest.json',
    'https://cdn.tailwindcss.com',
    'https://cdn.jsdelivr.net/npm/chart.js',
    'https://unpkg.com/lucide@latest'
];

// Install: cache assets
self.addEventListener('install', (e) => {
    e.waitUntil(
        caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSETS))
    );
    // Activate immediately, don't wait for old SW to finish
    self.skipWaiting();
});

// Activate: clean up old caches
self.addEventListener('activate', (e) => {
    e.waitUntil(
        caches.keys().then(keys =>
            Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k)))
        )
    );
    // Take control of all clients immediately
    self.clients.claim();
});

// Fetch: network-first for local files, cache-first for CDN
self.addEventListener('fetch', (e) => {
    const url = new URL(e.request.url);

    // Never cache API calls — they must always reach the server
    if (url.pathname.startsWith('/api/')) return;

    // For local files: try network first, fall back to cache
    if (url.origin === self.location.origin) {
        e.respondWith(
            fetch(e.request)
                .then(response => {
                    const clone = response.clone();
                    caches.open(CACHE_NAME).then(cache => cache.put(e.request, clone));
                    return response;
                })
                .catch(() => caches.match(e.request))
        );
    } else {
        // CDN: cache-first
        e.respondWith(
            caches.match(e.request).then(response => response || fetch(e.request))
        );
    }
});
