import unittest

from bank_account import BankAccount


class TestBankAccountCreation(unittest.TestCase):
    def test_create_account_stores_data(self):
        acc = BankAccount("Иван Иванов", "40817810099910004312")
        self.assertEqual(acc.owner, "Иван Иванов")
        self.assertEqual(acc.account_number, "40817810099910004312")

    def test_initial_balance_is_zero(self):
        acc = BankAccount("Пётр", "12345")
        self.assertEqual(acc.balance, 0)
        self.assertTrue(acc.is_empty())

    def test_create_with_empty_owner_raises(self):
        with self.assertRaises(ValueError):
            BankAccount("", "12345")

    def test_create_with_empty_account_number_raises(self):
        with self.assertRaises(ValueError):
            BankAccount("Иван", "")


class TestDeposit(unittest.TestCase):
    def setUp(self):
        self.acc = BankAccount("Иван", "111")

    def test_deposit_increases_balance(self):
        self.acc.deposit(1000)
        self.assertEqual(self.acc.balance, 1000)

    def test_deposit_multiple_times(self):
        self.acc.deposit(100)
        self.acc.deposit(250.5)
        self.assertAlmostEqual(self.acc.balance, 350.5)

    def test_deposit_zero_raises(self):
        with self.assertRaises(ValueError):
            self.acc.deposit(0)

    def test_deposit_negative_raises(self):
        with self.assertRaises(ValueError):
            self.acc.deposit(-50)

    def test_deposit_non_number_raises(self):
        with self.assertRaises(TypeError):
            self.acc.deposit("100")

    def test_balance_unchanged_after_failed_deposit(self):
        try:
            self.acc.deposit(-10)
        except ValueError:
            pass
        self.assertEqual(self.acc.balance, 0)


class TestWithdraw(unittest.TestCase):
    def setUp(self):
        self.acc = BankAccount("Иван", "111")
        self.acc.deposit(500)

    def test_withdraw_decreases_balance(self):
        self.acc.withdraw(200)
        self.assertEqual(self.acc.balance, 300)

    def test_withdraw_all(self):
        self.acc.withdraw(500)
        self.assertEqual(self.acc.balance, 0)
        self.assertTrue(self.acc.is_empty())

    def test_withdraw_more_than_balance_raises(self):
        with self.assertRaises(ValueError):
            self.acc.withdraw(500.01)
        self.assertEqual(self.acc.balance, 500)

    def test_withdraw_negative_raises(self):
        with self.assertRaises(ValueError):
            self.acc.withdraw(-100)
        self.assertEqual(self.acc.balance, 500)

    def test_withdraw_zero_raises(self):
        with self.assertRaises(ValueError):
            self.acc.withdraw(0)


class TestTransfer(unittest.TestCase):
    def setUp(self):
        self.src = BankAccount("Отправитель", "A")
        self.dst = BankAccount("Получатель", "B")
        self.src.deposit(1000)

    def test_transfer_moves_money(self):
        self.src.transfer(300, self.dst)
        self.assertEqual(self.src.balance, 700)
        self.assertEqual(self.dst.balance, 300)

    def test_transfer_amounts_equal(self):
        before_src = self.src.balance
        before_dst = self.dst.balance
        amount = 250
        self.src.transfer(amount, self.dst)
        self.assertEqual(before_src - self.src.balance, amount)
        self.assertEqual(self.dst.balance - before_dst, amount)

    def test_transfer_insufficient_funds_state_unchanged(self):
        with self.assertRaises(ValueError):
            self.src.transfer(1001, self.dst)
        self.assertEqual(self.src.balance, 1000)
        self.assertEqual(self.dst.balance, 0)

    def test_transfer_negative_amount_state_unchanged(self):
        with self.assertRaises(ValueError):
            self.src.transfer(-10, self.dst)
        self.assertEqual(self.src.balance, 1000)
        self.assertEqual(self.dst.balance, 0)

    def test_transfer_zero_state_unchanged(self):
        with self.assertRaises(ValueError):
            self.src.transfer(0, self.dst)
        self.assertEqual(self.src.balance, 1000)
        self.assertEqual(self.dst.balance, 0)

    def test_transfer_to_self_raises(self):
        with self.assertRaises(ValueError):
            self.src.transfer(100, self.src)
        self.assertEqual(self.src.balance, 1000)

    def test_transfer_wrong_target_type_raises(self):
        with self.assertRaises(TypeError):
            self.src.transfer(100, "not an account")


class TestBalanceAndEmpty(unittest.TestCase):
    def test_is_empty_true_for_new_account(self):
        self.assertTrue(BankAccount("X", "1").is_empty())

    def test_is_empty_false_after_deposit(self):
        acc = BankAccount("X", "1")
        acc.deposit(1)
        self.assertFalse(acc.is_empty())

    def test_is_empty_true_after_full_withdraw(self):
        acc = BankAccount("X", "1")
        acc.deposit(100)
        acc.withdraw(100)
        self.assertTrue(acc.is_empty())

    def test_balance_reflects_operations(self):
        acc = BankAccount("X", "1")
        acc.deposit(500)
        acc.withdraw(200)
        acc.deposit(50)
        self.assertEqual(acc.balance, 350)


if __name__ == "__main__":
    unittest.main(verbosity=2)