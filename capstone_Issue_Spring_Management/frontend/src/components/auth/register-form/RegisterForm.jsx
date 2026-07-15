import { useState } from "react";
import { useNavigate } from "react-router-dom";
import Input from "../../common/input/Input";
import Button from "../../common/button/Button";
import AuthService from "../../../services/auth-service";
import { ROUTES } from "../../../constants/routes";
import styles from "./Register.module.css";

function RegisterForm() {
    const navigate = useNavigate();
    const [form, setForm] = useState({
        name: "",
        email: "",
        password: "",
        role: "MEMBER"
    });
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);

    function isStrongPassword(password) {
        return /[A-Z]/.test(password) &&
            /[a-z]/.test(password) &&
            /\d/.test(password) &&
            /[^A-Za-z0-9]/.test(password) &&
            password.length >= 8;
    }

    function handleChange(event) {
        setForm({ ...form, [event.target.name]: event.target.value });
    }



async function handleSubmit(event) {
    event.preventDefault();
    setError("");

    const cleanForm = {
        ...form,
        name: form.name.trim(),
        email: form.email.trim().toLowerCase()
    };

    if (cleanForm.name.length < 3) {
        setError("Name must contain at least 3 characters.");
        return;
    }

    if (!isStrongPassword(cleanForm.password)) {
        setError("Password must include uppercase, lowercase, number, and special character.");
        return;
    }

    setLoading(true);

    try {
        await AuthService.register(cleanForm);
        navigate(ROUTES.LOGIN);
    } catch (error) {
        setError(error.response?.data?.detail || "Registration failed.");
    } finally {
        setLoading(false);
    }
}

return (
    <form className={styles.form} onSubmit={handleSubmit}>
        <Input
            label="Full Name"
            type="text"
            value={form.name}
            onChange={(e) => setForm({ ...form, name: e.target.value })}
            placeholder="John Doe"
        />

        <Input
            label="Email"
            type="email"
            value={form.email}
            onChange={(e) => setForm({ ...form, email: e.target.value })}
            placeholder="you@example.com"
        />

        <Input
            label="Password"
            type="password"
            value={form.password}
            onChange={(e) => setForm({ ...form, password: e.target.value })}
            placeholder="Create a secure password"
        />

        <div className={styles.field}>
            <label>Role</label>
            <select
                name="role"
                value={form.role}
                onChange={handleChange}
                className={styles.select}
            >
                <option value="MEMBER">Member</option>
                <option value="ADMIN">Admin</option>
            </select>
        </div>

        {error && <div className={styles.error}>{error}</div>}

        <Button type="submit" disabled={loading}>
            {loading ? "Creating..." : "Register"}
        </Button>
    </form>
);
}

export default RegisterForm;
