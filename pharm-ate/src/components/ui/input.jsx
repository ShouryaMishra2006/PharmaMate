import React from "react";

export function Input({ type = "text", className, ...props }) {
  return (
    <input
      type={type}
      className={`border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 ${className}`}
      {...props}
    />
  );
}
