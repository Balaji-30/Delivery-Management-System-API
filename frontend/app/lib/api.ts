import { Api } from "./client";

const api = new Api({
    baseURL: "http://127.0.0.1:8000",
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