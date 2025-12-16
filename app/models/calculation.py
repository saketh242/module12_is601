
from datetime import datetime
import uuid
import math
from typing import List
from sqlalchemy import Column, String, DateTime, ForeignKey, JSON, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, declared_attr
from sqlalchemy.ext.declarative import declared_attr
from app.database import Base

class AbstractCalculation:
    
    @declared_attr
    def __tablename__(cls):
        return 'calculations'

    @declared_attr
    def id(cls):
        return Column(
            UUID(as_uuid=True), 
            primary_key=True, 
            default=uuid.uuid4,
            nullable=False
        )

    @declared_attr
    def user_id(cls):
        return Column(
            UUID(as_uuid=True), 
            ForeignKey('users.id', ondelete='CASCADE'),
            nullable=False,
            index=True
        )

    @declared_attr
    def type(cls):
        return Column(
            String(50), 
            nullable=False,
            index=True
        )

    @declared_attr
    def inputs(cls):
        return Column(
            JSON, 
            nullable=False
        )

    @declared_attr
    def result(cls):
        return Column(
            Float,
            nullable=True
        )

    @declared_attr
    def created_at(cls):
        return Column(
            DateTime, 
            default=datetime.utcnow,
            nullable=False
        )

    @declared_attr
    def updated_at(cls):
        return Column(
            DateTime, 
            default=datetime.utcnow,
            onupdate=datetime.utcnow,
            nullable=False
        )

    @declared_attr
    def user(cls):
        return relationship("User", back_populates="calculations")

    @classmethod
    def create(cls, calculation_type: str, user_id: uuid.UUID, inputs: List[float]) -> "Calculation":
        calculation_classes = {
            'addition': Addition,
            'subtraction': Subtraction,
            'multiplication': Multiplication,
            'division': Division,
            'modulus': Modulus,
            'sin': Sin,
            'cos': Cos,
            'tan': Tan,
            'exponential': Exponential,
        }
        calculation_class = calculation_classes.get(calculation_type.lower())
        if not calculation_class:
            raise ValueError(f"Unsupported calculation type: {calculation_type}")
        return calculation_class(user_id=user_id, inputs=inputs)

    def get_result(self) -> float:
        raise NotImplementedError

    def __repr__(self):
        return f"<Calculation(type={self.type}, inputs={self.inputs})>"

class Calculation(Base, AbstractCalculation):
    __mapper_args__ = {
        "polymorphic_on": "type",
        "polymorphic_identity": "calculation",
        #"with_polymorphic": "*"
    }

class Addition(Calculation):
    __mapper_args__ = {"polymorphic_identity": "addition"}

    def get_result(self) -> float:
        if not isinstance(self.inputs, list):
            raise ValueError("Inputs must be a list of numbers.")
        if len(self.inputs) < 2:
            raise ValueError("Inputs must be a list with at least two numbers.")
        return sum(self.inputs)

class Subtraction(Calculation):
    __mapper_args__ = {"polymorphic_identity": "subtraction"}

    def get_result(self) -> float:
        if not isinstance(self.inputs, list):
            raise ValueError("Inputs must be a list of numbers.")
        if len(self.inputs) < 2:
            raise ValueError("Inputs must be a list with at least two numbers.")
        result = self.inputs[0]
        for value in self.inputs[1:]:
            result -= value
        return result

class Multiplication(Calculation):
    __mapper_args__ = {"polymorphic_identity": "multiplication"}

    def get_result(self) -> float:
        if not isinstance(self.inputs, list):
            raise ValueError("Inputs must be a list of numbers.")
        if len(self.inputs) < 2:
            raise ValueError("Inputs must be a list with at least two numbers.")
        result = 1
        for value in self.inputs:
            result *= value
        return result

class Division(Calculation):
    __mapper_args__ = {"polymorphic_identity": "division"}

    def get_result(self) -> float:
        if not isinstance(self.inputs, list):
            raise ValueError("Inputs must be a list of numbers.")
        if len(self.inputs) < 2:
            raise ValueError("Inputs must be a list with at least two numbers.")
        result = self.inputs[0]
        for value in self.inputs[1:]:
            if value == 0:
                raise ValueError("Cannot divide by zero.")
            result /= value
        return result

class Modulus(Calculation):
    __mapper_args__ = {"polymorphic_identity": "modulus"}

    def get_result(self) -> float:
        if not isinstance(self.inputs, list):
            raise ValueError("Inputs must be a list of numbers.")
        if len(self.inputs) < 2:
            raise ValueError("Inputs must be a list with at least two numbers.")
        result = self.inputs[0]
        for value in self.inputs[1:]:
            if value == 0:
                raise ValueError("Cannot perform modulus with zero.")
            result = result % value
        return result

class Sin(Calculation):
    __mapper_args__ = {"polymorphic_identity": "sin"}

    def get_result(self) -> float:
        if not isinstance(self.inputs, list):
            raise ValueError("Inputs must be a list of numbers.")
        if len(self.inputs) < 1:
            raise ValueError("At least one number is required for sine calculation.")
        # Sum all inputs and take sine of the result
        total = sum(self.inputs)
        return math.sin(math.radians(total))

class Cos(Calculation):
    __mapper_args__ = {"polymorphic_identity": "cos"}

    def get_result(self) -> float:
        if not isinstance(self.inputs, list):
            raise ValueError("Inputs must be a list of numbers.")
        if len(self.inputs) < 1:
            raise ValueError("At least one number is required for cosine calculation.")
        # Sum all inputs and take cosine of the result
        total = sum(self.inputs)
        return math.cos(math.radians(total))

class Tan(Calculation):
    __mapper_args__ = {"polymorphic_identity": "tan"}

    def get_result(self) -> float:
        if not isinstance(self.inputs, list):
            raise ValueError("Inputs must be a list of numbers.")
        if len(self.inputs) < 1:
            raise ValueError("At least one number is required for tangent calculation.")
        # Sum all inputs and take tangent of the result
        total = sum(self.inputs)
        angle_radians = math.radians(total)
        # Check if cos(angle) is close to 0
        if abs(math.cos(angle_radians)) < 1e-10:
            raise ValueError("Tangent is undefined at this angle.")
        return math.tan(angle_radians)

class Exponential(Calculation):
    __mapper_args__ = {"polymorphic_identity": "exponential"}

    def get_result(self) -> float:
        if not isinstance(self.inputs, list):
            raise ValueError("Inputs must be a list of numbers.")
        if len(self.inputs) < 1:
            raise ValueError("At least one number is required for exponential calculation.")
        # For multiple inputs, calculate e^(sum of inputs)
        total = sum(self.inputs)
        return math.exp(total)

class Power(Calculation):
    __mapper_args__ = {"polymorphic_identity": "power"}

    def get_result(self) -> float:
        if not isinstance(self.inputs, list):
            raise ValueError("Inputs must be a list of numbers.")
        if len(self.inputs) < 2:
            raise ValueError("At least two numbers are required for power calculation.")
        # Calculate first number to the power of second number
        base = self.inputs[0]
        exponent = self.inputs[1]
        return base ** exponent
