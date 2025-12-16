import pytest
from app.models.calculation import (
    Addition, Subtraction, Multiplication, Division,
    Modulus, Sin, Cos, Tan, Exponential, Power
)
import uuid
import math


@pytest.fixture
def test_user_id():
    return uuid.uuid4()


class TestAddition:
    def test_addition_two_numbers(self, test_user_id):
        calc = Addition(user_id=test_user_id, inputs=[10, 5])
        assert calc.get_result() == 15

    def test_addition_multiple_numbers(self, test_user_id):
        calc = Addition(user_id=test_user_id, inputs=[1, 2, 3, 4, 5])
        assert calc.get_result() == 15


class TestSubtraction:
    def test_subtraction_two_numbers(self, test_user_id):
        calc = Subtraction(user_id=test_user_id, inputs=[10, 3])
        assert calc.get_result() == 7

    def test_subtraction_multiple_numbers(self, test_user_id):
        calc = Subtraction(user_id=test_user_id, inputs=[20, 5, 3])
        assert calc.get_result() == 12


class TestMultiplication:
    def test_multiplication_two_numbers(self, test_user_id):
        calc = Multiplication(user_id=test_user_id, inputs=[4, 5])
        assert calc.get_result() == 20

    def test_multiplication_with_zero(self, test_user_id):
        calc = Multiplication(user_id=test_user_id, inputs=[5, 0, 10])
        assert calc.get_result() == 0


class TestDivision:
    def test_division_two_numbers(self, test_user_id):
        calc = Division(user_id=test_user_id, inputs=[20, 4])
        assert calc.get_result() == 5

    def test_division_by_zero_raises(self, test_user_id):
        calc = Division(user_id=test_user_id, inputs=[10, 0])
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            calc.get_result()


class TestModulus:
    def test_modulus_basic(self, test_user_id):
        calc = Modulus(user_id=test_user_id, inputs=[17, 5])
        assert calc.get_result() == 2

    def test_modulus_by_zero_raises(self, test_user_id):
        calc = Modulus(user_id=test_user_id, inputs=[10, 0])
        with pytest.raises(ValueError, match="Cannot perform modulus with zero"):
            calc.get_result()


class TestPower:
    def test_power_basic(self, test_user_id):
        calc = Power(user_id=test_user_id, inputs=[2, 3])
        assert calc.get_result() == 8

    def test_power_square(self, test_user_id):
        calc = Power(user_id=test_user_id, inputs=[5, 2])
        assert calc.get_result() == 25

    def test_power_zero_exponent(self, test_user_id):
        calc = Power(user_id=test_user_id, inputs=[5, 0])
        assert calc.get_result() == 1


class TestTrigonometric:
    def test_sine_zero(self, test_user_id):
        calc = Sin(user_id=test_user_id, inputs=[0])
        assert calc.get_result() == 0

    def test_cosine_zero(self, test_user_id):
        calc = Cos(user_id=test_user_id, inputs=[0])
        assert calc.get_result() == 1

    def test_tangent_zero(self, test_user_id):
        calc = Tan(user_id=test_user_id, inputs=[0])
        assert calc.get_result() == 0


class TestExponential:
    def test_exponential_zero(self, test_user_id):
        calc = Exponential(user_id=test_user_id, inputs=[0])
        assert calc.get_result() == 1

    def test_exponential_one(self, test_user_id):
        calc = Exponential(user_id=test_user_id, inputs=[1])
        assert abs(calc.get_result() - math.e) < 0.0001
