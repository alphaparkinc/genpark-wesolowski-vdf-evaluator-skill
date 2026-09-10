import hashlib
import math

class WesolowskiVDF:
    """
    Wesolowski's Verifiable Delay Function (VDF).
    Evaluates y = x^(2^T) mod N sequentially (requiring T steps).
    Generates proof pi = x^q mod N where 2^T = q*l + r (with l = hash(x, y)).
    Verification checks: pi^l * x^r == y (mod N) in O(1) multiplications!
    """
    def __init__(self, modulus):
        self.N = modulus

    def hash_prime(self, x, y):
        h = int(hashlib.sha256(f"{x}:{y}".encode()).hexdigest(), 16)
        cand = (h % 100000) | 1
        while True:
            is_p = True
            for d in range(3, int(math.isqrt(cand)) + 1, 2):
                if cand % d == 0:
                    is_p = False
                    break
            if is_p and cand > 2:
                return cand
            cand += 2

    def evaluate(self, x, T):
        curr = x
        for _ in range(T):
            curr = (curr * curr) % self.N
        y = curr

        l = self.hash_prime(x, y)
        two_T = 1 << T
        q = two_T // l
        r = two_T % l

        pi = pow(x, q, self.N)
        return y, pi, l, r

    def verify(self, x, y, pi, l, r):
        lhs = (pow(pi, l, self.N) * pow(x, r, self.N)) % self.N
        return lhs == (y % self.N)
