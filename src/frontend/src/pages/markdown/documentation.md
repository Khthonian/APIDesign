# Weather App: API Documentation

This is the documentation for the Weather API.

## Contents

- [Registering a User](#registering-a-user)
- [Logging in a User](#logging-in-a-user)
- [Getting a User Profile](#getting-a-user-profile)
- [Updating a User Profile](#updating-a-user-profile)
- [Deleting a User Profile](#deleting-a-user-profile)
- [Getting a User's Credit Balance](#getting-a-users-credit-balance)
- [Purchasing User Credits](#purchasing-user-credits)
- [Getting a User's Locations](#getting-a-users-locations)
- [Adding a New Location](#adding-a-new-location)
- [Deleting a User's Location](#deleting-a-users-location)

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

[↑ Return to top](#weather-app-api-documentation)

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
- `access_token`: A JSON Web Token access token, to be used for user authentication.
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

[↑ Return to top](#weather-app-api-documentation)

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

[↑ Return to top](#weather-app-api-documentation)

---

## Updating a User Profile

**Request type:** PUT

**Request body schema:** `application/json`

### API call

```
http://localhost:5000/api/v2/users/profile
```

#### Authorisations

- OAuth2PasswordBearer
  - Flow type: `password`
  - Token URL: `api/v2/users/login`

#### Request body

- **`username`**
  - **Type:** String
  - **Required:** Yes
  - **Description:** A unique username.

#### Example response

```
{
  "user": {
    "username": "newusertest"
  },
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzdHJpbmcyIiwiaWQiOjEsImV4cCI6MTcxMzM2MTA0NX0.FwLKZkLAB_grCzqHr9oO_B2PIH_xka3HfXSqsHCuRYA",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzdHJpbmcyIiwiaWQiOjEsInJlZnJlc2giOnRydWUsImV4cCI6MTcxMzk2NDA0NX0.Kxvtp0nIY0vPp2GOQ-ZKkbALqQQGSEKo9JxvDzl8p1o"
}
```

##### Response fields

- `user`
  - `user.username`: The new, updated username for the account.
- `access_token`: A JSON Web Token access token, to be used for user authentication.
- `refresh_token`: A JSON Web Token refresh token, to be used to acquire additional access tokens.

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

[↑ Return to top](#weather-app-api-documentation)

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

[↑ Return to top](#weather-app-api-documentation)

---

## Getting a User's Credit Balance

**Request type:** GET

### API call

```
http://localhost:5000/api/v2/credits
```

#### Authorisations

- OAuth2PasswordBearer
  - Flow type: `password`
  - Token URL: `api/v2/users/login`

#### Example response

```
{
  "credits": 2000
}
```

##### Response fields

- `credits`: The account balance.

#### Responses

- `200 - Successful Response`
  - Response schema: `application/json`
    - Any

[↑ Return to top](#weather-app-api-documentation)

---

## Purchasing User Credits

**Request type:** POST

### API call

```
http://localhost:5000/api/v2/credits/purchase?amount={amount}
```

#### Authorisations

- OAuth2PasswordBearer
  - Flow type: `password`
  - Token URL: `api/v2/users/login`

#### Query parameters

- **`amount`**
  - **Type:** Integer
  - **Required:** Yes
  - **Description:** The amount of credits to purchase.

#### Example response

```
{
  "message": "100 credits purchased successfully."
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

[↑ Return to top](#weather-app-api-documentation)

---

## Getting a User's Locations

**Request type:** GET

### API call

```
http://localhost:5000/api/v2/users/locations
```

#### Authorisations

- OAuth2PasswordBearer
  - Flow type: `password`
  - Token URL: `api/v2/users/login`

#### Example response

```
[
  {
    "temperature": 282.14,
    "city": "Retford",
    "latitude": 53.31880187988281,
    "user_id": 1,
    "timestamp": "2024-04-17T14:08:30.608436",
    "country": "United Kingdom",
    "id": 1,
    "description": "You may want to bring a waterproof jacket and some rain boots if you're heading out in Retford today. Stay dry and cozy!",
    "longitude": -0.9824000000953674
  }
]
```

##### Response fields

- A list of locations.
  - `temperature`: The temperature of the location, in Kelvin.
  - `city`: The name of the location.
  - `latitude`: The latitude of the user's IP address.
  - `user_id`: The ID of the user's account.
  - `timestamp`: The timestamp of the call request.
  - `country`: The name of the country.
  - `id`: The ID of the location in the database.
  - `description`: The AI-generated description message from OpenAI.
  - `longitude`: The longitude of the user's IP address.

#### Responses

- `200 - Successful Response`
  - Response schema: `application/json`
    - Any

[↑ Return to top](#weather-app-api-documentation)

---

## Adding a New Location

**Request type:** POST

### API call

```
http://localhost:5000/api/v2/users/locations
```

#### Authorisations

- OAuth2PasswordBearer
  - Flow type: `password`
  - Token URL: `api/v2/users/login`

#### Example response

```
{
  "message": "Location added successfully",
  "weather_info": "You may want to bring a waterproof jacket and some rain boots if you're heading out in Retford today. Stay dry and cozy!",
  "temperature": 282.14,
  "latitude": 53.31880187988281,
  "longitude": -0.9824000000953674,
  "ip": "109.147.83.165"
}
```

##### Response fields

- `message`: A simple confirmation message.
- `weather_info`: The AI-generated description message from OpenAI.
- `temperature`: The temperature of the location, in Kelvin.
- `latitude`: The latitude of the user's IP address.
- `longitude`: The longitude of the user's IP address.
- `ip`: The IP address of the user.

#### Responses

- `200 - Successful Response`
  - Response schema: `application/json`
    - Any

[↑ Return to top](#weather-app-api-documentation)

---

## Deleting a User's Location

**Request type:** DELETE

### API call

```
http://localhost:5000/api/v2/users/locations/{location_id}
```

#### Authorisations

- OAuth2PasswordBearer
  - Flow type: `password`
  - Token URL: `api/v2/users/login`

#### Example response

```
{
  "message": "Location deleted successfully."
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

[↑ Return to top](#weather-app-api-documentation)

---
