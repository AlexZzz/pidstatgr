# Pidstatgr. Plot as you can.

`pidstatgr` parses output of `pidstat` and plots graphs. Uses plotly and pandas to look like data science project.

## How to use
Run `pidstat -t 1 > ./result` or `pidstat -t -p $PID 1 > ./result` if you want info about a known PID. Hit `^C` when done and run `pidstatgr.py -i ./result`. Wait a bit and it'll start a web browser and show you graphs.

## For now it supports:
`pistat -t 1` output:
* Number of active threads. Sum of threads with %CPU > 0.
* CPU utilization. Per-thread and per-process CPU utilization graphs.
* Heatmap of CPU utilization by TID and command name.

## TODO
* Add more detailed statistics for CPU usage, e.g. delay time of processes, system/userspace time.
* Add ability to parse memory information. `pidstat -tr 1` output.

