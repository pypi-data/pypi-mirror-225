info = [
    # stock.stock_price()
    {
        "name": "stock_price",
        "description": "Get the stock price of a given company",
        "parameters": {
            "type": "object",
            "properties": {
                "company": {
                    "type": "string",
                    "description": "The company stock name, e.g. APPL",
                },
            },
            "required": ["company"],
        },
    }
]

functions = {
    "stock_price": stock.stock_price
}


