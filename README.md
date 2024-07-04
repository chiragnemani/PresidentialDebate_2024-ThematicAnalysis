![ThematicAnalysis_banner](https://github.com/chiragnemani/PresidentialDebate_2024-ThematicAnalysis/assets/148119942/292ae72d-d133-48cd-a4c5-4d523c302e72)

### This project analyzes the 2024 US Presidential Debate transcripts to uncover key themes and sentiments expressed by the candidates: President **Joe Biden** and former President **Donald Trump** 
---
## GOAL

The goal is to gain insights into the topics & concerns addressed and sentiments discussed during the debate. By analyzing the frequency of specific words and generating word clouds, this analysis aims to provide a visual representation of the candidates' focus areas and the overall tone of their discourse.

## DATA SOURCE

The debate transcripts were sourced from CNN, capturing the exchanges between the candidates moderated by anchors Jake Tapper and Dana Bash.

## TECH STACK

- **Python:** Programming language used for data processing and analysis.
- **NLTK (Natural Language Toolkit):** Library for natural language processing tasks.
- **Matplotlib:** Library for creating visualizations such as plots and word clouds.
- **WordCloud:** Library for generating word clouds from text data.

## PROCESS

### Step 1: Cleaning and Segregating Statements

The debate transcript was cleaned to remove stopwords, punctuation, and irrelevant words to focus on meaningful content. Statements were segregated by speakers using identifiers in the transcript: Biden, Trump, Tapper, and Bash.

### Step 2: Word Frequency Analysis

Performed word frequency analysis on each speaker's cleaned statements to identify the most frequently used words.

### Step 3: Generating Word Clouds

Generated word clouds for each speaker based on their word frequency analysis results. Word clouds visually represent the frequency of words, with larger words indicating higher frequency.

### Step 4: Visualization and Interpretation

Visualized and interpreted the word clouds to highlight key topics discussed by each candidate and their overall communication emphasis.

## RESULTS
### Word Cloud Visualization
<p float="left">
  <img src="https://github.com/chiragnemani/PresidentialDebate_2024-ThematicAnalysis/assets/148119942/560e076c-ec51-490b-8de4-91ca52fcc625" width="500" />
  <img src="https://github.com/chiragnemani/PresidentialDebate_2024-ThematicAnalysis/assets/148119942/fb8cfdae-cb2d-4f08-99af-7c67333c4e38" width="500" />
</p>

### Word Frequency Table
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
![Word_frequency_table](https://github.com/chiragnemani/PresidentialDebate_2024-ThematicAnalysis/assets/148119942/8dfa9183-b175-47c7-9653-c8adc80a36dc)



## CONCLUSION

This project provides valuable insights into the 2024 US Presidential Debate, illustrating the prominent themes and sentiments expressed by President Joe Biden, former President Donald Trump, co-anchors Jake Tapper and Dana Bash. The word clouds visually capture the focus areas and tone of the debate, encouraging viewers to reflect on the candidates' messages.
