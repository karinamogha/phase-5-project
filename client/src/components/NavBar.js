import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import axios from "axios";

const NavBar = ({ token }) => {
  const [searchQuery, setSearchQuery] = useState("");
  const [searchResults, setSearchResults] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [page, setPage] = useState(1); // Pagination
  const [totalPages, setTotalPages] = useState(1);

  // Debounce for search API call
  useEffect(() => {
    const delayDebounce = setTimeout(() => {
      if (searchQuery) {
        handleSearch();
      } else {
        setSearchResults([]);
      }
    }, 500); // 500ms debounce

    return () => clearTimeout(delayDebounce);
  }, [searchQuery, page]); // Re-run on search query or page change

  const handleSearch = async () => {
    if (!token) return;

    setIsLoading(true);
    try {
      const response = await axios.get("http://localhost:5555/users", {
        params: { q: searchQuery, page },
        headers: { Authorization: `Bearer ${token}` },
      });

      setSearchResults(response.data.results);
      setTotalPages(response.data.total_pages);
    } catch (err) {
      console.error("Error fetching search results:", err);
      alert("Failed to fetch search results.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div>
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

      {/* Search Bar Below NavBar */}
      <div className="search-container">
        <input
          type="text"
          placeholder="Search for users..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
        {isLoading ? (
          <p>Loading...</p>
        ) : (
          searchResults.length > 0 && (
            <div className="search-results">
              <ul>
                {searchResults.map((user) => (
                  <li key={user.id}>
                    <Link to={`/user/${user.id}`}>{user.name}</Link>
                  </li>
                ))}
              </ul>

              {/* Pagination */}
              <div className="pagination">
                {page > 1 && (
                  <button onClick={() => setPage(page - 1)}>Previous</button>
                )}
                {page < totalPages && (
                  <button onClick={() => setPage(page + 1)}>Next</button>
                )}
              </div>
            </div>
          )
        )}
      </div>
    </div>
  );
};

export default NavBar;



