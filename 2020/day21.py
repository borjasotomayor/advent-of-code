"""
Day 21
https://adventofcode.com/2020/day/21

1st star: 00:19:41
2nd star: 00:42:54

Not gonna lie, for part 1 I just kinda threw set operations at the wall
to see what would stick, and somehow stumbled upon the answer relatively
quickly. It took me a bit longer to understand exactly what was going on,
and arrive at part 2. The code below is a *very* cleaned up version of
the code I originally wrote.
"""

import util
import math
import sys
import re

from util import log


def read_foods(foods_txt):
    """
    Read the provided input into a list of (ingredients, allergens) tuples
    """
    foods = []
    for line in foods_txt:
        ingredients_txt, allergens_txt = line.split(" (contains ")
        ingredients = ingredients_txt.split()
        allergens = allergens_txt[:-1].split(", ")

        foods.append((ingredients, allergens))

    return foods


def compute_allergens(foods):
    """
    Find out what ingredient is associated with each allergen
    """

    # Create a dictionary mapping allergens to lists
    # of ingredients that may contain that allergen
    allergen_foods = {}
    for ingredients, allergens in foods:
        for allergen in allergens:
            allergen_foods.setdefault(allergen, []).append(set(ingredients))

    # For each allergen, compute the intersection of the lists
    # computed above. This will give us the set of ingredienta
    # that could contain that allergen
    candidate_ingredients = {}
    for allergen in allergen_foods:
        candidate_ingredients[allergen] = set.intersection(*allergen_foods[allergen])

    # Repeatedly find an allergen that can only be matched to a single
    # ingredient, and remove that ingredient from the list of candidate
    # ingredients for all the other allergens.
    allergens = {}
    while len(candidate_ingredients) > 0:

        for single_allergen, cings in candidate_ingredients.items():
            if len(cings) == 1:
                ingredient =  cings.pop()
                allergens[single_allergen] = ingredient
                break

        del candidate_ingredients[single_allergen]        

        for allergen in candidate_ingredients:
            if allergen != single_allergen:
                ingredient = allergens[single_allergen]
                candidate_ingredients[allergen].discard(ingredient)

    return allergens


def task1(foods_txt):
    foods = read_foods(foods_txt)

    # Compute the set of all ingredients
    all_ingredients = set()
    for ingredients, _ in foods:
        all_ingredients.update(ingredients)

    # Compute the set of ingredients that contain an allergent
    allergens = compute_allergens(foods)
    allergen_ingredients = set(allergens.values())

    # Compute the set of non-allergents
    non_allergens = all_ingredients - allergen_ingredients

    # Count up the ingredients that are non-allergents
    total = 0
    for ingredients, _ in foods:
        for ingredient in ingredients:
            if ingredient in non_allergens:
                total += 1

    return total


def task2(foods_txt):
    foods = read_foods(foods_txt)

    allergens = compute_allergens(foods)

    sorted_allergens = sorted(allergens.items(), key=lambda x:x[0])

    dangerous_ingredients = ",".join([x[1] for x in sorted_allergens])

    return dangerous_ingredients
    

if __name__ == "__main__":
    util.set_debug(False)

    sample = util.read_strs("input/sample/21.in", sep="\n")
    input = util.read_strs("input/21.in", sep="\n")

    print("TASK 1")
    util.call_and_print(task1, sample)
    util.call_and_print(task1, input)

    print("\nTASK 2")
    util.call_and_print(task2, sample)
    util.call_and_print(task2, input)
