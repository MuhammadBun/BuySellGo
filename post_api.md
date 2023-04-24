# **Get All Posts API**:

The Get All Posts API allows authenticated users to retrieve a list of all posts that have been created on the platform. The API returns a JSON object that includes information about each post, such as its unique ID, title, content, author, creation date, and any associated tags or categories.

**HTTP Method**: GET

**Endpoint**: http://127.0.0.1:8000/post/list_post/

**Permissions**:  This API requires the user to be authenticated.

**Response Codes:**

1. 200 OK: Returns the list of all posts in the JSON format.
2. 401 Unauthorized: If the user is not authenticated.



# **Get a Post by ID API**:

The Get a Post by ID API allows authenticated users to retrieve a specific post by its unique ID. The API returns a JSON object that includes information about the post, such as its title, content, author, creation date, and any associated tags or categories.

**HTTP Method**: GET

**Endpoint**: http://127.0.0.1:8000/post/get_user_post/

**Permissions**: This API requires the user to be authenticated and the owner of the post.

**Response Codes**:

1. 200 OK: Returns the post in the JSON format.
2. 401 Unauthorized: If the user is not authenticated or not the owner of the post.
3. 404 Not Found: If the post does not exist.

# **Create a New Post API**:

The Create a New Post API allows authenticated users to create a new post. The API requires the user to provide the post's title, content, author, and any associated tags or categories.

**HTTP Method**: POST

**Endpoint**: http://127.0.0.1:8000/post/new_post/

**Permissions**: This API requires the user to be authenticated.

**Response Codes**:

1. 201 Created: Returns the created post in the JSON format.
2. 400 Bad Request: If the provided data is invalid.
3. 401 Unauthorized: If the user is not authenticated.

# **Update a Post API**:

The Update a Post API allows authenticated users to update an existing post. The API requires the user to provide the post's new title, content, author, and any associated tags or categories.

**HTTP Method**: PUT

**Endpoint**: http://127.0.0.1:8000/post/post_pk/int:pk


**Permissions**: This API requires the user to be authenticated and the owner of the post.

**Response Codes**:

1. 200 OK: Returns the updated post in the JSON format.
2. 400 Bad Request: If the provided data is invalid.
3. 401 Unauthorized: If the user is not authenticated or not the owner of the post.
4. 404 Not Found: If the post does not exist.

# **Delete a Post API**:

The Delete a Post API allows authenticated users to delete an existing post. The API requires the user to be the owner of the post.

**HTTP Method**: DELETE

**Endpoint**: http://127.0.0.1:8000/post/post_pk/9

**Permissions**: This API requires the user to be authenticated and the owner of the post.

**Response Codes**:

1. 204 No Content: If the post is successfully deleted.
2. 401 Unauthorized: If the user is not authenticated or not the owner of the post.
3. 404 Not Found: If the post does not exist.


# **Get Posts by User ID**:

The Get Posts by User ID API allows authenticated users to retrieve a list of all posts created by a specific user. The API returns a JSON object that includes information about each post, such as its unique ID, title, content, author, creation date, and any associated tags or categories.

**HTTP Method**: GET

**Endpoint**: http://127.0.0.1:8000/post/get_user_post/int:pk

**Permissions**: This API requires the user to be authenticated and the owner of the post.

**Response Codes**:

1. 200 OK: Returns the list of all posts in the JSON format.
2. 401 Unauthorized: If the user is not authenticated or not the owner of the post.
3. 404 Not Found: If the user does not exist or has not created any posts.




