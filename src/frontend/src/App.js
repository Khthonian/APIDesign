import React, { useState } from 'react';
import axios from 'axios';

function App() {
    // State variables
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [loggedInUser, setLoggedInUser] = useState(null);
    const [error, setError] = useState('');

    // Function to handle user registration
    const registerUser = async () => {
        try {
            const response = await axios.post('http://localhost:5000/api/v2/users/register', {
                username: username,
                email: email,
                password: password,
            });
            console.log('User registered successfully:', response.data);
            // You can add additional logic after successful registration
        } catch (error) {
            setError('Registration failed. Please try again.');
        }
    };

    // Function to handle user login
    const loginUser = async () => {
      try {
          const formData = new FormData();
          formData.append('username', username);
          formData.append('password', password);
  
          const response = await axios.post('http://localhost:5000/api/v2/users/token', formData, {
              headers: {
                  'Content-Type': 'application/x-www-form-urlencoded',
              },
          });
  
          console.log('User logged in successfully:', response.data);
  
          // Store the access token in localStorage or sessionStorage
          localStorage.setItem('accessToken', response.data.access_token);
  
          setLoggedInUser(response.data);
      } catch (error) {
          console.error('Login failed:', error.response.data);
      }
  };

    // Function to display the currently logged-in user
    const displayCurrentUser = async () => {
      try {
          const response = await axios.get('http://localhost:5000/api/v2/users/profile', {
              headers: {
                  Authorization: `Bearer ${localStorage.getItem('accessToken')}`,
              },
          });
  
          console.log('Current user:', response.data);
  
          // Set the current user in state
          setLoggedInUser(response.data); // Assuming response.data.User contains the user data
  
      } catch (error) {
          setError('Failed to fetch current user.');
      }
  };

    return (
        <div>
            <h1>User Authentication</h1>
            <div>
                <h2>Register</h2>
                <input
                    type="text"
                    placeholder="Username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                />
                <input
                    type="email"
                    placeholder="Email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                />
                <input
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                />
                <button onClick={registerUser}>Register</button>
            </div>
            <div>
                <h2>Login</h2>
                <input
                    type="text"
                    placeholder="Username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                />
                <input
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                />
                <button onClick={loginUser}>Login</button>
            </div>
            {loggedInUser ? (
                <div>
                    <h2>Welcome, {loggedInUser.User}</h2>
                    <h2>Credits: {loggedInUser.Credits}</h2>
                    <button onClick={displayCurrentUser}>Display Current User</button>
                </div>
            ) : (
                <p>Please register or login.</p>
            )}
            {error && <p style={{ color: 'red' }}>{error}</p>}
        </div>
    );
}

export default App;
