const axios = require('axios');
const Ticker = require('../../domain/entities/Ticker');

class CoinbaseClient {
    constructor() {
        this.BaseUrl = 'https://api.exchange.coinbase.com/products';
        this.timeout = 10000; // 10 seconds
    }

    async getSymbols() {
        try {
            const response = await axios.get(this.BaseUrl, {
                timeout: this.timeout
            });

            if (response.status !== 200) {
                return [];
            }

            return response.data.map(product => product.id);
        } catch (error) {
            console.error('Erro ao buscar símbolos no Coinbase:', error.message);
            return [];
        }
    }

    async getTicker(symbol) {
        try {
            const [statsResponse, tickerResponse] = await Promise.all([
                axios.get(`${this.BaseUrl}/${symbol}/stats`, { timeout: this.timeout }),
                axios.get(`${this.BaseUrl}/${symbol}/ticker`, { timeout: this.timeout })
            ]);

            if (statsResponse.status !== 200 || tickerResponse.status !== 200) {
                return null;
            }

            const statsData = statsResponse.data;
            const tickerData = tickerResponse.data;

            return new Ticker(
                symbol,
                parseFloat(tickerData.bid || 0),
                parseFloat(tickerData.ask || 0),
                parseFloat(statsData.volume || 0),
                parseFloat(statsData.low || 0),
                parseFloat(statsData.high || 0),
                parseFloat(tickerData.price || 0)
            );
        } catch (error) {
            console.error(`Erro ao buscar ticker ${symbol} no Coinbase:`, error.message);
            return null;
        }
    }
}

module.exports = CoinbaseClient;