export async function getMatches() {
  const res = await fetch("http://localhost:8000/matches");
  return res.json();
}
