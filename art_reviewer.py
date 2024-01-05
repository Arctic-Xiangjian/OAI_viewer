import os
import sys
import json
import pandas as pd

from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import tkinter as tk
from tkinter import ttk
from tkinter import Toplevel

def get_file_path(filename):
    """get the absolute path of the file"""
    if getattr(sys, 'frozen', False):
        application_path = sys._MEIPASS
    else:
        application_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(application_path, filename)


def main():
    try:
        data_art = pd.read_csv(get_file_path('data/art.csv'))
        sid_filter = pd.read_csv(get_file_path('data/clin_data_selected.csv'))
    except FileNotFoundError:
        print('No data file found, please put the art.csv and clin_data_selected.csv in the ./data folder.')

    # 尝试读取 JSON 文件
    try:
        with open(get_file_path('data/art_measure.json'), 'r') as file:
            arc_data_json = json.load(file)
    except FileNotFoundError:
        print('No data file found, please put the art_measure.json in the ./data folder.')


    # build the GUI
    root = tk.Tk()
    root.title("Artery based Data Visualization")

    root.grid_rowconfigure(2, weight=1) # make the canvas expand to fill the entire grid
    root.grid_columnconfigure(0, weight=1) # make the canvas expand to fill the entire grid

    filter_sid = ['Risk', 'Smoker', 'Diabetes', 'Stroke', 'Heart Attack']

    checkbox_frame = ttk.Frame(root)
    checkbox_frame.grid(row=1, column=1)

    # 创建复选框变量
    checkbox_var = {}

    def update_dropdown():
        filtered_data = sid_filter.copy()
        for key, var in checkbox_var.items():
            if var.get() == 1:
                filtered_data = filtered_data[filtered_data[key] == 'Yes']
        
        # 更新下拉菜单的选项
        patient_id_dropdown['values'] = list(filtered_data['sid'].unique())
        if filtered_data['sid'].unique().size > 0:
            patient_id_dropdown.set(filtered_data['sid'].unique()[0])
        else:
            patient_id_dropdown.set('')

    # 创建并放置复选框
    for i, value in enumerate(filter_sid):
        checkbox_var[value] = tk.IntVar()
        checkbox = ttk.Checkbutton(checkbox_frame, text=value, variable=checkbox_var[value], command=update_dropdown)
        # checkbox.grid(row=3, column=i, sticky='w')
        checkbox.pack(side=tk.RIGHT)


    # 创建Combobox
    patient_id_dropdown = ttk.Combobox(root, values=list(sid_filter['sid'].unique()))
    patient_id_dropdown.set(int(sid_filter['sid'].unique()[0]))
    patient_id_dropdown.grid(row=0, column=0, padx=2, pady=2)

    # build the which measure dropdown
    which_measure_dropdown = ttk.Combobox(root, values=list(arc_data_json.keys()))
    which_measure_dropdown.set(list(arc_data_json.keys())[0])
    which_measure_dropdown.grid(row=1, column=0, padx=10, pady=10)

    # build the side
    side_var = tk.StringVar(value='L')
    side_frame = ttk.Frame(root)
    side_frame.grid(row=0, column=1, padx=10, pady=10)
    side_l = ttk.Radiobutton(side_frame, text='L', variable=side_var, value='L')
    side_r = ttk.Radiobutton(side_frame, text='R', variable=side_var, value='R')
    side_l.pack(side=tk.LEFT)
    side_r.pack(side=tk.LEFT)


    # 绘图区域
    fig, ax = plt.subplots(figsize=(5, 3))
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.grid(row=2, column=0, columnspan=2, sticky='nsew') # use sticky to expand the canvas to fill the entire grid

    # 可视化函数
    def plot_data(*args):
        which_measure = arc_data_json[which_measure_dropdown.get()]
        patient_id = patient_id_dropdown.get()
        side = side_var.get()
        available_time_points = data_art[(data_art['sid'] == int(patient_id)) &
                                            (data_art['side'] == side)
                                        ]['tp'].unique()
        available_time_points = sorted(available_time_points)

        filtered_data = data_art[(data_art['sid'] == int(patient_id)) &  
                                (data_art['side'] == side)]

        ax.clear()
        color_map = plt.get_cmap('tab10')

        # all_data = data_art[data_art['side'] == side]
        # avg_value_list = []
        # for tp in available_time_points:
        #     # 计算特定时间点的平均值
        #     avg_value = all_data[all_data['tp'] == tp][which_measure].mean()
        #     avg_value_list.append(avg_value)


        # ax.plot(available_time_points, avg_value_list, color='grey', linestyle='--')
        ax.scatter(available_time_points, filtered_data[which_measure], color=color_map(2))
        ax.plot(available_time_points, filtered_data[which_measure], color=color_map(2))
        ax.set_xticks(available_time_points)

        ax.set_xlabel('time points')
        ax.set_ylabel(which_measure_dropdown.get())
        ax.set_title(f'Patient: {patient_id}, Side: {side}')
        fig.tight_layout()
        # ax.legend()
        canvas.draw()


    plot_data()
    patient_id_dropdown.bind('<<ComboboxSelected>>', plot_data)
    which_measure_dropdown.bind('<<ComboboxSelected>>', plot_data)
    side_var.trace_add('write', plot_data)

    popup = None

    def Popinfo():

        nonlocal popup

        if popup is not None and popup.winfo_exists():
            popup.destroy()


        popup = Toplevel(root)
        popup.title("Patient Information")
        popup.geometry("400x600")

        try:
            data_cli = pd.read_csv(get_file_path('data/clin_data_selected.csv'))
        except FileNotFoundError:
            print('No data file found, please put the clin_data_selected.csv in the ./data folder')
            return

        try:
            cli_data_json = json.load(open(get_file_path('data/info_select.json')))
        except FileNotFoundError:
            print('No data file found, please put the info_select.json in the ./data folder')
            return
        
        info_labels = {}
        for i, (key, value) in enumerate(cli_data_json.items(), start=1):
            key_label = ttk.Label(popup, text=value)  # Change root to popup
            key_label.grid(row=i, column=0, sticky='e', padx=10, pady=2)

            value_label = ttk.Label(popup, text="")  # Change root to popup
            value_label.grid(row=i, column=1, sticky='w', padx=10, pady=2)

            info_labels[key] = value_label

        # Updating information function
        def update_info():
            selected_sid = patient_id_dropdown.get()
            patient_data = data_cli[data_cli['sid'] == int(selected_sid)]
            if not patient_data.empty:
                for key, label in info_labels.items():
                    display_text = f"{patient_data.iloc[0][key]}"
                    label.config(text=display_text)

        update_info()  # Call update_info to initialize the display with the current patient's data

    open_popup_button = tk.Button(root, text="Patient Information", command=Popinfo)
    open_popup_button.grid(row=3, column=0, columnspan=2, pady=10)  # Adjusted placement for button

    root.mainloop()

if __name__ == '__main__':
    main()