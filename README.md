# Url
https://fynd-intv.herokuapp.com/
# Logs
heroku logs --tail --app fynd-intv
# To scale heroku instance
heroku ps:scale web=1 --app fynd-intv

# Deployment link
https://fynd-intv.herokuapp.com/

**RESTful API that tracks jogging times of users**
### Project Structure & Setup

```
- Models/ 
   ("models": objects, functions which connect to database, 
    function as data abstraction layer)
- Tests/
   (tests repository)
- Routes/
   ("views": implementation of API validation, 
    RESTful & json responses)
- main.py
   (main application, route setting)
- requirements.txt
   (Pythonic requierments)
- DB table stucture
    (table_stucture.txt)
```

Install requirements by:
 
`pip install -r requirements.txt`

Prerequisites:
* RUN `run.py` to run server

#### CURD /users routes
    ```
    `GET https://fynd-intv.herokuapp.com/users`
    
    ```
    [{'id': 1, "name: 'amichay}]
    ```

#### CURD /auth : Authentication endpoints

* login is done by POST to `/auth` with payload that includes username & password. The login endpoint returns JWT access-token (which is short-lived) amd refresh-token used for getting a new access-token.
* Example response payload:
    
    `{'access_token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo0OCwiZXhwIjoxNTU5NjQ3MTI1LCJpYXQiOjE1NTk2NDUzMjUsIm5hbWUiOiJBbWljaGF5IE9yZW4iLCJlbWFpbCI6ImFtaWNoYXkub3Jlbis0Mzc4QGdtYWlsLmNvbSIsInNjb3BlcyI6WyJ1c2VyIl19.2arsjawnHlPT0StNxTkyO6kEdDImqgCnFPjVbcRidEs', 'refresh_token': '12a6c653839e03be9cfa56d35eed26931668b174a58bb589'}
    ` 
* `access_token` should be used in the header for all protected calls as followes:

    ```buildoutcfg
     headers = {"Authorization": f"Bearer {access_token}"}
    ```
* GET `/auth/verify` validates the access-token and responds with `{'valid': True}`
* GET `/auth/me` returns the user information attached to the token.
* GET `/auth/refresh` returns a new access-token. Keep in mind that the fresh-token is not expired in this basic implementation.
* An example of The JWT claims include:

    ```buildoutcfg
    {
      "user_id": 48,
      "exp": 1559647125,
      "iat": 1559645325,
      "name": "Amichay Oren",
      "username": "amichay.oren+4378@gmail.com",
    }
    ```
    * Be advised that the scope is presented, however scope is validated against what appears in the user_id database, and not what is passed in the scope. This means that if user scopes are changed, while they might not be reflected in the JWT claims (yet) they would still impact the authorization.
* Failure to authorize access to resource will return HTTP 403.

* POST `/register` to register user
    ```request
    {
        "name": "gilu",
        "username": "gilu@ggmail.com",
        "password": "Test@123"
    }
    
    ```
    ```response
    {
        "User created successfuly": "User 1: gilu@ggmail.com"
    }
    
    ```
* POST `/update_user/<user_id>` update user information (only for admin role with token authentication).
    ```request
    {
        "name": "Test",
        "email: "Test@test.com"
    }
    ```
* DELETE `/users/<user_id>` deactivate user information (only for admin role with token authentication).
#### CURD /Movies : Authentication required

* Movies API with authentication and endpoints

* POST `/upload` to upload movies data through file (only for admin role with token authentication)
    ```request
    {
        file upload
    }
    ```
* POST `/search_movies_id/<movie_id>` search movie (only for admin role with token authentication).
* POST `/add_movies` addm movies (only for admin role with token authentication).
    ```request
    {
        "movie_name": "Test movie",
        "popularity": 9,
        "imdbScore": 8.3,
        "genre": ["Action"],
        "director": "Test"
    }
* POST `/update_movies` update movies (only for admin role with token authentication).
    ```request
    {
        "id": 109,
        "movie_name": "Test movie changed",
        "popularity": 9,
        "imdbScore": 8.3,
        "genre": ["Action"],
        "director": "Test"
    }
#### Database Login Creds

* email nadivo1208@elastit.com
* pass Redmi@007

