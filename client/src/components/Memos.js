import React, { useEffect, useState } from "react";
import axios from "axios";

const Memos = ({ token }) => {
  const [memos, setMemos] = useState([]);

  useEffect(() => {
    const fetchMemos = async () => {
      try {
        const response = await axios.get("http://localhost:5555/memos/1", {
          headers: { Authorization: `Bearer ${token}` },
        });
        setMemos(response.data.memos_sent);
      } catch (err) {
        alert("Error fetching memos");
      }
    };

    if (token) {
      fetchMemos();
    }
  }, [token]);

  return (
    <div>
      <h2>Memos</h2>
      <ul>
        {memos.map((memo) => (
          <li key={memo.id}>{memo.content}</li>
        ))}
      </ul>
    </div>
  );
};

export default Memos;
