import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { getItems, loginUser, signupUser } from "./api";

export default function App() {
  const [items, setItems] = useState([]);
  const [authMode, setAuthMode] = useState("login");
  const [form, setForm] = useState({ email: "", password: "" });
  const [token, setToken] = useState(localStorage.getItem("token"));

  // Fetch items
  useEffect(() => {
    if (token) {
      getItems().then(setItems);
    }
  }, [token]);

  const handleAuth = async () => {
    const res =
      authMode === "login"
        ? await loginUser(form)
        : await signupUser(form);

    if (res.access_token) {
      localStorage.setItem("token", res.access_token);
      setToken(res.access_token);
    }
  };

  // ---------------- LOGIN UI ----------------
  if (!token) {
    return (
      <div className="min-h-screen flex items-center justify-center px-4">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          className="glass w-full max-w-md p-6 sm:p-8"
        >
          <h1 className="text-2xl sm:text-3xl font-bold mb-6 text-center">
            Xpiry
          </h1>

          <input
            type="email"
            placeholder="Email"
            className="w-full p-3 mb-3 rounded-lg bg-white/10 outline-none"
            onChange={(e) => setForm({ ...form, email: e.target.value })}
          />

          <input
            type="password"
            placeholder="Password"
            className="w-full p-3 mb-4 rounded-lg bg-white/10 outline-none"
            onChange={(e) => setForm({ ...form, password: e.target.value })}
          />

          <button
            onClick={handleAuth}
            className="w-full bg-blue-600 hover:bg-blue-700 p-3 rounded-lg transition"
          >
            {authMode === "login" ? "Login" : "Signup"}
          </button>

          <p
            className="text-center mt-4 text-sm cursor-pointer text-gray-400"
            onClick={() =>
              setAuthMode(authMode === "login" ? "signup" : "login")
            }
          >
            {authMode === "login"
              ? "Don't have an account? Signup"
              : "Already have an account? Login"}
          </p>
        </motion.div>
      </div>
    );
  }

  // ---------------- DASHBOARD ----------------
  return (
    <div className="min-h-screen px-4 py-6">
      <div className="max-w-6xl mx-auto">

        {/* Header */}
        <div className="flex flex-col sm:flex-row justify-between items-center mb-6 gap-4">
          <h1 className="text-xl sm:text-2xl md:text-3xl font-bold">
            Xpiry Dashboard
          </h1>

          <button
            onClick={() => {
              localStorage.removeItem("token");
              setToken(null);
            }}
            className="bg-red-500 px-4 py-2 rounded-lg"
          >
            Logout
          </button>
        </div>

        {/* Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">

          {items.map((item) => {
            const days =
              (new Date(item.expiry_date) - new Date()) / (1000 * 60 * 60 * 24);

            const urgent = days < 3;

            return (
              <motion.div
                key={item.id}
                whileHover={{ scale: 1.03 }}
                whileTap={{ scale: 0.97 }}
                className="glass p-4 sm:p-5"
              >
                <h2 className="text-lg sm:text-xl font-semibold">
                  {item.name}
                </h2>

                <p className="text-sm text-gray-400">{item.category}</p>

                <div
                  className={`mt-3 text-sm sm:text-base ${
                    urgent
                      ? "text-red-400 animate-pulse"
                      : "text-green-400"
                  }`}
                >
                  {new Date(item.expiry_date).toDateString()}
                </div>
              </motion.div>
            );
          })}

        </div>
      </div>
    </div>
  );
}
