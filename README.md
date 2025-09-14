# DDoS-Prevention-System
This system is designed for network intrusion detection.
## Create conda env
This project using conda for env
```
conda create --name ddos python=3.10
```
## Feature selection
Based on the paper [Reliable Feature Selection - table6 release 2024](https://arxiv.org/pdf/2404.04188) for Adversarially Robust Cyber-Attack Detection, we decided to select 26 important features from the feature selection process. Other intrusion detection system (IDS) datasets will be mapped to these 26 feature columns accordingly.