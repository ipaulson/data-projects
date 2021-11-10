Using Survey Data to Identify Failing Students
==============================================

Capstone project 2 for Springboard Data Science Career Track

Final Report
------------

### Introduction & Problem

Failing students add numerous tangible and intangible costs to schools, school districts, and even entire education systems. For example, failing students are usually required to retake classes, adding hours to teacher and paraeducator workloads; costly interventions are applied to failing students; and - fairly or unfairly - media and public attention is often drawn to the number of failing students jurisdictions.

Anecdotally, teachers and other education professionals observe common characteristics among their failing students. What if student student behavior surveys could be use to pick out common traits amongst failing students? This analysis attempts to answer this question by applying machine learning techniques from scikit-learn to a dataset containing student grades and behavioral surveys, found at: UCI Machine Learning Repository - Student Performance Data Set.

### Data Collection and Cleaning

The data was downloaded directly, as two `.csv` files from the UCI Machine Learning Repository.

The raw data of the Student Performance Data Set contains information on student achievement, demographic information, and lifestyle factors of Portuguese secondary students. The data was collected using school reports and student questionnaires. The data is split into two files, one for the mathematics subject area and one for Portuguese language.

The collected data was quite tidy and required little cleaning. The main task of the data cleaning step was to combine two datasets indentical datasets, one for mathematics and one for language grades into one dataframe.

### Exploratory Data Analysis

After data collection and cleaning, the next step I took was to explore the data for interesting features. For the exploratory data analysis (EDA) stage, much of the work was done on separate dataframes, in case an interesting feature could be observed in either the mathematics or language dataset that did not appear in the other.

The first task was to check the distributions of final grades.

![Grade distributions](/images/distributions.png)

The distributions look more or less as expected. The most unusual feature is the grades of zero that grow over time and begin to skew the distributions. One likely explanation is that these students dropped from the class and did not recieve a final grade. The goal of the project is to identify failing students, so these zeroes were left in place.

Next, I observed the correlations between variables in the mathematics and language dataframes.

![Math correlations](/images/maths.png)

![Language correlations](/images/lang.png)

Looking at the correlations, a story about the students began to emerge. Higher grades were most correlated with students' mothers' and fathers' educations. Study time was also correlated with grades, albeit weakly. Failures in other classes were most correlated, negatively, with grades.

Although I observed these correlations, none of them were particularly high.

Finally, I did not notice anything particularly alarming about the differences in grades between groups such as gender and school attended.

### Pre-processing

Using information from above and from the documentation for the dataset (see Appendix 1, below), the data can be grouped into a few different groups for processing.

#### 'True' Binaries

These variables relate to yes or no survey questions. They can be processed as 0 for 'no' and 1 for 'yes'.

- schoolsup: yes or no
- famsup: yes or no
- paid: yes or no
- acitivities: yes or no
- nursery: yes or no
- higher: yes or no
- internet: yes or no
- romantic: yes or no

#### Categories

##### Two categories

There a few more variables that contain only two categories, but it makes less sense simply transform them to 0 or 1. Instead, they can be one-hot encoded using pd.get_dummies().

- school: GP or MS
- sex: M or F
- address: U or R
- famsize: LE3 or GT3
- Pstatus: T or A

##### More than categories

These variables are also categorical but with more than two categories. For the sake of clarity they have been separated from the two-category variables above, but they can also be one-hot encoded using pd.get_dummies()

- Mjob: teacher, health, services, at home, other
- Fjob: teacher, health, services, at home, other
- reason: (close to) home, reputation, course (preference), other

#### Ordinals

##### Ordinal Categories

These variables deal with responses that ordered numerically, but distances between the responses are difficult or impossible to quantify. For instance, In the case of Medu and Fedu (mothers' and fathers' education) 0 does mean zero and 4 is higher than 3, but by how much? The same idea applies for traveltime and study time. 5 is higher than 3, but by how much. The data has been collected as an ordinal scale, so no processing is required.

- Medu: 0 - none, 1 - up to 4th, 2 – 5th to 9th grade, 3 - secondary, 4 - higher education
- Fedu: 0 - none, 1 - up to 4th, 2 – 5th to 9th grade, 3 – secondary, 4 - higher education
- traveltime: 1 - <15 min., 2 - 15 to 30 min., 3 - 30 min. to 1 hour, or 4 - >1 hour
- studytime: 1 - <2 hours, 2 - 2 to 5 hours, 3 - 5 to 10 hours, or 4 - >10 hours

##### Likert-type Responses

For some items, students were asked to respond on a five point scale, 1 being very low and 5 being very high. Data was collected as ordinal variables, although Likert scales are sometimes considered as continuous for analysis purposes. Again, no processing is required for this set of variables.

1, very low to 5, very high:

- famrel
- freetime
- goout
- Dalc
- Walc
- health

#### Numeric

These variables are integers for age, failures, absences, and grades, G3 being the file grade. For now, these variables will also be left as they are.

- age: 15 - 22
- failures: n if 1<=n<3, else 4
- absences
- G1
- G2

I did not complete some of the pre-processing steps until the modeling stage of the project. The reason for waiting was that I needed to be ready to start modeling before I knew how I wanted the data arranged. In this case, I recoded the variable to be predicted (failing or not failing) as a binary variable, scaled the data, and split the data into a train-test split in the final, modeling notebook.

### Modelling

I tried a variety of models to see which might be most appropriate for the task.

#### Dummy Classifier

First, I established a baseline using a dummy classifier. This dummy classier simply picks out the most frequent class in the dataset, the students whose grades are sufficient.

![Confusion matrix for dummy classifier](/images/dummy-conf-matrix.png)

Everything was predicted as 'not failing' so the accuracy matched the percentage of passing students in the dataset, 0.748.

#### Logistic Regression

After a baseline was established, I started with a simple model, logistic regression, to pick out which students have grades of 'not sufficient'. For all of the models, I used GridSearchCV for hyperparmeter tuning.

Here are the results of the first model:

>Best parameters: {'C': 1, 'penalty': 'l1'}
>
>Accuracy: 0.768
>
>Recall: 0.228

![ROC for Logistic Regression](/images/roc-logreg.png)

The predictions using logistic regression were fairly accurate. However, it was important to look at other metrics such as recall. Recall is an important metric for this problem. We don't want to identify just some failing students; we want to correctly identify as many of the failing students as possible. Unforunately, the recall score is quite low.

I took a closer look at the confusion matrix to see what is going on:

![Confusion Matrix for Logistic Regression](/images/conf-matrix-logreg.png)

#### K-nearest Neighbors

Next, I tried a k-nearest neighbor model, using the same method as above for hyperparameter tuning.

>Best parameters: {'metric': 'euclidean', 'n_neighbors': 13, 'weights': 'uniform'}
>
>Accuracy: 0.748
>
>Recall: 0.038

![ROC for k-nearest neighbors](/images/roc-knn.png)

![Confusion Matrix for k-nearest neighbors](/images/conf-matrix-knn.png)

The model was as accurate as the dummy classifier, with a recall score of 0.038. Althogh it managed to pick out a small few failing students, this model was not very helpful compared to the dummy classier.

#### Random Forest

Next, I tried a random forest model. The accuracy of the random forest model showed a slight improvement over logisictic regression, but the recall score was worse.

>Best parameters: {'class_weight': 'balanced', 'criterion': 'entropy', 'max_features': 'log2', 'n_estimators': 100}
>
>Accuracy: 0.768
>
>Recall: 0.165

![ROC for random forest](/images/roc-rforest.png)

![Confusion Matrix for random forest](/images/conf-matrix-rforest.png)

#### Gradient Boosting

Finally, I tried a gradient boosting model.

>Best parameters: {'learning_rate': 0.1, 'max_depth': 1, 'n_estimators': 50}
>
>Accuracy: 0.771
>
>Recall: 0.228

![ROC for random forest](/images/roc-gb.png)

![Confusion Matrix for random forest](/images/conf-matrix-gb.png)

The model with the best performance, accuracy and recall, was the gradient boosting model. However, it remains to be seen whehter it performed significantly better than logistic regression. In fact, none of the models performed much better than the dummy classifier. This observations points toward a major problem with the current analysis.

### Conclusion

The conclusion that I come to is that there is simply not enough data to deal this problem. The accuracy of each model at first looks decent, but looking at this score alone masks the fact that each model is really only picking out the most common class, like the dummy classifier.

### Next Steps

The most obvious recommendation is to gather more data and repeat the same processes with a larrger dataset. This dataset is slightly imbalanced, so similiar techniqes might be used along with oversampling techniqes — keeping in mind that the dataset as it has been processed is made up of non-continuous variables. In taking this approach, gradient boost looks like a promising model, as it shows the most improvements in recall which — it has been noted — is an important metric for identifying failing students in this context.

Also, since completing the analysis, I have come across some studies using similar methods that came up with a result. Taken together, this suggests the choice of variables in future analysis may be as crucial in addition to n size.

Appendix 1: Variables in the Data Set
-------------------------------------

### Attributes for both student-mat.csv (Math course) and student-por.csv (Portuguese language course) datasets:
1. school - student's school (binary: "GP" - Gabriel Pereira or "MS" - Mousinho da Silveira)
2. sex - student's sex (binary: "F" - female or "M" - male)
3. age - student's age (numeric: from 15 to 22)
4. address - student's home address type (binary: "U" - urban or "R" - rural)
5. famsize - family size (binary: "LE3" - less or equal to 3 or "GT3" - greater than 3)
6. Pstatus - parent's cohabitation status (binary: "T" - living together or "A" - apart)
7. Medu - mother's education (numeric: 0 - none,  1 - primary education (4th grade), 2 – 5th to 9th grade, 3 – secondary education or 4 – higher education)
8. Fedu - father's education (numeric: 0 - none,  1 - primary education (4th grade), 2 – 5th to 9th grade, 3 – secondary education or 4 – higher education)
9. Mjob - mother's job (nominal: "teacher", "health" care related, civil "services" (e.g. administrative or police), "at_home" or "other")
10. Fjob - father's job (nominal: "teacher", "health" care related, civil "services" (e.g. administrative or police), "at_home" or "other")
11. reason - reason to choose this school (nominal: close to "home", school "reputation", "course" preference or "other")
12. guardian - student's guardian (nominal: "mother", "father" or "other")
13. traveltime - home to school travel time (numeric: 1 - <15 min., 2 - 15 to 30 min., 3 - 30 min. to 1 hour, or 4 - >1 hour)
14. studytime - weekly study time (numeric: 1 - <2 hours, 2 - 2 to 5 hours, 3 - 5 to 10 hours, or 4 - >10 hours)
15. failures - number of past class failures (numeric: n if 1<=n<3, else 4)
16. schoolsup - extra educational support (binary: yes or no)
17. famsup - family educational support (binary: yes or no)
18. paid - extra paid classes within the course subject (Math or Portuguese) (binary: yes or no)
19. activities - extra-curricular activities (binary: yes or no)
20. nursery - attended nursery school (binary: yes or no)
21. higher - wants to take higher education (binary: yes or no)
22. internet - Internet access at home (binary: yes or no)
23. romantic - with a romantic relationship (binary: yes or no)
24. famrel - quality of family relationships (numeric: from 1 - very bad to 5 - excellent)
25. freetime - free time after school (numeric: from 1 - very low to 5 - very high)
26. goout - going out with friends (numeric: from 1 - very low to 5 - very high)
27. Dalc - workday alcohol consumption (numeric: from 1 - very low to 5 - very high)
28. Walc - weekend alcohol consumption (numeric: from 1 - very low to 5 - very high)
29. health - current health status (numeric: from 1 - very bad to 5 - very good)
30. absences - number of school absences (numeric: from 0 to 93)

### these grades are related with the course subject, Math or Portuguese:
31. G1 - first period grade (numeric: from 0 to 20)
32. G2 - second period grade (numeric: from 0 to 20)
33. G3 - final grade (numeric: from 0 to 20, output target)

Additional note: there are several (382) students that belong to both datasets . 
These students can be identified by searching for identical attributes
that characterize each student, as shown in the annexed R file.

Appendix 2: Project Organization in this Repository
---------------------------------------------------

    ├── README.md          <- README containing report and information on the project.
    ├── data
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    ├── notebooks         
    │   ├── data-collection.ipynb
    │   ├── eda.ipynb
    │   ├── pre-processing.ipynb
    │   └── modeling.ipynb
