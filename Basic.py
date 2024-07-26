String = "String"
Float = "Float"
Integer = "Integer"
Add = "Add"
Subtract = "Subtract"
Multiply = "Multiply"
Divide = "Divide"
Remainder = "Remainder"
ParL = "Parenthesis (L)"
ParR = "Parenthesis (R)"
Numbers = ".0123456789"
################################
#            b++               #
################################
################################################
#                    Bugs                      # 
################################################
#  1: "." doesnt know to be string or int      #
#  2: MakeNum Method doesnt know .2132.23132   #
#                                              #
#                                              #
################################################
class Error:
    def __init__(self, details):
        self.details = details
class CharError(Error):
    def __init__(self, details, Type="CharError"):
        self.type = Type
        super().__init__(details)
    def errorStr(self):
        return print(f"{self.type} |{self.details}|")

class ParsError(Error):
    pass



class Tokens:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value
    def __repr__(self):
        if self.value != None:return f"{self.type}:{self.value}"
        else: return f"{self.type}"
class Lexer:
    def __init__(self, text=None):
        self.text = text
        self.curPos = -1
        self.curChar = None
        self.advance()
    def advance(self):
        self.curPos += 1
        if self.curPos < len(self.text):
            self.curChar = self.text[self.curPos]
        if self.curPos == len(self.text):self.curChar = None
    def makeNumbers(self): #In future fix error when input is num.charnum and when you input something like: .1233.12321.12321
        number = ""
        decCount = 0 
        while self.curChar != None and self.curChar in (Numbers + "."):
            if self.curChar == ".":
                decCount += 1
                number += "."
            elif self.curChar in Numbers:
                number += self.curChar
            self.advance()
        if decCount == 0: number = Tokens(Integer, int(number))
        if decCount > 0: number = Tokens(Float, float(number))
        self.curPos -= 1
        return number
    def makeToken(self):
        tokens = []
        while self.curChar != None and self.curPos < len(self.text):
            if self.curChar in " \t":
                self.advance()
            elif self.curChar in Numbers:
               tokens.append(self.makeNumbers())
               self.advance()
            elif self.curChar == "+":
               tokens.append(Tokens(Add))
               self.advance()
            elif self.curChar == "-":
                tokens.append(Tokens(Subtract))
                self.advance()
            elif self.curChar == "*":
                tokens.append(Tokens(Multiply))
                self.advance()
            elif self.curChar == "/":
                tokens.append(Tokens(Divide))
                self.advance()
            elif self.curChar == "%":
                tokens.append(Tokens(Remainder))
                self.advance()
            elif self.curChar == "(":
                tokens.append(Tokens(ParL))
                self.advance()
            elif self.curChar == ")":
                tokens.append(Tokens(ParR))
                self.advance()
            elif isinstance(self.curChar, str):
                tokens.append(Tokens(String, self.curChar))
                self.advance()    
            else:
                return CharError(f"Unexpected character '{self.curChar}'").errorStr()
        return tokens 
class NumberNode:
    def __init__(self, token):
        self.token = token
    def __repr__(self):
        return f"{self.token}"
class BinaryOpNode:
    def __init__(self, left, opT, right):
        self.left = left
        self.opT = opT
        self.right = right
    def __repr__(self):
        return f"({self.left}, {self.opT}, {self.right})"

class Parser:
    def __init__(self, Tlist):
        self.tlist = Tlist
        self.curPos = -1
        self.curT = None
        self.advance()
    def advance(self):
        self.curPos += 1
        if self.curPos < len(self.tlist):
            self.curT = self.tlist[self.curPos]
        #else: self.curT = None if self.curPos == len(self.tlist): self.curT = None
    def parse(self):
        res = self.Expression()
        return res
    def Factor(self):
        NodeF = self.curT
        if NodeF.type in (Integer, Float):
            self.advance()
            return NumberNode(NodeF)
        elif NodeF == ParL:
            pass
        else: return None
    def Expression(self):
        return self.binop(self.Term, (Add, Subtract))
    def Term(self):
        return self.binop(self.Factor, (Multiply, Divide))
    def binop(self, func, ops):
        left = func()
        while self.curT.type in ops:
                op_tok = self.curT
                self.advance()
                right = func()
                left = BinaryOpNode(left, op_tok, right)
        return left



while True:
    inputs1 = str(input("Basic > "))
    if inputs1 == "end":     
        break
    else:
        
        this = Lexer(inputs1).makeToken()
        #print(this)
        parser = Parser(this)
        test = parser.parse()
        print(test)
