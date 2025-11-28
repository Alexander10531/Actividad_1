from pathlib import Path
import pandas as pd

#input_path = Path("comentarios.csv")
input_path = Path("02Dataset_anonimizado.csv")
tmp_path = Path("comentarios_sin_bytes_raros.csv")
output_path = Path("comentarios_limpio_utf8.csv")
BAD_BYTES = {0xBF, 0xA1, 0xB3}  # ¿, ¡, ³ en cp1252
 
with input_path.open("rb") as f_in, tmp_path.open("wb") as f_out:
    for raw_line in f_in:
        cleaned = bytes(b for b in raw_line if b not in BAD_BYTES)
        f_out.write(cleaned)

df = pd.read_csv(tmp_path, sep=";", encoding="latin1")

def arreglar_mojibake(s):
    if not isinstance(s, str):
        return s
    try:
        reparado = s.encode("latin1").decode("utf-8")
        return reparado
    except UnicodeError:
        return s

text_cols = df.select_dtypes(include="object").columns
for col in text_cols:
    df[col] = df[col].apply(arreglar_mojibake)

df.to_csv(output_path, sep=";", index=False, encoding="utf-8")
print("Archivo limpio guardado como:", output_path)

import pandas as pd 
df = pd.read_csv("comentarios_limpio_utf8.csv", sep=";", encoding="utf-8")