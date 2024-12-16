import React, { useState } from "react";
import { BrowserRouter as Router, Route, Switch, Redirect } from "react-router-dom";
import NavBar from "./components/NavBar";
import Login from "./components/Login";
import Register from "./components/Register";
import Invoices from "./components/Invoices";
import Memos from "./components/Memos";
import CreateInvoice from "./components/CreateInvoice";
import CreateMemo from "./components/CreateMemo";

const App = () => {
  const [token, setToken] = useState(null);

  return (
    <Router>
      <div>
        {!token ? (
          // Show homepage if not logged in
          <div className="homepage-container">
            <h1>Welcome to Orna Cloud</h1>
            <div className="homepage-buttons">
              <a href="/login">Login</a>
              <a href="/register">Register</a>
            </div>
          </div>
        ) : (
          // Show app content when logged in
          <>
            <NavBar /> {/* Display the NavBar */}
            <div className="app-content">
              <Switch>
                <Route exact path="/invoices">
                  <Invoices token={token} />
                </Route>
                <Route exact path="/memos">
                  <Memos token={token} />
                </Route>
                <Route exact path="/create-invoice">
                  <CreateInvoice token={token} />
                </Route>
                <Route exact path="/create-memo">
                  <CreateMemo token={token} />
                </Route>
                <Redirect to="/invoices" /> {/* Redirect to invoices by default */}
              </Switch>
            </div>
          </>
        )}
        <Switch>
          {/* Login and Register Routes */}
          <Route path="/login">
            <Login setToken={setToken} />
          </Route>
          <Route path="/register" component={Register} />
        </Switch>
      </div>
    </Router>
  );
};

export default App;








