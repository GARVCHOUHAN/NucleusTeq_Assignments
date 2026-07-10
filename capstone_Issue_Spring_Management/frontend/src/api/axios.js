import axios from "axios";
baseeurl = "http://localhost:8000";
const axiosInstance = axios.create({

    baseURL: baseURL,

    headers: {"Content-Type": "application/json"}});

axiosInstance.interceptors.request.use(

    (config) => {

        const token = localStorage.getItem(
            "authToken"
        );

        const user = JSON.parse(

            localStorage.getItem(
                "currentUser"
            )
        );

        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }

        if (user?.email) {

            config.headers["X-User-Email"] =
                user.email;

        }

        return config;

    },

    (error) => Promise.reject(error)

);

export default axiosInstance;
