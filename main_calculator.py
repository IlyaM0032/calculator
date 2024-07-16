import calculator_module

# Algorithm: https://habr.com/ru/articles/50196/

def calculate(expression: str = ""):
    return evalue(tokenize(expression))

class Token:
    def __init__(self, _token) -> None:
        self.value = _token
        if isinstance(_token, float):
            self.__isNumber = True
            self.__isOperator = False
        elif _token in "+-*/^%()":
            self.__isNumber = False
            self.__isOperator = True


    def isOperator(self): return self.__isOperator
    def isNumber(self): return self.__isNumber

class Operator(Token):
    def __init__(self, _token) -> None:
        super().__init__(_token)
        self.function = None
        if self.value == '+':
            self.function = calculator_module.add
            self.priority = 3
        elif self.value == '-':
            self.function = calculator_module.sub
            self.priority = 3
        elif self.value == '*':
            self.function = calculator_module.mult
            self.priority = 2
        elif self.value == '/':
            self.function = calculator_module.div
            self.priority = 2
        elif self.value == '^':
            self.function = calculator_module.pow
            self.priority = 1            
        elif self.value == '%':
            self.function = calculator_module.mod
            self.priority = 2
        elif self.value == '(':
            self.priority = 0
        elif self.value == ')':
            self.priority = 4
        
    def __str__(self) -> str:
        return self.value
      

def tokenize(expression: str):
    if not expression: raise Exception("Empty input")
    digits = '01234567890.'
    operators = "+-*/^%()"
    tokens = [Operator('(')]
    number = ""
    for i in expression.replace(' ', ''):
        if i in digits: number+=i; continue
        if number and i not in digits:
            tokens.append(Token(float(number)))
            number = ''
        if i in operators:
            tokens.append(Operator(i))
        else:
            raise Exception(f"Unsopported token {i}")
    if number: tokens.append(Token(float(number)))
    tokens.append(Operator(')'))    
    return tokens

def evalue(expression: list[Token] = []):
    numbers = []
    operators : list[Operator] = []
    
    for i in expression:
        if not isinstance(i, Operator): 
            numbers.append(i.value)
            continue

        if (not operators or operators[-1].value == '(' or 
            i.value == operators[-1].value == '^' or 
            i.priority < operators[-1].priority):

            operators.append(i)
            continue

        while operators and i.priority >= operators[-1].priority and (i.value == ')' or operators[-1].value != '('):
            action = operators.pop().function
            if action:
                b = numbers.pop()
                try:
                    a = numbers.pop()
                except IndexError:
                    raise Exception("Error")
                numbers.append(action(a, b))
            else: break
        else:
            if i.value != ')': operators.append(i)
    
    if operators or len(numbers) != 1:
        raise Exception("Error")
    return numbers[0]


# def main():
#     expression = input("Enter your expression entirely\nAllowed operatoins: + - * / ^ %\n> ")

#     print(calculate(expression))

# if __name__ == "__main__":
#     main()

# 2 + (1 * 3 + 4) - (3 * (12 ^ (1 * (1 + 1))))
# = -423

