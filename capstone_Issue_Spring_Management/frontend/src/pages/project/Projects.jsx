import Navbar from "../../components/project/common/navbar/Navbar";
import Sidebar from "../../components/project/common/sidebar/Sidebar";
import ProjectCard from "../../components/project/project-card/ProjectCard";
import ProjectForm from "../../components/project/projectform/ProjectForm";
import { useAuth } from "../../hooks/use-auth";
import { useProjects } from "../../hooks/use-project";

import styles from "./Project.module.css";


function Projects(){
const {currentUser}=useAuth();
const {
projects,
loading,
error,
loadProjects
}=useProjects();

return(
<div className={styles.layout}>

<Sidebar/>

<div className={styles.content}>
<Navbar/>

<main className={styles.page}>

<div className={styles.header}>
<div>
<h1>Projects</h1>
<p>{currentUser?.role==="ADMIN" ? "Manage projects and teams" : "Your assigned projects"}</p>
</div>
</div>

{currentUser?.role==="ADMIN" && <ProjectForm refresh={loadProjects}/>}

{error && <p className={styles.error}>{error}</p>}

<div className={styles.grid}>
{
loading?
<p>Loading...</p>
:
projects.length>0?
projects.map(project=>
<ProjectCard
key={project._id}
project={project}
refresh={loadProjects}
/>
)
:
<p>No projects found.</p>
}
</div>

</main>
</div>

</div>
);

}

export default Projects;
