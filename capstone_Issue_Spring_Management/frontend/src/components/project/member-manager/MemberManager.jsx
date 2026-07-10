import { useEffect, useMemo, useState } from "react";

import AuthService from "../../../services/auth-service";
import ProjectService from "../../../services/project-service";
import styles from "./MemberManager.module.css";


function MemberManager({project,refresh}){
const [email,setEmail]=useState("");
const [suggestions,setSuggestions]=useState([]);
const [loading,setLoading]=useState(false);
const [error,setError]=useState("");
const [expandMembers,setExpandMembers]=useState(false);
const INITIAL_MEMBERS_SHOWN=2;

const assignedEmails=useMemo(
()=>new Set((project.members || []).map((member)=>member.email)),
[project.members]
);

useEffect(()=>{
const timeoutId=setTimeout(async()=>{
const search=email.trim();

if(search.length<2){
setSuggestions([]);
return;
}

try{
setLoading(true);
const users=await AuthService.searchMembers(search);
setSuggestions(
users.filter((user)=>!assignedEmails.has(user.email))
);
}
catch(error){
setError(error.response?.data?.detail || "Unable to search members");
}
finally{
setLoading(false);
}
},300);

return()=>clearTimeout(timeoutId);
},[email,assignedEmails]);

async function addMember(memberEmail=email){
setError("");
const cleanEmail=memberEmail.trim().toLowerCase();

if(!cleanEmail){
setError("Email is required");
return;
}

try{
await ProjectService.addMember(
project._id,
cleanEmail
);
setEmail("");
setSuggestions([]);
refresh?.();
}
catch(error){
setError(error.response?.data?.detail || "Unable to add member");
}
}

async function removeMember(memberEmail){
setError("");
try{
await ProjectService.removeMember(
project._id,
memberEmail
);
refresh?.();
}
catch(error){
setError(error.response?.data?.detail || "Unable to remove member");
}
}

return(
<div className={styles.box}>
<h4>Team Members</h4>

<div className={styles.memberList}>
{
project.members?.length?
(expandMembers ? project.members : project.members.slice(0, INITIAL_MEMBERS_SHOWN)).map(member=>
<div
className={styles.member}
key={member.email}
>
<span>
<strong>{member.name}</strong>
<small>{member.email}</small>
</span>
<button
type="button"
className={styles.removeBtn}
onClick={()=>removeMember(member.email)}
title="Remove member"
>
✕
</button>
</div>
)
:
<p className={styles.empty}>No members assigned yet.</p>
}
</div>

{project.members?.length > INITIAL_MEMBERS_SHOWN && (
<button 
  className={styles.viewAllBtn}
  onClick={() => setExpandMembers(!expandMembers)}
>
  {expandMembers ? '▲ Show Less' : `▼ View All (${project.members.length})`}
</button>
)}

<div className={styles.search}>
<input
placeholder="Search members by name or email"
value={email}
onChange={(event)=>setEmail(event.target.value)}
/>
<button type="button" className={styles.addBtn} onClick={()=>addMember()}>
Add
</button>
</div>

{loading && <p className={styles.hint}>Searching...</p>}

{suggestions.length>0 && (
<div className={styles.suggestions}>
{suggestions.map((user)=>(
<button
type="button"
key={user.email}
onClick={()=>addMember(user.email)}
>
<span>{user.name}</span>
<small>{user.email}</small>
</button>
))}
</div>
)}

{error && <p className={styles.error}>{error}</p>}
</div>
);
}

export default MemberManager;
