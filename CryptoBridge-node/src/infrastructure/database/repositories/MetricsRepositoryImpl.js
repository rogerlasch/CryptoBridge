const database = require('../connection');
const { ExchangeMetric, TickerMetric } = require('../../../domain/entities/Metrics');

class MetricsRepositoryImpl {
    async recordExchangeAccess(exchangeName) {
        try {
            await database.exchangeMetrics.upsert({
                where: {
                    exchangeName: exchangeName
                },
                update: {
                    requestCount: {
                        increment: 1
                    },
                    lastAccessed: new Date()
                },
                create: {
                    exchangeName: exchangeName,
                    requestCount: 1,
                    lastAccessed: new Date()
                }
            });
        } catch (error) {
            console.error(`Erro detalhado no MetricsRepositoryImpl.recordExchangeAccess para ${exchangeName}:`, error);
            throw error;
        }
    }

    async recordTickerAccess(exchangeName, tickerSymbol) {
        try {
            await database.tickerMetrics.upsert({
                where: {
                    exchangeName_tickerSymbol: {
                        exchangeName: exchangeName,
                        tickerSymbol: tickerSymbol
                    }
                },
                update: {
                    requestCount: {
                        increment: 1
                    },
                    lastAccessed: new Date()
                },
                create: {
                    exchangeName: exchangeName,
                    tickerSymbol: tickerSymbol,
                    requestCount: 1,
                    lastAccessed: new Date()
                }
            });
        } catch (error) {
            console.error(`Erro detalhado no MetricsRepositoryImpl.recordTickerAccess para ${tickerSymbol} em ${exchangeName}:`, error);
            throw error;
        }
    }

    async recordApiCall(endpoint, method, statusCode, responseTimeMs) {
        try {
            await database.apiMetrics.create({
                data: {
                    endpoint: endpoint,
                    method: method,
                    statusCode: statusCode,
                    responseTimeMs: responseTimeMs
                }
            });
        } catch (error) {
            console.error(`Erro detalhado no MetricsRepositoryImpl.recordApiCall para ${endpoint}:`, error);
            throw error;
        }
    }

    async getTopExchanges(limit = 10) {
        try {
            const rows = await database.exchangeMetrics.findMany({
                orderBy: {
                    requestCount: 'desc'
                },
                take: limit
            });

            return rows.map(row => new ExchangeMetric(
                row.exchangeName,
                row.requestCount,
                row.lastAccessed,
                row.createdAt
            ));
        } catch (error) {
            console.error('Erro detalhado no MetricsRepositoryImpl.getTopExchanges:', error);
            throw error;
        }
    }

    async getTopTickers(limit = 10) {
        try {
            const rows = await database.tickerMetrics.findMany({
                orderBy: {
                    requestCount: 'desc'
                },
                take: limit
            });

            return rows.map(row => new TickerMetric(
                row.exchangeName,
                row.tickerSymbol,
                row.requestCount,
                row.lastAccessed,
                row.createdAt
            ));
        } catch (error) {
            console.error('Erro detalhado no MetricsRepositoryImpl.getTopTickers:', error);
            throw error;
        }
    }

    async getApiMetricsSummary() {
        try {
            const totalApiCalls = await database.apiMetrics.count();
            const averageResponseTime = await database.apiMetrics.aggregate({
                _avg: {
                    responseTimeMs: true
                }
            });

            return {
                total_api_calls: totalApiCalls || 0,
                average_response_time_ms: Math.round((averageResponseTime._avg.responseTimeMs || 0) * 100) / 100
            };
        } catch (error) {
            console.error('Erro detalhado no MetricsRepositoryImpl.getApiMetricsSummary:', error);
            throw error;
        }
    }
}

module.exports = MetricsRepositoryImpl;