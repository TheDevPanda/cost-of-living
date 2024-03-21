import json

import pandas as pd

with open("./costofliving/lebenshaltungskosten.json", "r", encoding="utf-8") as f:
    df = pd.read_json(
        f,
        orient="records",
        dtype={
            "Jahr": "int32",
            "Land": "string",
            "Lebenshaltungskosten": "float32",
            "Miete": "float32",
            "LebenshaltungPlusMiete": "float32",
            "Lebensmittel": "float32",
            "Gaststaetten": "float32",
            "Kaufkraft": "float32",
        },
    )

with open("./flags.json", "r", encoding="utf-8") as f:
    flags = pd.read_json(
        f, orient="records", dtype={"Land": "string", "Flagge": "string"}
    )

df = df.join(flags.set_index("Land"), on="Land", validate="m:1")


df = df.loc[df.Jahr == 2024]
df["name"] = df["Land"]

for col in [
    "Lebenshaltungskosten",
    "Miete",
    "LebenshaltungPlusMiete",
    "Lebensmittel",
    "Gaststaetten",
    "Kaufkraft",
]:
    df[col] /= df.loc[df.Land == "Deutschland"][col].iloc[0]

with open("costofliving.json", "w", encoding="utf-8") as f:
    df.to_json(f, orient="records", force_ascii=False)
