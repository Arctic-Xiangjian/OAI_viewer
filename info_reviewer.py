import json
import pandas as pd
import tkinter as tk
from tkinter import ttk

def main():
    # 读取数据
    try:
        data_cli = pd.read_csv('data/clin_data_selected.csv')
    except FileNotFoundError:
        print('No data file found, please put the clin_data.csv in the ./data folder')
        return

    try:
        cli_data_json = json.load(open('data/info_select.json'))
    except FileNotFoundError:
        print('No data file found, please put the info_select.json in the ./data folder')
        return

    # 构建GUI
    root = tk.Tk()
    root.title("Artery based Data Visualization")
    root.geometry('400x600')

    # 下拉菜单 - 病人ID
    patient_id_dropdown = ttk.Combobox(root, values=list(data_cli['sid'].unique()))
    patient_id_dropdown.set(int(list(data_cli['sid'].unique())[0]))
    patient_id_dropdown.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

    # 创建信息标签
    info_labels = {}
    for i, (key, value) in enumerate(cli_data_json.items(), start=1):
        key_label = ttk.Label(root, text=value)
        key_label.grid(row=i, column=0, sticky='e', padx=10, pady=2)

        value_label = ttk.Label(root, text="")
        value_label.grid(row=i, column=1, sticky='w', padx=10, pady=2)

        info_labels[key] = value_label

    # 更新信息的函数
    def update_info():
        selected_sid = patient_id_dropdown.get()
        patient_data = data_cli[data_cli['sid'] == int(selected_sid)]
        if not patient_data.empty:
            for key, label in info_labels.items():
                display_text = f"{patient_data.iloc[0][key]}"
                label.config(text=display_text)

    # 下拉菜单选择事件绑定
    patient_id_dropdown.bind("<<ComboboxSelected>>", lambda e: update_info())

    # 初始化显示
    update_info()

    # 运行主循环
    root.mainloop()

if __name__ == '__main__':
    main()
