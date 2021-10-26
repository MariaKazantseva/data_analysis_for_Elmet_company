import pandas as pd
from pathlib import Path
from matplotlib import pyplot as plt


def filling_df(file_name):
    df = pd.read_excel(file_name)
    df["Сумма"] = df["quantity"] * df["price"]
    proveden = (df["Проведен"] == "Да") & (df["ПометкаУдаления"] == "Нет")
    result = df[proveden].groupby(["id"])["Сумма"].sum()
    result.sort_values(ascending=False, inplace=True)
    result = result[:10]
    return pd.merge(result, df_products[["id", "Наименование"]], on="id", how="left")


PATH_BASE = Path.cwd() / "result_elmet"
df_products = pd.read_excel(Path.cwd() / "base" / "_Номенклатура.xlsx")
df_products.rename(columns={"Код": "id"}, inplace=True)
df_prihod = filling_df(PATH_BASE / "_результат_Приход товара.xlsx")
df_rashod = filling_df(PATH_BASE / "_результат_Расход товара.xlsx")


plt.subplots(2, 1)
ax = plt.gca()
ax.get_xaxis().get_major_formatter().set_scientific(False)

plt.subplot(211)
plt.title("Топ 10 покупаемых товаров")
plt.barh(df_prihod["Наименование"], df_prihod["Сумма"])

ax = plt.gca()
ax.get_xaxis().get_major_formatter().set_scientific(False)

plt.subplot(212)
plt.title("Топ 10 продаваемых товаров", fontsize=10)
plt.barh(df_rashod["Наименование"], df_rashod["Сумма"])

plt.show()

