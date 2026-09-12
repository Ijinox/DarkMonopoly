"""
DarkMonopoly - v1
Prototype de Monopoly classique européen (édition française).
Single-file, Tkinter, 4 thèmes : Clair / Sombre / Nuit Bleu / Nuit Rouge.

Lancement : python darkmonopoly.py
"""

import tkinter as tk
from tkinter import messagebox, simpledialog
from dataclasses import dataclass, field
from typing import List
import random

# ============================================================
#  CONSTANTES / DONNÉES
# ============================================================

CELL = 60
GRID = 11
BOARD_PX = CELL * GRID  # 660

PLAYER_COLORS = ["#e63946", "#457b9d", "#2a9d8f", "#e9c46a"]

GROUP_COLORS = {
    "brown": "#8b5a2b",
    "lightblue": "#aae0fa",
    "pink": "#d93a96",
    "orange": "#f7941d",
    "red": "#ed1b24",
    "yellow": "#fef200",
    "green": "#1fb25a",
    "darkblue": "#0072bb",
}

GROUP_HOUSE_COST = {
    "brown": 50, "lightblue": 50,
    "pink": 100, "orange": 100,
    "red": 150, "yellow": 150,
    "green": 200, "darkblue": 200,
}

THEMES = {
    "clair": {
        "label": "Clair",
        "bg": "#f0f2f5",
        "panel_bg": "#ffffff",
        "fg": "#1a1a1a",
        "muted": "#6b7280",
        "accent": "#2563eb",
        "accent_fg": "#ffffff",
        "board_bg": "#fafafa",
        "square_bg": "#ffffff",
        "border": "#cbd5e1",
        "button_bg": "#e5e7eb",
        "button_fg": "#1a1a1a",
        "button_active": "#d1d5db",
        "log_bg": "#ffffff",
        "log_fg": "#111827",
    },
    "sombre": {
        "label": "Sombre",
        "bg": "#181818",
        "panel_bg": "#242424",
        "fg": "#e5e5e5",
        "muted": "#9ca3af",
        "accent": "#60a5fa",
        "accent_fg": "#0a0a0a",
        "board_bg": "#1e1e1e",
        "square_bg": "#2a2a2a",
        "border": "#404040",
        "button_bg": "#333333",
        "button_fg": "#e5e5e5",
        "button_active": "#444444",
        "log_bg": "#1c1c1c",
        "log_fg": "#e5e5e5",
    },
    "nuit_bleu": {
        "label": "Nuit Bleu",
        "bg": "#0a1929",
        "panel_bg": "#0f2740",
        "fg": "#c9e4ff",
        "muted": "#6b9bc9",
        "accent": "#3fa9f5",
        "accent_fg": "#0a1929",
        "board_bg": "#0d2036",
        "square_bg": "#12294a",
        "border": "#1e4d7a",
        "button_bg": "#153562",
        "button_fg": "#c9e4ff",
        "button_active": "#1e4d7a",
        "log_bg": "#0b1e33",
        "log_fg": "#c9e4ff",
    },
    "nuit_rouge": {
        "label": "Nuit Rouge",
        "bg": "#1a0a0a",
        "panel_bg": "#2d1010",
        "fg": "#ffd0c9",
        "muted": "#c98a80",
        "accent": "#f53f3f",
        "accent_fg": "#1a0a0a",
        "board_bg": "#250d0d",
        "square_bg": "#381515",
        "border": "#7a1e1e",
        "button_bg": "#4a1515",
        "button_fg": "#ffd0c9",
        "button_active": "#7a1e1e",
        "log_bg": "#200a0a",
        "log_fg": "#ffd0c9",
    },
}


@dataclass
class Square:
    name: str
    kind: str                       # go / street / station / utility / chance / chest / tax / jail / freeparking / gotojail
    price: int = 0
    rents: List[int] = field(default_factory=list)  # [base, 1m, 2m, 3m, 4m, hôtel]
    group: str = ""
    tax: int = 0


SQUARES: List[Square] = [
    Square("DÉPART", "go"),
    Square("Boulevard de Belleville", "street", 60, [2, 10, 30, 90, 160, 250], "brown"),
    Square("Caisse de Communauté", "chest"),
    Square("Rue Lecourbe", "street", 60, [4, 20, 60, 180, 320, 450], "brown"),
    Square("Impôt sur le revenu", "tax", tax=200),
    Square("Gare Montparnasse", "station", 200),
    Square("Rue de Vaugirard", "street", 100, [6, 30, 90, 270, 400, 550], "lightblue"),
    Square("Chance", "chance"),
    Square("Rue de Courcelles", "street", 100, [6, 30, 90, 270, 400, 550], "lightblue"),
    Square("Avenue de la République", "street", 120, [8, 40, 100, 300, 450, 600], "lightblue"),
    Square("PRISON", "jail"),
    Square("Boulevard de la Villette", "street", 140, [10, 50, 150, 450, 625, 750], "pink"),
    Square("Compagnie Électricité", "utility", 150),
    Square("Boulevard de Neuilly", "street", 140, [10, 50, 150, 450, 625, 750], "pink"),
    Square("Rue de Paradis", "street", 160, [12, 60, 180, 500, 700, 900], "pink"),
    Square("Gare de Lyon", "station", 200),
    Square("Place de la Bourse", "street", 180, [14, 70, 200, 550, 750, 950], "orange"),
    Square("Caisse de Communauté", "chest"),
    Square("Rue Réaumur", "street", 180, [14, 70, 200, 550, 750, 950], "orange"),
    Square("Avenue de l'Opéra", "street", 200, [16, 80, 220, 600, 800, 1000], "orange"),
    Square("PARC GRATUIT", "freeparking"),
    Square("Boulevard Malesherbes", "street", 220, [18, 90, 250, 700, 875, 1050], "red"),
    Square("Chance", "chance"),
    Square("Avenue Henri-Martin", "street", 220, [18, 90, 250, 700, 875, 1050], "red"),
    Square("Faubourg Saint-Honoré", "street", 240, [20, 100, 300, 750, 925, 1100], "red"),
    Square("Gare du Nord", "station", 200),
    Square("Place Pigalle", "street", 260, [22, 110, 330, 800, 975, 1150], "yellow"),
    Square("Caisse de Communauté", "chest"),
    Square("Boulevard Saint-Michel", "street", 260, [22, 110, 330, 800, 975, 1150], "yellow"),
    Square("Avenue Mozart", "street", 280, [24, 120, 360, 850, 1025, 1200], "yellow"),
    Square("ALLEZ EN PRISON", "gotojail"),
    Square("Boulevard de la Madeleine", "street", 300, [26, 130, 390, 900, 1100, 1275], "green"),
    Square("Compagnie des Eaux", "utility", 150),
    Square("Boulevard Haussmann", "street", 300, [26, 130, 390, 900, 1100, 1275], "green"),
    Square("Rue La Fayette", "street", 320, [28, 150, 450, 1000, 1200, 1400], "green"),
    Square("Gare Saint-Lazare", "station", 200),
    Square("Chance", "chance"),
    Square("Avenue des Champs-Élysées", "street", 350, [35, 175, 500, 1100, 1300, 1500], "darkblue"),
    Square("Taxe de luxe", "tax", tax=100),
    Square("Rue de la Paix", "street", 400, [50, 200, 600, 1400, 1700, 2000], "darkblue"),
]

CHANCE_CARDS = [
    ("Avancez jusqu'à la case Départ. Recevez 200 €.", "move_to", 0),
    ("Avancez à la Rue de la Paix.", "move_to", 39),
    ("Reculez de 3 cases.", "move_back", 3),
    ("Allez en prison. Ne passez pas par la case Départ.", "goto_jail", None),
    ("Amende de vitesse : payez 15 €.", "pay", 15),
    ("Votre immeuble vous rapporte : recevez 150 €.", "gain", 150),
    ("Frais de scolarité : payez 50 €.", "pay", 50),
    ("Erreur de la banque en votre faveur : recevez 200 €.", "gain", 200),
    ("Vous gagnez le gros lot : recevez 100 €.", "gain", 100),
]

CHEST_CARDS = [
    ("Erreur de la banque en votre faveur : recevez 200 €.", "gain", 200),
    ("Frais de médecin : payez 50 €.", "pay", 50),
    ("Rendez-vous à la case Départ. Recevez 200 €.", "move_to", 0),
    ("Allez en prison. Ne passez pas par la case Départ.", "goto_jail", None),
    ("Vous héritez de 100 €.", "gain", 100),
    ("Frais d'hôpital : payez 100 €.", "pay", 100),
    ("Vente de votre stock : recevez 50 €.", "gain", 50),
    ("Frais de scolarité : payez 50 €.", "pay", 50),
]


# ============================================================
#  MODÈLE DE JEU
# ============================================================

class Player:
    def __init__(self, name: str, color: str, is_ai: bool = False):
        self.name = name
        self.color = color
        self.is_ai = is_ai
        self.money = 1500
        self.position = 0
        self.properties: List[int] = []
        self.in_jail = False
        self.alive = True

    @property
    def net_worth(self):
        return self.money + sum(SQUARES[p].price for p in self.properties)


class Game:
    def __init__(self, n_players: int):
        self.players: List[Player] = []
        for i in range(n_players):
            self.players.append(Player(
                name=f"Joueur {i+1}",
                color=PLAYER_COLORS[i % len(PLAYER_COLORS)],
                is_ai=(i != 0),
            ))
        self.current = 0
        self.owner = {}          # pos -> player index
        self.houses = {}         # pos -> 0..5
        self.dice = (0, 0)
        self.doubles = 0
        self.phase = "roll"      # roll | end
        self.log: List[str] = []
        self.game_over = False
        self.winner = None
        self.turn_count = 0

    # ---------- utilitaires ----------
    def current_player(self) -> Player:
        return self.players[self.current]

    def alive_players(self):
        return [p for p in self.players if p.alive]

    def add_log(self, msg: str):
        self.log.append(msg)

    def roll_dice(self):
        d1 = random.randint(1, 6)
        d2 = random.randint(1, 6)
        self.dice = (d1, d2)
        return d1, d2

    def group_positions(self, group: str):
        return [i for i, s in enumerate(SQUARES) if s.group == group]

    def has_monopoly(self, player_idx: int, group: str) -> bool:
        positions = self.group_positions(group)
        return all(self.owner.get(p) == player_idx for p in positions)

    def move_player(self, p: Player, steps: int, pass_go: bool = True):
        old = p.position
        new = (old + steps) % 40
        if pass_go and new < old:
            p.money += 200
            self.add_log(f"→ {p.name} passe par DÉPART (+200 €)")
        p.position = new

    def compute_rent(self, pos: int) -> int:
        sq = SQUARES[pos]
        owner_idx = self.owner.get(pos)
        if owner_idx is None:
            return 0
        houses = self.houses.get(pos, 0)

        if sq.kind == "street":
            if houses == 0:
                base = sq.rents[0]
                return base * 2 if self.has_monopoly(owner_idx, sq.group) else base
            return sq.rents[houses]

        if sq.kind == "station":
            n = sum(1 for i, s in enumerate(SQUARES)
                    if s.kind == "station" and self.owner.get(i) == owner_idx)
            return [0, 25, 50, 100, 200][min(n, 4)]

        if sq.kind == "utility":
            n = sum(1 for i, s in enumerate(SQUARES)
                    if s.kind == "utility" and self.owner.get(i) == owner_idx)
            mult = 10 if n == 2 else 4
            return (self.dice[0] + self.dice[1]) * mult

        return 0

    def pay(self, payer: Player, receiver, amount: int):
        """receiver: Player ou None (banque)."""
        if amount <= 0:
            return
        # liquidation automatique
        while payer.money < amount and payer.properties:
            pos = payer.properties.pop()
            sq = SQUARES[pos]
            refund = sq.price // 2
            payer.money += refund
            self.houses.pop(pos, None)
            self.owner.pop(pos, None)
            self.add_log(f"💸 {payer.name} hypothèque {sq.name} (+{refund} €)")

        if payer.money < amount:
            # faillite
            self.add_log(f"☠️ {payer.name} fait FAILLITE !")
            if receiver is not None:
                receiver.money += payer.money
                for pos in payer.properties:
                    self.owner[pos] = self.players.index(receiver)
                    receiver.properties.append(pos)
            payer.money = 0
            payer.properties = []
            payer.alive = False
            self.check_game_over()
            return

        payer.money -= amount
        if receiver is not None:
            receiver.money += amount

    def buy(self, p: Player, pos: int):
        sq = SQUARES[pos]
        if p.money < sq.price or pos in self.owner:
            return False
        p.money -= sq.price
        p.properties.append(pos)
        self.owner[pos] = self.players.index(p)
        return True

    def build_house(self, p: Player, pos: int) -> bool:
        sq = SQUARES[pos]
        if sq.kind != "street":
            return False
        if self.owner.get(pos) != self.players.index(p):
            return False
        if not self.has_monopoly(self.players.index(p), sq.group):
            return False
        current = self.houses.get(pos, 0)
        if current >= 5:
            return False
        cost = GROUP_HOUSE_COST[sq.group]
        if p.money < cost:
            return False
        # règle d'égalité approximative : pas plus d'une maison d'écart dans le groupe
        group = self.group_positions(sq.group)
        min_h = min(self.houses.get(g, 0) for g in group)
        if current > min_h:
            return False
        p.money -= cost
        self.houses[pos] = current + 1
        return True

    def next_turn(self):
        n = len(self.players)
        for _ in range(n):
            self.current = (self.current + 1) % n
            if self.players[self.current].alive:
                break
        self.phase = "roll"
        self.doubles = 0
        self.turn_count += 1
        self.add_log(f"─── Tour de {self.current_player().name} ───")

    def check_game_over(self):
        alive = self.alive_players()
        if len(alive) <= 1:
            self.game_over = True
            self.winner = alive[0] if alive else None


# ============================================================
#  APPLICATION / UI
# ============================================================

class DarkMonopolyApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("DarkMonopoly")
        self.root.geometry("1180x800")
        self.root.resizable(False, False)

        self.theme_name = "nuit_bleu"
        self.theme = THEMES[self.theme_name]

        # Choix du nombre de joueurs
        n = simpledialog.askinteger(
            "DarkMonopoly", "Nombre de joueurs (2 à 4) :",
            initialvalue=2, minvalue=2, maxvalue=4, parent=root,
        )
        if not n:
            n = 2

        self.game = Game(n)
        self.game.add_log("🎲 Nouvelle partie DarkMonopoly")
        self.game.add_log(f"Joueurs : {', '.join(p.name for p in self.game.players)}")
        self.game.add_log(f"─── Tour de {self.game.current_player().name} ───")

        self._build_ui()
        self.refresh()

        # Démarrage auto si le premier joueur est une IA (ne devrait pas arriver)
        self.root.after(400, self._maybe_auto_play)

    # --------------------------------------------------------
    #  Construction de l'UI
    # --------------------------------------------------------
    def _build_ui(self):
        t = self.theme
        self.root.configure(bg=t["bg"])

        # Barre de thème
        topbar = tk.Frame(self.root, bg=t["bg"])
        topbar.pack(fill="x", padx=12, pady=(10, 0))

        tk.Label(topbar, text="DarkMonopoly", bg=t["bg"], fg=t["accent"],
                 font=("Segoe UI", 16, "bold")).pack(side="left")

        tk.Label(topbar, text="Thème :", bg=t["bg"], fg=t["fg"],
                 font=("Segoe UI", 10)).pack(side="right", padx=(0, 6))
        for key, th in THEMES.items():
            b = tk.Button(
                topbar, text=th["label"],
                command=lambda k=key: self.set_theme(k),
                bg=t["button_bg"], fg=t["button_fg"],
                activebackground=t["button_active"], activeforeground=t["button_fg"],
                relief="flat", padx=10, pady=3, cursor="hand2",
                font=("Segoe UI", 9),
            )
            b.pack(side="right", padx=2)

        # Conteneur principal
        main = tk.Frame(self.root, bg=t["bg"])
        main.pack(fill="both", expand=True, padx=12, pady=10)

        # Canvas plateau
        self.canvas = tk.Canvas(main, width=BOARD_PX, height=BOARD_PX,
                                bg=t["board_bg"], highlightthickness=0)
        self.canvas.pack(side="left")

        # Panneau droit
        panel = tk.Frame(main, bg=t["panel_bg"], width=380)
        panel.pack(side="right", fill="y", padx=(14, 0))
        panel.pack_propagate(False)

        # Infos joueur courant
        self.lbl_current = tk.Label(panel, text="", bg=t["panel_bg"], fg=t["fg"],
                                    font=("Segoe UI", 13, "bold"), anchor="w")
        self.lbl_current.pack(fill="x", padx=12, pady=(12, 2))

        self.lbl_money = tk.Label(panel, text="", bg=t["panel_bg"], fg=t["accent"],
                                  font=("Segoe UI", 11), anchor="w")
        self.lbl_money.pack(fill="x", padx=12)

        self.lbl_dice = tk.Label(panel, text="", bg=t["panel_bg"], fg=t["fg"],
                                 font=("Consolas", 14, "bold"), anchor="w")
        self.lbl_dice.pack(fill="x", padx=12, pady=(6, 4))

        # Boutons d'action
        btn_frame = tk.Frame(panel, bg=t["panel_bg"])
        btn_frame.pack(fill="x", padx=12, pady=4)

        self.btn_roll = tk.Button(
            btn_frame, text="🎲 Lancer les dés", command=self.action_roll,
            bg=t["accent"], fg=t["accent_fg"],
            activebackground=t["button_active"], activeforeground=t["accent_fg"],
            relief="flat", pady=8, cursor="hand2",
            font=("Segoe UI", 11, "bold"),
        )
        self.btn_roll.pack(fill="x", pady=2)

        self.btn_end = tk.Button(
            btn_frame, text="✔ Terminer le tour", command=self.action_end_turn,
            bg=t["button_bg"], fg=t["button_fg"],
            activebackground=t["button_active"], activeforeground=t["button_fg"],
            relief="flat", pady=8, cursor="hand2",
            font=("Segoe UI", 11, "bold"),
        )
        self.btn_end.pack(fill="x", pady=2)

        self.btn_build = tk.Button(
            btn_frame, text="🏠 Construire une maison", command=self.action_build,
            bg=t["button_bg"], fg=t["button_fg"],
            activebackground=t["button_active"], activeforeground=t["button_fg"],
            relief="flat", pady=6, cursor="hand2",
            font=("Segoe UI", 10),
        )
        self.btn_build.pack(fill="x", pady=2)

        # Liste des joueurs
        tk.Label(panel, text="Joueurs", bg=t["panel_bg"], fg=t["muted"],
                 font=("Segoe UI", 10, "bold"), anchor="w").pack(fill="x", padx=12, pady=(10, 2))

        self.players_frame = tk.Frame(panel, bg=t["panel_bg"])
        self.players_frame.pack(fill="x", padx=12)

        # Journal
        tk.Label(panel, text="Journal", bg=t["panel_bg"], fg=t["muted"],
                 font=("Segoe UI", 10, "bold"), anchor="w").pack(fill="x", padx=12, pady=(10, 2))

        log_wrap = tk.Frame(panel, bg=t["panel_bg"])
        log_wrap.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        self.log_text = tk.Text(
            log_wrap, bg=t["log_bg"], fg=t["log_fg"],
            font=("Consolas", 9), relief="flat", wrap="word",
            state="disabled", height=12,
        )
        self.log_text.pack(side="left", fill="both", expand=True)

        sb = tk.Scrollbar(log_wrap, command=self.log_text.yview)
        sb.pack(side="right", fill="y")
        self.log_text.configure(yscrollcommand=sb.set)

    # --------------------------------------------------------
    #  Thème
    # --------------------------------------------------------
    def set_theme(self, name: str):
        if name not in THEMES:
            return
        self.theme_name = name
        self.theme = THEMES[name]
        for w in self.root.winfo_children():
            w.destroy()
        self._build_ui()
        self.refresh()

    # --------------------------------------------------------
    #  Rendu plateau
    # --------------------------------------------------------
    @staticmethod
    def grid_pos(i: int):
        if i == 0: return (10, 10)
        if 1 <= i <= 9: return (10, 10 - i)
        if i == 10: return (10, 0)
        if 11 <= i <= 19: return (10 - (i - 10), 0)
        if i == 20: return (0, 0)
        if 21 <= i <= 29: return (0, i - 20)
        if i == 30: return (0, 10)
        return (i - 30, 10)

    def draw_board(self):
        c = self.canvas
        t = self.theme
        c.delete("all")
        c.configure(bg=t["board_bg"])

        # Fond intérieur
        c.create_rectangle(CELL, CELL, BOARD_PX - CELL, BOARD_PX - CELL,
                           fill=t["board_bg"], outline="")

        # Logo centre
        c.create_text(BOARD_PX / 2, BOARD_PX / 2 - 20,
                      text="DarkMonopoly", fill=t["accent"],
                      font=("Segoe UI", 22, "bold"))
        c.create_text(BOARD_PX / 2, BOARD_PX / 2 + 16,
                      text="v1 • Monopoly classique", fill=t["muted"],
                      font=("Segoe UI", 10))

        for i, sq in enumerate(SQUARES):
            r, col = self.grid_pos(i)
            x1 = col * CELL
            y1 = r * CELL
            x2 = x1 + CELL
            y2 = y1 + CELL

            owner_idx = self.game.owner.get(i)
            fill = t["square_bg"]
            c.create_rectangle(x1, y1, x2, y2, fill=fill,
                               outline=t["border"], width=1)

            # Bande couleur (rues)
            if sq.kind == "street":
                gc = GROUP_COLORS[sq.group]
                band = 12
                if r == 10:      # bord bas -> bande en haut
                    c.create_rectangle(x1, y1, x2, y1 + band, fill=gc, outline="")
                elif r == 0:     # bord haut -> bande en bas
                    c.create_rectangle(x1, y2 - band, x2, y2, fill=gc, outline="")
                elif col == 0:   # bord gauche -> bande à droite
                    c.create_rectangle(x2 - band, y1, x2, y2, fill=gc, outline="")
                elif col == 10:  # bord droit -> bande à gauche
                    c.create_rectangle(x1, y1, x1 + band, y2, fill=gc, outline="")

            # Indicateur de propriétaire (liseré intérieur)
            if owner_idx is not None:
                pc = self.game.players[owner_idx].color
                c.create_rectangle(x1 + 1, y1 + 1, x2 - 1, y2 - 1,
                                   outline=pc, width=2)

            # Nom + prix
            text_color = t["fg"]
            name = sq.name
            # Raccourcis pour noms longs
            short = name
            if len(short) > 16:
                short = short.replace("Avenue ", "Av. ").replace("Boulevard ", "Bd ")
                short = short.replace("Caisse de Communauté", "Caisse")
                short = short.replace("Compagnie ", "Cie ")
                short = short.replace("Impôt sur le revenu", "Impôt revenu")
                short = short.replace("Allez en prison", "→ Prison")
                short = short.replace("Avenue des Champs-Élysées", "Champs-Élysées")
                short = short.replace("Faubourg Saint-Honoré", "Fbg St-Honoré")
                short = short.replace("Boulevard de la Madeleine", "Bd Madeleine")

            c.create_text((x1 + x2) / 2, (y1 + y2) / 2 - 6,
                          text=short, fill=text_color,
                          font=("Segoe UI", 7, "bold"),
                          width=CELL - 6, justify="center")

            if sq.price > 0:
                c.create_text((x1 + x2) / 2, (y1 + y2) / 2 + 14,
                              text=f"{sq.price} €", fill=t["muted"],
                              font=("Segoe UI", 7))
            elif sq.tax > 0:
                c.create_text((x1 + x2) / 2, (y1 + y2) / 2 + 14,
                              text=f"-{sq.tax} €", fill=t["muted"],
                              font=("Segoe UI", 7))

            # Maisons
            h = self.game.houses.get(i, 0)
            if h > 0:
                for k in range(h):
                    hx = x1 + 6 + k * 9
                    hy = y2 - 10
                    if h == 5:
                        c.create_rectangle(hx, hy, hx + 7, hy + 6,
                                           fill="#d62828", outline="")
                    else:
                        c.create_rectangle(hx, hy, hx + 7, hy + 6,
                                           fill="#2a9d8f", outline="")

        # Jetons joueurs
        self.draw_tokens()

    def draw_tokens(self):
        c = self.canvas
        # Grouper les joueurs par position
        by_pos = {}
        for idx, p in enumerate(self.game.players):
            if p.alive:
                by_pos.setdefault(p.position, []).append((idx, p))

        for pos, players in by_pos.items():
            r, col = self.grid_pos(pos)
            x1 = col * CELL
            y1 = r * CELL
            cx = x1 + CELL / 2
            cy = y1 + CELL / 2

            n = len(players)
            offsets = []
            if n == 1:
                offsets = [(0, -18)]
            elif n == 2:
                offsets = [(-12, -18), (12, -18)]
            elif n == 3:
                offsets = [(-12, -18), (12, -18), (0, 14)]
            else:
                offsets = [(-12, -18), (12, -18), (-12, 14), (12, 14)]

            for (idx, p), (dx, dy) in zip(players, offsets):
                is_current = (idx == self.game.current)
                rad = 7 if is_current else 6
                c.create_oval(cx + dx - rad, cy + dy - rad,
                              cx + dx + rad, cy + dy + rad,
                              fill=p.color,
                              outline="#ffffff" if is_current else "#000000",
                              width=2 if is_current else 1)

    # --------------------------------------------------------
    #  Refresh global
    # --------------------------------------------------------
    def refresh(self):
        self.draw_board()
        t = self.theme
        p = self.game.current_player()

        self.lbl_current.configure(
            text=f"{p.name}  {'🤖' if p.is_ai else '🧑'}",
            fg=p.color,
        )
        self.lbl_money.configure(text=f"💰 {p.money} €   •   Patrimoine net : {p.net_worth} €")

        d1, d2 = self.game.dice
        if d1 and d2:
            self.lbl_dice.configure(text=f"🎲 {d1} + {d2} = {d1 + d2}")
        else:
            self.lbl_dice.configure(text="🎲 —")

        # Boutons selon phase / tour
        human_turn = (not p.is_ai) and (not self.game.game_over)
        if self.game.phase == "roll" and human_turn:
            self.btn_roll.configure(state="normal")
            self.btn_end.configure(state="disabled")
        elif self.game.phase == "end" and human_turn:
            self.btn_roll.configure(state="disabled")
            self.btn_end.configure(state="normal")
        else:
            self.btn_roll.configure(state="disabled")
            self.btn_end.configure(state="disabled")

        if human_turn and self.game.phase == "end":
            self.btn_build.configure(state="normal")
        else:
            self.btn_build.configure(state="disabled")

        # Liste joueurs
        for w in self.players_frame.winfo_children():
            w.destroy()
        for i, pl in enumerate(self.game.players):
            row = tk.Frame(self.players_frame, bg=t["panel_bg"])
            row.pack(fill="x", pady=1)
            indicator = "▶ " if i == self.game.current and not self.game.game_over else "   "
            status = "" if pl.alive else "  (faillite)"
            tk.Label(row, text=indicator, bg=t["panel_bg"], fg=t["accent"],
                     font=("Segoe UI", 10, "bold")).pack(side="left")
            tk.Label(row, text="●", bg=t["panel_bg"], fg=pl.color,
                     font=("Segoe UI", 12)).pack(side="left", padx=(0, 4))
            tk.Label(row, text=f"{pl.name}{status}", bg=t["panel_bg"], fg=t["fg"],
                     font=("Segoe UI", 10), anchor="w").pack(side="left")
            tk.Label(row, text=f"{pl.money} €", bg=t["panel_bg"], fg=t["muted"],
                     font=("Segoe UI", 10)).pack(side="right")

        # Journal
        self.log_text.configure(state="normal")
        self.log_text.delete("1.0", "end")
        for line in self.game.log[-200:]:
            self.log_text.insert("end", line + "\n")
        self.log_text.see("end")
        self.log_text.configure(state="disabled")

    # --------------------------------------------------------
    #  Actions
    # --------------------------------------------------------
    def action_roll(self):
        if self.game.game_over:
            return
        p = self.game.current_player()
        if p.is_ai:
            return
        if self.game.phase != "roll":
            return
        self._do_roll()

    def action_end_turn(self):
        if self.game.game_over:
            return
        p = self.game.current_player()
        if p.is_ai:
            return
        if self.game.phase != "end":
            return
        self._end_turn()

    def action_build(self):
        p = self.game.current_player()
        if p.is_ai or self.game.game_over:
            return
        self._open_build_dialog(p)

    # --------------------------------------------------------
    #  Logique du tour
    # --------------------------------------------------------
    def _do_roll(self):
        p = self.game.current_player()

        # Prison : payer pour sortir
        if p.in_jail:
            if p.money >= 50:
                p.money -= 50
                p.in_jail = False
                self.game.add_log(f"🔓 {p.name} paie 50 € pour sortir de prison")
            else:
                self.game.add_log(f"⛓️ {p.name} reste en prison (pas assez d'argent)")
                self.game.phase = "end"
                self.refresh()
                return

        d1, d2 = self.game.roll_dice()
        total = d1 + d2
        self.game.add_log(f"🎲 {p.name} lance {d1} + {d2} = {total}")

        if d1 == d2:
            self.game.doubles += 1
            if self.game.doubles >= 3:
                self.game.add_log(f"🚔 3 doubles d'affilée : {p.name} va en prison !")
                p.position = 10
                p.in_jail = True
                self.game.phase = "end"
                self.refresh()
                return

        self.game.move_player(p, total)
        self.refresh()

        self.root.after(250, lambda: self._after_move(p, d1 == d2))

    def _after_move(self, p: Player, is_double: bool):
        self._handle_landing(p)
        self.refresh()

        if self.game.game_over:
            self._end_game()
            return

        if is_double and not p.in_jail:
            self.game.add_log(f"✨ Double ! {p.name} rejoue.")
            self.game.phase = "roll"
            self.refresh()
            if p.is_ai:
                self.root.after(700, self._do_roll)
            return

        self.game.phase = "end"
        self.refresh()

        # IA enchaîne
        if p.is_ai:
            self.root.after(700, self._end_turn)

    def _handle_landing(self, p: Player):
        pos = p.position
        sq = SQUARES[pos]
        self.game.add_log(f"➡️ {p.name} arrive sur : {sq.name}")

        if sq.kind in ("street", "station", "utility"):
            owner_idx = self.game.owner.get(pos)
            if owner_idx is None:
                # Achat
                if p.money >= sq.price:
                    if p.is_ai:
                        # IA : achète si elle garde une marge
                        if p.money - sq.price >= 150:
                            self.game.buy(p, pos)
                            self.game.add_log(f"🏷️ {p.name} achète {sq.name} pour {sq.price} €")
                    else:
                        buy = messagebox.askyesno(
                            "Achat de propriété",
                            f"Acheter « {sq.name} » pour {sq.price} € ?\n\n"
                            f"Votre argent : {p.money} €",
                            parent=self.root,
                        )
                        if buy:
                            self.game.buy(p, pos)
                            self.game.add_log(f"🏷️ {p.name} achète {sq.name} pour {sq.price} €")
                else:
                    self.game.add_log(f"❌ {p.name} n'a pas assez pour acheter {sq.name}")
            else:
                if owner_idx != self.game.current:
                    owner = self.game.players[owner_idx]
                    rent = self.game.compute_rent(pos)
                    self.game.add_log(f"💵 {p.name} paie {rent} € de loyer à {owner.name}")
                    self.game.pay(p, owner, rent)

        elif sq.kind == "tax":
            self.game.add_log(f"🧾 {p.name} paie {sq.tax} € de taxe")
            self.game.pay(p, None, sq.tax)

        elif sq.kind == "gotojail":
            self.game.add_log(f"🚔 {p.name} va en prison !")
            p.position = 10
            p.in_jail = True

        elif sq.kind == "chance":
            self._draw_card(p, CHANCE_CARDS, "Chance")

        elif sq.kind == "chest":
            self._draw_card(p, CHEST_CARDS, "Caisse de Communauté")

        # go / jail / freeparking : rien

    def _draw_card(self, p: Player, deck, deck_name: str):
        text, kind, val = random.choice(deck)
        self.game.add_log(f"🃏 [{deck_name}] {text}")
        if kind == "gain":
            p.money += val
        elif kind == "pay":
            self.game.pay(p, None, val)
        elif kind == "move_to":
            if val == 0:
                # Retour à la case départ : +200 €
                p.position = 0
                p.money += 200
                self.game.add_log(f"→ {p.name} reçoit 200 € pour être passé par DÉPART")
            else:
                p.position = val
        elif kind == "move_back":
            p.position = (p.position - val) % 40
        elif kind == "goto_jail":
            p.position = 10
            p.in_jail = True

    def _end_turn(self):
        if self.game.game_over:
            self._end_game()
            return
        self.game.next_turn()
        self.refresh()
        self._maybe_auto_play()

    def _maybe_auto_play(self):
        if self.game.game_over:
            self._end_game()
            return
        p = self.game.current_player()
        if p.is_ai:
            self.root.after(700, self._do_roll)

    def _end_game(self):
        w = self.game.winner
        if w is None:
            msg = "Partie terminée. Aucun survivant."
        else:
            msg = f"🏆 {w.name} remporte la partie !\nPatrimoine : {w.net_worth} €"
        self.game.add_log("═══ FIN DE PARTIE ═══")
        self.game.add_log(msg)
        self.refresh()
        messagebox.showinfo("DarkMonopoly", msg, parent=self.root)

    # --------------------------------------------------------
    #  Dialog construction
    # --------------------------------------------------------
    def _open_build_dialog(self, p: Player):
        buildable = []
        for pos in p.properties:
            sq = SQUARES[pos]
            if sq.kind != "street":
                continue
            if not self.game.has_monopoly(self.game.players.index(p), sq.group):
                continue
            if self.game.houses.get(pos, 0) >= 5:
                continue
            # règle d'égalité
            group = self.game.group_positions(sq.group)
            min_h = min(self.game.houses.get(g, 0) for g in group)
            if self.game.houses.get(pos, 0) > min_h:
                continue
            cost = GROUP_HOUSE_COST[sq.group]
            if p.money < cost:
                continue
            buildable.append((pos, sq, cost))

        if not buildable:
            messagebox.showinfo(
                "Construction",
                "Aucune construction possible.\n"
                "Il faut : un monopole de couleur, un nombre équilibré de maisons, "
                "et assez d'argent.",
                parent=self.root,
            )
            return

        win = tk.Toplevel(self.root)
        win.title("Construire une maison")
        win.configure(bg=self.theme["panel_bg"])
        win.transient(self.root)
        win.grab_set()

        tk.Label(win, text=f"💰 Argent : {p.money} €",
                 bg=self.theme["panel_bg"], fg=self.theme["fg"],
                 font=("Segoe UI", 11, "bold")).pack(padx=16, pady=(12, 6))

        for pos, sq, cost in buildable:
            row = tk.Frame(win, bg=self.theme["panel_bg"])
            row.pack(fill="x", padx=16, pady=2)
            tk.Label(row, text=f"{sq.name}  ({self.game.houses.get(pos, 0)}/5)",
                     bg=self.theme["panel_bg"], fg=self.theme["fg"],
                     font=("Segoe UI", 10), anchor="w").pack(side="left")
            tk.Button(
                row, text=f"Construire — {cost} €",
                bg=self.theme["accent"], fg=self.theme["accent_fg"],
                relief="flat", padx=8, pady=2, cursor="hand2",
                font=("Segoe UI", 9, "bold"),
                command=lambda pp=pos, w=win: self._do_build(p, pp, w),
            ).pack(side="right")

        tk.Button(win, text="Fermer", command=win.destroy,
                  bg=self.theme["button_bg"], fg=self.theme["button_fg"],
                  relief="flat", padx=12, pady=4, cursor="hand2",
                  font=("Segoe UI", 9)).pack(pady=10)

    def _do_build(self, p: Player, pos: int, win: tk.Toplevel):
        if self.game.build_house(p, pos):
            sq = SQUARES[pos]
            self.game.add_log(f"🏠 {p.name} construit une maison sur {sq.name} "
                              f"({GROUP_HOUSE_COST[sq.group]} €)")
            win.destroy()
            self.refresh()


# ============================================================
#  MAIN
# ============================================================

def main():
    root = tk.Tk()
    app = DarkMonopolyApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()