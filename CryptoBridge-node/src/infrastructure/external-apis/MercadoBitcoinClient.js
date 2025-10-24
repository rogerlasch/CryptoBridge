const axios = require('axios');
const Ticker = require('../../domain/entities/Ticker');

class MercadoBitcoinClient {
    constructor() {
        this.BaseUrl = 'https://api.mercadobitcoin.net/api/v4';
        this.timeout = 10000; // 10 seconds
    }

    async getSymbols() {
        try {
            const response = await axios.get(`${this.BaseUrl}/symbols`, {
                timeout: this.timeout
            });

            if (response.status !== 200) {
                return [];
            }

            return response.data.symbol || [];
        } catch (error) {
            console.error('Erro ao buscar símbolos no Mercado Bitcoin:', error.message);
            return [];
        }
    }

    async getTicker(symbol) {
        try {
            const response = await axios.get(`${this.BaseUrl}/tickers?symbols=${symbol}`, {
                timeout: this.timeout
            });

            if (response.status !== 200) {
                return null;
            }

            const data = response.data;

            if (!data || data.length === 0) {
                return null;
            }

            const tickerData = data[0];

            return new Ticker(
                symbol,
                parseFloat(tickerData.buy || 0),
                parseFloat(tickerData.sell || 0),
                parseFloat(tickerData.vol || 0),
                parseFloat(tickerData.low || 0),
                parseFloat(tickerData.high || 0),
                parseFloat(tickerData.last || 0)
            );
        } catch (error) {
            console.error(`Erro ao buscar ticker ${symbol} no Mercado Bitcoin:`, error.message);
            return null;
        }
    }
}

module.exports = MercadoBitcoinClient;