import axiosInstance from "../api/axios";


class DashboardService {
    async getStats() {
        const response = await axiosInstance.get(
            "/dashboard/stats"
        );
        return response.data;
    }
}

export default new DashboardService();
