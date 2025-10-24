class Exchange {
    constructor(name, symbols = []) {
        if (!name || typeof name !== 'string' || name.trim() === '') {
            throw new Error('Exchange name must be a non-empty string');
        }

        this.name = name;
        this.symbols = Array.isArray(symbols) ? symbols : [];
    }

    hasSymbol(symbol) {
        return this.symbols.includes(symbol);
    }
}

module.exports = Exchange;