Contents:
---------
1. qsort_small.elf  
   - RISC-V binary of the MiBench "qsort_small" benchmark.
   - Used as the workload for simulation runs in gem5.

2. config_sa1.py  
   - Python configuration script for gem5.
   - Automates simulation setup, cache parameter sweeps, and output generation.

3. cache_sweep_summary_both.xlsx  
   - Excel spreadsheet summarizing performance metrics across different cache configurations.
   - Includes IPC, miss rates, and runtime comparisons.

4. plots/  
   - Folder containing visual plots generated from simulation data.
   - Graphs include IPC vs. cache size, miss rate trends, and comparative performance charts.
