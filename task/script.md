# Video Script

Hello and welcome to my demonstration of my API design. The design I have chosen allows a user to make a request via the client, to retrieve their weather conditions. Using a combination of external APIs for geolocation, weather retrieval and AI chat completion, a customised description is returned to the user with the weather information.

Docker containers and images were used as a crucial part of the implementation, allowing for a simple artefact launch, and emulating a common development and deployment technique used in the industry.

A simple React application was built for the frontend representation of the API, comprising of a home page and the documentation page. A user is able to register, login, update their username, and use the service via this home page. The registration process has particular requirements from the user, such as uniqueness and email validation.

For testing purposes, the number of credits a request would cost is a single credit. In production, the actual cost is 400 credits.

The user's locations are displayed to them in a tabular format. A notable feature of the table is that it uses pagination; for demonstration purposes, the pagination limit was set to 2 rows, while in production, the limit will be set to 10.

It was important that at least one of each CRUD request was implemented. Accounts and locations can be deleted, the username can be updated; most functions of the application will use GET and POST requests.

As of the time of recording, a total of 70 commits have been made to the project repository. The project has made limited use of GitHub issues and extensive use of GitHub Actions. Special care was given to the workflow jobs used in the CI/CD process, determining executions, conditions, and necessary environmental variables.

Docker Hub was a notable integration in the version control process, to manage the built images alongside the source code itself. Docker Hub also allows for simple vulnerability checking via Docker Scout.

Both SwaggerUI and Redoc were used in the early testing and documentation phases of the project. Extra care was given to ensure that each endpoint used a response body schema to improve type validations.

The API documentation was made using the React Markdown library, allowing me to write the documentation faster and also in a more modular fashion if I wished to do so. A UML diagram was made to represent the structure of the entire application with particular highlights for notable integrations.
