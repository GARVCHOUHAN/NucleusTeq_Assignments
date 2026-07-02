import { useContext } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';

const Navbar = () => {
    const { user, logout } = useContext(AuthContext);
    const navigate = useNavigate();

    const handleLogout = () => {
        logout();
        navigate('/login');
    };

    return (
        <nav className="bg-gray-800 text-white p-4 shadow-md">
            <div className="container mx-auto flex justify-between items-center">
                <Link to="/dashboard" className="text-xl font-bold tracking-wider">
                    SprintManager
                </Link>
                
                {user && (
                    <div className="flex items-center gap-6">
                        <span className="text-sm text-gray-300">
                            Logged in as: <strong className="text-white">{user.username}</strong> 
                            <span className="ml-2 px-2 py-1 bg-blue-600 rounded-full text-xs">
                                {user.role}
                            </span>
                        </span>
                        <button 
                            onClick={handleLogout}
                            className="bg-red-500 hover:bg-red-600 px-4 py-2 rounded transition"
                        >
                            Logout
                        </button>
                    </div>
                )}
            </div>
        </nav>
    );
};

export default Navbar;