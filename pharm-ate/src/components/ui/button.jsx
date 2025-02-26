import React from "react";

export function Button({ children, variant = "default", className, ...props }) {
  const baseStyles = "px-4 py-2 rounded-lg font-semibold transition-all flex items-center justify-center gap-2";
  const variants = {
    default: "bg-blue-600 text-white hover:bg-blue-700",
    outline: "border border-gray-400 text-gray-700 hover:bg-gray-200",
  };

  return (
    <button className={`${baseStyles} ${variants[variant]} ${className}`} {...props}>
      {children}
    </button>
  );
}
