
import axiosInstance from "../api/axios";

class CommentService {

    async getComments(issueId) {
        const response = await axiosInstance.get(`/issues/${issueId}/comments`);
        return response.data;
    }

    async createComment(issueId, body) {
        const response = await axiosInstance.post(`/issues/${issueId}/comments`, { body });
        return response.data;
    }
    async updateComment(commentId, body) {
        const response = await axiosInstance.put(`/comments/${commentId}`, { body });
        return response.data;
    }

    async deleteComment(commentId) {
        const response = await axiosInstance.delete(`/comments/${commentId}`);
        return response.data;
    }

}

export default new CommentService();