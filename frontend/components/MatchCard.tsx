export default function MatchCard({ match }: any) {
  return (
    <div className="card">
      <h3>
        {match.teams.home.name} vs {match.teams.away.name}
      </h3>

      <p>
        ⚽ {match.goals.home} - {match.goals.away}
      </p>

      <small>
        🕒 {match.fixture.status.elapsed} min
      </small>
    </div>
  );
}
