import { NavLink } from "react-router-dom";
import { ROUTES } from "../../../../constants/routes";
import styles from "./Sidebar.module.css";


function Sidebar(){
const linkClass=({isActive})=>isActive ? styles.active : undefined;

return(
<aside className={styles.sidebar}>

<h2>IMS</h2>

<nav className={styles.nav}>
<NavLink className={linkClass} to={ROUTES.DASHBOARD}>Dashboard</NavLink>
<NavLink className={linkClass} to={ROUTES.PROJECTS}>Projects</NavLink>
<NavLink className={linkClass} to={ROUTES.ISSUES}>Issues</NavLink>
<NavLink className={linkClass} to={ROUTES.SPRINTS}>Sprints</NavLink>
</nav>

</aside>
);
}

export default Sidebar;
