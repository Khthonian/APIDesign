import React from "react";

function Documentation() {
  return (
    <div>
      <h1>Weather App</h1>
      <div>
        <h2>API Documentation</h2>
        <p>This is the documentation for the Weather API.</p>
        <div>
          <h3>Registering a User</h3>
          <div>
            <p>
              <b>Type:</b> POST
            </p>
          </div>
          <div>
            <h4>How to make an API call</h4>
            <div>
              <h5>API call</h5>
              <code>https://localhost:5000/api/v2/users/register</code>
              <h6>Request Body</h6>
              <table style={{ borderCollapse: 'collapse', width: '50%' }}>
                  <tr>
                      <td><code>username</code></td>
                      <td>required</td>
                      <td>A unique username.</td>
                  </tr>
                  <tr>
                      <td><code>email</code></td>
                      <td>required</td>
                      <td>A unique email address.</td>
                  </tr>
                  <tr>
                      <td><code>password</code></td>
                      <td>required</td>
                      <td>A unique password.</td>
                  </tr>
              </table>
              <h5>Example of API response</h5>
              <pre><code>
                {'{'} "message": "User registered successfully." {'}'}
              </code></pre>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Documentation;
