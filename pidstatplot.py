#!/usr/bin/env python3
import sys
import os
import pandas as pd
import argparse
import plotly.express as px

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
    
    # Skip main summarized info for a process
    df = df[df.TID != '-']

    df_active_cpu_count = df.groupby('Time').agg({'%CPU': get_greater})
    df_active_cpu_count = df_active_cpu_count.rename(columns={'%CPU':'Active CPU Count'})
    fig = px.line(df_active_cpu_count, y='Active CPU Count')
    fig.show()

    fig = px.line(df, x='Time', y='%CPU', color='TID')
    fig.show()

def main():
    parser = argparse.ArgumentParser(description="Plot pidstat results")
    parser.add_argument('--input','-i',type=str,help="Input file")
    args = parser.parse_args()
    work(args)
    
if __name__=='__main__':
    sys.exit(main())
