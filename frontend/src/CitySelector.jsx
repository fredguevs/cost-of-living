import { useState, useEffect } from "react";
import Select from "react-select";
import AsyncSelect from "react-select/async";
import makeAnimated from "react-select/animated";

export default function CitySelector({ cities, selectedCity, onChange }) {
  return (
    <Select
      value={selectedCity}
      onChange={onChange}
      options={cities}
      isSearchable
      placeholder="Search for a city"
    />
  );
}