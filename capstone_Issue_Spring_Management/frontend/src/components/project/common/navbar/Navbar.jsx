import { useNavigate } from "react-router-dom";

import { useAuth } from "../../../../hooks/use-auth";
import styles from "./Navbar.module.css";

function Navbar() {
    const { currentUser, logout } = useAuth();
    const navigate = useNavigate();

    function handleLogout() {
        logout();
        navigate("/login");
    }

    return (
        <div className={styles.navbar}>
            <div className={styles.brand}>Issue Management</div>
            <div className={styles.actions}>
                <span>{currentUser?.name}</span>
                <button onClick={handleLogout}>Logout</button>
            </div>
        </div>
    );
}

export default Navbar;
