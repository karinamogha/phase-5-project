import React from "react";
import { Link } from "react-router-dom";

const NavBar = () => {
  return (
    <nav>
      <ul>
        <li>
          <Link to="/login">Login</Link>
        </li>
        <li>
          <Link to="/register">Register</Link>
        </li>
        <li>
          <Link to="/invoices">Invoices</Link>
        </li>
        <li>
          <Link to="/memos">Memos</Link>
        </li>
      </ul>
    </nav>
  );
};

export default NavBar;
