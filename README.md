### Raw Data Processing
***
**Assumption**

Raw data is generated from an Oscilloscope.  
Model: SDS1104X-E
Two Channels are used, 
Vertical scale:  1.0V
Capture time period: ~2ns 
***
**Processes**

A capture period results in a single large CSV file. 

large csv files need to be split to track the reading process.

After splitting, running main.py will start the file processor and begin the analysis.

```Bash
cd raw_can_data
split -l 100000 large_oscope_file.csv
cd ..
can_stetho
```

The python script will prompt you for two identifiers. 

The first one is for the prefix added to the final data file. 

The second is for how the large file should be classified in individual smaller chunk files.

**Rational**

When working with large file sizes, there is effective human integration outputs
in the form of a status bar. The progress of this stats bar contains overhead in
its implementation. This overhead could be tracked per cycle of a large file read,
but it's found to be less overhead to just monitor the program's status reading 
individual files. In this day and age, we are rarely hard-drive space limited.




