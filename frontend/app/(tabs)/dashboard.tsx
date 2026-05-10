import { useEffect } from "react";
import { View, Text } from "react-native";
import { checkHealth } from "@/services/health_service";

export default function DashboardScreen() {
  useEffect(() => {
    async function testConnection() {
      try {
        const data = await checkHealth();
        console.log(data);
      } catch (error) {
        console.error(error);
      }
    }

    testConnection();
  }, []);

  return (
    <View
      style={{
        flex: 1,
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <Text>Dashboard</Text>
    </View>
  );
}
