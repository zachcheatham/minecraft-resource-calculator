@echo off
echo Compiling...

pyuic5 -o ..\python\ui\designer\new_craft_dialog.py new_craft_dialog.ui
pyuic5 -o ..\python\ui\designer\recipe_dialog.py recipe_dialog.ui
pyuic5 -o ..\python\ui\designer\main_window.py main_window.ui

echo Done.
