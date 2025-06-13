import {useState, useEffect} from 'react';
import Select from "react-select";
import AsyncSelect from "react-select/async";
import makeAnimated from "react-select/animated";

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


export default function Search() {
    const [selectedCity, setSelectedCity] = useState(null);
    const [cities, setCities] = useState([]);
    const [cityDetails, setCityDetails] = useState(null);
    
    async function handleCitySelect(selectedOption) {
      setSelectedCity(selectedOption);
      try {
        const response = await fetch(
          `http://127.0.0.1:5000/api/city/${selectedOption.value}`
        );
        const data = await response.json();
        setCityDetails(data);
      } catch (error) {
        console.error("Error fetching city details:", error);
      }
    }

    useEffect(() => {
        async function fetchCities() {
            try {
                const response = await fetch("http://127.0.0.1:5000/api/cities");
                const data = await response.json();
                setCities(data);
            } catch (error) {
                console.error("Error fetching cities:", error);
            }
        }

        fetchCities();
    }
    , []);

    return (
        <div>
            <Select
            value={selectedCity}
            onChange={handleCitySelect}
            options={cities}
            isSearchable
            placeholder="Search for a city"
            />
            {cityDetails && (
            <div className="city-details">
                <h2>Cost of living in {selectedCity.label}</h2>
                <div>
                {displayOrder.map((category) =>
                    cityDetails[category] ? (
                    <div key={category}>
                        <h3>{category}</h3>
                        {cityDetails[category].map((item, index) => (
                        <p key={index}>
                            {item.name}: {item.price}
                        </p>
                        ))}
                    </div>
                    ) : null
                )}
                </div>
            </div>
            )}
        </div>
    );
}