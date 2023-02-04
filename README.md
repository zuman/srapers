# Srapers
Collection of some useful scrapers.
<br/>
<br/>


## Visa Appointment Date Checker
The tool for Indians seeking the earliest available Schengen visa appointment date. This Python-based tool simplifies the process by automatically extracting the latest information from the official visa appointment website. No more manual checks and long wait times. With this tool, you can quickly and easily access the earliest appointment date, making your visa application process a breeze. Save time, effort, and simplify your travel plans with Visa Appointment Date Checker.

### Setup:

* Install [python](https://python.org)
* Install [pip](https://pip.pypa.io/en/stable/installation/)
* Install selenium package: `pip install selenium`

### Usage:
* Run the following command
```
python schengen-visa-date-checker.py -e your_email -p your_password
```
* During the first run, give appropriate permissions to the browser.
* Do not minimize or close the browser window.

#### Final output looks like this:
```
Chennai : 06/02/2023
Cochin : 06/02/2023
Bangalore : 07/02/2023
Pune : 07/02/2023
Kolkata : 08/02/2023
Panaji : 08/02/2023
Puducherry : 08/02/2023
Chandigarh : 09/02/2023
Mumbai : 09/02/2023
New Delhi : 13/02/2023
Hyderabad : 19/04/2023
Ahmedabad : 10/05/2023
```