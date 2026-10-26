class BankAccount:
    """Банковский счёт с базовыми операциями."""

    def __init__(self, owner: str, account_number: str):
        if not owner or not isinstance(owner, str):
            raise ValueError("Имя владельца должно быть непустой строкой")
        if not account_number or not isinstance(account_number, str):
            raise ValueError("Номер счёта должен быть непустой строкой")

        self.owner = owner
        self.account_number = account_number
        self._balance = 0  # начальный баланс всегда 0

    @property
    def balance(self) -> float:
        """Текущий баланс счёта."""
        return self._balance

    def is_empty(self) -> bool:
        """Счёт пуст, если баланс равен нулю."""
        return self._balance == 0

    def deposit(self, amount: float) -> None:
        """Пополнение счёта на указанную сумму."""
        if not isinstance(amount, (int, float)) or isinstance(amount, bool):
            raise TypeError("Сумма должна быть числом")
        if amount <= 0:
            raise ValueError("Сумма пополнения должна быть положительной")
        self._balance += amount

    def withdraw(self, amount: float) -> None:
        """Снятие денежных средств со счёта."""
        if not isinstance(amount, (int, float)) or isinstance(amount, bool):
            raise TypeError("Сумма должна быть числом")
        if amount <= 0:
            raise ValueError("Сумма снятия должна быть положительной")
        if amount > self._balance:
            raise ValueError("Недостаточно средств на счёте")
        self._balance -= amount

    def transfer(self, amount: float, target: "BankAccount") -> None:
        """Перевод средств на другой счёт.

        Если операция невозможна — состояние обоих счетов не меняется.
        """
        if not isinstance(target, BankAccount):
            raise TypeError("Получатель должен быть объектом BankAccount")
        if target is self:
            raise ValueError("Нельзя перевести средства на тот же счёт")

        # Проверки до изменения состояния (атомарность)
        if not isinstance(amount, (int, float)) or isinstance(amount, bool):
            raise TypeError("Сумма должна быть числом")
        if amount <= 0:
            raise ValueError("Сумма перевода должна быть положительной")
        if amount > self._balance:
            raise ValueError("Недостаточно средств для перевода")

        # Изменяем оба счёта только после успешных проверок
        self._balance -= amount
        target._balance += amount

    def __repr__(self) -> str:
        return (f"BankAccount(owner={self.owner!r}, "
                f"account_number={self.account_number!r}, "
                f"balance={self._balance})")