# DDoS-Prevention-System
This system is a Machine Learning–based Intrusion Detection and Prevention System (IDPS) trained to classify network traffic into three categories:
- **DDoS Attacks** – malicious traffic aiming to overwhelm and disrupt network services.  
- **Unauthorized Access** – attempts to gain access to systems or resources without permission.  
- **Normal Traffic** – legitimate, benign network activities.  

The models are trained and evaluated using two widely recognized benchmark datasets:  
- **NSL-KDD** – [a refined version](https://www.unb.ca/cic/datasets/nsl.html) of the KDD’99 dataset, widely used for intrusion detection research.  
  It is particularly employed for evaluating intrusion detection systems in **Internet of Things (IoT) environments**, where lightweight and efficient security solutions are essential.  

- **CIC-IDS2017** – [a modern dataset](https://www.unb.ca/cic/datasets/ids-2017.html) created by the **Canadian Institute for Cybersecurity, University of New Brunswick (Canada)**.  
  Its primary objective is to simulate **enterprise/organizational network environments**, containing realistic benign and malicious traffic across diverse attack scenarios.

# Repository Instructions

This repository is divided into three related parts, as illustrated in the diagram and explained below:
```
DDoS-Prevention-System
        |__ Document
        |    |__ Paper research
        |    |  | . . . 
        |    |
        |    |__Service Doc
        |       | . . .
        |
        |__ IDS_service    
        |    |__ config
        |    |  | . . .
        |    |__ models
        |    |  | . . .
        |    |__ . . .
        |    
        |__ Research     
             |__ data_preprocessing
            |  | . . .
            |__ training
            |  |. . .
            |__ . . .
        
```
## Doccument
This is a repo that place for document, you can reach the paper we reserach or document, some feature about system, please click [here](Document) to accsset to it. 
## IDS service
The IDS_system is the central service of our project.  
Developed with FastAPI, it is responsible for detecting malicious requests.  
Click [IDS_system](IDS_service) to explore it.
## Research
The **research** directory is organized into several submodules, including *crawl_data*, *training*, *inference*, and *preprocessing*.  
Together, these submodules represent the end-to-end research process: collecting and cleaning data, testing various models, selecting features, and training pipeline.  
This folder acts as a comprehensive record of our experiments and design choices throughout the project.  

For the deployed implementation, click [Research](Research) to access the main service.
