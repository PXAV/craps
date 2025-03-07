# Important Notice!
**This project is no longer maintained.**

# Craps
> Developed by pxav (c) 2021

Craps is a popular dice game, mainly played in the USA. It is considered an adoption of the western European gambling game Hazard, whose origins are obscure. Some sources date it back to the Crusades, however it is confirmed that British colonialists brought it to the new land in about 1805. This small application allows you to play the game at home without having to go to a casino.

![Craps Main Menu Screenshot](https://github.com/PXAV/craps/blob/master/resources/github/main_menu_screenshot.png)
> Example screenshot of the main menu in dark theme. Please note that this is alpha footage and everything is subject to change.

### Rules
* You start with two dices. If their sum is 7 or 11, you win. 2, 3 or 12 will make you lose immediately. The game ends in both of those cases.
* For any other case, you will throw the dice infinitely, till
    1. The sum is equal to 7: You lose.
    2. The sum is equal to your first sum: You win.

### Playing
Currently, there is no stable release available for Craps. You will find one [on the releases page](https://github.com/PXAV/craps/releases) once available. 

To test the game in an unstable state, clone the repository from GitHub:
```shell
mkdir craps
cd craps
git clone https://github.com/PXAV/craps.git 
```
Make sure you have ``pip3`` available from your command line and install the required dependencies:
````shell
pip3 install -r requirements.txt
````

Make sure the ``resources`` folder is available in the main directory and run `main.py` (recommended version for venv is 3.9)
````shell
python3 main.py
````

### Features
The main task was to wrap the game into an appealing user interface using python's built-in ``tkinter`` library.
* A full-blown theming system allowing the user to create custom color themes using simple [TOML](https://toml.io/en/) configurations.
* Automatic theme detection based on the operating system's preferences (dark/light theme)
* Custom buttons and widgets creating a modern and unique look of the app (based on [Pillow](https://python-pillow.org/))
* Extensible user preference API (used for locale and theme handling) 
* Upcoming: Detailed, SQL-based statistics system 
* Upcoming: Locale-system
* Note: Game mechanics are not fully implemented yet.
