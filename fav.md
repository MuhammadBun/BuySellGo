# Get Favorite Lists:

The Get Favorite Lists API allows authenticated users to retrieve a list of all favorite lists created by the user. The API returns a JSON object that includes information about each favorite list, such as its unique ID, title, associated post, and creation date.

**HTTP Method**: GET

**Endpoint**: http://127.0.0.1:8000/favorite_lists/get_favorite_list/

**Permissions**: This API requires the user to be authenticated.

**Response Codes**:

200 OK: Returns the list of all favorite lists in the JSON format.
401 Unauthorized: If the user is not authenticated.


# Create a New Favorite List:

The Create a New Favorite List API allows authenticated users to create a new favorite list. The API requires the user to provide the favorite list's title and associated post.

**HTTP Method**: POST

**Endpoint**: http://127.0.0.1:8000/favorite_lists/create_favorite_list/

**Permissions**: This API requires the user to be authenticated.

**Response Codes**:

201 Created: Returns the created favorite list in the JSON format.
400 Bad Request: If the provided data is invalid.
401 Unauthorized: If the user is not authenticated.

# Update a Favorite List:

The Update a Favorite List API allows authenticated users to update an existing favorite list. The API requires the user to provide the favorite list's new title and associated post.

**HTTP Method**: PUT

**Endpoint**: http://127.0.0.1:8000/favorite_lists/update_favorite_list/int:pk

**Permissions**: This API requires the user to be authenticated and the owner of the favorite list.

**Response Codes**:

200 OK: Returns the updated favorite list in the JSON format.
400 Bad Request: If the provided data is invalid.
401 Unauthorized: If the user is not authenticated or not the owner of the favorite list.
404 Not Found: If the favorite list does not exist.

# Delete a Favorite List:

The Delete a Favorite List API allows authenticated users to delete an existing favorite list. The API requires the user to be the owner of the favorite list.

**HTTP Method**: DELETE

**Endpoint**: http://127.0.0.1:8000/favorite_lists/delete_favorite_list/int:pk

**Permissions**: This API requires the user to be authenticated and the owner of the favorite list.

**Response Codes**:

204 No Content: If the favorite list is successfully deleted.
401 Unauthorized: If the user is not authenticated or not the owner of the favorite list.
404 Not Found: If the favorite list does not exist.