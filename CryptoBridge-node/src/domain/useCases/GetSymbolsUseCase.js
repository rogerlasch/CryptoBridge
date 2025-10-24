class GetSymbolsUseCase {
    constructor(exchangeRepository, metricsRepository) {
        this.exchangeRepository = exchangeRepository;
        this.metricsRepository = metricsRepository;
    }

    async execute(exchange) {
        if (!exchange) {
            return {
                status: 400,
                msg: 'Exchange não especificada.'
            };
        }

        if (typeof exchange !== 'string' || exchange.trim() === '') {
            return {
                status: 400,
                msg: 'Exchange deve ser uma string válida.'
            };
        }

        const availableExchanges = this.exchangeRepository.getAvailableExchanges();
        if (!availableExchanges.includes(exchange)) {
            return {
                status: 404,
                msg: 'A exchange especificada não existe no momento na bridge.'
            };
        }

        try {
            const symbols = await this.exchangeRepository.getSymbols(exchange);
            await this.metricsRepository.recordExchangeAccess(exchange);

            return {
                status: 200,
                symbols: symbols
            };
        } catch (error) {
            console.error('Erro detalhado no GetSymbolsUseCase:', error);
            return {
                status: 500,
                msg: 'Erro interno do servidor.'
            };
        }
    }
}

module.exports = GetSymbolsUseCase;