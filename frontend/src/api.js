const BASE_URL = import.meta.env.VITE_API_URL || "https://your-render-url.onrender.com";

export const getItems = async () => {
  const res = await fetch(`${BASE_URL}/items`, {
    headers: {
      Authorization: "Bearer " + localStorage.getItem("token"),
    },
  });
  return res.json();
};

export const loginUser = async (data) => {
  const res = await fetch(`${BASE_URL}/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });
  return res.json();
};

export const signupUser = async (data) => {
  const res = await fetch(`${BASE_URL}/signup`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });
  return res.json();
};
