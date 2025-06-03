import requests

class SoundCloud:
    def __init__(self):
        # Usa aqui o teu client_id válido e fixo
        self.client_id = "1yti6vQ083VZh29fcJTHSDD56pjuQvI9"

    def get_track_url(self, transcoding_url):
        """
        Recebe a URL de transcodificação e retorna o URL direto do áudio (progressive).
        """
        url = f"{transcoding_url}?client_id={self.client_id}"
        res = requests.get(url)
        if res.status_code == 200:
            data = res.json()
            return data.get("url")
        else:
            print(f"Erro ao obter URL do track: {res.status_code}")
            return None

    def search_playlist(self, query):
        """
        Pesquisa playlists no SoundCloud e retorna a primeira que tenha faixas.
        """
        url = f"https://api-v2.soundcloud.com/search/playlists?q={query}&client_id={self.client_id}&limit=10"
        print(f"🔍 A procurar playlists: {url}")
        res = requests.get(url)
        if res.status_code != 200:
            print(f"❌ Erro ao obter playlist: {res.status_code}")
            return None

        data = res.json()
        playlists = data.get("collection", [])
        if not playlists:
            print("❌ Nenhuma playlist encontrada.")
            return None

        # Procura a primeira playlist que tenha faixas
        playlist = None
        for p in playlists:
            if p.get("tracks"):
                playlist = p
                break

        if not playlist:
            print("❌ Nenhuma playlist com faixas encontrada.")
            return None

        tracks = []
        for track in playlist.get("tracks", []):
            transcodings = track.get("media", {}).get("transcodings", [])
            url_mp3 = None
            for t in transcodings:
                if t["format"]["protocol"] == "progressive":
                    url_mp3 = self.get_track_url(t["url"])
                    if url_mp3:
                        break
            if url_mp3:
                tracks.append({
                    "title": track["title"],
                    "url": url_mp3,
                    "duration": int(track["duration"] / 1000)
                })

        return {
            "title": playlist["title"],
            "tracks": tracks
        }
