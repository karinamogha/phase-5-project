import React, { useState } from "react";
import { BrowserRouter as Router, Route, Switch, Link } from "react-router-dom";
import Login from "./components/Login";
import Register from "./components/Register";

const App = () => {
  const [token, setToken] = useState(null);

  return (
    <Router>
      <div>
        {!token ? (
          // Homepage when not logged in
          <div className="homepage-container">
            <h1>Welcome to Orna Cloud</h1>
            <div className="homepage-buttons">
              <Link to="/login">Login</Link>
              <Link to="/register">Register</Link>
            </div>
          </div>
        ) : (
          // Content when logged in
          <h1>App Content Goes Here</h1>
        )}
        <Switch>
          <Route path="/login" component={() => <Login setToken={setToken} />} />
          <Route path="/register" component={Register} />
        </Switch>
      </div>
    </Router>
  );
};

export default App;







