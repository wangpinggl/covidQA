
# CovidQA

* This repository contains the important materials for our COVID-19 questioning answering system. The goal of this system is to offer an easier way for the public to receive information about COVID-19 through natural language questions. 

## Data Preparation
Our CovidQA database ([COVIDQA.db](https://github.com/wangpinggl/covidQA/blob/Srikar/COVIDQA.db)) contains data from six reliable databases which we detail in our paper. We include an automatic updater to update this database with the most recent data.
## Data Generation
The [natural_question.json](https://github.com/wangpinggl/covidQA/blob/Srikar/natural_question.json) file serves as our CovidQA dataset which contains populated entries for the question and sql templates. A comprehensive dataset containing populated natural language questions and queries can be generated through the [data_gen.py](https://github.com/wangpinggl/covidQA/blob/Srikar/data_gen.py) file. 

## Evaluation
### Type Group Recognition Matching
The type group recognition matching algorithm can be executed on our CovidQA dataset through the [match_type.py](https://github.com/wangpinggl/covidQA/blob/Srikar/match_type.py) file. 
### Two-step Matching
The two-step matching algorithm can be executed on our CovidQA dataset through the [match_2step.py](https://github.com/wangpinggl/covidQA/blob/Srikar/match_2step.py) file. 
### TAPAS
TAPAS can be executed on some of our question templates through the JupyterTAPAS.ipynb files. 



