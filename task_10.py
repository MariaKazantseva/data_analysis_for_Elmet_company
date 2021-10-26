import pandas as pd
from pathlib import Path
from matplotlib import pyplot as plt


def season(x):
    if x.split(".")[1] in ["12", "01", "02"]:
        return "Зима"
    elif x.split(".")[1] in ["03", "04", "05"]:
        return "Весна"
    elif x.split(".")[1] in ["06", "07", "08"]:
        return "Лето"
    else:
        return "Осень"


df = pd.read_excel(Path.cwd() / "result_elmet" / "_результат_Расход товара.xlsx")
df["Сумма"] = df["quantity"] * df["price"]
df = df[(df["Проведен"] == "Да") & (df["ПометкаУдаления"] == "Нет")]
df["Время года"] = df["Дата"].apply(season)
df = df.groupby(["Время года"])["Сумма"].sum()

ax = plt.gca()
ax.get_yaxis().get_major_formatter().set_scientific(False)
plt.bar(df.index, df)
plt.title("Прибыль по временам года")
plt.show()


