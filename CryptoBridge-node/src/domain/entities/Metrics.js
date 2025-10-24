class ExchangeMetric {
    constructor(exchangeName, requestCount, lastAccessed, createdAt = null) {
        this.exchangeName = exchangeName;
        this.requestCount = requestCount;
        this.lastAccessed = lastAccessed;
        this.createdAt = createdAt || new Date();
    }
}

class TickerMetric {
    constructor(exchangeName, tickerSymbol, requestCount, lastAccessed, createdAt = null) {
        this.exchangeName = exchangeName;
        this.tickerSymbol = tickerSymbol;
        this.requestCount = requestCount;
        this.lastAccessed = lastAccessed;
        this.createdAt = createdAt || new Date();
    }
}

class ApiMetric {
    constructor(endpoint, method, statusCode, responseTimeMs, timestamp = null) {
        this.endpoint = endpoint;
        this.method = method;
        this.statusCode = statusCode;
        this.responseTimeMs = responseTimeMs;
        this.timestamp = timestamp || new Date();
    }
}

module.exports = {
    ExchangeMetric,
    TickerMetric,
    ApiMetric
};