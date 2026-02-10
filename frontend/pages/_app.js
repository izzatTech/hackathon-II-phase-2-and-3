import { useEffect, useState } from "react";
import { AuthProvider } from "../src/context/AuthContext";

// ✅ Global / component CSS (ONLY existing files)
import "../src/components/TaskForm.css";
import "../src/components/TaskList.css";
import "../src/components/AuthForms.css";
import "../src/components/ChatInterface.css";
import "../src/components/Header.css";
import "./Dashboard.css";
import "./TasksPage.css";

function MyApp({ Component, pageProps }) {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) {
    return <p>Loading...</p>;
  }

  return (
    <AuthProvider>
      <Component {...pageProps} />
    </AuthProvider>
  );
}

export default MyApp;
