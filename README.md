# Unibrowser

## Installation requirements
- Python 3.6 or higher
- We recommend that you use [Anaconda](https://www.anaconda.com/) to install the following Python 3 packages:
  - numpy (1.15.4 or higher)
  - PyQT5 (5.9.2 or higher)
  - basemap (1.2.0 or higher)  
  - These packages can be installed using the Anaconda Prompt as follows:
    ```console
    conda install numpy pyqt basemap
    ```

## Usage
To launch the Unibrowser GUI `cd` into the `src/` directory and run the following command:
```console
    python unibrowser_gui.py
```

## Novelty
Unibrowser's novelty lies in its potential to enable a suite of intelligent search and selection tools to make web browsing， data enttry and navigation more convenient and accessiuble。Unibrowser's objective is to select an item based on the answers to questions supplied via BCI. In its current incarnation Unibrowser is presented as a game in which the user is asked to choose a country (the desired item). Unibrowser's objective then is to determine the country based on answers to the questions it selects to ask the user. Unibrowser's UI is designed to zoom in and highlight countrties it believes to be the best guess based on the current state of the game. The game is won by Unibrowser when the country is found in N questions or less, otherwise the user wins. The model behind the Unibrowser game is general and adaptable and could be used to minimize the clicks needed by a user to perform an action for any number of complex computer navigation tasks.

Applications:
- Data Entry: Text fields and drop down boxes can be time consuming and tedious to navigate. Unibrowser provides a means to ask useful questions to quickly determine entries based on, a simple set of questions and prior behaviour (including EEG response to questions - see below).
- UI and Web Navigation: Operating Systems and Websites with complex UIs can be difficult to navigate and knowing where to look can be half or more of the problem， By curating a set of facts related to each menu and UI option， Unibrowser could be used to streamline the navigation process and make finding the right menus and options more straightforward by a direct line of questioning as to the users desired action。  
- Object Manipulations：Maps，schematics and 3D model manipulation could all be made easier with intelligent EEG response， quickly cutting down to the tools or region that the user wants to use or view。Examples include architectural and engineering plans where details such as materials and function of each element in the plan are stored in a searchable and relateable way in programmes such as AutoCad.
- Data Exploration: Related to data entry, Unibrowser could make learning important details from spreadsheets amd another databases more accessible and intuitive.

Areas for Development:
- Unibrowser's great strength in data acquisition lies in it's game format which should drive user engagement. By attempting to beat the system, Unibrowser is able to improve and gather new data that could help to enable novel features.
