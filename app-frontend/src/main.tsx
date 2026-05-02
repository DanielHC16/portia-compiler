// src/main.tsx
import React from "react";
import ReactDOM from "react-dom/client";
import ViewSwitcher from "./components/ViewSwitcher";
import "./index.css";

// Mount the single-page compiler UI. StrictMode helps surface frontend issues
// during development without changing the compiler backend behavior.
ReactDOM.createRoot(document.getElementById("root") as HTMLElement).render(
  <React.StrictMode>
    <ViewSwitcher />
  </React.StrictMode>
);
