import pandas as pd
from pathlib import Path
from matplotlib import pyplot as plt

df_factura_sent = pd.read_excel(Path.cwd() / 'base' / "_СчетФактураВыданный.xlsx")
df_factura_sent.dropna(inplace=True)
df_invoices = pd.read_excel(Path.cwd() / 'base' / "_Счета Покупателю.xlsx")
df_changed = pd.read_excel(Path.cwd() / 'result_elmet' / "_результат_Счета Покупателю.xlsx")
df_factura_sent["common"] = df_factura_sent["СчетНаОплатуНомер"] + "*" + df_factura_sent["СчетНаОплатуДата"]
df_invoices["common"] = df_invoices["Номер"] + "*" + df_invoices["Дата"]
proveden = (df_factura_sent["Проведен"] == "Да") & (df_factura_sent["ПометкаУдаления"] == "Нет")
df_factura_sent = df_factura_sent[proveden]
proveden = (df_invoices["Проведен"] == "Да") & (df_invoices["ПометкаУдаления"] == "Нет")
df_invoices = df_invoices[proveden]
result = pd.merge(df_invoices, df_factura_sent[["common", "Номер"]], how='left', on='common')
result = result[result["Номер_y"].isna()]

df_changed["Сумма"] = df_changed["quantity"]*df_changed["price"]
df_changed["common"] = df_changed['Номер'] + "*" + df_changed['Дата']
df_changed = df_changed.groupby(["common"])["Сумма"].sum()

df_changed = df_changed.to_frame()
final = pd.merge(result, df_changed, how="left", on="common")
really_final = final.groupby(["КонтрагентКод"])["Сумма"].sum()
really_final.sort_values(ascending=False, inplace=True)
really_final = really_final.to_frame()
agents = pd.read_excel(Path.cwd() / 'base' / "_Контрагент.xlsx")
agents.rename(columns={"Код": "КонтрагентКод"}, inplace=True)
final_final = pd.merge(really_final, agents, how="left", on="КонтрагентКод")
final_final[["Наименование", "Сумма"]].to_excel("Должники.xlsx")

ax = plt.gca()
ax.get_xaxis().get_major_formatter().set_scientific(False)
plt.barh(final_final["Наименование"][:10], final_final["Сумма"][:10])
plt.title("Должники")
plt.show()






