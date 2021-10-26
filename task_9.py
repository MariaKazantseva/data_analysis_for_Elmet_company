import pandas as pd
from pathlib import Path
from matplotlib import pyplot as plt


df_products = pd.read_excel(Path.cwd() / "base" / "_Номенклатура.xlsx")
df_rashod = pd.read_excel(Path.cwd() / "result_elmet" / "_результат_Расход товара.xlsx")
df_rashod.rename(columns={"id": "Код"}, inplace=True)
df_rashod["Сумма"] = df_rashod["quantity"]*df_rashod["price"]
result = pd.merge(df_rashod, df_products[["РодительКод", "Код"]], on="Код", how="left")
result.rename(columns={"РодительКод": "common_code"}, inplace=True)
df_products.rename(columns={"Код": "common_code"}, inplace=True)
final = pd.merge(result, df_products[["Наименование", "common_code"]], on="common_code", how="left")
final_2 = final.groupby(["Наименование"])["Сумма"].sum()
final_2.sort_values(ascending=False, inplace=True)

ax = plt.gca()
ax.get_xaxis().get_major_formatter().set_scientific(False)
plt.barh(final_2.index, final_2)
plt.title("Самые прибыльные категории товаров")
plt.show()

