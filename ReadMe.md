# Schedule One Helper
(Name WIP)

## Overview
This tool is aimed at becoming a companion for the Game Schedule 1. It is currently a command-line interface designed to let the user input recepies for mixing he comes across and visualize them as a directed map.

## Setup
To run the Tool locally, follow these steps:

### 1. Clone the Repository:

```python
git clone https://github.com/Rexxic/Schedule-1-Helper.git
cd Schedule-1-Helper
```
### 2. Install Dependencies:
Ensure you have Python installed. Then, install the required dependencies:

```python
pip install -r Requirements.txt
```

### 3. Run the Application:
Execute the main script to start the CLI:
```python
python main.py
```
### 4. ...

### 5. Profit!

## Current Scope

The current version of the DrugSet Companion Tool includes the following features:

- **Command-Line Interface**: Provides a simple CLI for user interaction.
- **Drug Management**: Allows adding and retrieving drug details, including their values and relationships with other drugs.
- **Data Persistence**: Saves the current drug set to a JSON file and loads it upon startup.
- **Visualization**: Rendering of the dependencies using Pyvis to create interactive html.

### Commands

- ``help``: Displays available commands.
- ``add_drug``: Adds a drug with optional value, base drug, and ingredient.
- ``get_drug``: Retrieves details of a specified drug.
- ``save``: Saves the current drug set to a file.
- ``render``: Placeholder for rendering drug network visualizations.
- ``exit``: Exits the program.

## Future Heading
The tool should be Webhostable and provide a clean interface where the User can see the Map with a toolbar at the side. Here he should be able to quickly input crafting recepies by clicking or typing the ingridients and set a price. Nodes should be clickable and display all their avaliable information in the toolbar, where the user also should be able to make changes. The webserver may either only source the js/html, offloading processing to the user or provide an REST-Api the frontend can use to process user actions. In this case the Server should be truly stateless.