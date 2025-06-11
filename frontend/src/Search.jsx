import {useState, useEffect} from 'react';
import Select from "react-select";
import AsyncSelect from "react-select/async";
import makeAnimated from "react-select/animated";

export default function Search() {
    const [selectedCity, setSelectedCity] = useState(null);
    const [cities, setCities] = useState([]);

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
            <Select
                value={selectedCity}
                onChange={setSelectedCity}
                options={cities}
            />
        );
    }