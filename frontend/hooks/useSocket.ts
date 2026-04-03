import { useEffect, useState } from "react";
import { io } from "socket.io-client";

export function useSocket() {
  const [data, setData] = useState<any[]>([]);

  useEffect(() => {
    const socket = io("http://localhost:8000");

    socket.on("live", (msg) => {
      setData(msg.response || []);
    });

    return () => socket.disconnect();
  }, []);

  return data;
}
