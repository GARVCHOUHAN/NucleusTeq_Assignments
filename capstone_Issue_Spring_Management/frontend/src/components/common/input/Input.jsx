import styles from "./Input.module.css";


function Input({
    label,
    type,
    value,
    onChange,
    placeholder
}) {

    return (

        <div className={styles.inputGroup}>

            <label>
                {label}
            </label>

            <input
                type={type}
                value={value}
                onChange={onChange}
                placeholder={placeholder}
            />

        </div>

    );

}


export default Input;