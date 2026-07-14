import { Navigate } from "react-router-dom";
import { useAuth } from "../hooks/use-auth";


const ProtectedRoute = ({ children, requiredRole }) => {
    const { currentUser, loading } = useAuth();

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
