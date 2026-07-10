import { useContext } from "react";
import { Navigate } from "react-router-dom";
import { AuthContext } from "../context/auth-context";


const ProtectedRoute = ({ children, requiredRole }) => {
    const { currentUser, loading } = useContext(AuthContext);

    if (loading) {
        return null;
    }

    if (!currentUser) {
        return <Navigate to="/login" replace />;
    }

    if (requiredRole && currentUser.role !== requiredRole) {
        return <Navigate to="/dashboard" replace />;
    }

    return children;
};

export default ProtectedRoute;
