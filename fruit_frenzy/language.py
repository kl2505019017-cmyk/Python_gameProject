"""language.py - Bilingual (English / Bahasa Melayu) text for the interface."""

TEXT = {
    "en": {
        "title": "FRUIT FRENZY",
        "subtitle": "Catch the fruits, dodge the bombs!",
        "start": "Start Game",
        "instructions": "Instructions",
        "language": "Language: English",
        "exit": "Exit",
        "menu_hint": "Up/Down: select   Enter: confirm   L: language",
        "how_title": "HOW TO PLAY",
        "how_lines": [
            "Move the basket with the LEFT / RIGHT arrow keys.",
            "Catch fruits to score. Missing a fruit costs 1 life.",
            "Catching a bomb costs 1 life. Avoid them!",
            "Catch the heart power-up to gain 1 life (max 5).",
            "Chain catches for a combo multiplier (x2, x3).",
            "Survive 60 seconds to win. Lives at 0 = game over.",
            "P: pause    R: restart    ESC: back to menu",
        ],
        "points": "points",
        "life": "life",
        "bomb": "-1 life",
        "back_hint": "Press any key to go back",
        "score": "Score",
        "best": "Best",
        "time": "Time",
        "level": "Level",
        "combo": "Combo",
        "paused": "PAUSED",
        "paused_hint": "P: resume    R: restart    ESC: menu",
        "win": "YOU WIN!",
        "lose": "GAME OVER",
        "final_score": "Final score",
        "new_best": "New high score!",
        "over_hint": "R / Enter: play again    ESC: menu",
        "level_up": "LEVEL {n}",
    },
    "ms": {
        "title": "FRUIT FRENZY",
        "subtitle": "Tangkap buah, elak bom!",
        "start": "Mula Permainan",
        "instructions": "Arahan",
        "language": "Bahasa: Melayu",
        "exit": "Keluar",
        "menu_hint": "Atas/Bawah: pilih   Enter: sahkan   L: bahasa",
        "how_title": "CARA BERMAIN",
        "how_lines": [
            "Gerakkan bakul dengan kekunci anak panah KIRI / KANAN.",
            "Tangkap buah untuk skor. Terlepas buah hilang 1 nyawa.",
            "Menangkap bom hilang 1 nyawa. Elakkan bom!",
            "Tangkap hati untuk tambah 1 nyawa (maksimum 5).",
            "Tangkapan berturut-turut beri gandaan kombo (x2, x3).",
            "Bertahan 60 saat untuk menang. Nyawa 0 = tamat.",
            "P: jeda    R: mula semula    ESC: kembali ke menu",
        ],
        "points": "mata",
        "life": "nyawa",
        "bomb": "-1 nyawa",
        "back_hint": "Tekan sebarang kekunci untuk kembali",
        "score": "Skor",
        "best": "Terbaik",
        "time": "Masa",
        "level": "Tahap",
        "combo": "Kombo",
        "paused": "DIJEDA",
        "paused_hint": "P: sambung    R: mula semula    ESC: menu",
        "win": "ANDA MENANG!",
        "lose": "TAMAT PERMAINAN",
        "final_score": "Skor akhir",
        "new_best": "Skor tertinggi baru!",
        "over_hint": "R / Enter: main lagi    ESC: menu",
        "level_up": "TAHAP {n}",
    },
}


class Translator:
    """Small helper that returns text in the currently selected language."""

    def __init__(self, lang="en"):
        self.lang = lang

    def toggle(self):
        self.lang = "ms" if self.lang == "en" else "en"

    def __call__(self, key, **kwargs):
        value = TEXT[self.lang][key]
        return value.format(**kwargs) if isinstance(value, str) and kwargs else value
