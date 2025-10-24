class GetTickersUseCase {
    constructor(exchangeRepository, metricsRepository) {
        this.exchangeRepository = exchangeRepository;
        this.metricsRepository = metricsRepository;
    }

    async execute(exchange, tickers) {
        if (!exchange || !tickers) {
            return {
                status: 400,
                msg: 'O parâmetro exchange ou tickers não foi especificado corretamente.'
            };
        }

        if (!Array.isArray(tickers)) {
            return {
                status: 400,
                msg: 'O parâmetro tickers não é um array válido.'
            };
        }

        if (tickers.length === 0) {
            return {
                status: 400,
                msg: 'O array de tickers não pode estar vazio.'
            };
        }

        for (const ticker of tickers) {
            if (typeof ticker !== 'string' || ticker.trim() === '') {
                return {
                    status: 400,
                    msg: 'Todos os tickers devem ser strings válidas.'
                };
            }
        }

        const availableExchanges = this.exchangeRepository.getAvailableExchanges();
        if (!availableExchanges.includes(exchange)) {
            return {
                status: 404,
                msg: 'A exchange especificada ainda não está disponível na bridge.'
            };
        }

        try {
            const result = [];
            await this.metricsRepository.recordExchangeAccess(exchange);

            for (const ticker of tickers) {
                const tickerData = await this.exchangeRepository.getTicker(exchange, ticker);

                if (tickerData) {
                    await this.metricsRepository.recordTickerAccess(exchange, ticker);
                    result.push({
                        symbol: tickerData.symbol,
                        buy: tickerData.buy,
                        sell: tickerData.sell,
                        vol: tickerData.vol,
                        low: tickerData.low,
                        high: tickerData.high,
                        last: tickerData.last
                    });
                }
            }

            return {
                status: 200,
                tickers: result
            };
        } catch (error) {
            console.error('Erro detalhado no GetTickersUseCase:', error);
            return {
                status: 500,
                msg: 'Erro interno do servidor.'
            };
        }
    }
}

module.exports = GetTickersUseCase;