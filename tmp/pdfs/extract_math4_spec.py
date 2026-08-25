import ast, json, re
from pathlib import Path

src = Path("tmp/pdfs/build_math4_detailed_corrections.py").read_text()
tree = ast.parse(src)

motor = {}
games = []
for node in tree.body:
    if isinstance(node, ast.Assign) and getattr(node.targets[0], "id", "") == "MOTOR":
        motor = ast.literal_eval(node.value)
    if isinstance(node, ast.Assign) and getattr(node.targets[0], "id", "") == "games":
        for call in node.value.elts:
            a = [ast.literal_eval(x) for x in call.args]
            n, theme, title, sub, mkey, obs, why, new, rounds, fb, qa = a
            games.append(dict(
                id="p%02d" % n, tema=theme, ad=title, alt=sub, motor=mkey,
                motor_risk=motor[mkey][0], motor_geri=motor[mkey][1],
                sorunlar=obs, risk=why, sahne=new, turlar=rounds,
                geri=fb, kabul=qa))

Path("tmp/spec4.json").write_text(json.dumps(games, ensure_ascii=False, indent=1))
print(len(games), "oyun yazıldı")
print(sorted({g["motor"] for g in games}))
