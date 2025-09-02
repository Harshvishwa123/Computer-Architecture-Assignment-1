# 🧠 Cache Performance Analysis using gem5

This repository contains simulation scripts, results, and analysis for evaluating cache performance across varying L2 and L3 configurations using the gem5 framework. The study compares TimingSimpleCPU and O3CPU models to understand architectural trade-offs in cache design.

## 📌 Overview

The project explores:

- Effects of L2 and L3 cache size and associativity on miss rates  
- Performance differences between TimingSimpleCPU and O3CPU  
- Simulation ticks as a proxy for execution time  
- Visualization of trends to guide optimal cache configurations

## 🛠️ Methodology

- **Framework**: gem5  
- **Benchmark**: `qsort_small.elf`  
- **Sweep Parameters**:
  - L2 sizes: 128KB, 256KB, 512KB  
  - L3 sizes: 1MB, 2MB  
  - Associativity: 4-way, 8-way, 16-way  
- **Metrics Extracted**: `SimTicks`, `L2 Miss Rate`, `L3 Miss Rate`  
- **Tools Used**: Python for CSV parsing and plotting, matplotlib for visualization

## 📊 Results Summary

| CPU Model        | L2/L3 Config      | SimTicks (B) | L2 Miss Rate | L3 Miss Rate |
|------------------|------------------|--------------|--------------|--------------|
| TimingSimpleCPU  | 128KB / 1MB      | 58.56        | 0.645        | 0.437        |
| TimingSimpleCPU  | 256KB / 2MB      | 56.57        | 0.523        | 0.285        |
| TimingSimpleCPU  | 512KB / 2MB      | 55.84        | 0.397        | 0.375        |
| O3CPU            | 128KB / 1MB      | 10.57        | 0.648        | 0.433        |
| O3CPU            | 256KB / 2MB      | 9.53         | 0.525        | 0.280        |
| O3CPU            | 512KB / 2MB      | 9.30         | 0.399        | 0.370        |

## 📈 Visualizations

Plots include:

- L2 Miss Rate vs L2 Size (TimingSimpleCPU & O3CPU)  
- L3 Miss Rate vs L3 Size (TimingSimpleCPU & O3CPU)  
- Combined grid of miss rate trends across configurations

## 🔍 Key Insights

- Larger caches reduce miss rates, especially for L3  
- Associativity improves performance up to 8-way; gains plateau beyond that  
- O3CPU consistently outperforms TimingSimpleCPU due to out-of-order execution  
- TimingSimpleCPU serves well for baseline architectural analysis
