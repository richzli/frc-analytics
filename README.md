# FRC Data Analytics

Calculates the OPR and DPR of various stats for FRC events.

## Setup

1. Install Python. This project was created in Python 3.7.0, however, it should be compatible with any Python 3 installation. [Download the latest version of Python here.](https://www.python.org/downloads/)
2. Install the packages `pandas`, `numpy`, and `scipy`. To do so, run the following commands in order:
```
python -m pip install pandas
python -m pip install numpy
python -m pip install scipy
```
3. Create a new file named token.secret. :warning: Make sure the file extension is .secret, not .txt! :warning:
4. Put your username and authentication token inside token.secret. Your token.secret should look something like
```
sampleuser:7eaa6338-a097-4221-ac04-b6120fcc4d49
```

## Usage

1. Run FRCAnalytics.exe.
2. In the GUI that pops up, put the year name in the text box labeled "Year:" and put the competition code in the text box labeled "Competition Code:".
3. Click the "Get Data" button.
4. If you are on a Windows computer, a file with the calculated OPRs and DPRS should open up. If not, you can find the compiled data in `./data/processed/`.
