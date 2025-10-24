class MemoryCache {
    constructor(ttlSeconds = 60) {
        this.cache = new Map();
        this.ttl = ttlSeconds * 1000; // Convert to milliseconds
        console.log(`Iniciando sistema de cache com TTL=${ttlSeconds} segundos`);
    }

    async get(key) {
        const item = this.cache.get(key);

        if (!item) {
            return null;
        }

        const now = Date.now();
        if (now - item.timestamp > this.ttl) {
            this.cache.delete(key);
            return null;
        }

        return item.value;
    }

    async set(key, value) {
        this.cache.set(key, {
            value: value,
            timestamp: Date.now()
        });
    }

    async delete(key) {
        this.cache.delete(key);
    }

    async clear() {
        this.cache.clear();
    }

    async size() {
        return this.cache.size;
    }
}

module.exports = MemoryCache;