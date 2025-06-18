import React, { useState, useEffect } from "react";
import BlsLineChart from "./BlsLineChart";
import RentcastLineChart from "./RentcastLineChart";

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
  const [rentcastGraph, setRentcastGraph] = useState(null);

  useEffect(() => {
    setSelectedItem(null);
    setBlsGraph(null);
    setRentcastGraph(null);
  }, [selectedCity]);

  async function handleItemSelect(itemName) {
    setSelectedItem(itemName);
    setBlsGraph(null);
    setRentcastGraph(null);

    // Try BLS
    try {
      const blsRes = await fetch(
        `http://127.0.0.1:5000/api/bls/${encodeURIComponent(itemName)}`
      );
      if (blsRes.ok) {
        const blsData = await blsRes.json();
        if (blsData.length > 1) {
          setBlsGraph(blsData);
          return;
        }
      }
    } catch (err) {
      console.error("Error fetching BLS:", err);
    }

    // Fallback to RentCast
    try {
      const rentRes = await fetch(
        `http://127.0.0.1:5000/api/rentcast/${encodeURIComponent(
          selectedCity.value
        )}/${encodeURIComponent(itemName)}`
      );
      if (rentRes.ok) {
        const rentData = await rentRes.json();
        setRentcastGraph(rentData);
      } else {
        console.warn("RentCast API returned", rentRes.status);
      }
    } catch (err) {
      console.error("Error fetching RentCast:", err);
    }
  }

  return (
    <div className="city-details">
      <h2>Cost of living in {selectedCity.label}</h2>

      {displayOrder.map((category) =>
        cityDetails[category] ? (
          <div key={category} className="category-block">
            <h3>{category}</h3>
            {cityDetails[category].map((item) => (
              <p key={item.name}>
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
        <section className="chart-section">
          <h3>BLS Historical Prices for {selectedItem}</h3>
          <BlsLineChart data={blsGraph} />
        </section>
      )}

      {rentcastGraph && (
        <section className="chart-section">
          <h3>RentCast Trend for {selectedItem}</h3>
          <RentcastLineChart data={rentcastGraph} />
        </section>
      )}
    </div>
  );
}
