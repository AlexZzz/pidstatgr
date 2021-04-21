#!/usr/bin/env python3
import sys
import os
import pandas as pd
import argparse
import plotly.express as px

# Plots `pidstat -t -p PID 1` output

def get_greater(x):
    return x.gt(0.00).sum()

def work(args):
    with open(args.input) as f:
        # Skip first two lines of header
        for _ in range(2):
            next(f)
        # Next line is a table header
        header = f.readline().split()
        # But the first column has time instead of the word 'Time'
        header[0] = 'Time'
        df = pd.read_csv(f,names=header,delim_whitespace=True)
    
    # Add new datframe for the whole process stats
    dfsum = df[df.TID == '-']
    # Skip main summarized info for a process
    df = df[df.TID != '-']

    # Here we count number of active threads during the time interval
    df_active_cpu_count = df.groupby('Time').agg({'%CPU': get_greater})
    df_active_cpu_count = df_active_cpu_count.rename(columns={'%CPU':'Active Threads Count'})

    # Plotting number of active threads
    fig = px.line(df_active_cpu_count, y='Active Threads Count')
    fig.show()

    # Plotting CPU utilization
    fig = px.line(df, x='Time', y='%CPU', color='TID')
    fig.show()

    # Plotting summarized CPU utilization for a processes
    fig = px.line(dfsum, x='Time', y='%CPU', color='Command')
    fig.show()

def main():
    parser = argparse.ArgumentParser(description="Plot pidstat results")
    parser.add_argument('--input','-i',type=str,help="Input file")
    args = parser.parse_args()
    work(args)
    
if __name__=='__main__':
    sys.exit(main())
