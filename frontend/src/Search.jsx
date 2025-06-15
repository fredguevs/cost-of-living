import {useState, useEffect} from 'react';
import Select from "react-select";
import AsyncSelect from "react-select/async";
import makeAnimated from "react-select/animated";
import CitySelector from './CitySelector';
import CityDetails from './CityDetails';

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
            <CitySelector
                cities={cities}
                selectedCity={selectedCity}
                onChange={handleCitySelect}
            />
            {cityDetails && (
                <CityDetails cityDetails={cityDetails} selectedCity={selectedCity} />
            )}
        </div>
    );
}