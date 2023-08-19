# PBS-builder

A simplified version of workflow management system for scalable data analysis.

# Change log

- Version 0.4.1: auto-switch to corresponding pbs_server for qbatch
- Version 0.4.0: merge qcancel into qbatch commands, change API
- Version 0.3.1: add allocated/total gpus in `pestat` output
- Version 0.3.0: include `pestat` in package data
- Version 0.2.0: move `sample_sheet` from header to job section, add `group_sheet` support.
- Version 0.1.0: first functional version.

# Usage

`pbs-builder` include two commands:

- [`qbatch`](https://bioinfo.biols.ac.cn/git/zhangjy/pbs-builder/wiki/qbatch%3A+building+automated+and+reproducible+pipelines)for batch submission of TORQUE/SLURM jobs

- [`pestat`](https://bioinfo.biols.ac.cn/git/zhangjy/pbs-builder/wiki/pestat%3A+monitor+node+status) for monitoring cluster & nodes status 

Please refer to our [wiki](https://bioinfo.biols.ac.cn/git/zhangjy/pbs-builder/wiki/_pages) for detailed instructions.

# Installation

pbs-builder is heavily inspired by Snakemake, but uses native SLURM/Torque dependencies to build analysis pipeline.

pbs-builder runs in **python3.7+** with the `tomli` package installed, no other dependencies are required.

Install pbs-builder using the following command:

```bash
pip install pbs-builder
```
