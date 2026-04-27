# adcirc-view

A command-line tool to plot and compare `fort.61` output files from ADCIRC.

### Installing

Use pip to install locally:
```
pip install .
```

### Usage

Specify the folder to store the plots (will be created if doesn't exist) and the fort.61 files. 
At least one must be specified.

    adcirc-view -d output_dir fort.61.A fort.61.B fort.61.C [fort.61.D...]

This will create one plot for each elevation station in `output_dir`. 
