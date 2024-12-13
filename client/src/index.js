import React from "react";
import App from "./App";
import "./index.css"; // Assuming you have some styles here
import { createRoot } from "react-dom/client";

const container = document.getElementById("root");
const root = createRoot(container);
root.render(<App />);

