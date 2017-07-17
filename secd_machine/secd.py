import re
import copy

class SECDMachine:

    def __init__(self, code):
        self.secd = SECD([], {}, [code], [])

    def execute(self):
        """
        :param: code
        :return: result of execute.
        (((L_x.(L_y.y))a)b)
        """
        try:
            if len(self.secd.c) == 0 and len(self.secd.d) == 0:
                print("complete calculation")
                return
            print(self.secd)
            self.transform()
            print(self.secd)

        except:
            raise RuntimeError("source format is not formal")

    def transform(self):

        if self.control_null():
            self.transform_control_null()
        elif self.lambda_exp():
            self.transform_lambda_exp()
        elif self.identifier():
            self.transform_identifier()
        elif self.app():
            self.transform_app()
        elif self.combination():
            self.transform_combination()
        else:
            raise RuntimeError("構文が間違っている可能性があります")


    # -----------------------------
    # expression detectors
    def lambda_exp(self):
        """
        detect lambda_exp if hC is lambda_exp
        (L_.*)
        :rtype: bool
        :return: is_lambda exp or not 
        """
        if self.secd.hC[0] == '(' and self.secd.hC[1] == 'L' and self.secd.hC[2] == '_':
            return True
        else:
            return False

    def identifier(self):
        """
        detect lambda_exp if hC is lambda_exp
        a)
        :rtype: bool
        :return: is_lambda exp or not 
        """
        if self.secd.hC[0] != '(' and self.secd.hC != 'ap':
            return True
        else:
            return False

    def app(self):
        if self.secd.hC == 'ap':
            return True
        else:
            return False

    def combination(self):
        if self.secd.hC[0] == '(' and self.secd.hC[1] != 'L':
            return True
        else:
            return False

    def control_null(self):
        print(len(self.secd.c))
        if len(self.secd.c) < 1:
            return True
        else:
            return False

    # -----------------------------
    # secd transformers

    def transform_lambda_exp(self):
        self.secd.s.append(Closure(self.secd.c.pop(), self.secd.e))

    def transform_identifier(self):
        identifier = self.secd.c.pop()
        if identifier in self.secd.e:
            self.secd.s.append(self.secd.e[identifier])
        else:
            self.secd.s.append(identifier)

    def transform_app(self):
        if isinstance(self.secd.hS, Closure):
            env_from_closure = copy.deepcopy(self.secd.hS.environment)
            env_from_closure.update({self.secd.hS.bv: self.secd.s[-2]})
            self.secd.d = [
                self.secd.ttS if self.secd.ttS is not None else [],
                copy.deepcopy(self.secd.e),
                self.secd.tC if self.secd.tC is not None else [],
                []
            ]
            self.secd.c = [self.secd.hS.body]
            self.secd.e = env_from_closure
            self.secd.s = []
        else:
            self.secd.c.pop()
            if self.secd.tS is None:
                return
            elif self.secd.ttS is None:
                self.secd.s = [self.secd.s[-2] + self.secd.s[-1]]
            else:
                self.secd.s = [self.secd.s[-2] + self.secd.s[-1], self.secd.ttS]



    def transform_combination(self):
        combination = self.secd.c.pop()
        inside = combination[1:]

        rand = ""
        rator = ""
        ap = "ap"
        for i, char in enumerate(inside):
            if char == '(':
                tail_rator = get_block_last(inside[i:]) + i
                rator = inside[i:tail_rator + 1]
                rand = inside[tail_rator + 1]
                self.secd.c.extend([ap, rator, rand])
                return

    def transform_control_null(self):
        self.secd.s = self.secd.d[0] + self.secd.s
        self.secd.e = self.secd.d[1]
        self.secd.c = self.secd.d[2]
        self.secd.d = []



class SECD:

    def __init__(self, s, e, c, d, secd=None):
        if secd is None:
            self.s = s
            self.e = e
            self.c = c
            self.d = d
        else:
            self.s, self.e, self.c, self.d = secd.s, secd.e, secd.c, secd.d

    @property
    def hC(self):
        return self.c[-1]

    @property
    def hS(self):
        return self.s[-1]

    @property
    def tS(self):
        if len(self.s) > 1:
            return self.s[:-1]
        else:
            return None

    @property
    def tC(self):
        if len(self.c) > 1:
            return self.c[:-1]
        else:
            return None

    @property
    def ttS(self):
        if len(self.s) > 2:
            return self.s[:-2]
        else:
            return None


    def __repr__(self):
        return "<{class_name} [S:{s}, E:{e}, C:{c}, D:{d}]>".format(class_name=self.__class__.__name__, s=self.s, e=self.e, c=self.c, d=self.d)


def get_block_last(expression):

    string = expression
    count = 0
    index = 0

    for c in string:
        if c == '(':
            count += 1
        elif c == ')':
            count -= 1
            if count == 0:
                return index
        index += 1


def get_top_app_from_combination(combination):
    pass


class Closure:

    def __init__(self, lambda_exp, env):
        self.environment = env
        self.body = self.parse_body(lambda_exp)
        self.bv = self.parse_bv(lambda_exp)

    def parse_body(self, lambda_exp):
        exp = lambda_exp
        body_flag = 0
        for i, char in enumerate(exp):
            if body_flag == 3:
                if char == '(':
                    return exp[i:get_block_last(exp[i:]) + i + 1]
                else:
                    return char
            if char == "L":
                body_flag += 1
            elif char == "_":
                body_flag += 1
            elif char == ".":
                body_flag += 1


    def parse_bv(self, lambda_exp):
        exp = lambda_exp

        for i, char in enumerate(exp):
            if char == 'L' and exp[i+1] == '_':
                return exp[i+2]

    def __repr__(self):
        return "<{class_name} [env:{env}, bv:{bv}, body:{body}]>".format(class_name=self.__class__.__name__, env=self.environment, bv=self.bv, body=self.body)




