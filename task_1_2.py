import pandas as pd
from pathlib import Path
from matplotlib import pyplot as plt


def filling_df(file_name):
    df = pd.read_excel(file_name)
    df.index = pd.to_datetime(df["Дата"])
    df.drop("Дата", axis=1, inplace=True)
    df["Сумма"] = df["quantity"] * df["price"]
    proveden = (df["Проведен"] == "Да") & (df["ПометкаУдаления"] == "Нет")
    return df[proveden]["Сумма"].resample("Y").sum()


PATH_BASE = Path.cwd() / "result_elmet"
df_rashod = filling_df(PATH_BASE / "_результат_Расход товара.xlsx")
df_prihod = filling_df(PATH_BASE / "_результат_Приход товара.xlsx")

ax = plt.gca()
ax.get_yaxis().get_major_formatter().set_scientific(False)
plt.title("Прибыль и расходы")
plt.plot(df_rashod.index, df_rashod, label="Прибыль")
plt.plot(df_prihod.index, df_prihod, label="Расходы")
plt.legend()
plt.show()

