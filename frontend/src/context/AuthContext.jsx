import { createContext, useContext, useEffect, useMemo, useState } from "react";

import api from "../api/client";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem("access_token");
    if (!token) {
      setLoading(false);
      return;
    }
    api
      .get("/auth/me")
      .then((response) => setUser(response.data.user))
      .catch(() => localStorage.removeItem("access_token"))
      .finally(() => setLoading(false));
  }, []);

  const login = async (email, password) => {
    const response = await api.post("/auth/login", { email, password });
    localStorage.setItem("access_token", response.data.access_token);
    setUser(response.data.user);
  };

  const register = async (payload) => {
    const response = await api.post("/auth/register", payload);
    localStorage.setItem("access_token", response.data.access_token);
    setUser(response.data.user);
  };

  const logout = () => {
    localStorage.removeItem("access_token");
    setUser(null);
  };

  const value = useMemo(() => ({ user, loading, login, register, logout }), [user, loading]);
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  return useContext(AuthContext);
}
