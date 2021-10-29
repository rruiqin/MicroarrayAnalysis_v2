# Import packages
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import numpy as np
import pandas as pd

# Variables
open_next = []
initiate_analysis = []
user_message = "The analysis process can take up to a few minutes. User will be notified if an error occurs. Note that some output files could still be generated in the case of an error."

# Functions
def replist(input_list, n_reps):
    #n_reps: times each element in the list is repeated
    return [item for item in input_list for i in range(n_reps)]

def choosefile(store_dict, return_key, text, multiple):
    store_dict[return_key] = tk.filedialog.askopenfilename(filetypes = [("TXT", ".txt")], multiple = multiple)
    if type(store_dict[return_key]) == type((0,1)):
        show_text = str(len(store_dict[return_key])) + " file(s) chosen"
        text.set(show_text)
    elif type(store_dict[return_key]) == type("0") and len(store_dict[return_key])>1:
        show_text = "1 file(s) chosen"
        text.set(show_text)

def choosedirectory(store_dict, return_key, text):
    store_dict[return_key] = tk.filedialog.askdirectory()
    if len(store_dict[return_key]) > 1:
        text.set("1 folder chosen")

def compute_grubbs(x, channel, signal_col):
    if x["STD "+channel] == 0:
        return 0
    else:
        return abs(x[signal_col] - x["Mean "+channel])/x["STD "+channel]

def grubbs_check(x, channel, cutoff):
    if (x["Gval "+channel+" max"] == x["Gval "+channel] and x["Gval "+channel+" max"] > cutoff):
        return False
    else:
        return True


# Define a TkOptions class for creating multiple windows
class TkOptions():
    def __init__(self, max_column, divider_length, title):
        self.root = tk.Tk()
        self.root.title(title)
        self.column_max = max_column
        self.divider_len = divider_length     
        self.current_row = iter(range(100))
        self.param_dict = {}
    
    def info(self, info_text):
        tk.Label(self.root, text = info_text, justify = tk.LEFT).grid(row=next(self.current_row), sticky = tk.W)

    def divider(self):
        tk.Label(self.root, text = replist("*", self.divider_len)).grid(row=next(self.current_row), column = 0, columnspan = self.column_max, sticky = tk.W)
    
    def btn_choosefile(self, return_key, btn_text, multiple):
        row_num_temp = next(self.current_row)
        self.param_dict[return_key] = tk.StringVar()
        label_text_var = tk.StringVar()
        label_text_var.set('No file chosen...')
        tk.Button(self.root, text = btn_text, command = lambda: choosefile(self.param_dict, return_key, label_text_var, multiple=multiple)).grid(row=row_num_temp, column = 0, sticky = tk.NSEW)
        tk.Label(self.root, textvariable = label_text_var).grid(row=row_num_temp, column = 1, sticky = tk.NSEW)
    
    def btn_choosedir(self, return_key, btn_text):
        row_num_temp = next(self.current_row)
        label_text_var = tk.StringVar()
        label_text_var.set('No directory chosen...')
        tk.Button(self.root, text = btn_text, command = lambda: choosedirectory(self.param_dict, return_key, label_text_var)).grid(row=row_num_temp, column = 0, sticky = tk.NSEW)
        tk.Label(self.root, textvariable = label_text_var).grid(row=row_num_temp, column = 1, sticky = tk.NSEW)

    def btn(self, btn_text, btn_command):
        tk.Button(self.root, text = btn_text, command = btn_command).grid(row=next(self.current_row), column = 0, sticky = tk.NSEW)

    def radiobtn(self, return_key, rbtn_text, same_row):
        self.param_dict[return_key] = tk.IntVar()
        self.param_dict[return_key].set(0)
        if same_row:
            row_num_temp = next(self.current_row)
            for i in range(len(rbtn_text)):
                tk.Radiobutton(self.root, text = rbtn_text[i], value = i, variable = self.param_dict[return_key]).grid(row=row_num_temp, column = i, sticky = tk.W)
        else:
             for i in range(len(rbtn_text)):
                tk.Radiobutton(self.root, text = rbtn_text[i], value = i, variable = self.param_dict[return_key]).grid(row=next(self.current_row), columnspan = self.column_max, sticky = tk.W)           

    
    def entry_w_label(self, return_key, label_text, default_value, num_type):
        row_num_temp = next(self.current_row)
        tk.Label(self.root, text = label_text).grid(row=row_num_temp, column = 0, sticky = tk.W)
        if num_type == "int":
            self.param_dict[return_key] = tk.IntVar()
        else:
            self.param_dict[return_key] = tk.DoubleVar()
        self.param_dict[return_key].set(default_value)
        entry_temp = tk.Entry(self.root, textvariable=self.param_dict[return_key])
        entry_temp.grid(row=row_num_temp, column = 1, sticky = tk.W)
    
    def close(self, show_message, message_title, message, return_true):
        return_true.append(True)
        if show_message:
            tk.messagebox.showinfo(title = message_title, message = message)
        self.root.destroy()
    
    def __mainloop__(self):
        self.root.mainloop()

# Create a window for users to choose color mode (single color or dual color)
Root0 = TkOptions(max_column=2, divider_length=60, title="Genepix Microarray Data Analysis  - Version 2021.Sep.05")
Root0.divider()
Root0.info("Color mode")
Root0.radiobtn("Mode", ["Single color", "Dual color"], True)
Root0.divider()
Root0.btn("Confirm", lambda: Root0.close(False, 0, 0, open_next))
Root0.__mainloop__()
color_mode = int(Root0.param_dict["Mode"].get())

# Create the main window for users to define parameters for analysis
if open_next[0] and color_mode == 0:

    Root = TkOptions(max_column=4, divider_length=80, title="Genepix Microarray Data Analysis  - Version 2021.Sep.05 - Single Color")
    Root.info("Author: Rui (Ric) Qin; rq2@ualberta.ca")
    Root.divider()
    Root.info("Fluorescence channel of samples")
    Root.radiobtn("Sample channel", ["488nm", "532nm", "594nm", "635nm"], True)
    Root.divider()
    Root.btn_choosefile("Raw data files", "Choose raw input data file(s)", True)
    Root.btn_choosefile("Sample lists", "Choose sample list file(s)", True)
    Root.btn_choosefile("Probe list", "Choose probe list file(s)", False)
    Root.btn_choosedir("Output directory", "Choose output folder")
    Root.divider()
    Root.entry_w_label("Probe replicates", "Number of probe replicates per array", 3, "int")
    Root.entry_w_label("Grubbs cutoff", "Cut-off value for Grubbs test", 1.15, "double")
    Root.divider()
    Root.info("Type of intensity data to be used for analysis")
    Root.radiobtn("Intensity type", ["Median intensity value", "Mean intensity value"], True)
    Root.divider()
    Root.btn("Run Analysis", lambda: Root.close(True, "Message", user_message, initiate_analysis))
    Root.__mainloop__()

if open_next[0] and color_mode == 1:

    array_normalization_method = ["For each array, normalize the intensity of every spot to the median intensity of all spots in the corresponding channel", "For each array, normalize the intensity of every spot to the mean intensity of all spots in the corresponding channel", "For each array, normalize the ratio of every spot to the median of the ratios of all spots", "For each array, normalize the ratio of every spot to the mean of the ratios of all spots", "Do not normalize"]

    Root = TkOptions(max_column=4, divider_length=80, title="Genepix Microarray Data Analysis  - Version 2021.Sep.05 - Dual Color")
    Root.info("Author: Rui (Ric) Qin; rq2@ualberta.ca")
    Root.divider()
    Root.info("Fluorescence channel of samples")
    Root.radiobtn("Sample channel", ["488nm", "532nm", "594nm", "635nm"], True)
    Root.info("Fluorescence channel of reference materials")
    Root.radiobtn("Reference channel", ["488nm", "532nm", "594nm", "635nm"], True)
    Root.divider()
    Root.btn_choosefile("Raw data files", "Choose raw input data file(s)", True)
    Root.btn_choosefile("Sample lists", "Choose sample list file(s)", True)
    Root.btn_choosefile("Probe list", "Choose probe list file(s)", False)
    Root.btn_choosedir("Output directory", "Choose output folder")
    Root.divider()
    Root.entry_w_label("Probe replicates", "Number of probe replicates per array", 3, "int")
    Root.entry_w_label("Grubbs cutoff", "Cut-off value for Grubbs test", 1.15, "double")
    Root.divider()
    Root.info("Type of signal cutoffs")
    Root.radiobtn("Signal cutoff type", ["Conventional SNR", "SNR computed by Genepix", "Intensity (including background)"], True)
    Root.entry_w_label("Sample signal cutoff", "Signal cut-off for the sample channel", 3, "double")
    Root.entry_w_label("Reference signal cutoff", "Signal cut-off for the reference channel", 3, "double")
    Root.entry_w_label("Sample pt cutoff", "Percentage sample cutoff (between 0 and 1)", 0.5, "double")
    Root.divider()
    Root.info("Type of intensity data to be used for analysis")
    Root.radiobtn("Intensity type", ["Median intensity value", "Mean intensity value"], True)
    Root.divider()
    Root.info("Array normalization method")
    Root.radiobtn("Array normalization method", array_normalization_method, False)
    Root.divider()
    Root.btn("Run Analysis", lambda: Root.close(True, "Message", user_message, initiate_analysis))
    Root.__mainloop__()

# Pass parameters to a new dictionary
# The parameter dictionary could have the following items: 
# 'Sample channel','Reference channel','Raw data files','Sample lists','Probe list','Output directory','Probe replicates','Grubbs cutoff','Signal cutoff type','Sample signal cutoff','Reference signal cutoff','Sample pt cutoff','Intensity type','Array normalization method'
param_dict = {}
for i in Root.param_dict.keys():
    try:
        param_dict[i] = Root.param_dict[i].get()
    except:
        param_dict[i] = Root.param_dict[i]

if initiate_analysis[0]:
    try:
        # Single color data processing
        if color_mode == 0:
            # Get all parameters
            channel_dict = {0:"488", 1:"532", 2:"594", 3:"635"}
            channel = channel_dict[param_dict['Sample channel']]

            intensity_type_dict = {0: "Median", 1: "Mean"}
            intensity_type = intensity_type_dict[param_dict['Intensity type']]

            probe_list = pd.read_csv(param_dict['Probe list'])
            probe_list_list = probe_list.iloc[:,0].tolist()

            if type(param_dict['Raw data files']) == type((0,1)):
                raw_file_list = list(param_dict['Raw data files'])
            elif type(param_dict['Raw data files']) == type("0") and len(param_dict['Raw data files'])>1:
                raw_file_list = []
                raw_file_list.append(param_dict['Raw data files'])
            
            if type(param_dict['Sample lists']) == type((0,1)):
                sample_file_list = list(param_dict['Sample lists'])
            elif type(param_dict['Sample lists']) == type("0") and len(param_dict['Sample lists'])>1:
                sample_file_list = []
                sample_file_list.append(param_dict['Sample lists'])
            
            n_reps = param_dict['Probe replicates']
            grubbs_cutoff = param_dict['Grubbs cutoff']
            output_dir = param_dict['Output directory']

            n_probes = probe_list.iloc[:,0].count()
            n_slides = len(raw_file_list)

            #extract_columns: e.g. if channel is 635nm, extract ["Block", "Column", "Flags", "F635 Median", "F635 Median - B635", "SNR 635", "B635"] (7 columns)
            signal_colname = "F"+channel+" "+intensity_type+" - B"+channel
            extract_columns = ["Block", "Column", "Flags", "F"+channel+" "+intensity_type, signal_colname, "SNR "+channel, "B"+channel]

            ###########
            ###########Step 1: annotate each raw input file and combine them
            ###########
            for i in range(n_slides):
                ##Read raw input file and sample list, one slide at a time
                raw_file_path = raw_file_list[i]
                sample_file_path = sample_file_list[i]

                raw_data_input = pd.read_csv(raw_file_path, delimiter = "\t", skiprows = 32, na_values = "Error")
                sample_list = pd.read_csv(sample_file_path)

                ##Slide-specific parameters
                n_rows = raw_data_input["Row"].max()
                n_cols = raw_data_input["Column"].max()
                n_samples_i = sample_list.iloc[:,0].count()

                #Select the columns of interest from the raw_input dataframe
                raw_input_coi = raw_data_input.loc[:,extract_columns]

                #generate a list of probes, each probe repeated n_reps times in each block
                probe_list_rep = (replist(probe_list_list, n_reps))*n_samples_i
                probe_list_rep_df = pd.DataFrame(probe_list_rep)
                probe_list_rep_df.columns = ["Probe"]

                #generate a list of samples, each probe repeated n_rows*n_cols times in each block
                sample_list_list = sample_list.iloc[:,0].tolist()
                sample_list_rep = replist(sample_list_list,n_rows*n_cols)
                sample_list_rep_df = pd.DataFrame(sample_list_rep)
                sample_list_rep_df.columns = ["Sample"]
                
                if i == 0:
                    sample_list_all = sample_list_list
                else:
                    sample_list_all.extend(sample_list_list)

                raw_data_anno = pd.concat([probe_list_rep_df, sample_list_rep_df, raw_data_input], axis = 1) #axis = 1: join horizontally        

                if i == 0:
                    raw_data_anno_combined = raw_data_anno
                else:
                    raw_data_anno_combined = pd.concat([raw_data_anno_combined, raw_data_anno], axis = 0) #axis = 0: join vertically

            n_samples = len(sample_list_all)
            raw_data_anno_combined.reset_index(drop = True, inplace = True)

            ###########
            ########### Step 2: Grubbs' test
            ###########
            data_step2_grouped = raw_data_anno_combined.groupby(by = ["Sample", "Probe"], sort = False)

            Grubbs_mean = data_step2_grouped.mean()[[signal_colname]] 
            Grubbs_mean_list = Grubbs_mean.iloc[:,0].tolist()
            Grubbs_mean_rep = replist(Grubbs_mean_list,3)
            Grubbs_mean_rep_df = pd.DataFrame(Grubbs_mean_rep)
            Grubbs_mean_rep_df.columns = ["Mean "+channel]

            Grubbs_std = data_step2_grouped.std()[[signal_colname]] 
            Grubbs_std_list = Grubbs_std.iloc[:,0].tolist()
            Grubbs_std_rep = replist(Grubbs_std_list,3)
            Grubbs_std_rep_df = pd.DataFrame(Grubbs_std_rep)
            Grubbs_std_rep_df.columns = ["STD "+channel]

            raw_data_anno_combined_Grubbs = pd.concat([raw_data_anno_combined, Grubbs_mean_rep_df, Grubbs_std_rep_df], axis = 1)

            raw_data_anno_combined_Grubbs["Gval "+channel] = raw_data_anno_combined_Grubbs.apply(compute_grubbs, channel = channel, signal_col = signal_colname, axis = 1)

            data_step2_grouped_2 = raw_data_anno_combined_Grubbs.groupby(by = ["Sample", "Probe"], sort = False)

            Grubbs_max = data_step2_grouped_2.max()[["Gval "+channel]]
            Grubbs_max_list = Grubbs_max.iloc[:,0].tolist()
            Grubbs_max_rep = replist(Grubbs_max_list,3)
            Grubbs_max_rep_df = pd.DataFrame(Grubbs_max_rep)
            Grubbs_max_rep_df.columns = ["Gval "+channel+" max"]

            raw_data_anno_combined_Grubbs = pd.concat([raw_data_anno_combined_Grubbs, Grubbs_max_rep_df], axis = 1)
            raw_data_anno_combined_Grubbs["Grubbs_passed"] = raw_data_anno_combined_Grubbs.apply(grubbs_check, channel=channel, cutoff=grubbs_cutoff, axis = 1)

            raw_data_anno_combined_Grubbs.to_csv(output_dir + "/data_raw_annotated.txt", index = False, sep='\t')
            data_step2 = raw_data_anno_combined_Grubbs[raw_data_anno_combined_Grubbs["Grubbs_passed"]]
            data_step2.reset_index(drop = True, inplace = True)

            ###########
            ########### Step 3: Construct a final dataframe and write to file
            ###########
            data_step3_grouped = data_step2.groupby(by = ["Sample", "Probe"], sort = False)
            data_step3 = data_step3_grouped.mean()[signal_colname]
            data_step3 = pd.DataFrame(np.array(data_step3).reshape((n_samples, n_probes)))
            data_step3_int = pd.DataFrame(np.rint(data_step3))

            data_step3_int.columns = probe_list_list
            data_step3_int.index = sample_list_all
            data_step3_int = data_step3_int.transpose()
            data_step3_int.to_csv(output_dir + "/data_final.txt", index = True, sep = "\t")
            tk.messagebox.showinfo(title = "Message", message = "The analysis is finished.\nPlease find the output files in the designated folder.")

        # Dual color data processing
        if color_mode == 1:
            # Get all parameters
            channel_dict = {0:"488", 1:"532", 2:"594", 3:"635"}
            channel_s = channel_dict[param_dict['Sample channel']]
            channel_r = channel_dict[param_dict['Reference channel']]

            intensity_type_dict = {0: "Median", 1: "Mean"}
            intensity_type = intensity_type_dict[param_dict['Intensity type']]

            probe_list = pd.read_csv(param_dict['Probe list'])
            probe_list_list = probe_list.iloc[:,0].tolist()

            if type(param_dict['Raw data files']) == type((0,1)):
                raw_file_list = list(param_dict['Raw data files'])
            elif type(param_dict['Raw data files']) == type("0") and len(param_dict['Raw data files'])>1:
                raw_file_list = []
                raw_file_list.append(param_dict['Raw data files'])
            
            if type(param_dict['Sample lists']) == type((0,1)):
                sample_file_list = list(param_dict['Sample lists'])
            elif type(param_dict['Sample lists']) == type("0") and len(param_dict['Sample lists'])>1:
                sample_file_list = []
                sample_file_list.append(param_dict['Sample lists'])
            
            n_reps = param_dict['Probe replicates']
            grubbs_cutoff = param_dict['Grubbs cutoff']
            signal_cutoff_type = param_dict['Signal cutoff type']
            signal_cutoff_s = param_dict['Sample signal cutoff']
            signal_cutoff_r = param_dict['Reference signal cutoff']
            pt_cutoff = param_dict['Sample pt cutoff']
            norm_method = param_dict['Array normalization method']
            output_dir = param_dict['Output directory']

            n_probes = probe_list.iloc[:,0].count()
            n_slides = len(raw_file_list)

            #extract_columns
            signal_colname_s = "F"+channel_s+" "+intensity_type+" - B"+channel_s
            signal_colname_r = "F"+channel_r+" "+intensity_type+" - B"+channel_r
            extract_columns = ["Block", "Column", "Flags", "F"+channel_s+" "+intensity_type, signal_colname_s, "SNR "+channel_s, "B"+channel_s, "F"+channel_r+" "+intensity_type, signal_colname_r, "SNR "+channel_r, "B"+channel_r]

            ###########
            ###########Step 1: annotate each raw input file and combine them
            ###########
            for i in range(n_slides):
                ##Read raw input file and sample list, one slide at a time
                raw_file_path = raw_file_list[i]
                sample_file_path = sample_file_list[i]

                raw_data_input = pd.read_csv(raw_file_path, delimiter = "\t", skiprows = 32, na_values = "Error")
                sample_list = pd.read_csv(sample_file_path)

                ##Slide-specific parameters
                n_rows = raw_data_input["Row"].max()
                n_cols = raw_data_input["Column"].max()
                n_samples_i = sample_list.iloc[:,0].count()

                #select the columns of interest from the raw_input dataframe
                raw_input_coi = raw_data_input.loc[:,extract_columns]

                #generate a list of probes, each probe repeated n_reps times in each block
                probe_list_rep = (replist(probe_list_list, n_reps))*n_samples_i
                probe_list_rep_df = pd.DataFrame(probe_list_rep)
                probe_list_rep_df.columns = ["Probe"]

                #generate a list of samples, each probe repeated n_rows*n_cols times in each block
                sample_list_list = sample_list.iloc[:,0].tolist()
                sample_list_rep = replist(sample_list_list,n_rows*n_cols)
                sample_list_rep_df = pd.DataFrame(sample_list_rep)
                sample_list_rep_df.columns = ["Sample"]
                
                if i == 0:
                    sample_list_all = sample_list_list
                else:
                    sample_list_all.extend(sample_list_list)

                raw_data_anno = pd.concat([probe_list_rep_df, sample_list_rep_df, raw_data_input], axis = 1) #axis = 1: join horizontally        

                if i == 0:
                    raw_data_anno_combined = raw_data_anno
                else:
                    raw_data_anno_combined = pd.concat([raw_data_anno_combined, raw_data_anno], axis = 0) #axis = 0: join vertically

            n_samples = len(sample_list_all)
            raw_data_anno_combined.reset_index(drop = True, inplace = True)


            ###########
            ###########Step 2: Grubbs' test
            ###########
            data_step2_grouped = raw_data_anno_combined.groupby(by = ["Sample", "Probe"], sort = False)

            Grubbs_mean = data_step2_grouped.mean()[[signal_colname_s]] 
            Grubbs_mean_list = Grubbs_mean.iloc[:,0].tolist()
            Grubbs_mean_rep = replist(Grubbs_mean_list,3)
            Grubbs_mean_rep_df = pd.DataFrame(Grubbs_mean_rep)
            Grubbs_mean_rep_df.columns = ["Mean "+channel_s]

            Grubbs_std = data_step2_grouped.std()[[signal_colname_s]] 
            Grubbs_std_list = Grubbs_std.iloc[:,0].tolist()
            Grubbs_std_rep = replist(Grubbs_std_list,3)
            Grubbs_std_rep_df = pd.DataFrame(Grubbs_std_rep)
            Grubbs_std_rep_df.columns = ["STD "+channel_s]

            raw_data_anno_combined_Grubbs = pd.concat([raw_data_anno_combined, Grubbs_mean_rep_df, Grubbs_std_rep_df], axis = 1)

            Grubbs_mean = data_step2_grouped.mean()[[signal_colname_r]] 
            Grubbs_mean_list = Grubbs_mean.iloc[:,0].tolist()
            Grubbs_mean_rep = replist(Grubbs_mean_list,3)
            Grubbs_mean_rep_df = pd.DataFrame(Grubbs_mean_rep)
            Grubbs_mean_rep_df.columns = ["Mean "+channel_r]

            Grubbs_std = data_step2_grouped.std()[[signal_colname_r]] 
            Grubbs_std_list = Grubbs_std.iloc[:,0].tolist()
            Grubbs_std_rep = replist(Grubbs_std_list,3)
            Grubbs_std_rep_df = pd.DataFrame(Grubbs_std_rep)
            Grubbs_std_rep_df.columns = ["STD "+channel_r]

            raw_data_anno_combined_Grubbs = pd.concat([raw_data_anno_combined_Grubbs, Grubbs_mean_rep_df, Grubbs_std_rep_df], axis = 1)

            raw_data_anno_combined_Grubbs["Gval "+channel_s] = raw_data_anno_combined_Grubbs.apply(compute_grubbs, channel = channel_s, signal_col = signal_colname_s, axis = 1)
            raw_data_anno_combined_Grubbs["Gval "+channel_r] = raw_data_anno_combined_Grubbs.apply(compute_grubbs, channel = channel_r, signal_col = signal_colname_r, axis = 1)

            data_step2_grouped_2 = raw_data_anno_combined_Grubbs.groupby(by = ["Sample", "Probe"], sort = False)

            Grubbs_max = data_step2_grouped_2.max()[["Gval "+channel_s]]
            Grubbs_max_list = Grubbs_max.iloc[:,0].tolist()
            Grubbs_max_rep = replist(Grubbs_max_list,3)
            Grubbs_max_rep_df = pd.DataFrame(Grubbs_max_rep)
            Grubbs_max_rep_df.columns = ["Gval "+channel_s+" max"]

            raw_data_anno_combined_Grubbs = pd.concat([raw_data_anno_combined_Grubbs, Grubbs_max_rep_df], axis = 1)
            raw_data_anno_combined_Grubbs["Grubbs Result "+channel_s] = raw_data_anno_combined_Grubbs.apply(grubbs_check, channel=channel_s, cutoff=grubbs_cutoff, axis = 1)

            Grubbs_max = data_step2_grouped_2.max()[["Gval "+channel_r]]
            Grubbs_max_list = Grubbs_max.iloc[:,0].tolist()
            Grubbs_max_rep = replist(Grubbs_max_list,3)
            Grubbs_max_rep_df = pd.DataFrame(Grubbs_max_rep)
            Grubbs_max_rep_df.columns = ["Gval "+channel_r+" max"]

            raw_data_anno_combined_Grubbs = pd.concat([raw_data_anno_combined_Grubbs, Grubbs_max_rep_df], axis = 1)
            raw_data_anno_combined_Grubbs["Grubbs Result "+channel_r] = raw_data_anno_combined_Grubbs.apply(grubbs_check, channel=channel_r, cutoff=grubbs_cutoff, axis = 1)

            # A spot passes this test if at least one channel has a grubbs statistics less than cutoff
            raw_data_anno_combined_Grubbs["Grubbs_passed"] = np.logical_or(raw_data_anno_combined_Grubbs["Grubbs Result "+channel_s], raw_data_anno_combined_Grubbs["Grubbs Result "+channel_r])
            raw_data_anno_combined_Grubbs.to_csv(output_dir + "/data_raw_annotated.txt", index = False, sep='\t')
            data_step2 = raw_data_anno_combined_Grubbs[raw_data_anno_combined_Grubbs["Grubbs_passed"]]
            data_step2.reset_index(drop = True, inplace = True)

            ###########
            ###########Step 3: SNR annotation
            ###########
            data_step3 = data_step2.copy()

            if signal_cutoff_type == 0:
                data_step3["SC "+channel_s] = data_step3["F"+channel_s+" "+intensity_type]/data_step3["B"+channel_s]
                data_step3["SC "+channel_r] = data_step3["F"+channel_r+" "+intensity_type]/data_step3["B"+channel_r]
            elif signal_cutoff_type == 1:
                data_step3["SC "+channel_s] = data_step3["SNR "+channel_s]
                data_step3["SC "+channel_r] = data_step3["SNR "+channel_r]
            else:
                data_step3["SC "+channel_s] = data_step3["F"+channel_s+" "+intensity_type]
                data_step3["SC "+channel_r] = data_step3["F"+channel_r+" "+intensity_type]

            data_step3_grouped = data_step3.groupby(by = ["Sample", "Probe"], sort = False)

            SC_mean_s = data_step3_grouped.mean()["SC "+channel_s].tolist()
            SC_count_s = data_step3_grouped.count()["SC "+channel_s].tolist()
            SC_mean_r = data_step3_grouped.mean()["SC "+channel_r].tolist()
            SC_count_r = data_step3_grouped.count()["SC "+channel_r].tolist()

            SC_mean_s_rep = []
            for i in range(len(SC_count_s)):
                SC_mean_s_temp = [SC_mean_s[i]]*int(SC_count_s[i])
                SC_mean_s_rep.extend(SC_mean_s_temp)
            SC_mean_s_rep_df = pd.DataFrame(SC_mean_s_rep)
            SC_mean_s_rep_df.columns = ["SC "+channel_s+" Mean"]

            SC_mean_r_rep = []
            for i in range(len(SC_count_r)):
                SC_mean_r_temp = [SC_mean_r[i]]*int(SC_count_r[i])
                SC_mean_r_rep.extend(SC_mean_r_temp)
            SC_mean_r_rep_df = pd.DataFrame(SC_mean_r_rep)
            SC_mean_r_rep_df.columns = ["SC "+channel_r+" Mean"]

            SC_count_rep = []
            for i in range(len(SC_count_r)):
                SC_count_temp = [SC_count_r[i]]*int(SC_count_r[i])
                SC_count_rep.extend(SC_count_temp)
            SC_count_rep_df = pd.DataFrame(SC_count_rep)
            SC_count_rep_df.columns = ["Count"]

            data_step3 = pd.concat([data_step3, SC_mean_s_rep_df, SC_mean_r_rep_df, SC_count_rep_df], axis = 1)
            data_step3["SC Result"] = data_step3.apply(lambda x: 1/x["Count"] if (x["SC "+channel_s+" Mean"] >= signal_cutoff_s and x["SC "+channel_r+" Mean"] >= signal_cutoff_r) else 0, axis = 1)


            ###########
            ###########Step 4: Remove probes
            ###########
            data_step4_grouped = data_step3.groupby(by = ["Sample", "Probe"], sort = False)
            SNR_result = np.array(data_step4_grouped.sum()["SC Result"].tolist()).reshape((n_samples, n_probes))
            SNR_final_count = SNR_result.sum(axis = 0).flatten().tolist()

            probe_failed = [probe_list_list[i] for i in range(n_probes) if SNR_final_count[i] < (pt_cutoff * n_samples)] #List comprehension
            probe_passed = [i for i in probe_list_list if i not in probe_failed]

            SC_filter = ~data_step3.Probe.isin(probe_failed)

            data_step4 = data_step3[SC_filter]
            data_step4.reset_index(drop = True, inplace = True)

            ###########
            ###########Step 5: Centering and compute ratios
            ###########

            data_step5 = data_step4.loc[:,["Sample", "Probe", signal_colname_s, signal_colname_r]]
            data_step5["Ratio not normalized"] = pd.DataFrame(data_step5[signal_colname_s] / data_step5[signal_colname_r])

            data_step5_grouped = data_step5.groupby(by = "Sample", sort = False)
            probe_pass_count = data_step5_grouped.count()["Probe"].tolist()

            def array_norm(input_df, output_df, col_s, col_r, method):
                if method == "median":
                    calibrator_s = input_df.median()[col_s].tolist()
                    calibrator_r = input_df.median()[col_r].tolist()
                elif method == "mean":
                    calibrator_s = input_df.mean()[col_s].tolist()
                    calibrator_r = input_df.mean()[col_r].tolist()
            
                calibrator_s_rep = []
                for i in range(n_samples):
                    calibrator_s_temp = [calibrator_s[i]]*int(probe_pass_count[i])
                    calibrator_s_rep.extend(calibrator_s_temp)
                output_df["Calibrator "+channel_s] = calibrator_s_rep
                
                calibrator_r_rep = []
                for i in range(n_samples):
                    calibrator_r_temp = [calibrator_r[i]]*int(probe_pass_count[i])
                    calibrator_r_rep.extend(calibrator_r_temp)
                output_df["Calibrator "+channel_r] = calibrator_r_rep
            
            if norm_method == 0:
                array_norm(data_step5_grouped, data_step5, signal_colname_s, signal_colname_r, "median")
            elif norm_method == 1:
                array_norm(data_step5_grouped, data_step5, signal_colname_s, signal_colname_r, "mean")
            elif norm_method == 2:
                array_norm(data_step5_grouped, data_step5, "Ratio not normalized", "Ratio not normalized", "median")
            elif norm_method == 3:
                array_norm(data_step5_grouped, data_step5, "Ratio not normalized", "Ratio not normalized", "mean")

            if norm_method <=1:
                data_step5["Normalized Ratio"] = (data_step5[signal_colname_s] / data_step5["Calibrator "+channel_s]) / (data_step5[signal_colname_r] / data_step5["Calibrator "+channel_r])
            elif norm_method <=3:
                data_step5["Normalized Ratio"] = data_step5["Ratio not normalized"] / data_step5["Calibrator "+channel_s]
            else:
                data_step5["Normalized Ratio"] = data_step5["Ratio not normalized"]


            ###########
            ###########Step 6: Construct a final dataframe and write to file
            ###########
            data_step6_grouped = data_step5.groupby(by = ["Sample", "Probe"], sort = False)
            data_step6 = data_step6_grouped.mean()["Normalized Ratio"]
            data_step6 = pd.DataFrame(np.array(data_step6).reshape((n_samples, len(probe_passed))))
            data_step6_log2 = pd.DataFrame(np.log2(data_step6))

            data_step6_log2.columns = probe_passed
            data_step6_log2.index = sample_list_all
            data_step6_log2 = data_step6_log2.transpose()
            data_step6_log2.to_csv(output_dir + "/data_final.txt", index = True, sep = "\t")
            
            tk.messagebox.showinfo(title = "Message", message = "The analysis is finished.\nPlease find the output files in the designated folder.")
            print(param_dict)
    except Exception as e:
        tk.messagebox.showinfo(title = "Message", message = "An error occured.")
        print(e)
