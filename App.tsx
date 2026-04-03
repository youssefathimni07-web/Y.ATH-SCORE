import { useEffect } from "react";
import { useSocket } from "./hooks/useSocket";
import { initNotifications } from "./firebase";
import MatchCard from "./components/MatchCard";
import Navbar from "./components/Navbar";

export default function App() {
  const matches = useSocket();

  useEffect(() => {
    initNotifications();
  }, []);

  return (
    <>
      <Navbar />

      <div className="container">
        <h2>⚽ Live Matches</h2>

        {matches.length === 0 && <p>Loading...</p>}

        {matches.map((m: any) => (
          <MatchCard key={m.fixture.id} match={m} />
        ))}
      </div>
    </>
  );
}
