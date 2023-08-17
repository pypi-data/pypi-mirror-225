# Calibration Scores Module
## Overview
This module is a work in progress method to assign a score to each sensor used at PBR events. The program takes input data from one event and compares each player's metrics to those that they achieved at past events. Each calibration is assigned a score from 0-1, with 1 being the most accurate score and 0 being completely inaccurate. Currently, the module supports scores for trackman pitching data and scores the calibrations based on extension, release height, and release width (relside). Further support will be added for blast data and swift 60 yard dash times.

## Environment
This folder was set up in the poetry virtual environment. Poetry allows for dependencies to be added easily, with the command `poetry add DEPENDENCY`.
### Dependencies
- Python "^3.9"
- numpy = "^1.25.1"
- pandas = "^2.0.3"
- matplotlib = "^3.7.2"

## Data Gathering
To run these programs on your local machine with up to date data, you may query for in in AWS Athena. For instructions on gathering data and what queries to run, follow the below links to the notebook folder in this repository.
(Add links here once files are pushed to repo)


## Usage
This package will be integrated into the UI for event coordinators. After an event finishes, the coordinator will be able to see this information on their device and choose whether or not to send the event data in with or without a flag.

All functions currently supported have their uses demonstrated in the calibration_scores_example.ipynb file located in the notebooks folder of this repository. Feel free to modify or add commands as you see fit for your workflow.

## Contributing
Contributions to this package are encouraged as it is not a finished product. Feel free to suggest changes to the code or testing files. Make sure to include a clear description of your changes in your pull request. Aditionally, for code to be pushed, it is required that one reviewer approves your changes.
