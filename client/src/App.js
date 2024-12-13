import React from "react";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import NavBar from "./components/NavBar";
import Login from "./components/Login";       // Updated import paths
import Register from "./components/Register";
import Invoices from "./components/Invoices";
import Memos from "./components/Memos";



const App = () => {
  return (
    <Router>
      <div>
        <h1>OrnaCloud</h1>
        <Switch>
          <Route path="/login" component={Login} />
          <Route path="/register" component={Register} />
          <Route path="/invoices" component={Invoices} />
          <Route path="/memos" component={Memos} />
        </Switch>
      </div>
    </Router>
  );
};

export default App;



