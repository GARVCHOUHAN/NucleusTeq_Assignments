import { useState } from "react";

import { useAuth } from "../../../hooks/use-auth";
import ProjectService from "../../../services/project-service";
import MemberManager from "../member-manager/MemberManager";
import styles from "./ProjectCard.module.css";


function ProjectCard({project,refresh}){
const {currentUser}=useAuth();
const [editing,setEditing]=useState(false);
const [saving,setSaving]=useState(false);
const [error,setError]=useState("");
const [form,setForm]=useState({
name:project.name || "",
description:project.description || "",
project_key:project.project_key || ""
});

function resetForm(){
setForm({
name:project.name || "",
description:project.description || "",
project_key:project.project_key || ""
});
}

function updateField(event){
setForm({
...form,
[event.target.name]:event.target.value
});
}

async function saveProject(){
setError("");

const payload={
name:form.name.trim(),
description:form.description.trim(),
project_key:form.project_key.trim().toUpperCase()
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
setSaving(true);
await ProjectService.updateProject(project._id,payload);
setEditing(false);
resetForm();
refresh?.();
}
catch(error){
setError(error.response?.data?.detail || "Unable to update project");
}
finally{
setSaving(false);
}
}

async function deleteProject(){
setError("");

try{
await ProjectService.deleteProject(project._id);
refresh?.();
}
catch(error){
setError(error.response?.data?.detail || "Unable to delete project");
}
}

return(
<div className={styles.card}>

{editing?
<div className={styles.editForm}>
<label className={styles.fieldLabel}>Project Name</label>
<input
name="name"
value={form.name}
onChange={updateField}
placeholder="Project Name"
/>
<label className={styles.fieldLabel}>Description</label>
<textarea
name="description"
value={form.description}
onChange={updateField}
placeholder="Project Description"
/>
<label className={styles.fieldLabel}>Project Key</label>
<input
name="project_key"
value={form.project_key}
onChange={updateField}
placeholder="Project Key"
/>
</div>
:
<>
<h3>{project.name}</h3>
<p>{project.description}</p>
<span>{project.project_key}</span>

<div style={{marginTop: 'auto', paddingTop: '12px', borderTop: '1px solid #f0f0f0'}}>
    <p style={{margin: '8px 0', fontSize: '0.9rem', color: '#6b7280'}}>
        👥 Members: <strong style={{color: '#1f2937'}}>{project.members?.length || 0}</strong>
    </p>
</div>
</>
}

{error && <p className={styles.error}>{error}</p>}

{
currentUser?.role==="ADMIN" &&
<div className={styles.actions}>

{editing?
<>
<button onClick={saveProject} disabled={saving}>
{saving?"Saving...":"Save"}
</button>
<button onClick={() => { resetForm(); setEditing(false); }} disabled={saving}>
Cancel
</button>
</>
:
<>
<button onClick={()=>{ resetForm(); setEditing(true); }}>
✏️ Edit
</button>
<button onClick={deleteProject} style={{background: '#ef4444'}}>
🗑️ Delete
</button>
</>
}

</div>
}
{
currentUser?.role==="ADMIN" && !editing &&
<MemberManager
project={project}
refresh={refresh}
/>
}

</div>
);

}

export default ProjectCard;
