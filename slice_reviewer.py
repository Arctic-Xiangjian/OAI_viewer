import os
import sys
import json
import pandas as pd

from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import tkinter as tk
from tkinter import ttk
from tkinter import Toplevel

# Define global constants
MIN_WINDOW_WIDTH = 900
MIN_WINDOW_HEIGHT = 500

def get_file_path(filename):
    """get the absolute path of the file"""
    if getattr(sys, 'frozen', False):
        application_path = sys._MEIPASS
    else:
        application_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(application_path, filename)


# read in the data
def main():
    # try:
    #     data_loc = pd.read_csv('data/loc.csv')
    #     sid_filter = pd.read_csv('data/clin_data_selected.csv')
    # except FileNotFoundError:
    #     print('no data file found, please put the loc.csv/art.csv in the ./data folder')

    # try:
    #     vessel_data_json = json.load(open('data/vessel_measure.json'))
    #     # arc_data_json = json.load(open('data/data_dictionary_art.json'))
    # except FileNotFoundError:
    #     print('no data file found, please put the vessel_measure.json in the ./data folder')

    '''
    Read in the data
    '''
    try:
        data_loc = pd.read_csv(get_file_path('data/loc.csv'))
        sid_filter = pd.read_csv(get_file_path('data/clin_data_selected.csv'))
    except FileNotFoundError:
        print('No data file found, please put the loc.csv and clin_data_selected.csv in the ./data folder.')

    # 尝试读取 JSON 文件
    try:
        with open(get_file_path('data/vessel_measure.json'), 'r') as file:
            vessel_data_json = json.load(file)
    except FileNotFoundError:
        print('No data file found, please put the vessel_measure.json in the ./data folder.')

    ##############################################################################################################
    # Build the GUI
    ##############################################################################################################
    # The root window is the main GUI window
    root = tk.Tk()
    root.title("Slice based Data Visualization")

    root.grid_rowconfigure(2, weight=1) # make the canvas expand to fill the entire grid
    root.grid_columnconfigure(0, weight=1) # make the canvas expand to fill the entire grid

    # set the minimum size of the window
    root.minsize(MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT)

    # Create a frame for the comboboxes, patient count, and their labels
    top_left_frame = ttk.Frame(root)
    top_left_frame.grid(row=0, column=0, padx=10, pady=10)
    # Create a frame for the side selection, timepoint checkboxes, and their labels
    top_right_frame = ttk.Frame(root)
    top_right_frame.grid(row=0, column=1, padx=10, pady=10)

    filter_sid = ['Risk', 'Smoker', 'Diabetes', 'Stroke', 'Heart Attack']

    # filter_checkbox_frame = ttk.Frame(root)
    filter_checkbox_frame = ttk.Frame(top_right_frame)
    filter_checkbox_frame.grid(row=2, column=1, sticky='w', padx = 10)

    # Create a label for the filter checkboxes
    filter_checkbox_label = ttk.Label(top_right_frame, text=f"Filter by:")
    filter_checkbox_label.grid(row=2, column=0, padx=5, pady=5, sticky='e')

    # build the multi-select checkbox
    checkbox_var = {}

    ##############################################################################################################
    # Update the filtered patients when the checkboxes are clicked
    ##############################################################################################################
    def update_filtered_patients():
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
        # Get the number of filtered patients
        num_filtered_patients = len(patient_id_dropdown['values'])
        print(f'number of filtered patients: {num_filtered_patients}')
        # Update the num_patients_label
        # num_patients_label.config(text = f"Number of filtered patients: \t {num_filtered_patients} of {num_total_patients} total patients")
        num_patients_label_count.config(text = f"{num_filtered_patients} of {num_total_patients} total patients")

    ##############################################################################################################
    # Create the portion of the GUI for risk factor filters: ['Risk', 'Smoker', 'Diabetes', 'Stroke', 'Heart Attack']
    ##############################################################################################################
    # 创建并放置复选框
    # Create the checkboxes for ['Risk', 'Smoker', 'Diabetes', 'Stroke', 'Heart Attack']
    for i, value in enumerate(filter_sid):
        checkbox_var[value] = tk.IntVar()
        checkbox = ttk.Checkbutton(filter_checkbox_frame, text=value, variable=checkbox_var[value], command=update_filtered_patients)
        if (i < 4):
            checkbox.grid(row=3, column=i, sticky='w', padx = (0, 6))
        else:
            checkbox.grid(row=3, column=i, sticky='w', padx = (0, 12))

    ##############################################################################################################
    # Create the portion of the GUI for the patient ID selection
    ##############################################################################################################
    # Add a label for the patient id combobox
    patient_id_dropdown_label = ttk.Label(top_left_frame, text=f"Select a patient ID:")
    patient_id_dropdown_label.grid(row=1, column=0, padx=5, pady=5, sticky='e')
    
    # 创建Combobox
    # build the patient ID dropdown
    patient_id_dropdown = ttk.Combobox(top_left_frame, values=list(sid_filter['sid'].unique()))
    patient_id_dropdown.set(int(sid_filter['sid'].unique()[0]))
    # patient_id_dropdown.grid(row=1, column=0, padx=2, pady=2)
    patient_id_dropdown.grid(row=1, column=1, padx=5, pady=5)

    # Get the number of filtered patients. 
    num_total_patients = len(patient_id_dropdown['values'])
    print(f'number of total patients: {num_total_patients}')
    # Nothing is filtered yet, so this is the total number of patients
    num_filtered_patients = num_total_patients

    # Add a label that displays the number of patient ids that match the filter
    num_patients_label = ttk.Label(top_left_frame, text=f"Number of filtered patients:")
    num_patients_label.grid(row=0, column=0, padx=5, pady=(10, 5), sticky='w')
    num_patients_label_count = ttk.Label(top_left_frame, text=f"{num_filtered_patients} of {num_total_patients} total patients")
    num_patients_label_count.grid(row=0, column=1, padx=5, pady=(10, 5), sticky='e')

    ##############################################################################################################
    # Create the portion of the GUI for the measurement selection
    ##############################################################################################################
    # Add a label for the measurement type combobox
    which_measure_dropdown_label = ttk.Label(top_left_frame, text=f"Select a measurement:")
    which_measure_dropdown_label.grid(row=2, column=0, padx=5, pady=5, sticky='e')

    # build the which measure dropdown
    which_measure_dropdown = ttk.Combobox(top_left_frame, values=list(vessel_data_json.keys()), state='readonly')
    which_measure_dropdown.set(list(vessel_data_json.keys())[0])
    which_measure_dropdown.grid(row=2, column=1, padx=5, pady=5)

    ##############################################################################################################
    # Create the portion of the GUI for the time point selection
    ##############################################################################################################
    # Create a label for the time point selection checkboxes
    time_point_checkboxes_label = ttk.Label(top_right_frame, text=f"Select time points:")
    time_point_checkboxes_label.grid(row=1, column=0, padx=5, pady=5, sticky='e')

    # build the time point frame which is multi-select checkboxes
    time_point_checkboxes_frame = ttk.Frame(top_right_frame)
    time_point_checkboxes_frame.grid(row=1, column=1)
    time_point_checkboxes = {}

    ##############################################################################################################
    # Update the time point portion of the GUI based on patient and side selection
    ##############################################################################################################
    # dynamically update the time points when the patient ID is selected
    def update_time_points(*args):
        patient_id = patient_id_dropdown.get()
        side = side_var.get()
        available_time_points = data_loc[(data_loc['sid'] == int(patient_id)) &
                                            (data_loc['side'] == side)
                                        ]['tp'].unique()

        # clear the frame
        for widget in time_point_checkboxes_frame.winfo_children():
            widget.destroy()
        # check the old states of the checkboxes
        old_states = [tp for tp, var in time_point_checkboxes.items() if var.get()]
        time_point_checkboxes.clear()

        # create new checkboxes
        for tp in sorted(available_time_points):
            var = tk.BooleanVar(value = True if tp in old_states else False)
            cb = ttk.Checkbutton(time_point_checkboxes_frame, text=str(tp), variable=var)
            cb.pack(side=tk.LEFT, padx = 3)
            time_point_checkboxes[tp] = var
            var.trace_add('write', plot_data)

    # when the patient ID is selected, update the time points
    # patient_id_dropdown.bind('<<ComboboxSelected>>', update_time_points)

    ##############################################################################################################
    # Create the portions of the GUI for the side selection
    ##############################################################################################################
    side_selection_frame = ttk.Frame(top_right_frame)
    side_selection_frame.grid(row=0, column=1)
    # Create a label for the side selection radiobuttons
    side_var_label = ttk.Label(top_right_frame, text=f"Select a side:")
    side_var_label.grid(row=0, column=0, padx=5, pady=5, sticky='e')

    # build the side selection radiobuttons
    side_var = tk.StringVar(value='L')
    side_left = ttk.Radiobutton(side_selection_frame, text='Left', variable=side_var, value='L')
    side_right = ttk.Radiobutton(side_selection_frame, text='Right', variable=side_var, value='R')
    side_left.grid(row=0, column=0, padx = 3, pady = 3, sticky='w')
    side_right.grid(row=0, column=1, padx = 3, pady = 3, sticky='w')

    # side_var.trace_add('write', update_time_points)

    ##############################################################################################################
    # Plot the filtered data for the selected patient ID, side, and time points
    ##############################################################################################################
    # 绘图区域
    fig, ax = plt.subplots(figsize=(5, 3))
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.grid(row=2, column=0, columnspan=2, sticky='nsew') # use sticky to expand the canvas to fill the entire grid

    # 可视化函数
    def plot_data(*args):
        which_measure = vessel_data_json[which_measure_dropdown.get()]
        patient_id = patient_id_dropdown.get()
        side = side_var.get()
        selected_time_points = [tp for tp, var in time_point_checkboxes.items() if var.get()]

        ax.clear()
        color_map = plt.get_cmap('tab10')

        for i, tp in enumerate(selected_time_points):
            # filter data
            filtered_data = data_loc[(data_loc['sid'] == int(patient_id)) & 
                                    (data_loc['tp'] == int(tp)) & 
                                    (data_loc['side'] == side)]
            sorted_data = filtered_data.sort_values(by='loc')

            # A scatterplot and a line plot are created for each time point so that the points indicate actual values, but lines link the points for clarity
            ax.scatter(sorted_data['loc'], sorted_data[which_measure], color=color_map(i))
            ax.plot(sorted_data['loc'], sorted_data[which_measure], label=f'Time Point: {str(tp)}', color=color_map(i))


            # Calculate and plot the average value for all data at the current time point and side
            # Here is little redundant, but it is easy to implement
            all_data = data_loc[(data_loc['tp'] == int(0)) & (data_loc['side'] == side)]
            average_value = all_data.groupby('loc')[which_measure].mean()

            avg_values_to_plot = average_value.reindex(sorted_data['loc'])
            ax.plot(sorted_data['loc'], avg_values_to_plot, linestyle='--', color='grey')

        # It would be better to move the average calculation out of the loop. For some reason it relies on the filtered_data in the loop though...

        # # Calculate and plot the average value for all data at the current time point and side
        # # Here is little redundant, but it is easy to implement
        # all_data = data_loc[(data_loc['tp'] == int(0)) & (data_loc['side'] == side)]
        # average_value = all_data.groupby('loc')[which_measure].mean()

        # avg_values_to_plot = average_value.reindex(sorted_data['loc'])
        # ax.plot(sorted_data['loc'], avg_values_to_plot, linestyle='--', color='grey')

        ax.set_xlabel('Slice Number')
        ax.set_ylabel(which_measure_dropdown.get())
        ax.set_title(f'Patient: {patient_id}, Side: {side}')
        ax.legend()
        fig.tight_layout()
        canvas.draw()

    ##############################################################################################################
    # Update the time points and plot the data when the patient ID is selected
    ##############################################################################################################
    def on_patient_id_selected(event=None):
        # 先更新时间点
        update_time_points()
        # 然后绘图
        plot_data()

    update_time_points()
    # patient_id_dropdown.bind('<<ComboboxSelected>>', update_time_points)
    side_var.trace_add('write', update_time_points)

    plot_data()
    # patient_id_dropdown.bind('<<ComboboxSelected>>', plot_data)
    
    ##############################################################################################################
    # Bind the data
    ##############################################################################################################
    patient_id_dropdown.bind('<<ComboboxSelected>>', on_patient_id_selected)
    which_measure_dropdown.bind('<<ComboboxSelected>>', plot_data)
    side_var.trace_add('write', plot_data)

    ##############################################################################################################
    # Create a popup window to display patient information
    ##############################################################################################################
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
            print('No data file found, please put the clin_data.csv in the ./data folder')
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

    ##############################################################################################################
    # Run the main loop
    ##############################################################################################################
    root.mainloop()


if __name__ == '__main__':
    main()