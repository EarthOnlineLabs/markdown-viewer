/* Markdown Viewer — service worker
   Purpose: PWA installability, offline app-shell, and Web Share Target handling.
   Kept conservative: only same-origin GET app-shell is cached; cross-origin
   markdown fetches and the local /api/read are passed straight through. */

const CACHE = 'mdv-shell-v2';
const MARKED = 'https://cdn.jsdelivr.net/npm/marked/marked.min.js';
const SHELL = [
  '/',
  '/md-viewer.html',
  '/manifest.webmanifest',
  '/favicon.svg',
  '/icons/icon-192.png',
  '/icons/icon-512.png',
  MARKED,
];

self.addEventListener('install', (e) => {
  self.skipWaiting();
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(SHELL).catch(() => {})));
});

self.addEventListener('activate', (e) => {
  e.waitUntil((async () => {
    const keys = await caches.keys();
    await Promise.all(
      keys.filter((k) => k !== CACHE && k !== 'md-shared').map((k) => caches.delete(k))
    );
    await self.clients.claim();
  })());
});

self.addEventListener('fetch', (e) => {
  const req = e.request;
  const url = new URL(req.url);

  // --- Web Share Target: receive shared file/text/url, stash it, redirect to viewer ---
  if (req.method === 'POST' && url.pathname === '/share-target') {
    e.respondWith((async () => {
      let text = '', name = '分享内容', shareUrl = '';
      try {
        const form = await req.formData();
        const file = form.get('file');
        text = (form.get('text') || '').toString();
        shareUrl = (form.get('url') || '').toString();
        if (file && typeof file.text === 'function' && file.size) {
          text = await file.text();
          name = file.name || '分享文件.md';
        }
        const cache = await caches.open('md-shared');
        await cache.put(
          '/__shared__',
          new Response(JSON.stringify({ text, name, url: shareUrl }), {
            headers: { 'Content-Type': 'application/json' },
          })
        );
      } catch (_) {}
      return Response.redirect('/?from=share', 303);
    })());
    return;
  }

  // marked CDN: cache-first so the app works offline
  if (req.url === MARKED) {
    e.respondWith(caches.match(req).then((c) => c || fetch(req)));
    return;
  }

  // pass through cross-origin (external markdown URLs) and non-GET
  if (req.method !== 'GET' || url.origin !== self.location.origin) return;

  // same-origin GET: network-first (fresh on deploy), fall back to cache offline
  e.respondWith((async () => {
    try {
      const net = await fetch(req);
      if (net && net.ok) {
        const c = await caches.open(CACHE);
        c.put(req, net.clone()).catch(() => {});
      }
      return net;
    } catch (_) {
      const cached = await caches.match(req);
      return cached || caches.match('/md-viewer.html') || Response.error();
    }
  })());
});
