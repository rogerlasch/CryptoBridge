class ErrorHandler {
    static handle() {
        return (err, req, res, next) => {
            console.error('Erro detalhado no ErrorHandler:', err);

            // Log error details for debugging
            console.error('Stack trace:', err.stack);
            console.error('Request path:', req.path);
            console.error('Request method:', req.method);
            console.error('Request body:', req.body);

            res.status(500).json({
                status: 500,
                msg: 'Erro interno do servidor.'
            });
        };
    }

    static notFound() {
        return (req, res) => {
            res.status(404).json({
                status: 404,
                msg: 'Endpoint não encontrado.'
            });
        };
    }
}

module.exports = ErrorHandler;