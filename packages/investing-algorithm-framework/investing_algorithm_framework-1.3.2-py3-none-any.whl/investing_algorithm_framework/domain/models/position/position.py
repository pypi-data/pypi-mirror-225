from investing_algorithm_framework.domain.models.base_model import BaseModel


class Position(BaseModel):

    def __init__(
        self,
        symbol=None,
        amount=0,
        portfolio_id=None
    ):
        self.symbol = symbol
        self.amount = amount
        self.portfolio_id = portfolio_id

    def get_symbol(self):
        return self.symbol

    def set_symbol(self, symbol):
        self.symbol = symbol.upper()

    def get_amount(self):
        return self.amount

    def set_amount(self, amount):
        self.amount = amount

    def get_portfolio_id(self):
        return self.portfolio_id

    def set_portfolio_id(self, portfolio_id):
        self.portfolio_id = portfolio_id

    def __repr__(self):
        return self.repr(
            symbol=self.symbol,
            amount=self.amount,
            portfolio_id=self.portfolio_id,
        )
