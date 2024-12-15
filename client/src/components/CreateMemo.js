import React, { useState } from "react";

const CreateMemo = ({ token }) => {
  const [recipient, setRecipient] = useState("");
  const [content, setContent] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch("http://localhost:5555/memos", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ receiver_id: recipient, content }),
      });
      if (response.ok) {
        alert("Memo sent successfully!");
        setRecipient(""); // Clear input fields after successful submission
        setContent("");
      } else {
        const errorData = await response.json();
        alert(`Failed to send memo: ${errorData.error}`);
      }
    } catch (err) {
      console.error("Error sending memo:", err);
      alert("Failed to send memo.");
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Create Memo</h2>
      <input
        type="text"
        placeholder="Recipient Email"
        value={recipient}
        onChange={(e) => setRecipient(e.target.value)}
      />
      <textarea
        placeholder="Memo Content"
        value={content}
        onChange={(e) => setContent(e.target.value)}
      />
      <button type="submit">Send Memo</button>
    </form>
  );
};

export default CreateMemo;
