const CACHE_NAME = 'testsoal-v2';
const STATIC_CACHE = 'testsoal-static-v2';
const DYNAMIC_CACHE = 'testsoal-dynamic-v2';

// Files to cache immediately
const STATIC_FILES = [
    '/',
    '/static/css/style.css',
    '/static/manifest.json',
    'https://cdn.tailwindcss.com',
];

// Install event - cache static assets
self.addEventListener('install', (event) => {
    console.log('[Service Worker] Installing...');
    event.waitUntil(
        caches.open(STATIC_CACHE)
            .then((cache) => {
                console.log('[Service Worker] Caching static assets');
                return cache.addAll(STATIC_FILES);
            })
            .catch((err) => {
                console.log('[Service Worker] Cache failed:', err);
            })
    );
    self.skipWaiting();
});

// Activate event - clean up old caches
self.addEventListener('activate', (event) => {
    console.log('[Service Worker] Activating...');
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames
                    .filter((cacheName) => {
                        return cacheName !== STATIC_CACHE && cacheName !== DYNAMIC_CACHE;
                    })
                    .map((cacheName) => {
                        console.log('[Service Worker] Deleting old cache:', cacheName);
                        return caches.delete(cacheName);
                    })
            );
        })
    );
    return self.clients.claim();
});

// Fetch event - serve from cache, fallback to network
self.addEventListener('fetch', (event) => {
    const { request } = event;
    const url = new URL(request.url);

    // Skip cross-origin requests
    if (url.origin !== location.origin) {
        // For Tailwind CDN and external resources, use network first
        event.respondWith(
            fetch(request)
                .then((response) => {
                    return caches.open(DYNAMIC_CACHE).then((cache) => {
                        cache.put(request, response.clone());
                        return response;
                    });
                })
                .catch(() => caches.match(request))
        );
        return;
    }

    // NETWORK FIRST strategy for quiz/soal pages (always get latest data when online)
    const isQuizPage = url.pathname.includes('/quiz/') ||
        url.pathname.includes('/dashboard') ||
        url.pathname.includes('/history') ||
        url.pathname.includes('/take_quiz');

    if (isQuizPage && request.method === 'GET') {
        event.respondWith(
            fetch(request)
                .then((response) => {
                    // Clone the response
                    const responseToCache = response.clone();

                    // Update cache with latest content
                    caches.open(DYNAMIC_CACHE)
                        .then((cache) => {
                            cache.put(request, responseToCache);
                        });

                    return response;
                })
                .catch(() => {
                    // If offline, fallback to cache
                    return caches.match(request)
                        .then((cachedResponse) => {
                            if (cachedResponse) {
                                return cachedResponse;
                            }
                            // Ultimate fallback
                            if (request.destination === 'document') {
                                return caches.match('/');
                            }
                        });
                })
        );
        return;
    }

    // CACHE FIRST strategy for other pages (faster loading)
    event.respondWith(
        caches.match(request)
            .then((cachedResponse) => {
                if (cachedResponse) {
                    // Return cached version and update cache in background
                    fetch(request)
                        .then((response) => {
                            return caches.open(DYNAMIC_CACHE).then((cache) => {
                                cache.put(request, response.clone());
                                return response;
                            });
                        })
                        .catch(() => { });
                    return cachedResponse;
                }

                // Not in cache, fetch from network
                return fetch(request)
                    .then((response) => {
                        // Don't cache non-successful responses
                        if (!response || response.status !== 200 || response.type === 'error') {
                            return response;
                        }

                        // Clone the response
                        const responseToCache = response.clone();

                        // Cache pages and assets
                        if (request.method === 'GET') {
                            caches.open(DYNAMIC_CACHE)
                                .then((cache) => {
                                    cache.put(request, responseToCache);
                                });
                        }

                        return response;
                    })
                    .catch(() => {
                        // Offline fallback
                        if (request.destination === 'document') {
                            return caches.match('/');
                        }
                    });
            })
    );
});

// Background sync for quiz submissions (optional)
self.addEventListener('sync', (event) => {
    if (event.tag === 'sync-quiz-answers') {
        event.waitUntil(syncQuizAnswers());
    }
});

async function syncQuizAnswers() {
    // Implement background sync logic if needed
    console.log('[Service Worker] Syncing quiz answers...');
}

// Push notifications (optional for future)
self.addEventListener('push', (event) => {
    const options = {
        body: event.data ? event.data.text() : 'New notification',
        icon: '/static/images/icon-192x192.png',
        badge: '/static/images/icon-192x192.png',
        vibrate: [200, 100, 200],
    };

    event.waitUntil(
        self.registration.showNotification('Test Soal', options)
    );
});
