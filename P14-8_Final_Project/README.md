## Phishing Email Detection using Machine Learning

### Project Overview:
Phishing attacks remain a significant cybersecurity threat, with attackers impersonating legitimate entities to trick individuals into disclosing sensitive information. This project aims to contribute to the security against these phishing attacks by developing a machine learning model to detect phishing emails.

Our approach involves extracting features from email attributes, such as word counts, capitalization percentages, and keyword patterns. Using these features, we trained an SVC-based classification model, with key findings showing the model achieving an accuracy of 93.05%, demonstrating its effectiveness in phishing detection.

To enhance usability, we deployed the model via an API, enabling integration with other applications. A live web application was also developed, allowing real-time classification of new email inputs as either legitimate or phishing.


### Package Installation:
    pip install -r requirements.txt

### Web Application Testing:
1) Install necessary packages
2) Run app.py
3) Login with username: admin, password: password
4) Enter email prompts

### Dataset References:
[1] W. Cukierski, “The Enron Email Dataset,” Kaggle. Available: https://www.kaggle.com/datasets/wcukierski/enron-email-dataset<br>
[2] A. Islam, “Phishing Email Curated Datasets,” Zenodo. Available: https://zenodo.org/records/8339691
  


