import { useContext } from 'react';
import { AuthContext } from '../context/AuthContext';
import Navbar from '../components/Navbar';

const Dashboard = () => {
    const { user } = useContext(AuthContext);

    return (
        <div className="min-h-screen bg-gray-50">
            <Navbar />
            
            <main className="container mx-auto p-8">
                <div className="bg-white rounded-lg shadow p-6">
                    <h1 className="text-3xl font-bold text-gray-800 mb-4">
                        Welcome to the Dashboard!
                    </h1>
                    
                    <p className="text-gray-600 mb-6">
                        If you are seeing this, your JWT token was successfully decoded and your ProtectedRoute allowed you in.
                    </p>

                    <div className="p-4 bg-gray-100 rounded border border-gray-200">
                        <h3 className="font-bold text-gray-700 border-b pb-2 mb-2">Your Current Session Data</h3>
                        <ul className="text-sm text-gray-600 space-y-2">
                            <li><strong>Username/Email:</strong> {user?.username}</li>
                            <li><strong>Assigned Role:</strong> {user?.role}</li>
                        </ul>
                    </div>
                </div>
            </main>
        </div>
    );
};

export default Dashboard;