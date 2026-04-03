// 🌍 رابط السيرفر (Render)
const API = "https://y-ath-score-9.onrender.com"

// 🔁 طلب عام مع retry
async function fetchWithRetry(url: string, retries = 3) {
  try {
    const res = await fetch(url)

    if (!res.ok) throw new Error("Network error")

    return await res.json()
  } catch (err) {
    if (retries > 0) {
      console.log("Retrying...", retries)
      return fetchWithRetry(url, retries - 1)
    }
    console.error("API Failed:", err)
    return null
  }
}

//////////////////////////////////////////////////////////
// ⚽ المباريات المباشرة
//////////////////////////////////////////////////////////

export const getLiveMatches = async () => {
  const data = await fetchWithRetry(`${API}/matches`)

  if (!data || !data.response) return []

  return data.response.map((m: any) => ({
    id: m.fixture.id,
    date: m.fixture.date,
    status: m.fixture.status.short,
    elapsed: m.fixture.status.elapsed,

    league: {
      name: m.league.name,
      logo: m.league.logo,
      round: m.league.round
    },

    home: {
      id: m.teams.home.id,
      name: m.teams.home.name,
      logo: m.teams.home.logo
    },

    away: {
      id: m.teams.away.id,
      name: m.teams.away.name,
      logo: m.teams.away.logo
    },

    goals: {
      home: m.goals.home,
      away: m.goals.away
    }
  }))
}

//////////////////////////////////////////////////////////
// 🧠 AI Prediction
//////////////////////////////////////////////////////////

export const getPrediction = async (home: number, away: number) => {
  const data = await fetchWithRetry(`${API}/predict/${home}/${away}`)

  if (!data) return { result: "غير متوفر" }

  return data
}

//////////////////////////////////////////////////////////
// ⭐ Favorites (LocalStorage)
//////////////////////////////////////////////////////////

const FAVORITES_KEY = "favorites_matches"

export const getFavorites = (): number[] => {
  const data = localStorage.getItem(FAVORITES_KEY)
  return data ? JSON.parse(data) : []
}

export const toggleFavorite = (id: number) => {
  const favs = getFavorites()

  if (favs.includes(id)) {
    const updated = favs.filter(f => f !== id)
    localStorage.setItem(FAVORITES_KEY, JSON.stringify(updated))
    return updated
  } else {
    const updated = [...favs, id]
    localStorage.setItem(FAVORITES_KEY, JSON.stringify(updated))
    return updated
  }
}

export const isFavorite = (id: number) => {
  return getFavorites().includes(id)
}

//////////////////////////////////////////////////////////
// 🔔 إرسال Token للإشعارات
//////////////////////////////////////////////////////////

export const saveUserToken = async (token: string) => {
  try {
    await fetch(`${API}/save-token`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ token })
    })
  } catch (err) {
    console.error("Token error:", err)
  }
}

//////////////////////////////////////////////////////////
// 📊 ترتيب (لو أضفت endpoint لاحقًا)
//////////////////////////////////////////////////////////

export const getStandings = async () => {
  const data = await fetchWithRetry(`${API}/standings`)
  return data?.response || []
}

//////////////////////////////////////////////////////////
// 💬 Chat (اختياري لاحقًا)
//////////////////////////////////////////////////////////

export const sendMessage = async (msg: string) => {
  try {
    await fetch(`${API}/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ message: msg })
    })
  } catch (err) {
    console.error("Chat error:", err)
  }
}

//////////////////////////////////////////////////////////
// ⚡ Helper
//////////////////////////////////////////////////////////

export const formatTime = (date: string) => {
  return new Date(date).toLocaleTimeString("ar", {
    hour: "2-digit",
    minute: "2-digit"
  })
}
