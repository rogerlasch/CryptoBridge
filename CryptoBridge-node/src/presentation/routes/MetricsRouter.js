const express = require('express');
const Joi = require('joi');

const router = express.Router();

// Validation schema
const limitSchema = Joi.object({
    limit: Joi.number().integer().min(1).max(50).default(10)
});

class MetricsRouter {
    constructor(metricsService) {
        this.metricsService = metricsService;
        this.setupRoutes();
    }

    setupRoutes() {
        // GET /metrics/exchanges/top - Top exchanges por número de requisições
        router.get('/exchanges/top', async (req, res) => {
            try {
                const { error, value } = limitSchema.validate({ limit: req.query.limit });
                if (error) {
                    return res.status(422).json({
                        status: 422,
                        msg: 'Parâmetro limit inválido.',
                        details: error.details
                    });
                }

                const result = await this.metricsService.getTopExchanges(value.limit);
                res.json(result);
            } catch (error) {
                console.error('Erro detalhado ao buscar top exchanges:', error);
                res.status(500).json({
                    status: 500,
                    msg: 'Erro interno do servidor.'
                });
            }
        });

        // GET /metrics/tickers/top - Top tickers por número de requisições
        router.get('/tickers/top', async (req, res) => {
            try {
                const { error, value } = limitSchema.validate({ limit: req.query.limit });
                if (error) {
                    return res.status(422).json({
                        status: 422,
                        msg: 'Parâmetro limit inválido.',
                        details: error.details
                    });
                }

                const result = await this.metricsService.getTopTickers(value.limit);
                res.json(result);
            } catch (error) {
                console.error('Erro detalhado ao buscar top tickers:', error);
                res.status(500).json({
                    status: 500,
                    msg: 'Erro interno do servidor.'
                });
            }
        });

        // GET /metrics/performance - Métricas de performance da API
        router.get('/performance', async (req, res) => {
            try {
                const result = await this.metricsService.getPerformanceMetrics();
                res.json(result);
            } catch (error) {
                console.error('Erro detalhado ao buscar métricas de performance:', error);
                res.status(500).json({
                    status: 500,
                    msg: 'Erro interno do servidor.'
                });
            }
        });

        // GET /metrics/summary - Resumo geral das métricas
        router.get('/summary', async (req, res) => {
            try {
                const result = await this.metricsService.getSummary();
                res.json(result);
            } catch (error) {
                console.error('Erro detalhado ao buscar resumo de métricas:', error);
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

module.exports = MetricsRouter;