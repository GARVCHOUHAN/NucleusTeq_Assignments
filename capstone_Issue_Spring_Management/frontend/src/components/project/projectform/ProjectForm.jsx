import {useState} from "react";
import ProjectService from "../../../services/project-service";
import Input from "../../project/common/input/Input";
import Button from "../../project/common/button/Button";
import styles from "./ProjectForm.module.css";

function ProjectForm({refresh}){

const [project,setProject]=useState({
name:"",
description:"",
project_key:"",
members:[]
});
const [error,setError]=useState("");
const [loading,setLoading]=useState(false);

async function submit(e){
e.preventDefault();

setError("");

const payload={
name:project.name.trim(),
description:project.description.trim(),
project_key:project.project_key.trim().toUpperCase(),
members:project.members
};

if(payload.name.length<3){
setError("Project name must be at least 3 characters");
return;
}

if(payload.description.length<5){
setError("Description must be at least 5 characters");
return;
}

if(payload.project_key.length<2){
setError("Project key must be at least 2 characters");
return;
}

try{
setLoading(true);
await ProjectService.createProject(payload);

refresh();
setProject({
name:"",
description:"",
project_key:"",
members:[]
});
}
catch(error){
setError(error.response?.data?.detail || "Project creation failed");
}
finally{
setLoading(false);
}

}

return(
<form className={styles.form} onSubmit={submit}>
<div className={styles.headerBlock}>
<h3>Create Project</h3>
<p>Use a consistent format so every project is easy to scan.</p>
</div>

<Input
label="Project Name"
value={project.name}
onChange={(e)=>
setProject({...project,name:e.target.value})
}
/>

<Input
label="Description"
value={project.description}
onChange={(e)=>
setProject({...project,description:e.target.value})
}
/>

<Input
label="Project Key"
value={project.project_key}
onChange={(e)=>
setProject({...project,project_key:e.target.value})
}
/>

<div className={styles.actions}>
<Button type="submit" disabled={loading}>
{loading?"Creating...":"Create Project"}
</Button>
</div>

{error && <p className={styles.error}>{error}</p>}

</form>
);

}

export default ProjectForm;
