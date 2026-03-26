import { createContext, useEffect, useMemo, useState } from "react";
import { fetchMe, loginUser, registerUser } from "../api/authApi";

export const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const bootstrap = async () => {
      const token = localStorage.getItem("access_token");
      if (!token) {
        setIsLoading(false);
        return;
      }
      try {
        const me = await fetchMe();
        setUser(me);
      } catch {
        localStorage.removeItem("access_token");
        setUser(null);
      } finally {
        setIsLoading(false);
      }
    };
    bootstrap();
  }, []);

  const login = async (payload) => {
    const tokenData = await loginUser(payload);
    localStorage.setItem("access_token", tokenData.access_token);
    const me = await fetchMe();
    setUser(me);
    return me;
  };

  const register = async (payload) => registerUser(payload);

  const logout = () => {
    localStorage.removeItem("access_token");
    setUser(null);
  };

  const value = useMemo(
    () => ({ user, isLoading, login, register, logout, isAuthenticated: !!user }),
    [user, isLoading]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

