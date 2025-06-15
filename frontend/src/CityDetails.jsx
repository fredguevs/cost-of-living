import { useState, useEffect } from "react";

const displayOrder = [
  "Restaurants",
  "Markets",
  "Transportation",
  "Utilities (Monthly)",
  "Rent Per Month",
  "Buy Apartment Price",
  "Salaries And Financing",
  "Childcare",
  "Clothing And Shoes",
  "Sports And Leisure",
];

export default function CityDetails({ cityDetails, selectedCity }) {
  const [selectedItem, setSelectedItem] = useState(null);
  const [blsGraph, setBlsGraph] = useState(null);
  
  async function handleItemSelect(itemName) {
    setSelectedItem(itemName);
    try {
      const response = await fetch(
        `http://127.0.0.1:5000/api/bls/${encodeURIComponent(itemName)}`
      );
      const data = await response.json();
      setBlsGraph(data);
    } catch (error) {
      console.error("Error fetching BLS:", error);
    }
  }

  return (
    <div className="city-details">
      <h2>Cost of living in {selectedCity.label}</h2>
      <div>
        {displayOrder.map((category) =>
          cityDetails[category] ? (
            <div key={category}>
              <h3>{category}</h3>
              {cityDetails[category].map((item, index) => (
                <p key={index}>
                  <button onClick={() => handleItemSelect(item.name)}>
                    {item.name}
                  </button>
                  : {item.price}
                </p>
              ))}
            </div>
          ) : null
        )}
        {blsGraph && (
          <div>
            <h3>BLS Graph for {selectedItem}</h3>
            <ul>
              {blsGraph.map((entry, i) => (
                <li key={i}>
                  {entry.date}: ${entry.price}
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}