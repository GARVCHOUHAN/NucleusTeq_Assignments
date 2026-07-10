import { Navigate } from "react-router-dom";

import { useAuth } from "../hooks/use-auth";

import { ROUTES } from "../constants/routes";

function ProtectedRoute({ children }) {

    const {

        loading,

        isAuthenticated

    } = useAuth();

    if (loading) {

        return <p>Loading...</p>;

    }

    if (!isAuthenticated) {

        return (

            <Navigate
                to={ROUTES.LOGIN}
                replace
            />

        );

    }

    return children;

}

export default ProtectedRoute;