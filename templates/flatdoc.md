title: Pinoy Cuisines API
---

# Pinoy Cuisines API

A RESTful API for browsing Filipino dishes and their ingredients.


# Endpoints

### DISPLAY ALL DISHES
Displays all dishes in the database.

`https://pinoy-cuisines-api.onrender.com/dishes`


### SEARCH DISHES BY INGREDIENTS
Search for dishes using a specific ingredient. All entries with searched
ingredient will appear.

`https://pinoy-cuisines-api.onrender.com/ingredients/{ingredient_name}`

### ADD NEW DISHES

Add new dishes to the database. (through Post Request 'POST')

JSON File should be formatted as:


        {
            "name": "Bulalo",
            "classification": "Soup",
            "methodology": "Boiling",
            "origin": "Batangas",
            "taste_profile": "Savory, Rich",
            "description": "Beef shank soup with bone marrow and vegetables.",
            "ingredients": {
            "meat": ["beef shank", "bone marrow"],
            "vegetable": ["corn", "cabbage", "potato"]
            }
        }

### SEARCH DISH DETAILS BY NAME

Get specific dish details by name (case-insensitive).

`https://pinoy-cuisines-api.onrender.com/dishes/{dish_name}`

Output should be seen as:


        {
        "classification": "Meryenda",
        "description": "Buko ni Juan.",
        "id": 4,
        "ingredients": {
            "meat": [
            "None"
            ],
            "vegetable": [
            "None"
            ]
        },
        "methodology": "Shake",
        "name": "Buko Shake",
        "origin": "Nationwide",
        "taste_profile": "Sweet"
        }

### SEARCH DISH DETAILS BY ID

Get specific dish details by ID.

`https://pinoy-cuisines-api.onrender.com/dishes/{id}`

Output should be seen as:


        {
        "classification": "Main Dish",
        "description": "Meat marinated and simmered in vinegar, soy sauce, garlic, bay leaves, and peppercorns.",
        "id": 2,
        "ingredients": {
            "meat": [
            "pork",
            "chicken"
            ],
            "vegetable": [
            "garlic",
            "bay leaves"
            ]
        },
        "methodology": "Stewing",
        "name": "Adobo",
        "origin": "Nationwide",
        "taste_profile": "Savory, Sour"
        }


### UPDATE DISH DETAILS

Update a dish's information and ingredients (through Post Request 'PUT').

- Update Dish Details By ID 
- Update Dish Details By Name


### DELETE DISHES

Delete a dish (through Post Request 'DELETE').

- Delete Dish Details By ID 
- Delete Dish Details By Name

## Notes

- All responses are in JSON.
- Use lowercase for ingredient and dish name searches.
