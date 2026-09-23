import React from "react";
import ReactDOM from "react-dom/client";
import OneSignal from "react-onesignal";
import { savePushSubscription } from "./api";
import App from "./App.jsx";
import "./index.css";

const initOneSignal = async () => {
  try {
    await OneSignal.init({
      appId: import.meta.env.VITE_ONESIGNAL_APP_ID,
      allowLocalhostAsSecureOrigin: true,
    });

    console.log("OneSignal initialized successfully.");
    const subscriptionId = await OneSignal.User.PushSubscription.id;

if (subscriptionId) {
  console.log("OneSignal subscription ID:", subscriptionId);

  await savePushSubscription(subscriptionId);

  console.log("Push subscription saved to backend.");
} else {
  console.log("No OneSignal subscription ID available yet.");
}

    await OneSignal.Slidedown.promptPush();
  } catch (error) {
    console.error("OneSignal initialization failed:", error);
  }
};

initOneSignal();

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);