// RentcastLineChart.js
import React, { useState } from "react";
import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from "recharts";

/**
 * Props:
 *  - data: Array<{ date: "YYYY-MM", price: number }>
 */
export default function RentcastLineChart({ data }) {
  const [showPrev, setShowPrev] = useState(true);
  const [showCurr, setShowCurr] = useState(true);
  const now = new Date();
  const currentYear = now.getFullYear();
  const prevYear = currentYear - 1;

  // Split data by year
  const prevData = data.filter(
    (d) => parseInt(d.date.split("-")[0]) === prevYear
  );
  const currData = data.filter(
    (d) =>
      parseInt(d.date.split("-")[0]) === currentYear &&
      parseInt(d.date.split("-")[1]) <= now.getMonth() + 1
  );

  const monthFormatter = (dateString) => {
    const [year, month] = dateString.split("-");
    const d = new Date(year, month - 1);
    return d.toLocaleString("en-US", { month: "short" });
  };

  return (
    <div>
      <div style={{ marginBottom: 12 }}>
        <button onClick={() => setShowPrev((s) => !s)}>
          {showPrev ? "Hide" : "Show"} {prevYear}
        </button>
        <button
          style={{ marginLeft: 8 }}
          onClick={() => setShowCurr((s) => !s)}
        >
          {showCurr ? "Hide" : "Show"} {currentYear}
        </button>
      </div>
      <ResponsiveContainer width="100%" height={250}>
        <LineChart
          data={data}
          margin={{ top: 5, right: 10, left: 10, bottom: 5 }}
        >
          <CartesianGrid strokeDasharray="3 3" opacity={0.2} />
          <XAxis
            dataKey="date"
            tickFormatter={monthFormatter}
            interval={0}
            tickLine={false}
            padding={{ left: 10, right: 10 }}
          />
          <YAxis
            tickFormatter={(val) => `$${val}`}
            tickLine={false}
            axisLine={false}
            width={60}
          />
          <Tooltip
            labelFormatter={monthFormatter}
            formatter={(value) => `$${value}`}
            cursor={{ stroke: "#aaa", strokeDasharray: "3 3" }}
          />
          <Legend verticalAlign="top" height={24} />
          {showPrev && (
            <Line
              type="monotone"
              dataKey="price"
              data={prevData}
              name={`${prevYear}`}
              stroke="#82ca9d"
              strokeWidth={2}
              dot={false}
            />
          )}
          {showCurr && (
            <Line
              type="monotone"
              dataKey="price"
              data={currData}
              name={`YTD ${currentYear}`}
              stroke="#ff7300"
              strokeWidth={2}
              dot={false}
            />
          )}
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
