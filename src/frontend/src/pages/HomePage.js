import React, { useState, useEffect } from "react";
import axios from "axios";

function App() {
  // State variables
  const [registerUsername, setRegisterUsername] = useState("");
  const [registerEmail, setRegisterEmail] = useState("");
  const [registerPassword, setRegisterPassword] = useState("");
  const [updateUsername, setUpdateUsername] = useState("");
  const [loginUsername, setLoginUsername] = useState("");
  const [loginPassword, setLoginPassword] = useState("");
  const [loggedInUser, setLoggedInUser] = useState(null);
  const [error, setError] = useState("");
  const [successMessage, setSuccessMessage] = useState("");
  const [userLocations, setUserLocations] = useState([]);
  const [purchaseAmount, setPurchaseAmount] = useState(0);

  // Function to handle user registration
  const registerUser = async () => {
    try {
      const response = await axios.post(
        "http://localhost:5000/api/v2/users/register",
        {
          username: registerUsername,
          email: registerEmail,
          password: registerPassword,
        },
      );
      console.log("User registered successfully:", response.data);
      setSuccessMessage("Registration successful."); // Set success message
      setTimeout(() => {
        setSuccessMessage("Registration successful."); // Clear success message after 10 seconds
      }, 10000);
    } catch (error) {
      setTimeout(() => {
        setError("Registration failed. Please try again.");
      }, 10000);
    }
  };

  // Function to handle user login
  const loginUser = async () => {
    try {
      const formData = new FormData();
      formData.append("username", loginUsername);
      formData.append("password", loginPassword);

      const response = await axios.post(
        "http://localhost:5000/api/v2/users/login",
        formData,
        {
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
          },
        },
      );

      console.log("User logged in successfully:", response.data);

      // Store the access token in localStorage or sessionStorage
      localStorage.setItem("accessToken", response.data.access_token);

      setLoggedInUser(response.data);

      await displayCurrentUser();
      await fetchUserLocations(); // Fetch user locations after login
    } catch (error) {
      console.error("Login failed:", error.response.data);
    }
  };

  // Function to handle user logout
  const logoutUser = () => {
    localStorage.removeItem("accessToken"); // Clear access token
    setLoggedInUser(null); // Reset loggedInUser state
  };

  // Function to handle credit purchase
  const purchaseCredits = async () => {
    try {
      // Check if the purchase amount is within the valid range (1-500)
      if (purchaseAmount < 1 || purchaseAmount > 500) {
        setError("Please enter a valid purchase amount between 1 and 500.");
        return;
      }

      // Send POST request to purchase credits
      await axios.post(
        `http://localhost:5000/api/v2/credits/purchase?amount=${purchaseAmount}`,
        null,
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
          },
        },
      );

      console.log("Credits purchased successfully.");
      setError(""); // Clear any previous error
      await displayCurrentUser(); // Refresh the credit amount
    } catch (error) {
      console.error("Failed to purchase credits:", error.response.data);
      setError("Failed to purchase credits. Please try again.");
    }
  };

  // Function to display the currently logged-in user
  const displayCurrentUser = async () => {
    try {
      const response = await axios.get(
        "http://localhost:5000/api/v2/users/profile",
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
          },
        },
      );

      console.log("Current user:", response.data);

      // Set the current user in state
      setLoggedInUser(response.data);
    } catch (error) {
      setError("Failed to fetch current user.");
    }
  };

  // Function to fetch user locations
  const fetchUserLocations = async () => {
    try {
      const response = await axios.get(
        "http://localhost:5000/api/v2/users/locations",
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
          },
        },
      );
      console.log("User locations:", response.data);
      setUserLocations(response.data);
    } catch (error) {
      console.error("Failed to fetch user locations:", error.response.data);
    }
  };

  // Fucntion to format date
  const formatDate = (dateStr) => {
    const date = new Date(dateStr);

    const year = date.getFullYear();
    const month = ("0" + (date.getMonth() + 1)).slice(-2);
    const day = ("0" + date.getDate()).slice(-2);
    const hours = ("0" + date.getHours()).slice(-2);
    const minutes = ("0" + date.getMinutes()).slice(-2);
    const seconds = ("0" + date.getSeconds()).slice(-2);

    return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
  };

  // Function to convert temperature from Kelvin to Celsius and format
  const formatTemperature = (kelvin) => {
    // Convert Kelvin to Celsius
    const celsius = kelvin - 273.15;
    // Round to two decimal places
    const roundedCelsius = celsius.toFixed(2);
    // Add Celsius symbol
    return `${roundedCelsius} °C`;
  };

  // Function to refresh user locations
  const refreshUserLocations = async () => {
    await fetchUserLocations();
  };

  // Function to handle "Get Weather" button click
  const handleGetWeather = async () => {
    try {
      await axios.post(
        "http://localhost:5000/api/v2/users/locations",
        null, // You can pass any data you want to post here
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
          },
        },
      );
      console.log("Weather data posted successfully.");
      await displayCurrentUser();
      refreshUserLocations(); // Refresh the table after posting
    } catch (error) {
      console.error("Failed to post weather data:", error.response.data);
    }
  };

  // Function to handle location deletion
  const deleteLocation = async (locationId) => {
    try {
      await axios.delete(
        `http://localhost:5000/api/v2/users/locations/${locationId}`,
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
          },
        },
      );
      console.log("Location deleted successfully.");
      refreshUserLocations(); // Refresh the table after deleting
    } catch (error) {
      console.error("Failed to delete location:", error.response.data);
    }
  };

  // Function to update user profile
  const updateUserProfile = async () => {
    try {
      const response = await axios.put(
        "http://localhost:5000/api/v2/users/profile",
        {
          username: updateUsername,
        },
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
          },
        },
      );

      console.log("User profile updated successfully:", response.data);

      // Update loggedInUser state with updated user profile
      setLoggedInUser(response.data.user);
      await displayCurrentUser();
      await fetchUserLocations();
    } catch (error) {
      console.error("Failed to update user profile:", error.response.data);
      setError("Failed to update user profile. Please try again.");
    }
  };

  // Function to delete user profile
  const deleteUserProfile = async () => {
    try {
      await axios.delete("http://localhost:5000/api/v2/users/profile", {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
        },
      });

      console.log("User profile deleted successfully.");
      setLoggedInUser(null); // Reset loggedInUser state after deletion
    } catch (error) {
      console.error("Failed to delete user profile:", error.response.data);
      setError("Failed to delete user profile. Please try again.");
    }
  };

  // Run this effect when the component mounts
  useEffect(() => {
    if (loggedInUser) {
      fetchUserLocations();
    }
  }, [loggedInUser]);

  return (
    <div>
      <h1>Weather App</h1>
      <div>
        <h2>Register</h2>
        <input
          type="text"
          placeholder="Username"
          value={registerUsername}
          onChange={(e) => setRegisterUsername(e.target.value)}
        />
        <input
          type="email"
          placeholder="Email"
          value={registerEmail}
          onChange={(e) => setRegisterEmail(e.target.value)}
        />
        <input
          type="password"
          placeholder="Password"
          value={registerPassword}
          onChange={(e) => setRegisterPassword(e.target.value)}
        />
        <button onClick={registerUser}>Register</button>
      </div>
      <div>
        <h2>Login</h2>
        <input
          type="text"
          placeholder="Username"
          value={loginUsername}
          onChange={(e) => setLoginUsername(e.target.value)}
        />
        <input
          type="password"
          placeholder="Password"
          value={loginPassword}
          onChange={(e) => setLoginPassword(e.target.value)}
        />
        <button onClick={loginUser}>Login</button>
        {loggedInUser && <button onClick={logoutUser}>Logout</button>}
        {loggedInUser && (
          <button onClick={deleteUserProfile}>Delete Account</button>
        )}
      </div>
      <div>
        <h2>Update Profile</h2>
        <input
          type="text"
          placeholder="New Username"
          value={updateUsername}
          onChange={(e) => setUpdateUsername(e.target.value)}
        />
        <button onClick={updateUserProfile}>Update Profile</button>
      </div>
      {loggedInUser ? (
        <div>
          <h2>Welcome, {loggedInUser.username}</h2>
          <h2>Credits: {loggedInUser.credits}</h2>
          <div>
            <input
              type="number"
              placeholder="Enter amount (1-500)"
              value={purchaseAmount}
              onChange={(e) => setPurchaseAmount(e.target.value)}
              min="1"
              max="500"
            />
            <button onClick={purchaseCredits}>Submit</button>
          </div>
          <h2>User Locations:</h2>
          <button onClick={handleGetWeather}>Get Weather</button>{" "}
          {/* Button to get weather */}
          <table style={{ borderCollapse: "collapse", width: "100%" }}>
            <thead>
              <tr>
                <th style={{ border: "1px solid black" }}>Date</th>
                <th style={{ border: "1px solid black" }}>City</th>
                <th style={{ border: "1px solid black" }}>Country</th>
                <th style={{ border: "1px solid black" }}>Temperature</th>
                <th style={{ border: "1px solid black" }}>Description</th>
              </tr>
            </thead>
            <tbody>
              {userLocations.map((location) => (
                <tr key={location.id}>
                  <td style={{ border: "1px solid black" }}>
                    {formatDate(location.timestamp)}
                  </td>
                  <td style={{ border: "1px solid black" }}>{location.city}</td>
                  <td style={{ border: "1px solid black" }}>
                    {location.country}
                  </td>
                  <td style={{ border: "1px solid black" }}>
                    {formatTemperature(location.temperature)}
                  </td>
                  <td style={{ border: "1px solid black" }}>
                    {location.description}
                  </td>
                  <td style={{ border: "1px solid black" }}>
                    <button onClick={() => deleteLocation(location.id)}>
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <p>Please register or login.</p>
      )}
      {error && <p style={{ color: "red" }}>{error}</p>}
      {successMessage && <p style={{ color: "green" }}>{successMessage}</p>}
    </div>
  );
}

export default App;
