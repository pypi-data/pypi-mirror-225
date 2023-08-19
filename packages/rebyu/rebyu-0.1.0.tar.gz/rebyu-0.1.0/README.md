# Rebyu (レビュー)
🌟 Review Analysis Made Easy

```python
from rebyu import Rebyu
from rebyu.pipeline import NLTK_PIPELINE

rb = Rebyu(data='twitter.csv', pipeline=NLTK_PIPELINE) # Initialize the data and pipeline
rb.run() # Run the pipeline

print(rb.data['vader_polarity'])
```

Rebyu, a Review Analysis Library equipped with text processing, transformers, and diverse analyses like sentiment, topics, emotion, and named-entities. It plans to be language-flexible, highly scalable, and offers both preset pipelines and customizable options.

**Version 0.1.0 (Unreleased)** - [Change Log](CHANGELOG.md)

```bash
pip install -U rebyu
```

---

### Concept

![Rebyu Concept](docs/images/Rebyu_Concept_sm.png)


The essence of Rebyu for Review Analysis lies in its structured 
pipeline approach to enhancing existing data. By leveraging a range of 
tools within this pipeline, we streamline the process, avoiding repetitive 
analyses and accelerating the generation of insights.


---

### Documentation

| Documentation      | Description |      |
| :---:        |    :----:   |          :---: |
| Read the Docs      | Official Documentation       | [Link]()   |
| Replit Example   | Multiple examples to run on Replit        | [Link]()      |


---

### Author

- Abhishta Gatya ([Email](mailto:abhishtagatya@yahoo.com)) - Software and Machine Learning Engineer
