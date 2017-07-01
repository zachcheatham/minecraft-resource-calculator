@echo off
echo Compiling...

pyuic5 -o ..\python\ui\qt\designer\new_craft_dialog.py new_craft_dialog.ui
pyuic5 -o ..\python\ui\qt\designer\recipe_dialog.py recipe_dialog.ui
pyuic5 -o ..\python\ui\qt\designer\main_window.py main_window.ui
pyuic5 -o ..\python\ui\qt\designer\recipe_list_dialog.py recipe_list_dialog.ui


echo Done.
