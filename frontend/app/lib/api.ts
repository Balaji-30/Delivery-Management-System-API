import { Api } from "./client";

const baseUrl = import.meta.env.VITE_BACKEND_URL || "http://localhost:8000";

const api = new Api({
    baseURL: baseUrl,
    securityWorker: (token)=>{
        if (token) {
            return {
                headers: {
                    Authorization: `Bearer ${token}`,
            }
        }
    }
    return {}
}})

export default api;