class GetExchangesUseCase {
    constructor(exchangeRepository) {
        this.exchangeRepository = exchangeRepository;
    }

    async execute() {
        try {
            const exchanges = this.exchangeRepository.getAvailableExchanges();
            return {
                status: 200,
                exchanges: exchanges
            };
        } catch (error) {
            console.error('Erro detalhado no GetExchangesUseCase:', error);
            return {
                status: 500,
                msg: 'Erro interno do servidor.'
            };
        }
    }
}

module.exports = GetExchangesUseCase;