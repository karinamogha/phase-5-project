import React, { useEffect, useState } from "react";
import axios from "axios";

const Invoices = ({ token }) => {
  const [invoices, setInvoices] = useState([]);

  useEffect(() => {
    const fetchInvoices = async () => {
      try {
        const response = await axios.get("http://localhost:3000/invoices/1", {
          headers: { Authorization: `Bearer ${token}` },
        });
        setInvoices(response.data.invoices_sent);
      } catch (err) {
        alert("Error fetching invoices");
      }
    };

    if (token) {
      fetchInvoices();
    }
  }, [token]);

  return (
    <div>
      <h2>Invoices</h2>
      <ul>
        {invoices.map((invoice) => (
          <li key={invoice.id}>
            {invoice.description} - ${invoice.amount}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Invoices;

