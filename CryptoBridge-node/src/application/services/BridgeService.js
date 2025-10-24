const GetExchangesUseCase = require('../../domain/useCases/GetExchangesUseCase');
const GetSymbolsUseCase = require('../../domain/useCases/GetSymbolsUseCase');
const GetTickersUseCase = require('../../domain/useCases/GetTickersUseCase');

class BridgeService {
    constructor(exchangeRepository, metricsRepository) {
        this.getExchangesUseCase = new GetExchangesUseCase(exchangeRepository);
        this.getSymbolsUseCase = new GetSymbolsUseCase(exchangeRepository, metricsRepository);
        this.getTickersUseCase = new GetTickersUseCase(exchangeRepository, metricsRepository);
    }

    async getExchanges() {
        try {
            return await this.getExchangesUseCase.execute();
        } catch (error) {
            console.error('Erro detalhado no BridgeService.getExchanges:', error);
            return {
                status: 500,
                msg: 'Erro interno do servidor.'
            };
        }
    }

    async getSymbols(exchange) {
        try {
            return await this.getSymbolsUseCase.execute(exchange);
        } catch (error) {
            console.error('Erro detalhado no BridgeService.getSymbols:', error);
            return {
                status: 500,
                msg: 'Erro interno do servidor.'
            };
        }
    }

    async getTickers(exchange, tickers) {
        try {
            return await this.getTickersUseCase.execute(exchange, tickers);
        } catch (error) {
            console.error('Erro detalhado no BridgeService.getTickers:', error);
            return {
                status: 500,
                msg: 'Erro interno do servidor.'
            };
        }
    }
}

module.exports = BridgeService;