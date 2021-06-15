# stalking_lectures

## A project developed by group of students in Technical University - Sofia. This software allows for deep analysis on data from moodle platforms.

### Features include:
- Analysis on uploaded exercises by students and the number of reviewed lectures
	- Frequency distribution
	- Measures of central tendency
	- Measures of disperion
	- Correlation analysis

### Requirements before running:
1. Install Python (3.9.5 used for this project)
2. Install virtualenv -> environment used for this project so you don't install all dependencies on your system
```pip3 install virtualenv```
3. Go to project directory and create your virtualenv
```virtualenv env```
4. Start virtual environment:
	- Mac/Linux:
```source ./env/bin/activate```
	- Windows:
```env\Scripts\activate.bat```
5. Install requirements with:
```pip3 install -r requirements.txt```
6. Run server:
```python3 manage.py runserver```
