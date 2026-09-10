from client import WesolowskiVDF

def main():
    print("=== Testing Wesolowski Verifiable Delay Function (VDF) ===")
    vdf = WesolowskiVDF(modulus=1000000007)
    x = 3
    T = 16

    y, pi, l, r = vdf.evaluate(x, T)
    print(f"Sequential evaluation output y={y} after {T} squarings.")
    print(f"Proof pi={pi}, challenge l={l}")

    valid = vdf.verify(x, y, pi, l, r)
    print(f"O(1) Verification result: {valid}")
    assert valid is True
    print("=== All tests passed successfully! ===")

if __name__ == "__main__":
    main()
