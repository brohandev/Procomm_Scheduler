# 8-Day Schedule for Walter's Coroporate Visits

### Workflow

1. Install all prerequsite libraries as stated by my imported libraries
2. Open `./Procomm_Scheduler/Documents/input.xslx` Excel file
    - Navigate to `COMPANIES` sheet and insert postal codes of the companies under the appropriate headers (MORE PROFITABLE COMPANIES or LESS PROFITABLE COMPANIES)
    - Navigate to `REQUIREMENTS` sheet and insert the period number Walter would like to have his luncha and tea breaks. The same period number will be used for all of the 8 days. Insert period number under the appropriate headers (LUNCH PERIOD and TEA PERIOD)
3. From `./Procomm_Scheduler/` folder, run `py schedule_generator.py` to 
    - Retrieve relevant information from input.xslx
    - Compute Adjacency Duration Matrix via Google Maps and OneMaps APIs
    - Generate Walter's 8 Day Schedule from the main schedule_generator() function inside schedule_generator.py file using an approximation of the Travelling Salesman Problem and Hamiltonian Paths
4. The final output will be written to `./Procomm_Scheduler/Documents/output.xslx`, with each row representing each day in the 8 day schedule. The final column states the total duration of each day, thereby fulfilling all requirements of the task.

_For suggestions on how to improve this tool, please reach out to me via email. Thank you!_