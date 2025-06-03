const form = document.getElementById("search-form");
const input = document.getElementById("search-input");
const playlistTitle = document.getElementById("playlist-title");
const trackList = document.getElementById("track-list");
const playlistInfo = document.getElementById("playlist-info");
const audio = document.getElementById("audio-player");

let tracks = [];
let currentTrackIndex = 0;

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const query = input.value.trim();
  if (!query) return;

  playlistTitle.textContent = "Carregando...";
  trackList.innerHTML = "";
  playlistInfo.classList.remove("hidden");
  audio.pause();
  audio.src = "";

  try {
    const res = await fetch(`/search?query=${encodeURIComponent(query)}`);
    if (!res.ok) throw new Error("Nenhuma playlist encontrada.");

    const data = await res.json();
    playlistTitle.textContent = data.title || "Playlist";
    tracks = data.tracks || [];
    if (tracks.length === 0) {
      trackList.innerHTML = "<li>Nenhuma faixa encontrada.</li>";
      return;
    }
    renderTrackList();
    playTrack(0);
  } catch (error) {
    playlistTitle.textContent = "Erro: " + error.message;
    trackList.innerHTML = "";
  }
});

function renderTrackList() {
  trackList.innerHTML = "";
  tracks.forEach((track, i) => {
    const li = document.createElement("li");
    li.textContent = track.title;
    li.title = `Duração: ${formatDuration(track.duration)}`;
    li.dataset.index = i;
    li.addEventListener("click", () => {
      playTrack(i);
    });
    trackList.appendChild(li);
  });
  updateActiveTrack();
}

function playTrack(index) {
  if (index < 0 || index >= tracks.length) return;
  currentTrackIndex = index;
  audio.src = tracks[index].url;
  audio.play();
  updateActiveTrack();
}

function updateActiveTrack() {
  const lis = trackList.querySelectorAll("li");
  lis.forEach((li) => li.classList.remove("active"));
  const currentLi = trackList.querySelector(`li[data-index="${currentTrackIndex}"]`);
  if (currentLi) currentLi.classList.add("active");
}

audio.addEventListener("ended", () => {
  if (currentTrackIndex < tracks.length - 1) {
    playTrack(currentTrackIndex + 1);
  }
});

function formatDuration(seconds) {
  const m = Math.floor(seconds / 60);
  const s = seconds % 60;
  return `${m}:${s.toString().padStart(2, "0")}`;
}
