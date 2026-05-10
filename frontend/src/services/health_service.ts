import { api } from "@/api/client";

export async function checkHealth() {
    try {
        const response = await api.get("/api/v1/health/");
        return response.data;
    } catch (error) {
        console.error("Health check failed:", error);
        throw error;
    }
}
