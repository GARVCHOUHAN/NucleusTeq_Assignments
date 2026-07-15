import { useEffect, useState } from "react";
import { AuthContext } from "./auth-context";


export function AuthProvider({ children }) {
    const [currentUser, setCurrentUser] = useState(null);
    const [loading, setLoading] = useState(true);

    // create a utility function for adding the details in local storage, also make the function generics
    const setLocalStorageItem = (key, value) => {
        localStorage.setItem(key, JSON.stringify(value));
    };

    useEffect(() => {
        const savedUser = localStorage.getItem("currentUser");

        if (savedUser) {
            setCurrentUser(
                JSON.parse(savedUser)
            );
        }

        setLoading(false);
    }, []);

    const login = (authPayload) => {
        const user = authPayload.user || authPayload;
        const token = authPayload.access_token || authPayload.token;

        localStorage.setItem(
            "currentUser",
            JSON.stringify(user)
        );

        if (token) {
            localStorage.setItem(
                "authToken",
                token
            );
        }

        setCurrentUser(user);
    };

    const logout = () => {
        localStorage.removeItem(
            "currentUser"
        );
        localStorage.removeItem(
            "authToken"
        );
        setCurrentUser(null);
    };

    return (
        <AuthContext.Provider
            value={{
                currentUser,
                login,
                logout,
                loading,
                isAuthenticated: currentUser !== null
            }}
        >
            {children}
        </AuthContext.Provider>
    );
}
