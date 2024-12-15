import React from "react";
import { Link } from "react-router-dom";

const NavBar = () => {
  return (
    <nav>
      <ul>
        <li>
          <Link to="/invoices">Invoices</Link>
        </li>
        <li>
          <Link to="/memos">Memos</Link>
        </li>
        <li>
          <Link to="/create-invoice">Create Invoice</Link>
        </li>
        <li>
          <Link to="/create-memo">Create Memo</Link>
        </li>
      </ul>
    </nav>
  );
};

export default NavBar;

