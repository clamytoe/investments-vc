# Investments Venture Capitalists (*investments-vc*)

> *Capstone project that I created as part of CareerERA's Post Graduate Program*

![Python version][python-version]
![Latest version][latest-version]
[![GitHub issues][issues-image]][issues-url]
[![GitHub forks][fork-image]][fork-url]
[![GitHub Stars][stars-image]][stars-url]
[![License][license-image]][license-url]

NOTE: This project was generated with [Cookiecutter](https://github.com/audreyr/cookiecutter) along with [@clamytoe's](https://github.com/clamytoe) [toepack](https://github.com/clamytoe/toepack) project template.

## Initial setup

```zsh
cd Projects
git clone https://github.com/clamytoe/investments-vc.git
cd investments-vc
```

### Anaconda setup

If you are an Anaconda user, this command will get you up to speed with the base installation.

```zsh
conda create --name vc --file requirements.txt
conda activate vc
```

### Regular Python setup

If you are just using normal Python, this will get you ready, but I highly recommend that you do this in a virtual environment.
There are many ways to do this, the simplest using *venv*.

```zsh
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Creating a cleaned dataset

The initial dataset required a lot of tweaking in order to get it ready. The cleaned dataset exceeds the maximum size requirements for GitHub, so it was not provided. Not to worry though, I have provided a script to generate it.

Simply run the follwing command:

```bash
python cleanup_data.py
Created data/cleaned_data.csv
```

## Generating the model

To generate the model, simply run the following command:

```bash
python create_model.py
Importing dataset: data/cleaned_data.csv
Processing data...
Resampling imbalanced classes...
Splitting the data into train, validation, and test sets...
Scaling numeric features...
One Hot Encoding categorical features...
Creating model...
Fitting the model...
Testing the model...

Classification Report
              precision    recall  f1-score   support

           0       0.89      0.81      0.85       988
           1       0.83      0.90      0.87      1012

    accuracy                           0.86      2000
   macro avg       0.86      0.86      0.86      2000
weighted avg       0.86      0.86      0.86      2000


Confusion Matrix
[[805 183]
 [ 98 914]]

Saving the model...
[DONE] Model saved to rf-up-86.pkl
```

## License

Distributed under the terms of the [MIT](https://opensource.org/licenses/MIT) license, "investments-vc" is free and open source software.

## Issues

If you encounter any problems, please [file an issue](https://github.com/clamytoe/toepack/issues) along with a detailed description.

[python-version]:https://img.shields.io/badge/python-3.9.15-brightgreen.svg
[latest-version]:https://img.shields.io/badge/version-0.1.0-blue.svg
[issues-image]:https://img.shields.io/github/issues/clamytoe/investments-vc.svg
[issues-url]:https://github.com/clamytoe/investments-vc/issues
[fork-image]:https://img.shields.io/github/forks/clamytoe/investments-vc.svg
[fork-url]:https://github.com/clamytoe/investments-vc/network
[stars-image]:https://img.shields.io/github/stars/clamytoe/investments-vc.svg
[stars-url]:https://github.com/clamytoe/investments-vc/stargazers
[license-image]:https://img.shields.io/github/license/clamytoe/investments-vc.svg
[license-url]:https://github.com/clamytoe/investments-vc/blob/master/LICENSE
