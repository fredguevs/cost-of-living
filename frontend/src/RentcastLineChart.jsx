import React, { useState, useMemo } from "react";
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
  const currentMonth = now.getMonth() + 1; // 1–12

  // Split data by year
  const prevData = useMemo(
    () =>
      data
        .filter((d) => +d.date.slice(0, 4) === prevYear)
        .map((d) => ({
          month: +d.date.slice(5, 7),
          price: d.price,
        })),
    [data, prevYear]
  );

  const currData = useMemo(
    () =>
      data
        .filter((d) => +d.date.slice(0, 4) === currentYear)
        .map((d) => ({
          month: +d.date.slice(5, 7),
          price: d.price,
        })),
    [data, currentYear]
  );

  // Build a chartData array for months 1–12
  const chartData = useMemo(() => {
    const months = Array.from({ length: 12 }, (_, i) => i + 1);
    return months.map((m) => {
      const entry = { month: m };
      const prev = prevData.find((d) => d.month === m);
      const curr = currData.find((d) => d.month === m);
      if (prev) entry[prevYear] = prev.price;
      if (curr && m <= currentMonth) entry[`YTD ${currentYear}`] = curr.price;
      return entry;
    });
  }, [prevData, currData, prevYear, currentYear, currentMonth]);

  // Format month number to "Jan", "Feb", etc.
  const monthFormatter = (m) =>
    new Date(2000, m - 1).toLocaleString("en-US", { month: "short" });

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
          {showCurr ? "Hide" : "Show"} YTD {currentYear}
        </button>
      </div>

      <ResponsiveContainer width="100%" height={250}>
        <LineChart
          data={chartData}
          margin={{ top: 5, right: 10, left: 10, bottom: 5 }}
        >
          <CartesianGrid strokeDasharray="3 3" opacity={0.15} />

          <XAxis
            dataKey="month"
            type="category"
            ticks={[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]}
            tickFormatter={monthFormatter}
            interval={0}
            axisLine={false}
            tickLine={false}
            height={30}
          />

          <YAxis
            tickFormatter={(val) => `$${val}`}
            axisLine={false}
            tickLine={false}
            width={60}
          />

          <Tooltip
            labelFormatter={(m) => monthFormatter(m)}
            formatter={(value, name) => [`$${value}`, name]}
            cursor={{ stroke: "#aaa", strokeDasharray: "3 3" }}
          />

          <Legend verticalAlign="top" height={24} />

          {showPrev && (
            <Line
              type="monotone"
              dataKey={`${prevYear}`}
              name={`${prevYear}`}
              stroke="#82ca9d"
              strokeWidth={2}
              dot={false}
              connectNulls
            />
          )}
          {showCurr && (
            <Line
              type="monotone"
              dataKey={`YTD ${currentYear}`}
              name={`YTD ${currentYear}`}
              stroke="#ff7300"
              strokeWidth={2}
              dot={false}
              connectNulls
            />
          )}
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
