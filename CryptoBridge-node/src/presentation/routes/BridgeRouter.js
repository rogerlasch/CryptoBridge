const express = require('express');
const Joi = require('joi');

const router = express.Router();

// Validation schemas
const symbolsSchema = Joi.object({
    exchange: Joi.string().min(1).required()
});

const tickersSchema = Joi.object({
    exchange: Joi.string().min(1).required(),
    tickers: Joi.array().items(Joi.string().min(1)).min(1).required()
});

class BridgeRouter {
    constructor(bridgeService) {
        this.bridgeService = bridgeService;
        this.setupRoutes();
    }

    setupRoutes() {
        // GET / - Lista exchanges disponíveis
        router.get('/', async (req, res) => {
            try {
                const result = await this.bridgeService.getExchanges();
                res.json(result);
            } catch (error) {
                console.error('Erro detalhado ao buscar exchanges:', error);
                res.status(500).json({
                    status: 500,
                    msg: 'Erro interno do servidor.'
                });
            }
        });

        // POST /symbols - Lista símbolos de uma exchange
        router.post('/symbols', async (req, res) => {
            try {
                // Validate request body
                const { error, value } = symbolsSchema.validate(req.body);
                if (error) {
                    return res.status(422).json({
                        status: 422,
                        msg: 'Dados de entrada inválidos.',
                        details: error.details
                    });
                }

                const result = await this.bridgeService.getSymbols(value.exchange);
                res.json(result);
            } catch (error) {
                console.error('Erro detalhado ao buscar símbolos:', error);
                res.status(500).json({
                    status: 500,
                    msg: 'Erro interno do servidor.'
                });
            }
        });

        // POST /tickers - Busca preços de tickers
        router.post('/tickers', async (req, res) => {
            try {
                // Validate request body
                const { error, value } = tickersSchema.validate(req.body);
                if (error) {
                    return res.status(422).json({
                        status: 422,
                        msg: 'Dados de entrada inválidos.',
                        details: error.details
                    });
                }

                const result = await this.bridgeService.getTickers(value.exchange, value.tickers);
                res.json(result);
            } catch (error) {
                console.error('Erro detalhado ao buscar tickers:', error);
                res.status(500).json({
                    status: 500,
                    msg: 'Erro interno do servidor.'
                });
            }
        });
    }

    getRouter() {
        return router;
    }
}

module.exports = BridgeRouter;