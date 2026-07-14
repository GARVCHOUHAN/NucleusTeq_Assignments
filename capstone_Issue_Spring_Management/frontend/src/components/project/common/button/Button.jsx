import styles from "./Button.module.css";


function Button({
children,
type="button",
onClick,
disabled
}){
return(
<button
type={type}
onClick={onClick}
disabled={disabled}
className={styles.button}
>
{children}
</button>
);
}

export default Button;
