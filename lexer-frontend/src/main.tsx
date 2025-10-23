// src/main.tsx
import React from "react";
import ReactDOM from "react-dom/client";
import ViewSwitcher from "./components/ViewSwitcher";
import "./index.css";

ReactDOM.createRoot(document.getElementById("root") as HTMLElement).render(
  <React.StrictMode>
    <ViewSwitcher />
  </React.StrictMode>
);
