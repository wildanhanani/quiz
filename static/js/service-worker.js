const STATIC_CACHE = 'belajaruji-static-v3';
const DYNAMIC_CACHE = 'belajaruji-dynamic-v3';
const OFFLINE_URL = '/offline/';

const STATIC_FILES = [
    '/',
    OFFLINE_URL,
    '/static/css/app.css',
    '/static/manifest.json',
    '/static/js/pwa.js',
    '/static/images/icon-192x192.png',
    '/static/images/icon-512x512.png',
];

self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(STATIC_CACHE).then((cache) => cache.addAll(STATIC_FILES))
    );
    self.skipWaiting();
});

self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then((cacheNames) => Promise.all(
            cacheNames
                .filter((cacheName) => ![STATIC_CACHE, DYNAMIC_CACHE].includes(cacheName))
                .map((cacheName) => caches.delete(cacheName))
        ))
    );
    self.clients.claim();
});

async function networkFirst(request) {
    const dynamicCache = await caches.open(DYNAMIC_CACHE);

    try {
        const response = await fetch(request);
        if (response && response.ok) {
            dynamicCache.put(request, response.clone());
        }
        return response;
    } catch (error) {
        const cachedResponse = await caches.match(request);
        if (cachedResponse) {
            return cachedResponse;
        }

        if (request.mode === 'navigate') {
            const offlineResponse = await caches.match(OFFLINE_URL);
            if (offlineResponse) {
                return offlineResponse;
            }
        }

        throw error;
    }
}

async function staleWhileRevalidate(request) {
    const cachedResponse = await caches.match(request);
    const fetchPromise = fetch(request)
        .then(async (response) => {
            if (response && response.ok) {
                const dynamicCache = await caches.open(DYNAMIC_CACHE);
                dynamicCache.put(request, response.clone());
            }
            return response;
        })
        .catch(() => null);

    return cachedResponse || fetchPromise;
}

self.addEventListener('fetch', (event) => {
    const { request } = event;

    if (request.method !== 'GET') {
        return;
    }

    const url = new URL(request.url);
    if (!['http:', 'https:'].includes(url.protocol)) {
        return;
    }

    if (request.mode === 'navigate') {
        event.respondWith(networkFirst(request));
        return;
    }

    if (url.origin !== self.location.origin) {
        event.respondWith(
            fetch(request).catch(() => caches.match(request))
        );
        return;
    }

    event.respondWith(staleWhileRevalidate(request));
});

self.addEventListener('push', (event) => {
    const options = {
        body: event.data ? event.data.text() : 'New notification',
        icon: '/static/images/icon-192x192.png',
        badge: '/static/images/icon-192x192.png',
        vibrate: [200, 100, 200],
    };

    event.waitUntil(
        self.registration.showNotification('BelajarUji', options)
    );
});
