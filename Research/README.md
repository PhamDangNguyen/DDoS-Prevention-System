
## Create conda env
This project using conda for env
```
conda create --name ddos python=3.10
```
## Feature selection
Based on the paper [Enhanced Intrusion Detection via Hybrid Data Resampling and Feature Optimization - table3 release 21/08/2025](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=11141474) we decided to select the 42 most important features as the foundation for subsequent processing steps with the dataset.