import pandas as pd
from pathlib import Path
from matplotlib import pyplot as plt


df_factura_received = pd.read_excel(Path.cwd() / 'base' / "_СчетФактураПолученный.xlsx")
df_prihod = pd.read_excel(Path.cwd() / 'result_elmet' / "_результат_Приход товара.xlsx")
duplicated = df_factura_received.duplicated(["ДокументОснованиеНомер", "ДокументОснованиеДата"])
print(duplicated[duplicated == True])
df_prihod["common"] = df_prihod["Номер"] + "*" + df_prihod["Дата"]
df_factura_received["common"] = df_factura_received["ДокументОснованиеНомер"] + "*" \
                                + df_factura_received["ДокументОснованиеДата"]
result = pd.merge(df_prihod, df_factura_received[["common", "СуммаДокумента"]], how="left", on="common")
result = result[["common", "СуммаДокумента_x", "СуммаДокумента_y"]]
result["difference"] = result["СуммаДокумента_x"] - result["СуммаДокумента_y"]
print(result[result["difference"] > 0])







