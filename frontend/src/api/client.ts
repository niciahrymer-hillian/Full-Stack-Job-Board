// Axios instance with a request interceptor that attaches the JWT to every call.
// Storing the token in localStorage is fine for a demo; for production prefer an
// httpOnly cookie to keep it out of reach of XSS.
import axios from "axios";

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL ?? "http://localhost:8000",
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});
