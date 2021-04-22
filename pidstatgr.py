#!/usr/bin/env python3
import sys
import os
import pandas as pd
import argparse
import plotly.express as px
import plotly.graph_objects as go
import fileinput
import re

# WARNING
# This script changes the file a bit
# but saves the original one with .bak suffix
#
# Plots `pidstat -t -p PID 1` output
# or `pidstat -t 1` output

def get_greater(x):
    return x.gt(0.00).sum()

def cleanup_file(args):
    header_first = False
    with fileinput.FileInput(args.input, inplace=1, backup='.bak') as f:
        for line in f:
            if re.match(r'[0-9][0-9]:[0-9][0-9]:[0-9][0-9].*', line):
                if not re.match(r'[0-9][0-9]:[0-9][0-9]:[0-9][0-9].+UID.+Command', line):
                    print(line, end='')
                elif not header_first:
                    header_first = True
                    print(line, end='')

def work(args):
    with open(args.input) as f:
        # First line is a table header
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

    # Number of delayed threads during the time interval
    df_wait_threads_count = df.groupby('Time').agg({'%wait': get_greater})
    df_wait_threads_count = df_wait_threads_count.rename(columns={'%wait':'Delayed Threads Count'})

    # Plotting number of active threads
    fig = px.line(df_active_cpu_count, y='Active Threads Count')
    fig.show()

    # Plotting number of delayed threads
    fig = px.line(df_wait_threads_count, y='Delayed Threads Count')
    fig.show()

    # Plotting CPU utilization
    fig = px.line(df, x='Time', y='%CPU', color='TID')
    fig.show()

    # Plotting summarized CPU utilization for a processes
    fig = px.line(dfsum, x='Time', y='%CPU', color='Command')
    fig.show()

    # Thread CPU utilization heatmap
    fig = go.Figure(data=go.Heatmap(
                    z=df['%CPU'],y=df['TID']+' '+df['Command'],x=df['Time'],
                    hoverongaps=False),
                    layout=go.Layout(yaxis=dict(automargin=False)
                    ))
    fig.show()

    # Thread runqueue delay heatmap
    fig = go.Figure(data=go.Heatmap(
                    z=df['%wait'],y=df['TID']+' '+df['Command'],x=df['Time'],
                    hoverongaps=False),
                    layout=go.Layout(yaxis=dict(automargin=False)
                    ))
    fig.show()

def main():
    parser = argparse.ArgumentParser(description="Plot pidstat results")
    parser.add_argument('--input','-i',type=str,help="Input file")
    args = parser.parse_args()
    cleanup_file(args)
    work(args)
    
if __name__=='__main__':
    sys.exit(main())
