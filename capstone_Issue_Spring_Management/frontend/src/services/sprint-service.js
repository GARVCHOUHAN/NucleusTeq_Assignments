import axiosInstance from "../api/axios";


class SprintService {
    async getSprints(projectId = "") {
        const response = await axiosInstance.get(
            "/sprints",
            {
                params: projectId ? {
                    project_id: projectId
                } : {}
            }
        );
        return response.data;
    }

    async createSprint(data) {
        const response = await axiosInstance.post(
            "/sprints",
            data
        );
        return response.data;
    }

    async addIssue(sprintId, issueId) {
        const response = await axiosInstance.post(
            `/sprints/${sprintId}/issues`,
            {
                issue_id: issueId
            }
        );
        return response.data;
    }

    async removeIssue(sprintId, issueId) {
        const response = await axiosInstance.delete(
            `/sprints/${sprintId}/issues/${issueId}`
        );
        return response.data;
    }

    async startSprint(sprintId) {
        const response = await axiosInstance.patch(
            `/sprints/${sprintId}/start`
        );
        return response.data;
    }

    async completeSprint(sprintId) {
        const response = await axiosInstance.patch(
            `/sprints/${sprintId}/complete`
        );
        return response.data;
    }
}

export default new SprintService();
