# course-recommendation-system
Course recommendation system using Udemy's course, with over 10,000 courses.

The model has been trained using a dataset of 3,000 courses! Find the dataset

## Tech Used

**Language:** python(3.9.5)

**Front End:** Flask, HTML, CSS, Javascript

## Installation / Working

### Requirements
```
pandas==1.3.0
numpy==1.23.4
neattext==0.1.3
scikit-learn==1.0.2
Flask==2.1.1
```

## Work Flow

### Data Collection:
In order to create system based on latest course, information about all the courses are fetched from Udemy. For getting data of Udemy's courses, API is used. Udemy provides API for developer & instructor(it is under maintenance as on 20-11-2022). These 10K courses are collected from different categories including marketing, design, IT, art, personal development etc.

_data source: [udemy](https://www.udemy.com)_

### Model Building:
After collecting data using API, collected data is pre-processed and seperate .scv file is created. Then using pre-processed data model is bult on the top of recommendation engine theory.

### Model integration:
Once model start giving appropriate results, web application is developed using Flask, CSS, HTML & javascript. 


## Screen Shots

![image](https://user-images.githubusercontent.com/85471620/202887119-82e10485-7bad-42ca-b672-9f202b43f90f.png)

![image](https://user-images.githubusercontent.com/85471620/202887132-3edb91e0-f0d4-44c2-8a7e-878d6eeec926.png)

![image](https://user-images.githubusercontent.com/85471620/202887157-c204a060-ec64-4b67-adf6-a3ebba967316.png)

