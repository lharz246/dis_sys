import React from 'react';
import './SearchBox.css';

function SearchBox({ onSearch }) {
  const handleSubmit = (e) => {
    e.preventDefault();
    const city = e.target.elements.city.value;
    if (city.trim()) {
      onSearch(city);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="search-bar">
      <input
        type="text"
        name="city"
        placeholder="Enter city name..."
      />
      <button type="submit">Search</button>
    </form>
  );
}

export default SearchBox;