# Rate convert tool
> To help myself deal with the CNY-HKD calculation on trip.

# Requirement
> python3
> pandas
> numpy
> beautifulsoup4


# Usage

### Step 1: install requirements.
```shell
pip3 install -r requirements.txt
```
If the download speed is low(in China), try using these

```shell
pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple some-package
```

or follow the instruction to set the mirror on [this](https://mirrors.tuna.tsinghua.edu.cn/help/pypi/).

### Step 2: generate template.csv
```shell
# For futher information can see with -h
python3 calculate.py -g
```

### Step 3: filled the template csv file
Fill the `csv` file with the corresponding date, and cost of money. Pay attention to the format.

### Step 4: calculate the total amount of CNY
```shell
python3 calculate.py -f template.csv
```
