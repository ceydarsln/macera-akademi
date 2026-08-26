import ast, json
from pathlib import Path

src = Path("tmp/pdfs/build_sosyal4_detailed_corrections.py").read_text()
tree = ast.parse(src)
D = {}
for node in tree.body:
    if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name):
        ad = node.targets[0].id
        if ad in ("ENGINE","TYPE_RISK","TYPE_FEEDBACK","TYPE_ACCEPT",
                  "DESIGNS"):
            D[ad] = ast.literal_eval(node.value)

oyunlar = json.loads(Path("tmp/pdfs/sosyal4_games.json").read_text())

def kip(kaz):
    return "sosyal"



out = []
for g in oyunlar:
    t = g["type"]
    motor_ad, motor_sorun = D["ENGINE"][t]
    tasarim = D["DESIGNS"][g["id"]]
    out.append(dict(
        id=g["id"], tema=g["group"], ad=g["title"], alt=g["sub"], kaz=g["kaz"],
        eskiTip=t, eskiYonerge=g.get("instruction",""), sayilar=g.get("n",{}),
        motorAd=motor_ad, motorSorun=motor_sorun,
        tipRisk=D["TYPE_RISK"][t], tipGeri=D["TYPE_FEEDBACK"][t], tipKabul=D["TYPE_ACCEPT"][t],
        sahne=tasarim[0], ikinciTur=tasarim[1], ucuncuTur=tasarim[2]))

Path("tmp/spec_sb.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))
print(len(out), "oyun yazıldı")
from collections import Counter
print("eski tipler:", dict(Counter(g["eskiTip"] for g in out)))
print("temalar:", dict(Counter(g["tema"] for g in out)))
