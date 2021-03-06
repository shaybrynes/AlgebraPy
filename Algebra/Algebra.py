__authors__ = ["Shay Brynes"]
__version__ = ["1.0p"]

from decimal import *

getcontext().prec = 101


class Number:
    """
    Basic number construction as a replacement of the built in system.
    """

    def __init__(self, value, imag=0):
        """
        Class constructor for the number class.

        :param value: The real component of the number | A Number instance.
        :param imag: The complex component of the number.
        """

        if (type(value) is not Number) and (type(value) is not complex):

            self.real = Decimal(str(value))
            self.imag = Decimal(str(imag))

            if self.imag == 0:
                self.name = str(self.real)

            elif self.imag == 1:
                self.name = str(self.real) + " + i"

            elif self.imag == -1:
                self.name = str(self.real) + " + -i"

            else:
                self.name = str(self.real) + " + " + str(self.imag) + "i"

        elif type(value) is Number:

            self.name = value.name
            self.real = value.real
            self.imag = value.imag

        else:

            self.real = Decimal(str(value.real))
            self.imag = Decimal(str(value.imag))

            if self.imag == 0:
                self.name = str(self.real)

            elif self.imag == 1:
                self.name = str(self.real) + " + i"

            elif self.imag == -1:
                self.name = str(self.real) + " + -i"

            else:
                self.name = str(self.real) + " + " + str(self.imag) + "i"

    @staticmethod
    def __format_num__(value):
        """
        Formats the numbers to the correct number of decimal places (removes trailing zeroes)

        :param value: The Decimal value of the number.
        :return: The trimed value.
        :rtype: Decimal
        """

        if value.as_tuple().exponent == (-1 * getcontext().prec):

            return Decimal("0")

        else:
            return value.quantize(Decimal("1")) if value == value.to_integral() else value.normalize()

    def __str__(self):
        """
        Class string method.

        :return: The name of the number.
        """

        real_str = str(Number.__format_num__(self.real))
        imag_str = str(Number.__format_num__(self.imag))

        if imag_str == "0":
            self.name = str(real_str)

        elif imag_str == "1":
            self.name = "(" + str(real_str) + " + i)"

        elif imag_str == "-1":
            self.name = "(" + str(real_str) + " + -i)"

        else:
            self.name = "(" + str(real_str) + " + " + str(imag_str) + "i)"

        return self.name

    def __eq__(self, other):
        """
        Evaluates the value of the equality.

        :param other: The object being compared to this.
        :return: The result of the equality.
        :rtype: bool
        """

        if type(other) is Number:

            if self.real == other.real and self.imag == other.imag:

                return True

            else:

                return False

        else:

            return False

    def __complex__(self):
        """
        Class complex method

        :return: A built in complex type.
        """

        return complex(self.real, self.imag)

    def __mul__(self, other):
        """
        Class multiplication method

        :param other: The right hand side of the multiplication.
        :return: The value of multiplication.
        """

        if (type(other) is Decimal) or (type(other) is int) or (type(other) is float):
            new_real = self.real * other
            new_imag = self.imag * other

            return Number(new_real, new_imag)

        if (type(other) is complex) or type(other) is Number:
            new_real = (self.real * Decimal(other.real)) - (self.imag * Decimal(other.imag))
            new_imag = (self.real * Decimal(other.imag)) + (self.imag * Decimal(other.real))

            return Number(new_real, new_imag)

        if type(other) is Variable:
            raw = str(self) + other.name
            data = {"multiple": self,
                    "variables": [other],
                    "power": [Number(1)]}

            construct = {"raw": raw,
                         "data": data}

            return Expression(construct)

        if type(other) is Expression:
            new_multiple = self * other.construct["data"]["multiple"]
            new_variables = other.construct["data"]["variables"]
            new_power = other.construct["data"]["power"]

            data = {"multiple": new_multiple,
                    "variables": new_variables,
                    "power": new_power}

            raw = Expression.raw_construct(data)

            construct = {"raw": raw, "data": data}

            return Expression(construct)

        if issubclass(type(other), Expression):
            return self * Expression(other.construct)

    def __truediv__(self, other):
        """
        Variable division method.

        :param other: The denominator of the fraction.
        :return: An expression representing the division.
        """

        if (type(other) is Decimal) or (type(other) is int) or (type(other) is float):
            new_real = self.real / Decimal(other)
            new_imag = self.imag / Decimal(other)

            return Number(new_real, new_imag)

        if (type(other) is complex) or (type(other) is Number):
            multiplier = Decimal("1") / (other.real ** Decimal("2") + other.imag ** Decimal("2"))

            new_real = ((self.real * other.real) + (self.imag * other.imag)) * multiplier
            new_imag = ((self.imag * other.real) - (self.real * other.imag)) * multiplier

            return Number(new_real, new_imag)

        if type(other) is Variable:
            raw = str(self) + other.name + "^(-1)"
            data = {"multiple": self,
                    "variables": [other],
                    "power": [Number("-1")]}

            construct = {"raw": raw,
                         "data": data}

            return Expression(construct)

        if type(other) is Expression:

            temp_multiple = Number("1") / Number(other.construct["data"]["multiple"])
            temp_variables = other.construct["data"]["variables"]
            temp_power = []

            for i in range(0, len(other.construct["data"]["power"])):
                temp_power.append(other.construct["data"]["power"][i] * Number(-1))

            data = {"multiple": temp_multiple,
                    "variables": temp_variables,
                    "power": temp_power}

            raw = Expression.raw_construct(data)

            construct = {"raw": raw, "data": data}

            return Expression(construct) * self

        if issubclass(type(other), Expression):
            return self / Expression(other.construct)

    def __pow__(self, power, modulo=None):
        """
        Raising a standard number to the power of a value.

        :param power: The exponent.
        :return: The value of the number raised to a power.
        """

        if (type(power) is Decimal) or (type(power) is int) or (type(power) is float):
            return self ** Number(power)

        if (type(power) is complex) or (type(power) is Number):
            return Number(complex(self) ** complex(power))

        if type(power) is Variable:
            data = {"multiple": Number(1),
                    "variables": [self],
                    "power": [power]}
            raw = Expression.raw_construct(data)

            construct = {"raw": raw,
                         "data": data}

            return Expression(construct)

        if type(power) is Expression:
            data = {"multiple": Number(1),
                    "variables": [self],
                    "power": [power]}
            raw = Expression.raw_construct(data)

            construct = {"raw": raw,
                         "data": data}

            return Expression(construct)

    def __add__(self, other):
        """
        Class addition method.

        :param other: The right hand side of the addition.
        :return: The result of the addition.
        """

        if (type(other) is Decimal) or (type(other) is int) or (type(other) is float):
            return self + Number(other)

        if (type(other) is complex) or (type(other) is Number):
            new_real = self.real + Decimal(other.real)
            new_imag = self.imag + Decimal(other.imag)

            return Number(new_real, new_imag)

    def __sub__(self, other):
        """
        Class subtraction method.

        :param other: The right hand side of the subtraction.
        :return: The result of the subtraction.
        """

        # If other is a built in numerical type
        if (type(other) is Decimal) or (type(other) is int) or (type(other) is float) or (type(other) is complex):
            return self - Number(other)

        # If other is a custom numerical class Number or a builtin complex.
        if (type(other) is complex) or (type(other) is Number):
            new_real = self.real - Decimal(other.real)
            new_imag = self.imag - Decimal(other.imag)

            return Number(new_real, new_imag)

    def value(self):

        return self

    def is_real(self):
        """
        Evaluates if the number is real.
        :return: The realty of the number
        :rtype: bool
        """
        realty = False

        if self.imag == 0:
            realty = True

        return realty

    __rmul__ = __mul__
    __radd__ = __add__
    __rsub__ = __sub__


class Variable:
    """
    Basic variable construction for a set of functions.
    """

    __super_dict = {"0": u"\u00B0", "1": u"\u00B9", "2": u"\u00B2", "3": u"\u00B3", "4": u"\u2074",
                    "5": u"\u2075", "6": u"\u2076", "7": u"\u2077", "8": u"\u2078", "9": u"\u2079",

                    "-": u"\u207B", ".": u"\u02D9", "+": u"\u207A", "(": u"\u207d", ")": u"\u207e",

                    "a": u"\u1d43", "b": u"\u1d47", "c": u"\u1d9c", "d": u"\u1d48", "e": u"\u1d49",
                    "f": u"\u1da0", "g": u"\u1d4d", "h": u"\u02b0", "i": u"\u2071", "j": u"\u02B2",
                    "k": u"\u1d4f", "l": u"\u02e1"}

    __builtin_names = ["e", "ln",
                       # Trigonometric
                       "sin", "cos", "tan",
                       "arcsin", "arccos", "arctan",
                       "cosec", "sec", "cot",
                       "arccsc", "arcsec", "arccot",
                       # Hyperbolic
                       "sinh", "cosh", "tanh",
                       "arsinh", "arcosh", "artanh"
                       ]

    def __init__(self, name, human_name=None, numeric_value=None):
        """
        Class constructor for the variable class

        :param str name: The name of the variable.
        """

        if name not in self.__builtin_names:
            self.name = name
            self.human_name = human_name
            self.numeric_value = numeric_value

        else:
            raise ValueError("Variable name matches built in name: " + name)

    def __str__(self):
        """
        Class string method

        :return: The name of the variable.
        """

        return self.name

    def __eq__(self, other):
        """
        Evaluates the value of the equality.

        :param other: The object being compared to this.
        :return: The result of the equality.
        :rtype: bool
        """

        equality = False

        if type(other) == Variable:

            if other.name == self.name:
                equality = True

        return equality

    def __mul__(self, other):
        """
        Variable multiplication method.

        :param other: The right side of the multiplication
        :return: An expression representing the multiplication
        :rtype: Expression
        """

        if (type(other) is Decimal) or (type(other) is int) or (type(other) is float) or (type(other) is complex):
            return self * Number(other)

        if type(other) is Number:
            raw = str(other) + self.name
            data = {"multiple": other,
                    "variables": [self],
                    "power": [Number(1)]}

            construct = {"raw": raw,
                         "data": data}

            return Expression(construct)

        if type(other) is Variable:

            # If the variables are the same (i.e x*x)
            if self.name == other.name:

                raw = self.name + "^(2)"
                data = {"multiple": Number(1),
                        "variables": [self],
                        "power": [Number(1)]}

                construct = {"raw": raw,
                             "data": data}

            # If the variables have different names (i.e x*y)
            else:

                raw = self.name + other.name
                data = {"multiple": Number(1),
                        "variables": [self, other],
                        "power": [Number(1), Number(1)]}

                construct = {"raw": raw,
                             "data": data}

            return Expression(construct)

        if type(other) is Expression:

            # If the variable already exists in 'other'.
            if self in other.construct["data"]["variables"]:

                index = other.construct["data"]["variables"].index(self)
                new_power = other.construct["data"]["power"][index] + Number(1)
                other.construct["data"]["power"][index] = new_power

                construct = {"raw": Expression.raw_construct(other.construct["data"]),
                             "data": other.construct["data"]}

            else:

                other.construct["data"]["variables"].append(self)
                other.construct["data"]["power"].append(Number(1))

                construct = {"raw": Expression.raw_construct(other.construct["data"]),
                             "data": other.construct["data"]}

            return Expression(construct)

        if issubclass(type(other), Expression):
            return self * Expression(other.construct)

    def __truediv__(self, other):
        """
        Variable division method.

        :param other: The denominator of the fraction.
        :return: An expression representing the division.
        :rtype: Expression
        """

        if (type(other) is Decimal) or (type(other) is int) or (type(other) is float) or (type(other) is complex):
            return self / Number(other)

        if type(other) is Number:
            raw = str(other) + self.name
            data = {"multiple": Number(1) / other,
                    "variables": [self],
                    "power": [Number(1)]}

            construct = {"raw": raw,
                         "data": data}

            return Expression(construct)

        if type(other) is Variable:

            # If the variables are the same (i.e x/x)
            if self.name == other.name:
                raw = "1"
                data = {"multiple": Number(1),
                        "variables": [],
                        "power": []}

                construct = {"raw": raw,
                             "data": data}

            # If the variables have different names (i.e x/y)
            else:
                raw = self.name + other.name + "^(-1)"
                data = {"multiple": Number(1),
                        "variables": [self, other],
                        "power": [Number(1), Number(-1)]}

                construct = {"raw": raw,
                             "data": data}

            return Expression(construct)

        if type(other) is Expression:

            temp_multiple = Number(1) / Number(other.construct["data"]["multiple"])
            temp_variables = other.construct["data"]["variables"]
            temp_power = []

            for i in range(0, len(other.construct["data"]["power"])):
                temp_power.append(other.construct["data"]["power"][i] * Number(-1))

            data = {"multiple": temp_multiple,
                    "variables": temp_variables,
                    "power": temp_power}

            raw = Expression.raw_construct(data)

            construct = {"raw": raw, "data": data}

            return Expression(construct) * self

        if issubclass(type(other), Expression):
            return self / Expression(other.construct)

    def __pow__(self, power):
        """
        Variable power method.

        :param power: The power that the variable is being raised by
        :return: An expression representing the exponentiation
        :rtype: Expression
        """

        if (type(power) is Decimal) or (type(power) is int) or (type(power) is float) or (type(power) is complex):
            return self ** Number(power)

        if type(power) is Number:
            data = {"multiple": Number(1),
                    "variables": [self],
                    "power": [power]}
            raw = Expression.raw_construct(data)

            construct = {"raw": raw,
                         "data": data}

            return Expression(construct)

        if type(power) is Variable:
            data = {"multiple": Number(1),
                    "variables": [self],
                    "power": [power]}
            raw = Expression.raw_construct(data)

            construct = {"raw": raw,
                         "data": data}

            return Expression(construct)

        if type(power) is Expression:
            data = {"multiple": Number(1),
                    "variables": [self],
                    "power": [power]}
            raw = Expression.raw_construct(data)

            construct = {"raw": raw,
                         "data": data}

            return Expression(construct)

    def set_value(self, value):
        """
        Set the value of the variable

        :param value: The new value of the instance.
        """

        if (type(value) is Decimal) or (type(value) is int) or (type(value) is float) or type(value) is complex:

            self.set_value(Number(value))

        elif type(value) is Number:

            self.numeric_value = value

    def value(self):
        """
        Gets the numerical value of the variable

        :return: The value of the variable
        """

        return self.numeric_value

    __rmul__ = __mul__


class Expression:
    """
    Basic expression handler for simple functions.
    """

    def __init__(self, construct):
        """
        Class constructor for the expression class

        :param (dict | Variable) construct: The expression's construction identity.
        """

        # If we have been handed a Variable, we can construct a suitable Expression
        if type(construct) is Variable:
            raw = construct.name
            data = {"multiple": Number(1), "variables": [construct], "power": [Number(1)]}

            construct = {"raw": raw, "data": data}

        self.construct = construct

    def __str__(self):
        """
        Class string method

        :return: The expression's raw string data.
        """

        return Expression.raw_construct(self.construct["data"])

    @staticmethod
    def raw_construct(data):
        """
        Construct the instance's raw string form the data in its dictionary.

        :param data: The dictionary of the expression data
        :return: A string that represents the expression in a human read-able way.
        :rtype: str
        """

        zipped = list(zip(data["variables"], data["power"]))
        string_list = []

        for pair in zipped:
            try:
                if pair[1] == Number(1):
                    next_string = str(pair[0])

                elif pair[1] == Number(0):
                    next_string = ""

                else:
                    next_string = "[" + str(pair[0]) + "^(" + str(pair[1]) + ")]"

            except TypeError:
                next_string = "[" + str(pair[0]) + "^(" + str(pair[1]) + ")]"

            string_list.append(next_string)

        if not string_list:

            raw = str(data["multiple"])

        elif data["multiple"] == Number(0):

            raw = "0"

        else:
            raw = str(data["multiple"]) + "".join(string_list)

        return raw

    def __eq__(self, other):
        """
        Evaluates the value of the equality.

        :param other: The object being compared to this.
        :return: The result of the equality.
        :rtype: bool
        """
        equality = False

        if type(other) is Expression:

            if other.construct == self.construct:
                equality = True

        return equality

    def __mul__(self, other):
        """
        Expression multiplication method.

        :param other: The right side of the multiplication
        :return: An expression representing the multiplication
        :rtype: Expression
        """

        if (type(other) is Decimal) or (type(other) is int) or (type(other) is float)or (type(other) is complex):
            return self * Number(other)

        if type(other) is Number:
            new_multiple = self.construct["data"]["multiple"] * other
            new_variables = self.construct["data"]["variables"]
            new_power = self.construct["data"]["power"]

            new_data = {"multiple": new_multiple,
                        "variables": new_variables,
                        "power": new_power}

            construct = {"raw": Expression.raw_construct(new_data),
                         "data": new_data}

            return Expression(construct)

        if type(other) is Variable:

            # If the Variable is already in the expression.
            if other in self.construct["data"]["variables"]:

                new_multiple = self.construct["data"]["multiple"]
                new_variables = self.construct["data"]["variables"]

                index = self.construct["data"]["variables"].index(other)
                new_power = self.construct["data"]["power"][index] + Number(1)

                new_data = {"multiple": new_multiple,
                            "variables": new_variables,
                            "power": new_power}

                construct = {"raw": Expression.raw_construct(new_data),
                             "data": new_data}

            else:

                new_multiple = self.construct["data"]["multiple"]
                new_variables = self.construct["data"]["variables"]
                new_power = self.construct["data"]["power"]

                new_variables.append(other)
                new_power.append(Number(1))

                new_data = {"multiple": new_multiple,
                            "variables": new_variables,
                            "power": new_power}

                construct = {"raw": Expression.raw_construct(new_data),
                             "data": new_data}

            return Expression(construct)

        if type(other) is Expression:

            # Calculate the new multiple first.
            new_multiple = self.construct["data"]["multiple"] * other.construct["data"]["multiple"]
            new_variables = self.construct["data"]["variables"]
            new_power = self.construct["data"]["power"]

            # Iterate over the variables in other to find matches.
            for i in range(0, len(other.construct["data"]["variables"])):

                # If the variable is not in the current expression.
                if other.construct["data"]["variables"][i] not in self.construct["data"]["variables"]:

                    # Add the required information.
                    new_variables.append(other.construct["data"]["variables"][i])
                    new_power.append(other.construct["data"]["power"][i])

                else:

                    # Update the currently held information (namely the power).
                    index = self.construct["data"]["variables"].index(other.construct["data"]["variables"][i])
                    new_power[index] = other.construct["data"]["power"][i] + new_power[index]

            new_data = {"multiple": new_multiple,
                        "variables": new_variables,
                        "power": new_power}

            construct = {"raw": Expression.raw_construct(new_data),
                         "data": new_data}

            return Expression(construct)

        if issubclass(type(other), Expression):
            return self * Expression(other.construct)

    def __truediv__(self, other):
        """
        Expression division method.

        :param other: The denominator of the fraction.
        :return: An expression representing the division.
        :rtype: Expression
        """

        if (type(other) is Decimal) or (type(other) is int) or (type(other) is float) or (type(other) is complex):
            return self / Number(other)

        if type(other) is Number:
            new_multiple = self.construct["data"]["multiple"] / other
            new_variables = self.construct["data"]["variables"]
            new_power = self.construct["data"]["power"]

            data = {"multiple": new_multiple,
                    "variables": new_variables,
                    "power": new_power}

            raw = Expression.raw_construct(data)

            construct = {"raw": raw, "data": data}

            return Expression(construct)

        if type(other) is Variable:

            # If the expression already contains the variable.
            if other in self.construct["data"]["variables"]:

                new_multiple = self.construct["data"]["multiple"]
                new_variables = self.construct["data"]["variables"]
                new_power = self.construct["data"]["power"]

                index = self.construct["data"]["variables"].index(other)
                new_power[index] = self.construct["data"]["power"][index] - 1

                data = {"multiple": new_multiple,
                        "variables": new_variables,
                        "power": new_power}

                raw = Expression.raw_construct(data)

                construct = {"raw": raw, "data": data}

                return Expression(construct)

            else:

                new_multiple = self.construct["data"]["multiple"]
                new_variables = self.construct["data"]["variables"].append(other)
                new_power = self.construct["data"]["power"].append(Number(1))

                data = {"multiple": new_multiple,
                        "variables": new_variables,
                        "power": new_power}

                raw = Expression.raw_construct(data)

                construct = {"raw": raw, "data": data}

                return Expression(construct)

        if type(other) is Expression:

            temp_multiple = Number(1) / Number(other.construct["data"]["multiple"])
            temp_variables = other.construct["data"]["variables"]
            temp_power = []

            for i in range(0, len(other.construct["data"]["power"])):
                temp_power.append(other.construct["data"]["power"][i] * Number(-1))

            data = {"multiple": temp_multiple,
                    "variables": temp_variables,
                    "power": temp_power}

            raw = Expression.raw_construct(data)

            construct = {"raw": raw, "data": data}

            return Expression(construct) * self

        if issubclass(type(other), Expression):
            return self / Expression(other.construct)

    def __pow__(self, power, modulo=None):
        """
        An expression raised to a power.

        :param power: The exponent the to raise the expression by.
        :return: The expression raised to the power.
        :rtype: Expression.
        """

        if (type(power) is Decimal) or (type(power) is int) or (type(power) is float) or (type(power) is complex):
            return self ** Number(power)

        if type(power) is Number:
            data = {"multiple": self.construct["data"]["multiple"] ** power,
                    "variables": self.construct["data"]["variables"],
                    "power": [power * p for p in self.construct["data"]["power"]]}
            raw = self.raw_construct(data)

            construct = {"raw": raw,
                         "data": data}

            return Expression(construct)

        if type(power) is Variable:
            data = {"multiple": Number(1),
                    "variables": self.construct["data"]["variables"],
                    "power": [power * p for p in self.construct["data"]["power"]]}

            data["variables"].append(self.construct["data"]["multiple"])
            data["power"].append(power)

            raw = self.raw_construct(data)

            construct = {"raw": raw,
                         "data": data}

            return Expression(construct)

        if type(power) is Expression:


            data = {"multiple": Number(1),
                    "variables": self.construct["data"]["variables"],
                    "power": [power * p for p in self.construct["data"]["power"]]}

            raw = self.raw_construct(data)

            construct = {"raw": raw,
                         "data": data}

            return Expression(construct)

    def value(self):
        """
        Finds the value of the Expression.

        :return: The value of the expression
        :rtype: Expression
        """

        new_multiple = self.construct["data"]["multiple"]
        new_variables = []
        new_power = []

        to_ignore = []

        for i in range(0, len(self.construct["data"]["variables"])):

            var_value = self.construct["data"]["variables"][i].value()
            pow_value = self.construct["data"]["power"][i].value()

            if (var_value is not None) and (pow_value is not None):
                new_multiple = new_multiple * (var_value ** pow_value)
                to_ignore.append(i)

        for j in range(0, len(self.construct["data"]["variables"])):

            if j not in to_ignore:
                new_variables.append(self.construct["data"]["variables"][j])
                new_power.append(self.construct["data"]["power"][j])

        if len(new_variables) != 0:
            new_data = {"multiple": new_multiple,
                        "variables": new_variables,
                        "power": new_power}

            construct = {"raw": Expression.raw_construct(new_data),
                         "data": new_data}

            return Expression(construct)

        else:

            return new_multiple

    __rmul__ = __mul__


class CustomF(Expression):
    """
    The builtin extension of the functions class representing custom functions.
    """

    def __init__(self, name):
        """
        Class constructor for custom functions.

        :param name: The name of the function
        """

        raw = name
        data = {"multiple": Number(1), "variables": [self], "power": [Number(1)]}

        self.construct = {"raw": raw, "data": data}

        super().__init__(self.construct)


class exp(CustomF):
    """
    Built in class representing the algebraic construction of 'e'.
    """

    def __init__(self):
        """
        Class constructor method for the exponential function.
        """

        self.name = "e"
        super().__init__(self.name)

    def __str__(self):
        """
        Class string method.

        :return: The raw string for the function 'e'.
        """

        return self.name

    def __eq__(self, other):
        """
        Evaluates the value of the equality.

        :param other: The object being compared to this.
        :return: The result of the equality.
        :rtype: bool
        """
        equality = False

        if type(other) is exp:
            equality = True

        return equality
    
    def __pow__(self, power, modulo=None):
        """
        Calculate the result of e raised to the power of a Number().
        
        :param power: The exponent
        :return: The result of the exponentiation
        """
        
        if type(power) is Number:
            
            return Number(((exp**power.real)*cos(power.imag)).value(),
                          ((exp**power.real)*sin(power.imag)).value())

    def value(self):
        """
        Returns the numerical value e.

        :return: The value e
        :rtype: Number
        """

        return Number(Decimal.exp(Decimal("1")), 0)


class sin(CustomF):
    """
    Built in representation of the algebraic construction of the sine function.
    """

    def __init__(self, x):
        """
        Class constructor method for the sin function.
        """
        self.name = "sin"
        self.x = x
        super().__init__(self.name)

    def __str__(self):
        """
        Class string method.

        :return: The raw string for the function sin().
        """
        return self.name + "(" + str(self.x) + ")"

    def __eq__(self, other):
        """
        Evaluates the value of the equality.

        :param other: The object being compared to this.
        :return: The result of the equality.
        :rtype: bool
        """
        equality = False

        if type(other) is sin:

            if other.x == self.x:
                equality = True

        return equality

    def value(self):
        """
        Finds the value of the sine function.

        :return: The value of the sine.
        :rtype: Expression
        """

        x_val = self.x.value()
        if type(x_val) is Number:

            if x_val.is_real():
                getcontext().prec += 2

                sin_val = Decimal("0")
                sin_val_prev = Decimal("1")
                n = Decimal("0")

                while sin_val != sin_val_prev:
                    sin_val_prev = sin_val

                    twoNone = (Decimal("2")*n) + Decimal("1")
                    fact = Decimal("1")

                    for i in range(0, int(twoNone)):
                        fact *= twoNone - i

                    sin_val += (Decimal("-1")**(n)) * (x_val.real**(twoNone))/fact

                    n += 1

                getcontext().prec -= 2
                return Number(sin_val)

        else:
            return sin(x_val)


class cos(CustomF):
    """
    Built in representation of the algebraic construction of the cosine function.
    """

    def __init__(self, x):
        """
        Class constructor method for the cosine function
        """

        self.name = "cos"
        self.x = x
        super().__init__(self.name)

    def __str__(self):
        """
        Class string method.

        :return: The raw string for the function cos().
        """
        return self.name + "(" + str(self.x) + ")"

    def __eq__(self, other):
        """
        Evaluates the value of the equality.

        :param other: The object being compared to this.
        :return: The result of the equality.
        :rtype: bool
        """

        equality = False

        if type(other) is cos:

            if other.x == self.x:
                equality = True

        return equality

    def value(self):
        """
        Finds the value of the cosine function.

        :return: The value of the cosine.
        :rtype: Expression
        """

        x_val = self.x.value()
        if type(x_val) is Number:

            if x_val.is_real():
                getcontext().prec += 2

                cos_val = Decimal("0")
                cos_val_prev = Decimal("1")
                n = Decimal("0")

                while cos_val != cos_val_prev:
                    cos_val_prev = cos_val

                    twoN = (Decimal("2")*n)
                    fact = Decimal("1")

                    for i in range(0, int(twoN)):
                        fact *= twoN - i

                    cos_val += (Decimal("-1")**(n)) * (x_val.real**(twoN))/fact

                    n += 1

                getcontext().prec -= 2
                return Number(cos_val)

        else:
            return sin(x_val)


class tan(CustomF):
    """
    Built in representation of the algebraic construction of the tangent function.
    """

    def __init__(self, x):
        """
        Class constructor method for the tangent function
        """

        self.name = "tan"
        self.x = x
        super().__init__(self.name)

    def __str__(self):
        """
        Class string method.

        :return: The raw string for the function tan().
        """
        return self.name + "(" + str(self.x) + ")"

    def __eq__(self, other):
        """
        Evaluates the value of the equality.

        :param other: The object being compared to this.
        :return: The result of the equality.
        :rtype: bool
        """

        equality = False

        if type(other) is tan:

            if other.x == self.x:
                equality = True

        return equality


class cosec(CustomF):
    """
    Built in representation of the algebraic construction of the cosecant function.
    """

    def __init__(self, x):
        """
        Class constructor method for the cosec function.
        """
        self.name = "cosec"
        self.x = x
        super().__init__(self.name)

    def __str__(self):
        """
        Class string method.

        :return: The raw string for the function cosec().
        """
        return self.name + "(" + str(self.x) + ")"

    def __eq__(self, other):
        """
        Evaluates the value of the equality.

        :param other: The object being compared to this.
        :return: The result of the equality.
        :rtype: bool
        """
        equality = False

        if type(other) is cosec:

            if other.x == self.x:
                equality = True

        return equality


class sec(CustomF):
    """
    Built in representation of the algebraic construction of the secant function.
    """

    def __init__(self, x):
        """
        Class constructor method for the sec function.
        """
        self.name = "sec"
        self.x = x
        super().__init__(self.name)

    def __str__(self):
        """
        Class string method.

        :return: The raw string for the function sec().
        """
        return self.name + "(" + str(self.x) + ")"

    def __eq__(self, other):
        """
        Evaluates the value of the equality.

        :param other: The object being compared to this.
        :return: The result of the equality.
        :rtype: bool
        """
        equality = False

        if type(other) is sec:

            if other.x == self.x:
                equality = True

        return equality


class cot(CustomF):
    """
    Built in representation of the algebraic construction of the cotangent function.
    """

    def __init__(self, x):
        """
        Class constructor method for the cot function.
        """
        self.name = "cot"
        self.x = x
        super().__init__(self.name)

    def __str__(self):
        """
        Class string method.

        :return: The raw string for the function sec().
        """
        return self.name + "(" + str(self.x) + ")"

    def __eq__(self, other):
        """
        Evaluates the value of the equality.

        :param other: The object being compared to this.
        :return: The result of the equality.
        :rtype: bool
        """
        equality = False

        if type(other) is sec:

            if other.x == self.x:
                equality = True

        return equality


class arcsin(CustomF):
    """
    Built in representation of the algebraic construction of the arcsine function.
    """

    def __init__(self, x):
        """
        Class constructor method for the arcsin function
        """

        self.name = "arcsin"
        self.x = x
        super().__init__(self.name)

    def __str__(self):
        """
        Class string method.

        :return: The raw string for the function arcsin().
        """
        return self.name + "(" + str(self.x) + ")"

    def __eq__(self, other):
        """
        Evaluates the value of the equality.

        :param other: The object being compared to this.
        :return: The result of the equality.
        :rtype: bool
        """

        equality = False

        if type(other) is arcsin:

            if other.x == self.x:
                equality = True

        return equality


class arccos(CustomF):
    """
    Built in representation of the algebraic construction of the arccosine function.
    """

    def __init__(self, x):
        """
        Class constructor method for the arccosine function
        """

        self.name = "arccos"
        self.x = x
        super().__init__(self.name)

    def __str__(self):
        """
        Class string method.

        :return: The raw string for the function arccos().
        """
        return self.name + "(" + str(self.x) + ")"

    def __eq__(self, other):
        """
        Evaluates the value of the equality.

        :param other: The object being compared to this.
        :return: The result of the equality.
        :rtype: bool
        """

        equality = False

        if type(other) is arccos:

            if other.x == self.x:
                equality = True

        return equality


class arctan(CustomF):
    """
    Built in representation of the algebraic construction of the arctangent function.
    """

    def __init__(self, x):
        """
        Class constructor method for the arctangent function
        """

        self.name = "arctan"
        self.x = x
        super().__init__(self.name)

    def __str__(self):
        """
        Class string method.

        :return: The raw string for the function arctan().
        """
        return self.name + "(" + str(self.x) + ")"

    def __eq__(self, other):
        """
        Evaluates the value of the equality.

        :param other: The object being compared to this.
        :return: The result of the equality.
        :rtype: bool
        """

        equality = False

        if type(other) is arctan:

            if other.x == self.x:
                equality = True

        return equality


class arccsc(CustomF):
    """
    Built in representation of the algebraic construction of the arccosecant function.
    """

    def __init__(self, x):
        """
        Class constructor method for the arccosecant function
        """

        self.name = "arccsc"
        self.x = x
        super().__init__(self.name)

    def __str__(self):
        """
        Class string method.

        :return: The raw string for the function arccsc().
        """
        return self.name + "(" + str(self.x) + ")"

    def __eq__(self, other):
        """
        Evaluates the value of the equality.

        :param other: The object being compared to this.
        :return: The result of the equality.
        :rtype: bool
        """

        equality = False

        if type(other) is arccsc:

            if other.x == self.x:
                equality = True

        return equality


class arcsec(CustomF):
    """
    Built in representation of the algebraic construction of the arcsecant function.
    """

    def __init__(self, x):
        """
        Class constructor method for the arcsecant function
        """

        self.name = "arcsec"
        self.x = x
        super().__init__(self.name)

    def __str__(self):
        """
        Class string method.

        :return: The raw string for the function arcsec().
        """
        return self.name + "(" + str(self.x) + ")"

    def __eq__(self, other):
        """
        Evaluates the value of the equality.

        :param other: The object being compared to this.
        :return: The result of the equality.
        :rtype: bool
        """

        equality = False

        if type(other) is arcsec:

            if other.x == self.x:
                equality = True

        return equality


class arccot(CustomF):
        """
        Built in representation of the algebraic construction of the arccotangent function.
        """

        def __init__(self, x):
            """
            Class constructor method for the arccotangent function
            """

            self.name = "arccot"
            self.x = x
            super().__init__(self.name)

        def __str__(self):
            """
            Class string method.

            :return: The raw string for the function arccot().
            """
            return self.name + "(" + str(self.x) + ")"

        def __eq__(self, other):
            """
            Evaluates the value of the equality.

            :param other: The object being compared to this.
            :return: The result of the equality.
            :rtype: bool
            """

            equality = False

            if type(other) is arccot:

                if other.x == self.x:
                    equality = True

            return equality
