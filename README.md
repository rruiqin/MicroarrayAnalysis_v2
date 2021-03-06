# MicroarrayAnalysis_v2
A new version of the program to convert raw fluorescence data generated by Genepix™ microarray scanner to to expression data.

- This program is initially designed for lectin microarray analysis (dual color and single color) but it is also applicable to the microarrays.

- This program is integrated with a GUI (tkinter).

- User can initiate the program by running the python file (.py) in an IDE on a machine with python 3.6 or above installed. 

- For users who do not wish to install python or IDE, a convenient, user-friendly version (for 64 bit windows only) is also provided (Microarray Analysis_Sep2021_win64.zip). See part III for instructions.


  Changes in this version compared the last version:
  
  - Now users can select fluorescence channels (available options: 635nm, 594nm, 532nm, 488nm)
  - Now includes "conventional SNR" and "absolute intensity" options for signal cutoffs for more versatile analysis
  - More infomation included in the output annotated raw file.
  - Improved GUI


## I. Description of the data analysis workflow

  #### 1. Graphic description of the analysis process

  ![image](https://user-images.githubusercontent.com/79244493/124423871-3eac3880-dd23-11eb-819e-79d41e2c1162.png) 

  ![image](https://user-images.githubusercontent.com/79244493/124423906-4d92eb00-dd23-11eb-881b-290c5fcd89f1.png)


  #### 2. Output files

        (1) Dual color mode

        •	A tab delimited text file containing the annotated raw data.

        •	A tab delimited text file containing the unadjusted/adjusted average ratios of each lectin for each sample.

        (2) Single color mode

        •	A tab delimited text file containing the annotated raw data.

        •	A tab delimited text file containing the average fluorescence values of each lectin for each sample.



## II. Input files

  #### 1. Raw data file(s)

        •	The files must be .txt files (the default output file format in Genepix).

        •	The program extracts data from the columns with the following names (case sensitive, note the spaces, columns names separated by comma) for calculation. Here only shows the columns when 635nm channel is used.

        Block, Column, F635 Median, F635 Median - B635, SNR 635, F635 Median, F635 Mean

        Making sure the names of these columns are correct is critical. 


  #### 2. Sample list file(s)

        •	The files must be .txt files (the default output file format in Genepix) or .csv files.

        •	The program ignores the first row of each sample list file. Therefore, the first row of each sample file can be basically any text (e.g., “sample”, “sample ID”)

        •	The number of samples in each sample list must match the corresponding raw data file.


  #### 3. Lectin list file

        •	Only one file can be selected at a time.

        •	The file must be .txt file (the default output file format in Genepix) or .csv file.

        •	The program ignores the first row of the lectin list file. Therefore, the first row of the lectin list file can be basically any text (e.g., “lectin”, “lectin or antibody”)

        •	The number of lectins (including the spots with no probes) must match the corresponding raw data files.

        •	Important: this program assumes that starting from spot one, all replicates of a probe are next to each other in the raw data files.


 #### 4. Multiple input files

        •	Multiple raw data files and sample list files can be selected at a time; the number of raw data files must be the same as the number of sample list  files.

        •	Users cannot select raw data files in different folders. This is also true when selecting sample list files.

        •	The raw data files are first sorted by FILE PATHS. Same for sample list files. Then the raw data files and sample list files are matched based on their position in the sorted queues.



## III. How to use

#### If user is running the .py file (Lectin array data analysis with GUI - 2021Mar05.py) in an IDE
  
  1. Make sure required packages are installed: tkinter, numpy, pandas
  
  2. Run the script. A user interface should appear on the screen.

  3. Select input files, options and enter parameters using the user interface.

    •	Number of replicates of lectins per array must be a positive integer

    •	Grubbs’ test cut-off must be a positive real number

    •	SNR cut-offs must be positive real numbers

    •	Percentage sample cut-off must be a real number between 0 and 1

  4. Run analysis.
   
  
#### If user is using the user-friendly version (Microarray Analysis_verMar2021_win64.zip)
  
  1. Unzip the file.
  
  2. In the unzipped folder, find "Run analysis.bat" and open this file.
  
  3. If a user interface appears on the screen, select input files, options and enter parameters:

    •	Number of replicates of lectins per array must be a positive integer

    •	Grubbs’ test cut-off must be a positive real number

    •	SNR cut-offs must be positive real numbers

    •	Percentage sample cut-off must be a real number between 0 and 1

  4. Run analysis.

  Note: 
  
  •	Do not change the content or the file names of the content of the folder.

  •	This only works on win64 platform.
  

