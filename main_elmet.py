import pandas as pd
from pathlib import Path


def format_func(y):
    return y.replace(" ", "").replace(",", ".")


def change_df_cells(src_df, src_index, src_str):
    src_df.at[src_index, 'id'] = src_str.split(";")[0]
    src_df.at[src_index, 'quantity'] = format_func(src_str.split(";")[1])
    src_df.at[src_index, 'price'] = format_func(src_str.split(";")[-1])
    src_df.at[src_index, 'Товары'] = src_str


my_files = ["_Приход товара", "_Расход товара", "_Счета от Поставщика", "_Счета Покупателю", "_СчетФактураВыданный"]
PATH_BASE = Path.cwd() / 'base'
for f in my_files:
    df = pd.read_excel(PATH_BASE / f'{f}.xlsx', dtype={"Товары": str})
    df.dropna(inplace=True)
    df["id"] = ""
    df["quantity"] = 0.0
    df["price"] = 0.0
    print("\n", f, df.shape[0])
    num = 0
    for i, row in df.iterrows():
        num += 1
        if num % 100 == 0:
            print(num, "/", end="")
        goods = row["Товары"]
        if "\n" in goods:
            list_goods = goods.split("\n")
            change_df_cells(df, i, list_goods[0])
            df_temp = df.loc[[i], :]
            for l in range(1, len(list_goods)):
                index_temp = df.last_valid_index() + 1
                df_temp.index = [index_temp]
                change_df_cells(df_temp, index_temp, list_goods[l])
                df = df.append(df_temp)
        else:
            change_df_cells(df, i, goods)
    df.to_excel(Path.cwd() / "result_elmet" / f"_результат{f}.xlsx")



