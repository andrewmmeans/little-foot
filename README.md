# little-foot

![little-foot](https://github.com/andrewmmeans/little-foot/blob/master/images/bigfoot_small.jpg)

A NLP Case Study of BigFoot Sightings

## A view of the raw data

## EDA

### Additional Datasets

#### Census.gov

Population per state from 2010 Census - https://www.census.gov/data/datasets/time-series/demo/popest/2010s-state-total.html#par_textimage_1873399417

### Classification of Reports

Source: https://www.bfro.net/GDB/classify.asp

+ Class A

Class A reports involve clear sightings in circumstances where misinterpretation or misidentification of other animals can be ruled out with greater confidence. For example, there are several footprint cases that are very well documented. These are considered Class A reports, because misidentification of common animals can be confidently ruled out, thus the potential for misinterpretation is very low.

+ Class B

Incidents where a possible sasquatch was observed at a great distance or in poor lighting conditions and incidents in any other circumstance that did not afford a clear view of the subject are considered Class B reports.

For example, credible reports where nothing was seen but distinct and characteristic sounds of sasquatches were heard are always considered Class B reports and never Class A, even in the most compelling "sound-only" cases. This is because the lack of a visual element raises a much greater potential for a misidentification of the sounds.

Class B reports are not considered less credible or less important than Class A reports--both types are deemed credible enough by the BFRO to show to the public. For example, one of the best documented reports ever received by the BFRO is a Class B report from Trinity County California. It involved a very credible witness who backpacked into a remote area that has a history of sasquatch-related incidents. He described various occurrences around his camp at night that are strongly suspected to be sasquatch-related. The report is still considered Class B though because there was no clear visual observation to confirm what was heard outside the tent.

Almost all reports included in the database are first-hand reports. Occassionally a second-hand report is considered reliable enough to add to the database, but those reports are never Class A, because of the higher potential for inaccuracy when the story does not come straight from the eyewitness.

+ Class C

Most second-hand reports, and any third-hand reports, or stories with an untraceable sources, are considered Class C, because of the high potential for inaccuracy. Those reports are kept in BFRO archives but are very rarely listed publicly in this database. The exceptions are for published, or locally documented incidents from before 1958 (before the word "Bigfoot" entered the American vocabulary), and sightings mentioned in non-tabloid newspapers or magazines.

## Overview of the NLP Pipeline
  ```python
def remove_stopwords_and_punct(entry):
    words = str(entry).split()
    words = [word.lower() for word in words if word.lower() not in stopwords_ and word.lower() not in punctuation_]
    words = [lemmatizer.lemmatize(word, pos = 'v') for word in words]
    words = [snow.stemmer.stem(word) for word in words]
    
    return " ".join(words)  
    
df['OBSERVED'] = df['OBSERVED'].apply(lambda x: remove_stopwords_and_punct(x))
```

## Machine Learning Model Decisioning
We decided on a Random Forest Classifier as our class classification model.  Initially we wanted to classify each sighting to class A, B, or C, but due to the very low instances of class C, we decided to split it into two categories:
- Class A: Reliable
- Not Class A: Unreliable

With the Random Forest Classifier, we were able to predict class with an Accuracy of .8023, and Log Loss of 0.5154.
## Tuning and Evaluation
![feature_importance](https://github.com/andrewmmeans/little-foot/blob/master/images/feature_importances.png)

We decided to examine some of these words by 
![forest_pred_by_word](https://github.com/andrewmmeans/little-foot/blob/master/images/forest_pred_by_word.png)

## Results


## Questions
What state has the most bigfoot sightings?

Are there regional differences of language used to describe reports of bigfoot?

