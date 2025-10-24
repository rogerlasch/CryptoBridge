const { PrismaClient } = require('../../generated/prisma');

class Database {
    constructor() {
        this.prisma = new PrismaClient();
    }

    async connect() {
        try {
            await this.prisma.$connect();
            console.log('Banco de dados conectado via Prisma.');
        } catch (error) {
            console.error('Erro ao conectar com banco de dados:', error);
            throw error;
        }
    }

    async initializeTables() {
        // Com Prisma, não precisamos criar tabelas manualmente
        // As tabelas são criadas automaticamente através das migrations
        console.log('Tabelas gerenciadas pelo Prisma - nenhuma inicialização manual necessária.');
    }

    // Métodos de acesso ao Prisma Client para compatibilidade
    get exchangeMetrics() {
        return this.prisma.exchangeMetrics;
    }

    get tickerMetrics() {
        return this.prisma.tickerMetrics;
    }

    get apiMetrics() {
        return this.prisma.apiMetrics;
    }

    // Método genérico para queries SQL rawas (se necessário)
    async raw(sql, params = []) {
        return await this.prisma.$queryRawUnsafe(sql, ...params);
    }

    async close() {
        try {
            await this.prisma.$disconnect();
            console.log('Conexão com banco de dados fechada.');
        } catch (error) {
            console.error('Erro ao fechar conexão:', error);
            throw error;
        }
    }
}

// Singleton instance
const database = new Database();

module.exports = database;