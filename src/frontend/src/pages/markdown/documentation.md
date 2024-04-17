# Weather App: API Documentation

This is the documentation for the Weather API.

---

## Registering a User

**Request type:** POST

**Request body schema:** `application/json`

### API call

```
http://localhost:5000/api/v2/users/register
```

#### Request body

- **`username`**
  - **Type:** String
  - **Required:** Yes
  - **Description:** A unique username.
- **`email`**
  - **Type:** String (Email format)
  - **Required:** Yes
  - **Description:** A unique email address.
- **`password`**
  - **Type:** String
  - **Required:** Yes
  - **Description:** A unique password.

#### Example response

```
{
  "message": "User registered successfully."
}
```

##### Response fields

- `message`: A simple confirmation message.

#### Responses

- `200 - Successful Response`
  - Response schema: `application/json`
    - Any
- `422 - Validation Error`
  - Response schema: `application/json`
    - `detail`
      - `detail.loc`
        - Type: Array of string or integers
        - Required: Yes
      - `detail.msg`
        - Type: String
        - Required: Yes
      - `detail.type`
        - Type: String
        - Required: Yes

---

## Logging in a User

**Request type:** POST

**Request body schema:** `application/x-www-form-urlencoded`

### API call

```
http://localhost:5000/api/v2/users/login
```

#### Request body

- **`grant_type`**
  - **Type:** String or null
  - **Required:** No
- **`username`**
  - **Type:** String
  - **Required:** Yes
  - **Description:** A unique username.
- **`password`**
  - **Type:** String
  - **Required:** Yes
  - **Description:** A unique password.
- **`scope`**
  - **Type:** String (Default: `""`)
  - **Required:** No
- **`client_id`**
  - **Type:** String or null
  - **Required:** No
- **`client_secret`**
  - **Type:** String or null
  - **Required:** No

#### Example response

```
{
  "message": "User successfully logged in.",
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzdHJpbmciLCJpZCI6MSwiZXhwIjoxNzEzMzUxMDY3fQ.WXD0-EVnIuYr9acZH0JTkvgoAeizZWm-OYSn-QPCSn0",
  "token_type": "bearer"
}
```

##### Response fields

- `message`: A simple confirmation message.
- `access_token`: A JSON Web Token (JWT), to be used for user authentication.
- `token_type`: The type of the access token, typically `bearer`.

#### Responses

- `200 - Successful Response`
  - Response schema: `application/json`
    - `message`
      - Type: String
      - Required: Yes
    - `access_token`
      - Type: String
      - Required: Yes
    - `token_type`
      - Type: String
      - Required: Yes
- `422 - Validation Error`
  - Response schema: `application/json`
    - `detail`
      - `detail.loc`
        - Type: Array of string or integers
        - Required: Yes
      - `detail.msg`
        - Type: String
        - Required: Yes
      - `detail.type`
        - Type: String
        - Required: Yes

---

## Getting a User Profile

**Request type:** GET

### API call

```
http://localhost:5000/api/v2/users/profile
```

#### Authorisations

- OAuth2PasswordBearer
  - Flow type: `password`
  - Token URL: `api/v2/users/login`

#### Example response

```
{
  "user": "string",
  "credits": 2000
}
```

##### Response fields

- `user`: The username of the account being returned.
- `credits`: The credit balanced of the account.

#### Responses

- `200 - Successful Response`
  - Response schema: `application/json`
    - Any

---

## Updating a User Profile

**Request type:** PUT

**Request body schema:** `application/json`

### API call

```
http://localhost:5000/api/v2/users/profile
```

#### Request body

- **`username`**
  - **Type:** String
  - **Required:** No
  - **Description:** A unique username.
- **`email`**
  - **Type:** String
  - **Required:** No
  - **Description:** A unique email address.

---

## Deleting a User Profile

**Request type:** DELETE

### API call

```
http://localhost:5000/api/v2/users/profile
```

#### Authorisations

- OAuth2PasswordBearer
  - Flow type: `password`
  - Token URL: `api/v2/users/login`

#### Example response

```
{
  "message": "User deleted successfully."
}
```

##### Response fields

- `message`: A simple confirmation message.

#### Responses

- `200 - Successful Response`
  - Response schema: `application/json`
    - Any
