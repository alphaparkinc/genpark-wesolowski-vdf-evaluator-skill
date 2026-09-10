import sys
import json
from client import WesolowskiVDF

vdf = WesolowskiVDF(1000000007)

def handle_call(name, arguments):
    if name == "evaluate":
        x = arguments["x"]
        t = arguments.get("t", 16)
        y, pi, l, r = vdf.evaluate(x, t)
        return {"y": y, "proof": pi, "challenge": l, "r": r}
    elif name == "verify":
        x = arguments["x"]
        y = arguments["y"]
        pi = arguments["proof"]
        l = arguments["challenge"]
        r = arguments["r"]
        return {"valid": vdf.verify(x, y, pi, l, r)}
    return {"error": f"Unknown tool: {name}"}

def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            res = handle_call(req.get("name"), req.get("arguments", {}))
            print(json.dumps({"id": req.get("id"), "result": res}))
            sys.stdout.flush()
        except Exception as e:
            print(json.dumps({"error": str(e)}))
            sys.stdout.flush()

if __name__ == "__main__":
    main()
