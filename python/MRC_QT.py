import sys
import recipes

from ui.qt.init import start_application

if __name__ == "__main__":
    recipes.read()
    start_application()
