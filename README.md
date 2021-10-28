###Raw Data Processing
***
**Assumption**

Raw data is generated from an Oscilloscope.  
Model: SDS1104X-E
Two Channels are used, 
Vertical scale:  1.0V
Capture time period: 2ns 
***
**Processes**

A capture period results in a single large CSV file. 

Files are split to be easier to track the reading process, 
Then run the python script rename_split_files.py found in the raw_can_data folder

```Bash
cd raw_can_data
split -l 100000 large_oscope_file.csv
python rename_split_files.py
```

The python script will prompt you for an identifier of your choice. 
We utilize this ID as a prefix to track the split files. 

**Rational**

When working with large file sizes, there is effective human integration outputs
in the form of a status bar. The progress of this stats bar contains overhead in
its implementation. This overhead could be tracked per cycle of a large file read,
but it's found to be less overhead to just monitor the program's status reading 
individual files. In this day and age, we are rarely hard-drive space limited.




