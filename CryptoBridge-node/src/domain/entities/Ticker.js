class Ticker {
    constructor(symbol, buy, sell, vol, low, high, last) {
        if (!symbol || typeof symbol !== 'string' || symbol.trim() === '') {
            throw new Error('Symbol must be a non-empty string');
        }

        this.symbol = symbol;
        this.buy = Math.max(0, parseFloat(buy) || 0);
        this.sell = Math.max(0, parseFloat(sell) || 0);
        this.vol = Math.max(0, parseFloat(vol) || 0);
        this.low = Math.max(0, parseFloat(low) || 0);
        this.high = Math.max(0, parseFloat(high) || 0);
        this.last = Math.max(0, parseFloat(last) || 0);
    }
}

module.exports = Ticker;