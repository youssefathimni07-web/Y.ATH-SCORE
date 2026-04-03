import { useEffect, useState } from "react";
import { io } from "socket.io-client";

export function useSocket() {
  const [data, setData] = useState<any[]>([]);

  useEffect(() => {
    const socket = io("https://y-ath-score-9.onrender.com");

    socket.on("live", (msg) => {
      setData(msg.response || []);
    });

    return () => socket.disconnect();
  }, []);

  return data;
}
