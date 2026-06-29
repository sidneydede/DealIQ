// Service worker minimal — coque applicative en cache (offline partiel, mobile-first).
const CACHE = "dealiq-shell-v1";
const SHELL = ["/", "/index.html", "/manifest.webmanifest", "/icon.svg"];

self.addEventListener("install", (event) => {
  event.waitUntil(caches.open(CACHE).then((c) => c.addAll(SHELL)));
  self.skipWaiting();
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k))),
    ),
  );
  self.clients.claim();
});

self.addEventListener("fetch", (event) => {
  const { request } = event;
  if (request.method !== "GET") return;
  // Ne jamais mettre en cache les appels API.
  if (new URL(request.url).pathname.startsWith("/api/")) return;

  // Navigations : réseau d'abord, repli sur la coque en cache (offline).
  if (request.mode === "navigate") {
    event.respondWith(fetch(request).catch(() => caches.match("/index.html")));
    return;
  }
  // Autres GET : cache d'abord, puis réseau.
  event.respondWith(caches.match(request).then((hit) => hit || fetch(request)));
});
