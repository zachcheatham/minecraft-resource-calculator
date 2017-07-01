import json
import os
import time
import util

recipes = None
last_edit = 0

def save():
    with open("recipes.json", "w") as outfile:
        json.dump(recipes, outfile)
        print ("DEBUG: Wrote recipes.json")

def read():
    global last_edit

    if os.path.exists("recipes.json"):
        print ("DEBUG: Opening recipes.json...")
        with open("recipes.json", "r") as infile:
            global recipes
            recipes = json.load(infile)
    else:
        recipes = {}

    last_edit = time.time()

def set_recipe(item_name, ingredients=None, produced=-1):
    global recipes
    global last_edit

    if ingredients == None:
        recipes[item_name] = None
    else:
        recipes[item_name] = {"r": ingredients, "p": produced}

    last_edit = time.time()
    save()

def remove_recipe(item_name):
    global recipes
    global last_edit

    del recipes[item_name]

    last_edit = time.time()
    save()

def recipe_exists(item_name):
    global recipes
    return item_name in recipes.keys()

def have_missing(item_name):
    global recipes

    if item_name in recipes.keys():
        if recipes[item_name] != None:
            for ingredient, amount in recipes[item_name]["r"].items():
                if have_missing(ingredient):
                    return True
    else:
        return True

    return False

def get_last_edit():
    global last_edit
    return last_edit

def get_known_items():
    global recipes
    return recipes.keys()

def get_missing_recipes(item_name):
    global recipes

    missing = []

    if item_name in recipes.keys():
        recipe_data = recipes[item_name]
        if recipe_data != None:
            for ingredient, amount in recipe_data["r"].items():
                missing = util.merge_lists(get_missing_recipes(ingredient), missing)
    else:
        missing.insert(0, item_name)

    return missing

def get_recipe(item_name):
    global recipes
    return recipes[item_name]

def get_excess(item_name, excess):
    if item_name in excess.keys():
        return excess[item_name]
    else:
        return 0

def adjust_excess(item_name, adjustment, excess):
    if item_name in excess.keys():
        excess[item_name] += adjustment
        if excess[item_name] <= 0:
            del excess[item_name]
    elif adjustment > 0:
        excess[item_name] = adjustment

def add_craft(item_name, produced, required_items, depth):
    # Make sure array is large enough
    while len(required_items) <= depth:
        required_items.append({})

    if item_name in required_items[depth].keys():
        required_items[depth][item_name] += produced
    else:
        required_items[depth][item_name] = produced

def craft(item_name, qty, required_items, excess, depth=0, single=False):
    print ("Crafting", item_name)
    # Pull item's recipe
    recipe = get_recipe(item_name)

    # Check if we have any excess
    needed = qty - get_excess(item_name, excess)
    if needed < 0:
        needed = 0

    # Remove it from excess since we're using it
    used = qty - needed
    if used > 0:
        adjust_excess(item_name, -used, excess)
    elif used < 0:
        print ("Programming Error: We used a negative excess!")
        raise

    # Craft as needed
    while needed > 0:
        #print ("[debug] Performing craft of {}".format(item_name))

        if not single:
            # Loop through each ingredient that needs crafted
            for ingredient, ingredient_qty in recipe["r"].items():
                ingredient_recipe = get_recipe(ingredient)
                if ingredient_recipe != None:
                    # Craft that ingredient
                    craft(ingredient, ingredient_qty, required_items, excess, depth+1)

        # Loop through each ingredient that doesn't need crafted
        for ingredient, ingredient_qty in recipe["r"].items():
            ingredient_recipe = None
            if not single:
                ingredient_recipe = get_recipe(ingredient)

            if ingredient_recipe == None:
                # Check excess
                ingredient_needed = ingredient_qty - get_excess(ingredient, excess)
                if ingredient_needed < 0:
                    ingredient_needed = 0

                # Remove used excess
                ingredient_used = ingredient_qty - ingredient_needed
                if ingredient_used > 0:
                    adjust_excess(ingredient, -ingredient_used, excess)
                elif ingredient_used < 0:
                    print ("Programming Error: We used a negative ingredient excess!")
                    raise

                # Add needed to next step in list
                add_craft(ingredient, ingredient_needed, required_items, depth + 1)

        # Add craft to list
        add_craft(item_name, recipe["p"], required_items, depth)

        # take away from needed
        needed -= recipe["p"]

    # Add leftover from crafting to excess
    if needed < 0:
        adjust_excess(item_name, abs(needed), excess)

    # Return
    if depth == 0:
        return (required_items, excess)

def item_in_steps(item_name, steps):
    for step in range(0, len(steps)):
        if item_name in steps[step].keys():
            return step
    return None

def organize_items_to_steps(required_items):
    steps = []
    step = -1
    to_delete = []

    # Intitialize steps array
    for i in range(0, len(required_items)):
        steps.append({})

    # Iterate our crafting depth
    for i in range(len(required_items) - 1, -1, -1):
        step = len(required_items) - 1 - i # Step number is the inverse of our crafting depth

        # Iterate through each item
        for item, qty in required_items[i].items():
            # Check if item already exists in list
            existing_step = item_in_steps(item, steps)
            if existing_step == None: # Item isn't in steps yet
                steps[step][item] = qty
            elif existing_step == step: # Item already exists in this step (idk how this would happen)
                steps[step][item] += qty
            elif existing_step < step: # Item exists in earlier step
                # Merge item to earlier step
                steps[existing_step][item] += qty
            elif existing_step > step: # Item exists in later step (idk how this would happen either)
                # Merge later step to current step
                steps[step][item] = qty + steps[existing_step][item]
                # Delete item from later step
                del steps[existing_step][item]

    # Move all raw materials to very first step
    steps.insert(0, {}) # Insert empty dict at begining
    for step in range(1, len(steps)):
        for item, qty in steps[step].items():
            # Raw is an item without a recipe
            recipe = get_recipe(item)
            if recipe == None:
                steps[0][item] = qty # Copy it to the first step
                to_delete.append(item) # Queue it for deletion (can't delete while iterating)

        # Handle the delete Queue
        for item in to_delete:
            del steps[step][item]
        del to_delete[:] # Empty the delete array (for reuse)

    # Delete empty steps
    for step in range(1, len(steps)):
        if len(steps[step]) == 0:
            to_delete.append(step) # Queue for deletion (can't delete while iterating)

    # Handle delete queue
    for step in to_delete:
        del steps[step]

    return steps
