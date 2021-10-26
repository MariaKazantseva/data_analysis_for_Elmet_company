import pandas as pd
from pathlib import Path
from matplotlib import pyplot as plt
from datetime import datetime, timedelta


def func1(d):
    return datetime.strptime(d, "%d.%m.%Y %H:%M:%S")


def func2(d2):
    if d2.days > 30:
        return d2.days - 30
    else:
        return 0

df_factura_sent = pd.read_excel(Path.cwd() / 'base' / "_СчетФактураВыданный.xlsx")
df_factura_sent.dropna(inplace=True)
df_invoices = pd.read_excel(Path.cwd() / 'base' / "_Счета Покупателю.xlsx")
df_factura_sent["common"] = df_factura_sent["СчетНаОплатуНомер"] + "*" + df_factura_sent["СчетНаОплатуДата"]
df_invoices["common"] = df_invoices["Номер"] + "*" + df_invoices["Дата"]
proveden = (df_factura_sent["Проведен"] == "Да") & (df_factura_sent["ПометкаУдаления"] == "Нет")
df_factura_sent = df_factura_sent[proveden]
proveden = (df_invoices["Проведен"] == "Да") & (df_invoices["ПометкаУдаления"] == "Нет")
df_invoices = df_invoices[proveden]
result = pd.merge(df_invoices, df_factura_sent[["common", "Номер", "Дата"]], how='left', on='common')
result.drop(result[result["Номер_y"].isna()].index, inplace=True)

result['difference'] = (result["Дата_y"].apply(func1) - result["Дата_x"].apply(func1)).apply(func2)

result = result.groupby(['КонтрагентКод'])['difference'].sum()
result.sort_values(ascending=False, inplace=True)
result = result.to_frame()
result.drop(result[result['difference'] == 0].index, inplace=True)

agents = pd.read_excel(Path.cwd() / 'base' / "_Контрагент.xlsx")
agents.rename(columns={"Код": "КонтрагентКод"}, inplace=True)
final_final = pd.merge(result, agents[['КонтрагентКод', 'Наименование']], how="left", on="КонтрагентКод")
final_final[["Наименование", "difference"]].to_excel("Дни_просроченных_плетежей.xlsx")

ax = plt.gca()
ax.get_xaxis().get_major_formatter().set_scientific(False)
plt.barh(final_final["Наименование"][:10], final_final["difference"][:10])
plt.title("Дни просроченных плетежей")
plt.show()









