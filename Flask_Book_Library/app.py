from project import app
from flask import request
import subprocess

@app.get("/debug/unsafe-eval")
def unsafe_eval():
    expr = request.args.get("expr", "2+2")
    return str(eval(expr))

@app.get("/debug/unsafe-cmd")
def unsafe_cmd():
    cmd = request.args.get("cmd", "echo CI_test")
    out = subprocess.check_output(cmd, shell=True, text=True)
    return out

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
