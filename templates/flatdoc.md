title: Pinoy Cuisines API
---

# Pinoy Cuisines API

A RESTful API for browsing Filipino dishes and their ingredients.

---

## Endpoints

### GET `/dishes`

Returns all dishes.

### POST `/dishes`

Add new dishes (in JSON array format).

### GET `/dishes/{dish_name}`

Get dish details by name (case-insensitive).

### GET `/dishes/{id}`

Get dish details by ID.

### PUT `/dishes/{id}`

Update a dish's information and ingredients.

### DELETE `/dishes/{id}` or `/dishes/{dish_name}`

Delete a dish.

### GET `/ingredients/{ingredient_name}`

Search for dishes using a specific ingredient.

---

## Notes

- All responses are in JSON.
- Use lowercase for ingredient and dish name searches.
