const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const morgan = require('morgan');

// Infrastructure
const database = require('./src/infrastructure/database/connection');
const ExchangeRepositoryImpl = require('./src/infrastructure/database/repositories/ExchangeRepositoryImpl');
const MetricsRepositoryImpl = require('./src/infrastructure/database/repositories/MetricsRepositoryImpl');

// Application Services
const BridgeService = require('./src/application/services/BridgeService');
const MetricsService = require('./src/application/services/MetricsService');

// Presentation Layer
const BridgeRouter = require('./src/presentation/routes/BridgeRouter');
const MetricsRouter = require('./src/presentation/routes/MetricsRouter');
const MetricsMiddleware = require('./src/presentation/middleware/MetricsMiddleware');
const ErrorHandler = require('./src/presentation/middleware/ErrorHandler');

const app = express();

async function initializeApp() {
    try {
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

        // Security and logging middleware
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

        // Start server
        const PORT = process.env.PORT || 3001;
        app.listen(PORT, () => {
            console.log(`CryptoBridge Node.js API iniciada na porta ${PORT}`);
            console.log('Endpoints disponíveis:');
            console.log('  GET  / - Lista exchanges disponíveis');
            console.log('  POST /symbols - Lista símbolos (body: {exchange})');
            console.log('  POST /tickers - Busca preços (body: {exchange, tickers[]})');
            console.log('  GET  /metrics/* - Endpoints de métricas');
        });

    } catch (error) {
        console.error('Erro ao iniciar o servidor:', error);
        process.exit(1);
    }
}

// Graceful shutdown
process.on('SIGINT', async () => {
    console.log('Encerrando servidor...');
    await database.close();
    process.exit(0);
});

process.on('SIGTERM', async () => {
    console.log('Encerrando servidor...');
    await database.close();
    process.exit(0);
});

// Initialize application
initializeApp();