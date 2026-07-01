import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import ProtectedRoute from './components/ProtectedRoute';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import AdminPanel from './pages/AdminPanel'; // Example admin page

function App() {
    return (
        <AuthProvider>
            <Router>
                <Routes>
                    {/* Public Route */}
                    <Route path="/login" element={<Login />} />

                    {/* Protected Route for any logged-in user */}
                    <Route 
                        path="/dashboard" 
                        element={
                            <ProtectedRoute>
                                <Dashboard />
                            </ProtectedRoute>
                        } 
                    />

                    {/* Protected Route STRICTLY for Admins */}
                    <Route 
                        path="/admin" 
                        element={
                            <ProtectedRoute requiredRole="admin">
                                <AdminPanel />
                            </ProtectedRoute>
                        } 
                    />

                    {/* Default redirect to login */}
                    <Route path="/" element={<Navigate to="/login" replace />} />
                    
                    <Route path="/login" element={<Login />} />

                    <Route 
                        path="/dashboard" 
                        element={
                            <ProtectedRoute>
                                <Dashboard />
                            </ProtectedRoute>
                        } 
                    />

                    {/* New Sprint Board Route */}
                    <Route 
                        path="/board" 
                        element={
                            <ProtectedRoute>
                                <SprintBoard />
                            </ProtectedRoute>
                        } 
                    />
                </Routes>
            </Router>
        </AuthProvider>
    );
}

export default App;