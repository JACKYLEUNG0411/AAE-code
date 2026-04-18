prec = 2
#jacky ivan edmond
class fixNum:
    def __init__(self, a=0, b=0):
        self.a = int(a)
        self.b = int(b)
        self._normalize()

    def _normalize(self):
        scale = 10 ** prec
        carry = self.b // scale
        self.a += carry
        self.b = self.b % scale
        if self.b < 0:
            self.a -= 1
            self.b += scale

    def input(self):
        while True:
            try:
                a = int(input("Input integer part (a): "))
                b_str = input("Input fractional part (b): ").strip()
                if b_str.isdigit() and len(b_str) < prec:
                    b_str += '0' * (prec - len(b_str))
                b = int(b_str)
                self.a = a
                self.b = b
                self._normalize()
                break
            except:
                print("Invalid input! Please enter integers.")

    def __str__(self):
        b_str = f"{self.b:0{prec}d}"
        return f"{self.a}.{b_str}"

    def __mul__(self, other):
        if not isinstance(other, fixNum):
            raise TypeError
        scale = 10 ** prec
        s = self.a * scale + self.b
        o = other.a * scale + other.b
        res = (s * o) // scale
        return fixNum(res // scale, res % scale)

    def _reciprocal(self):
        if self.a == 0 and self.b == 0:
            raise ValueError
        scale = 10 ** prec
        num = self.a * scale + self.b
        recip = (scale * scale) // num
        return fixNum(recip // scale, recip % scale)

    def __pow__(self, exp):
        if isinstance(exp, int):
            if self.a == 0 and self.b == 0 and exp <= 0:
                print("Error: Fixed-point number is zero.")
                return None
            if exp == 0:
                return fixNum(1, 0)
            if exp < 0:
                return self._reciprocal() ** (-exp)
            res = fixNum(1, 0)
            base = fixNum(self.a, self.b)
            while exp > 0:
                if exp % 2 == 1:
                    res = res * base
                base = base * base
                exp //= 2
            return res
        elif isinstance(exp, fixNum):
            if self.a == 0 and self.b == 0:
                print("Error: Base is zero.")
                return None
            scale = 10 ** prec
            bf = self.a + self.b/scale
            ef = exp.a + exp.b/scale
            pr = round(bf ** ef * scale)
            return fixNum(pr // scale, pr % scale)
