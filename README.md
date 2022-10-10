# Toy Retirement App

A toy retirement app built for Intro to FinTech1 for the UCF M.S. FinTech. 

Creating using PySimpleGUI (never again), and matplotlib.

Packaged using PyInstaller
Pyinstaller commmand used:

```python -m PyInstaller -F --add-data "asset_allocation.csv;data" --add-data "life_expect.csv;data" --hidden-import 'Retire_Calc' --hidden-import 'helpers' --onefile --noconsole  GUI.py```


![screen1](screen1.jpeg)

![screen2](screen2.jpeg)
