const API_BASE = "https://stockguard-api.onrender.com";

export const signupUser = async (data) => {
  const res = await fetch(`${API_BASE}/signup`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });
  return res.json();
};

export const loginUser = async (data) => {
  const res = await fetch(`${API_BASE}/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });
  return res.json();
};

export const getItems = async (token) => {
  const res = await fetch(`${API_BASE}/items`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  return res.json();
};
