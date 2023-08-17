from opaw.util import func_meta


def stock_price(company):
    if company == "APPL":
        return 100
    elif company == "AMZN":
        return 150
    else:
        return 0




funcs_meta = [
    func_meta("stock_price",  # name
              "Get the stock price of a given company",  # desc
              ["company", "string", "The company stock name, e.g. APPL"],  # properties
              ["company"])  # required
]

funcs = {
    "stock_price": stock_price
}

# original function metadata
# funcs_meta = [
#     # stock_price()
#     {
#         "name": "stock_price",
#         "description": "Get the stock price of a given company",
#         "parameters": {
#             "type": "object",
#             "properties": {
#                 "company": {
#                     "type": "string",
#                     "description": "The company stock name, e.g. APPL",
#                 },
#             },
#             "required": ["company"],
#         },
#     }
# ]