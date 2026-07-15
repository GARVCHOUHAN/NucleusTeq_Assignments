import { useCallback, useEffect, useState } from "react";

import ProjectService from "../services/project-service";
import { useAuth } from "./use-auth";


export function useProjects(){
const {currentUser}=useAuth();
const [projects,setProjects]=useState([]);
const [loading,setLoading]=useState(false);
const [error,setError]=useState("");

const loadProjects=useCallback(async()=>{
if(!currentUser){
setProjects([]);
return;
}

setLoading(true);
setError("");

try{
const data=currentUser.role==="ADMIN"
? await ProjectService.getProjects()
: await ProjectService.getAssignedProjects();
setProjects(data);
}
catch(error){
setError(error.response?.data?.detail || "Unable to load projects");
}
finally{
setLoading(false);
}

},[currentUser]);

useEffect(()=>{
loadProjects();
},[loadProjects]);

return{
projects,
loading,
error,
loadProjects
};

}
