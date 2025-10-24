const CoinbaseClient = require('../../external-apis/CoinbaseClient');
const MercadoBitcoinClient = require('../../external-apis/MercadoBitcoinClient');
const MemoryCache = require('../../cache/MemoryCache');

class ExchangeRepositoryImpl {
    constructor() {
        this.clients = {
            'mercadobitcoin': new MercadoBitcoinClient(),
            'coinbase': new CoinbaseClient()
        };
        this.cache = new MemoryCache(60); // 60 seconds TTL
    }

    getAvailableExchanges() {
        return Object.keys(this.clients);
    }

    async getSymbols(exchange) {
        try {
            if (!this.clients[exchange]) {
                return [];
            }

            const cacheKey = `symbols-${exchange}`;
            const cachedSymbols = await this.cache.get(cacheKey);

            if (cachedSymbols) {
                return cachedSymbols;
            }

            const client = this.clients[exchange];
            const symbols = await client.getSymbols();

            if (symbols && symbols.length > 0) {
                await this.cache.set(cacheKey, symbols);
            }

            return symbols;
        } catch (error) {
            console.error(`Erro detalhado no ExchangeRepositoryImpl.getSymbols para ${exchange}:`, error);
            return [];
        }
    }

    async getTicker(exchange, symbol) {
        try {
            if (!this.clients[exchange]) {
                return null;
            }

            const cacheKey = `ticker-${exchange}-${symbol}`;
            const cachedTicker = await this.cache.get(cacheKey);

            if (cachedTicker) {
                return cachedTicker;
            }

            const client = this.clients[exchange];
            const ticker = await client.getTicker(symbol);

            if (ticker) {
                await this.cache.set(cacheKey, ticker);
            }

            return ticker;
        } catch (error) {
            console.error(`Erro detalhado no ExchangeRepositoryImpl.getTicker para ${symbol} em ${exchange}:`, error);
            return null;
        }
    }
}

module.exports = ExchangeRepositoryImpl;