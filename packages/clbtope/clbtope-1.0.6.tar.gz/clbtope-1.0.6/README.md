# **CLBTope**
A computational approach had been developed for predicting both types (linear/conformational) of B-cell epitopes. 
## Introduction
CLBTope is developed to predict, scan, and, design the both types (linear/conformational) of B-cell epitopes using sequence information only. In the pip version, Random Forest based model is implemented along with the BLAST search, named it as hybrid approach.
CLBTope is also available as web-server at https://webs.iiitd.edu.in/raghava/clbtope. Please read/cite the content about the clbtope for complete information including algorithm behind the approach.
____________________________________________________________________
## Model.zip
Note: The pip version will automatically fetch the model, eliminating the need for repeated downloads. However, a stable internet connection is required for this process.
____________________________________________________________________

## Standalone
The Standalone version of clbtope is written in python3 and following libraries are necessary for the successful run:
- scikit-learn
- Pandas
- Numpy
- blastp
## Installation
To install the CLBTope pip version follow the following command:
```
pip install clbtope
```
## Minimum USAGE
To know about the available option for the stanadlone, type the following command:
```
clbtope -h
```
To run the example, type the following command:
```
clbtope -i example_input.fa
```
This will predict if the submitted sequences can B-cell epitope or not. It will use other parameters by default. It will save the output in "outfile.csv" in CSV (comma seperated variables).

## Full Usage
```
usage: clbtope [-h] 
                       [-i INPUT 
                       [-o OUTPUT]
		       [-j {1,2,3}]
		       [-t THRESHOLD]
                       [-w {8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30}]
		       [-d {1,2}]
```
```
Please provide following arguments for successful run

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Input: protein or peptide sequence(s) in FASTA format
                        or single sequence per line in single letter code
  -o OUTPUT, --output OUTPUT
                        Output: File for saving results by default outfile.csv
  -j {1,2,3}, --job {1,2,3}
                        Job Type: 1:Predict, 2: Design, 3:Scan, by default 1
  -t THRESHOLD, --threshold THRESHOLD
                        Threshold: Value between 0 to 1 by default 0.16
  -w {8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30}, --winleng {8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30}
                        Window Length: 8 to 30 (scan mode only), by default 9
  -d {1,2}, --display {1,2}
                        Display: 1:Diabetic peptides only, 2: All peptides, by default 1
```

**Input File:** It allow users to provide input in the FASTA format.

**Output File:** Program will save the results in the CSV format, in case user do not provide output file name, it will be stored in "outfile.csv".

**Threshold:** User should provide threshold between 0 and 1, by default its 0.53.

**Job:** User is allowed to choose between three different modules, such as, 1 for prediction, 2 for Designing and 3 for scanning, by default its 1.

**Window length**: User can choose any pattern length between 8 and 30 in long sequences. This option is available for only scanning module.

