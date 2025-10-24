const request = require('supertest');
const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const morgan = require('morgan');

// Real API components
const database = require('../../src/infrastructure/database/connection');
const ExchangeRepositoryImpl = require('../../src/infrastructure/database/repositories/ExchangeRepositoryImpl');
const MetricsRepositoryImpl = require('../../src/infrastructure/database/repositories/MetricsRepositoryImpl');
const BridgeService = require('../../src/application/services/BridgeService');
const MetricsService = require('../../src/application/services/MetricsService');
const BridgeRouter = require('../../src/presentation/routes/BridgeRouter');
const MetricsRouter = require('../../src/presentation/routes/MetricsRouter');
const MetricsMiddleware = require('../../src/presentation/middleware/MetricsMiddleware');
const ErrorHandler = require('../../src/presentation/middleware/ErrorHandler');

describe('API Integration Tests', () => {
    let app;
    let server;
    let baseURL;
    const TEST_PORT = 3002; // Use different port for testing

    beforeAll(async () => {
        // Set test database path
        database.dbPath = ':memory:';

        // Initialize Express app - same as index.js
        app = express();

        // Connect to database and initialize tables
        await database.connect();
        await database.initializeTables();

        // Initialize repositories
        const exchangeRepository = new ExchangeRepositoryImpl();
        const metricsRepository = new MetricsRepositoryImpl();

        // Initialize services
        const bridgeService = new BridgeService(exchangeRepository, metricsRepository);
        const metricsService = new MetricsService(metricsRepository);

        // Initialize middleware
        const metricsMiddleware = new MetricsMiddleware(metricsService);

        // Security and logging middleware (same as production)
        app.use(helmet());
        app.use(morgan('combined'));
        app.use(cors());
        app.use(express.json());

        // Metrics tracking middleware
        app.use(metricsMiddleware.track());

        // Initialize routers
        const bridgeRouter = new BridgeRouter(bridgeService);
        const metricsRouter = new MetricsRouter(metricsService);

        // Routes
        app.use('/', bridgeRouter.getRouter());
        app.use('/metrics', metricsRouter.getRouter());

        // Error handling
        app.use(ErrorHandler.notFound());
        app.use(ErrorHandler.handle());

        // Start the real server for testing
        return new Promise((resolve) => {
            server = app.listen(TEST_PORT, () => {
                baseURL = `http://localhost:${TEST_PORT}`;
                console.log(`Test API server started on port ${TEST_PORT}`);
                resolve();
            });
        });
    });

    afterAll(async () => {
        // Close server and database
        if (server) {
            await new Promise((resolve) => {
                server.close(() => {
                    console.log('Test server closed');
                    resolve();
                });
            });
        }
        await database.close();
    });

    describe('Bridge Endpoints', () => {
        it('getShouldReturnAvailableExchanges', async () => {
            const response = await request(baseURL).get('/');

            expect(response.status).toBe(200);
            expect(response.body.status).toBe(200);
            expect(response.body.exchanges).toEqual(expect.arrayContaining(['mercadobitcoin', 'coinbase']));
        });

        it('postSymbolsShouldRequireExchangeParameter', async () => {
            const response = await request(baseURL)
                .post('/symbols')
                .send({});

            expect(response.status).toBe(422);
        });

        it('postSymbolsShouldHandleValidExchange', async () => {
            const response = await request(baseURL)
                .post('/symbols')
                .send({ exchange: 'coinbase' });

            expect(response.status).toBe(200);
            expect(response.body.status).toBe(200);
            expect(response.body).toHaveProperty('symbols');
        });

        it('postSymbolsShouldHandleInvalidExchange', async () => {
            const response = await request(baseURL)
                .post('/symbols')
                .send({ exchange: 'invalid' });

            expect(response.status).toBe(200);
            expect(response.body.status).toBe(404);
        });

        it('postTickersShouldRequireParameters', async () => {
            const response = await request(baseURL)
                .post('/tickers')
                .send({});

            expect(response.status).toBe(422);
        });

        it('postTickersShouldHandleValidRequest', async () => {
            const response = await request(baseURL)
                .post('/tickers')
                .send({
                    exchange: 'coinbase',
                    tickers: ['BTC-USD']
                });

            expect(response.status).toBe(200);
            expect(response.body.status).toBe(200);
            expect(response.body).toHaveProperty('tickers');
        });

        it('postTickersShouldHandleInvalidExchange', async () => {
            const response = await request(baseURL)
                .post('/tickers')
                .send({
                    exchange: 'invalid',
                    tickers: ['BTC-USD']
                });

            expect(response.status).toBe(200);
            expect(response.body.status).toBe(404);
        });

        it('postTickersShouldHandleEmptyTickersArray', async () => {
            const response = await request(baseURL)
                .post('/tickers')
                .send({
                    exchange: 'coinbase',
                    tickers: []
                });

            expect(response.status).toBe(422);
        });
    });

    describe('Metrics Endpoints', () => {
        it('getMetricsExchangesTopShouldReturnTopExchanges', async () => {
            const response = await request(baseURL).get('/metrics/exchanges/top');

            expect(response.status).toBe(200);
            expect(response.body.status).toBe(200);
            expect(response.body).toHaveProperty('top_exchanges');
        });

        it('getMetricsExchangesTopShouldHandleLimitParameter', async () => {
            const response = await request(baseURL).get('/metrics/exchanges/top?limit=5');

            expect(response.status).toBe(200);
            expect(response.body.status).toBe(200);
            expect(response.body).toHaveProperty('top_exchanges');
        });

        it('getMetricsTickersTopShouldReturnTopTickers', async () => {
            const response = await request(baseURL).get('/metrics/tickers/top');

            expect(response.status).toBe(200);
            expect(response.body.status).toBe(200);
            expect(response.body).toHaveProperty('top_tickers');
        });

        it('getMetricsTickersTopShouldHandleLimitParameter', async () => {
            const response = await request(baseURL).get('/metrics/tickers/top?limit=3');

            expect(response.status).toBe(200);
            expect(response.body.status).toBe(200);
            expect(response.body).toHaveProperty('top_tickers');
        });

        it('getMetricsPerformanceShouldReturnPerformanceMetrics', async () => {
            const response = await request(baseURL).get('/metrics/performance');

            expect(response.status).toBe(200);
            expect(response.body.status).toBe(200);
            expect(response.body).toHaveProperty('performance');
        });

        it('getMetricsSummaryShouldReturnMetricsSummary', async () => {
            const response = await request(baseURL).get('/metrics/summary');

            expect(response.status).toBe(200);
            expect(response.body.status).toBe(200);
            expect(response.body).toHaveProperty('summary');
        });
    });

    describe('Error Handling', () => {
        it('shouldReturn404ForNonExistentEndpoint', async () => {
            const response = await request(baseURL).get('/non-existent');

            expect(response.status).toBe(404);
            expect(response.body.status).toBe(404);
            expect(response.body.msg).toBe('Endpoint não encontrado.');
        });
    });
});