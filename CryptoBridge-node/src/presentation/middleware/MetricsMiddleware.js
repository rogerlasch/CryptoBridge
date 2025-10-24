class MetricsMiddleware {
    constructor(metricsService) {
        this.metricsService = metricsService;
    }

    track() {
        const metricsService = this.metricsService;

        return async (req, res, next) => {
            const startTime = Date.now();

            // Override res.json to capture response
            const originalJson = res.json;
            res.json = function(body) {
                const processTime = Date.now() - startTime;

                // Record API call metrics asynchronously
                setImmediate(async () => {
                    try {
                        await metricsService.recordApiCall(
                            req.path,
                            req.method,
                            res.statusCode,
                            processTime
                        );
                    } catch (error) {
                        console.error('Erro ao registrar métricas:', error);
                    }
                });

                return originalJson.call(this, body);
            };

            next();
        };
    }
}

module.exports = MetricsMiddleware;