# ColonyCounter

ColonyCounter is an image analysis pipeline for counter bacterial and yeast 
colonies on agar plates. This pipeline will count the number of colonies and 
mark them on the agar plate image.

## Installation

ColonyCounter runs on Python 3.6 and higher and requires the following packages:
- numpy
- scikit-image
- pandas

To install ColonyCounter using Anaconda, git clone or download and unzip the 
ColonyCounter code.

`https://github.com/jingliu-ut/ColonyCounter.git`

From the ColonyCounter directory, create the environment 
and activate the environment.

`conda create -n ColonyCounter python=3.6 numpy scikit-image pandas`

To run ColonyCounter, you need to put your plate images (.tif) in the 
`Inputs` folder. Then from the ColonyCounter directory, run the code using 
`python ColonyCounter.py`.

The output of ColonyCounter will be written to the `Outputs` subfolder. This 
folder will contain all the analyzed images (.png) and the results in a CSV 
file.
