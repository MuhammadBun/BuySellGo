# Authentication
The authentication folder contains a set of APIs that allow users to authenticate and manage their accounts on the platform. This includes APIs for registering a new account, logging in to an existing account, logging out of the current session, and logging out of all active sessions.

The register API allows users to create a new account with the provided information, including email, password, username, bio, contact information, image, and account status. The login API allows users to authenticate by providing their email and password, and if successful, returns an authentication token that can be used to access protected resources. The logout API allows users to log out of the current session, while the logout all API allows users to log out of all active sessions across devices.

The authentication APIs are designed to be secure and reliable, using industry-standard encryption algorithms and authentication protocols to protect user data and prevent unauthorized access. These APIs are essential for any web application that requires user authentication and management, ensuring that only authorized users can access protected resources and that user accounts are managed securely and efficiently.

## Register
The **Register** API allows users to create a new account with the provided information, including email, password, username, bio, contact information, image, and account status. The email field is mandatory and must be a unique email address. The password must meet certain requirements, including having at least one lowercase and one uppercase letter, at least one number, and being at least 8 characters long. The username must be unique and must contain at least one letter and be at least 6 characters long.

If the provided email or username already exists in the database, the API will return an error message indicating that the user already exists. Once all of the required fields have been provided and validated, the API will create a new user account and return a success message indicating that the user has been registered.

The Register API is a secure and reliable way for users to create new accounts on the platform, ensuring that all information is validated and checked for uniqueness before the account is created.

**POST Create** - http://127.0.0.1:8000/auth/create-user/

## Login

The **Login API** allows users to authenticate to the platform by providing their email and password. Once authenticated, the API returns an authentication token that can be used to access protected resources.

The login process involves validating the provided email and password against the user database, and if the credentials are correct, generating and returning a unique authentication token. This token is used to identify the user in subsequent requests and allows them to access protected resources without the need to re-authenticate with their email and password.

The Login API is designed to be secure and reliable, using industry-standard encryption algorithms and authentication protocols to protect user data and prevent unauthorized access. This API is essential for any web application that requires user authentication, ensuring that only authorized users can access protected resources and that user accounts are managed securely and efficiently.

### **POST Login** - http://127.0.0.1:8000/auth/login/

## Logout & Logout All
The **Logout API** allows users to log out of their current session on the platform. This involves revoking the authentication token associated with the current session, thereby preventing any further access to protected resources using that token. Once logged out, the user must re-authenticate to access protected resources again.

The **Logout All** API allows users to log out of all active sessions on the platform. This involves revoking all authentication tokens associated with the user's account, thereby preventing any further access to protected resources using those tokens. This API is useful in situations where a user suspects their account has been compromised, or when they want to terminate all active sessions across devices.

Both the Logout and Logout All APIs are designed to be secure and reliable, using industry-standard encryption algorithms and authentication protocols to protect user data and prevent unauthorized access. These APIs are essential for any web application that requires user authentication and management, ensuring that user accounts are managed securely and efficiently.

### **POST Logout & Logout All** - http://127.0.0.1:8000/auth/logout/

## Update User Information
The **Update API** allows users to update their account information on the platform. This API accepts new values for the user's email, username, bio, contact information, and image, and updates these fields in the user's account.

The Update Info API validates the new information provided by the user and ensures that it meets any required constraints or standards. For example, the API might check that the new email address is not already in use by another account, or that the new username meets minimum length requirements.

The Update API is an important component of any user management system, allowing users to keep their account information up-to-date and relevant. It is designed to be secure and reliable, using industry-standard encryption algorithms and authentication protocols to protect user data and prevent unauthorized access.

### **Update** - http://127.0.0.1:8000/auth/update-user/5/



