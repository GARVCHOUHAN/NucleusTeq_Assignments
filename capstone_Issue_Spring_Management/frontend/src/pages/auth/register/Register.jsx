import { useNavigate } from "react-router-dom";
import RegisterForm from "../../../components/auth/register-form/RegisterForm";
import { ROUTES } from "../../../constants/routes";
import styles from "./Register.module.css";

function Register() {
    const navigate = useNavigate();

    return (
        <div className={styles.page}>
            <div className={styles.card}>
                <div className={styles.header}>
                    <p className={styles.overline}>Create your workspace</p>
                    <h2 className={styles.title}>Register for SprintManager</h2>
                    <p className={styles.subtitle}>Create an account to manage your projects, assign issues, and track sprint progress.</p>
                </div>
                <RegisterForm />

                <div className={styles.divider}>
                    <span>Already have an account?</span>
                </div>

                <button 
                    type="button"
                    className={styles.loginButton}
                    onClick={() => navigate(ROUTES.LOGIN)}
                >
                    Sign In
                </button>
            </div>
        </div>
    );
}

export default Register;