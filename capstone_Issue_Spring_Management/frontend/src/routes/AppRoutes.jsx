import {
    BrowserRouter,
    Navigate,
    Route,
    Routes
} from "react-router-dom";

import ProtectedRoute from "../components/ProtectedRoute";
import { ROUTES } from "../constants/routes";
import Dashboard from "../pages/dashboard/Dashboard";
import IssuesList from "../pages/IssuesList";
import Projects from "../pages/project/Projects";
import SprintBoard from "../pages/SprintBoard";
import Login from "../pages/auth/Login";
import Register from "../pages/auth/register/Register";


function AppRoutes() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<Navigate to={ROUTES.DASHBOARD} />} />
                <Route path={ROUTES.LOGIN} element={<Login />} />
                <Route path={ROUTES.REGISTER} element={<Register />} />

                <Route
                    path={ROUTES.DASHBOARD}
                    element={
                        <ProtectedRoute>
                            <Dashboard />
                        </ProtectedRoute>
                    }
                />
                <Route
                    path={ROUTES.PROJECTS}
                    element={
                        <ProtectedRoute>
                            <Projects />
                        </ProtectedRoute>
                    }
                />
                <Route
                    path={ROUTES.ISSUES}
                    element={
                        <ProtectedRoute>
                            <IssuesList />
                        </ProtectedRoute>
                    }
                />
                <Route
                    path={ROUTES.SPRINTS}
                    element={
                        <ProtectedRoute>
                            <SprintBoard />
                        </ProtectedRoute>
                    }
                />
            </Routes>
        </BrowserRouter>
    );
}

export default AppRoutes;
