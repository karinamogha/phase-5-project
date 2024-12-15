import React, { useState } from "react";

const CreateInvoice = ({ token }) => {
  const [recipient, setRecipient] = useState("");
  const [amount, setAmount] = useState("");
  const [description, setDescription] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch("http://localhost:5555/invoices", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ recipient, amount, description }),
      });
      if (response.ok) alert("Invoice created successfully!");
    } catch (err) {
      console.error("Error creating invoice:", err);
      alert("Failed to create invoice.");
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Create Invoice</h2>
      <input
        type="text"
        placeholder="Recipient Email"
        value={recipient}
        onChange={(e) => setRecipient(e.target.value)}
      />
      <input
        type="number"
        placeholder="Amount"
        value={amount}
        onChange={(e) => setAmount(e.target.value)}
      />
      <textarea
        placeholder="Description"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
      />
      <button type="submit">Send Invoice</button>
    </form>
  );
};

export default CreateInvoice;
