import axiosInstance from "../api/axios";


class IssueService {
    async getIssues(params = {}) {
        const response = await axiosInstance.get(
            "/issues",
            {
                params
            }
        );
        return response.data;
    }

    async createIssue(data) {
        const response = await axiosInstance.post(
            "/issues",
            data
        );
        return response.data;
    }

    async updateIssue(issueId, data) {
        const response = await axiosInstance.patch(
            `/issues/${issueId}`,
            data
        );
        return response.data;
    }

    async getSubtasks(issueId) {
        const response = await axiosInstance.get(
            `/issues/${issueId}/subtasks`
        );
        return response.data;
    }

    async deleteIssue(issueId) {
        const response = await axiosInstance.delete(
            `/issues/${issueId}`
        );
        return response.data;
    }

    async updateStatus(issueId, status) {
        const response = await axiosInstance.patch(
            `/issues/${issueId}/status`,
            {
                status
            }
        );
        return response.data;
    }

    async getComments(issueId) {
        const response = await axiosInstance.get(
            `/issues/${issueId}/comments`
        );
        return response.data;
    }

    async addComment(issueId, body) {
        const response = await axiosInstance.post(
            `/issues/${issueId}/comments`,
            {
                body
            }
        );
        return response.data;
    }

    async updateComment(commentId, body) {
        const response = await axiosInstance.put(
            `/comments/${commentId}`,
            {
                body
            }
        );
        return response.data;
    }

    async deleteComment(commentId) {
        const response = await axiosInstance.delete(
            `/comments/${commentId}`
        );
        return response.data;
    }
}

export default new IssueService();
