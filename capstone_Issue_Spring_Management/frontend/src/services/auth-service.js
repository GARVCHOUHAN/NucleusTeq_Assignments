import axiosInstance from "../api/axios";


class AuthService {
    async register(registerData) {
        const response = await axiosInstance.post(
            "/auth/register",
            registerData
        );
        return response.data;
    }

    async login(loginData) {
        const response = await axiosInstance.post(
            "/auth/login",
            loginData
        );
        return response.data;
    }

    async searchMembers(search) {
        const response = await axiosInstance.get(
            "/auth/users",
            {
                params: {
                    search
                }
            }
        );
        return response.data;
    }
}

export default new AuthService();
