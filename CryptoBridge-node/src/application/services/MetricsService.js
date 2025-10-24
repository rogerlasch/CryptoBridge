class MetricsService {
    constructor(metricsRepository) {
        this.metricsRepository = metricsRepository;
    }

    async recordApiCall(endpoint, method, statusCode, responseTimeMs) {
        try {
            await this.metricsRepository.recordApiCall(endpoint, method, statusCode, responseTimeMs);
        } catch (error) {
            console.error('Erro detalhado no MetricsService.recordApiCall:', error);
        }
    }

    async getTopExchanges(limit = 10) {
        try {
            const exchanges = await this.metricsRepository.getTopExchanges(limit);
            return {
                status: 200,
                top_exchanges: exchanges.map(e => ({
                    exchange_name: e.exchangeName,
                    request_count: e.requestCount,
                    last_accessed: e.lastAccessed.toISOString(),
                    created_at: e.createdAt.toISOString()
                }))
            };
        } catch (error) {
            console.error('Erro detalhado no MetricsService.getTopExchanges:', error);
            return {
                status: 500,
                msg: 'Erro interno do servidor.'
            };
        }
    }

    async getTopTickers(limit = 10) {
        try {
            const tickers = await this.metricsRepository.getTopTickers(limit);
            return {
                status: 200,
                top_tickers: tickers.map(t => ({
                    exchange_name: t.exchangeName,
                    ticker_symbol: t.tickerSymbol,
                    request_count: t.requestCount,
                    last_accessed: t.lastAccessed.toISOString(),
                    created_at: t.createdAt.toISOString()
                }))
            };
        } catch (error) {
            console.error('Erro detalhado no MetricsService.getTopTickers:', error);
            return {
                status: 500,
                msg: 'Erro interno do servidor.'
            };
        }
    }

    async getPerformanceMetrics() {
        try {
            const summary = await this.metricsRepository.getApiMetricsSummary();
            return {
                status: 200,
                performance: summary
            };
        } catch (error) {
            console.error('Erro detalhado no MetricsService.getPerformanceMetrics:', error);
            return {
                status: 500,
                msg: 'Erro interno do servidor.'
            };
        }
    }

    async getSummary() {
        try {
            const topExchanges = await this.metricsRepository.getTopExchanges(5);
            const topTickers = await this.metricsRepository.getTopTickers(5);
            const performance = await this.metricsRepository.getApiMetricsSummary();

            return {
                status: 200,
                summary: {
                    top_5_exchanges: topExchanges.map(e => ({
                        exchange_name: e.exchangeName,
                        request_count: e.requestCount
                    })),
                    top_5_tickers: topTickers.map(t => ({
                        exchange_name: t.exchangeName,
                        ticker_symbol: t.tickerSymbol,
                        request_count: t.requestCount
                    })),
                    performance: performance
                }
            };
        } catch (error) {
            console.error('Erro detalhado no MetricsService.getSummary:', error);
            return {
                status: 500,
                msg: 'Erro interno do servidor.'
            };
        }
    }
}

module.exports = MetricsService;