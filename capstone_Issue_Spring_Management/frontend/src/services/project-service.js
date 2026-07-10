import axiosInstance from "../api/axios";
class ProjectService{

async getProjects(){
const response=await axiosInstance.get("/projects");
return response.data;
}

async getAssignedProjects(){
const response=await axiosInstance.get("/projects/assigned/me");
return response.data;
}

async createProject(data){
const response=await axiosInstance.post("/projects",data);
return response.data;
}

async updateProject(id,data){
const response=await axiosInstance.put(`/projects/${id}`,data);
return response.data;
}

async deleteProject(id){
const response=await axiosInstance.delete(`/projects/${id}`);
return response.data;
}

async addMember(projectId,email){
const response=await axiosInstance.post(
`/projects/${projectId}/members`,
{email}
);
return response.data;
}

async removeMember(projectId,email){
const response=await axiosInstance.delete(
`/projects/${projectId}/members/${email}`
);
return response.data;
}

}

export default new ProjectService();