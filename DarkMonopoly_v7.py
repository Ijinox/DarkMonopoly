"""
DarkMonopoly PC v7.0 — Fix IA + Mains publiques PvP + Thème clair
==================================================================

Correctifs v7.0 :
- FIX : un bot qui pioche une carte joue maintenant sa main de façon
  centralisée dans _end_turn (plus de blocage, plus d'accumulation).
- FIX : try/except sur les effets de cartes pour éviter tout freeze.
- FIX : refresh() après chaque pioche (humain comme IA).
- FIX : les cartes des bots ne sont plus affichées (main cachée).
- FIX : les cartes n'apparaissent plus dans le compteur public en PvP.

Nouveautés v7.0 :
- Mode PvP (tous humains) : affiche les mains de TOUS les joueurs en
  bas du plateau (une ligne par joueur).
- Thème "Clair" : boutons avec gris franc (#d1d5db), bordures plus
  foncées, contraste amélioré.

Lancement :
    python darkmonopoly_v7.py
"""

import tkinter as tk
from tkinter import messagebox, filedialog
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
import random
import datetime


# ============================================================
#  CONSTANTES
# ============================================================

CELL = 90
GRID = 7
BOARD_PX = CELL * GRID
HAND_BASE_PX = 110

DEFAULT_TARGET = 2500
DEFAULT_MAX_TURNS = 40
EXTENDED_MAX_TURNS = 100

COMPANIES = ["NEXA", "VOLT", "AURUM", "KAVI"]
COMPANY_COLORS = ["#ef4444", "#3b82f6", "#10b981", "#f59e0b"]

GROUP_COLORS = {
    "blue":   "#3b82f6", "green":  "#10b981", "yellow": "#f59e0b",
    "red":    "#ef4444", "purple": "#a855f7", "orange": "#f97316",
    "pink":   "#ec4899", "cyan":   "#06b6d4",
}

CAT_COLORS = {"invest": "#10b981", "seize": "#ef4444", "money": "#f59e0b"}
CAT_LABELS = {"invest": "INVESTISSEMENT", "seize": "PRISE", "money": "ARGENT"}


THEMES = {
    "clair": {
        "label": "Clair",
        "bg": "#f5f6f8", "panel_bg": "#ffffff", "panel_2": "#e2e8f0",
        "fg": "#111827", "muted": "#6b7280",
        "accent": "#2563eb", "accent_fg": "#ffffff",
        "board_bg": "#f9fafb", "cell_bg": "#ffffff", "border": "#94a3b8",
        "pending": "#1f2937",
        "btn_bg": "#d1d5db", "btn_fg": "#111827", "btn_act": "#9ca3af",
        "log_bg": "#ffffff", "log_fg": "#374151",
    },
    "sombre": {
        "label": "Sombre",
        "bg": "#111111", "panel_bg": "#1c1c1c", "panel_2": "#242424",
        "fg": "#e5e5e5", "muted": "#9ca3af",
        "accent": "#60a5fa", "accent_fg": "#0a0a0a",
        "board_bg": "#161616", "cell_bg": "#1f1f1f", "border": "#2f2f2f",
        "pending": "#ffffff",
        "btn_bg": "#262626", "btn_fg": "#e5e5e5", "btn_act": "#333333",
        "log_bg": "#141414", "log_fg": "#d1d5db",
    },
    "nuit_bleu": {
        "label": "Nuit Bleu",
        "bg": "#071624", "panel_bg": "#0b2138", "panel_2": "#123458",
        "fg": "#c9e4ff", "muted": "#5b87b0",
        "accent": "#3fa9f5", "accent_fg": "#071624",
        "board_bg": "#081c2e", "cell_bg": "#0f2a47", "border": "#1a4a73",
        "pending": "#ffffff",
        "btn_bg": "#123458", "btn_fg": "#c9e4ff", "btn_act": "#1a4a73",
        "log_bg": "#071624", "log_fg": "#c9e4ff",
    },
    "nuit_rouge": {
        "label": "Nuit Rouge",
        "bg": "#170808", "panel_bg": "#2a0e0e", "panel_2": "#3a1414",
        "fg": "#ffd0c9", "muted": "#c98a80",
        "accent": "#f53f3f", "accent_fg": "#170808",
        "board_bg": "#1e0a0a", "cell_bg": "#341313", "border": "#6e1a1a",
        "pending": "#ffffff",
        "btn_bg": "#441414", "btn_fg": "#ffd0c9", "btn_act": "#6e1a1a",
        "log_bg": "#170808", "log_fg": "#ffd0c9",
    },
    "sepia": {
        "label": "Sépia",
        "bg": "#f4ecd8", "panel_bg": "#faf3e0", "panel_2": "#e2d5b0",
        "fg": "#3d2817", "muted": "#7a6040",
        "accent": "#a0522d", "accent_fg": "#faf3e0",
        "board_bg": "#ede4cc", "cell_bg": "#faf3e0", "border": "#a08458",
        "pending": "#5c3a1a",
        "btn_bg": "#d8c8a0", "btn_fg": "#3d2817", "btn_act": "#b8a478",
        "log_bg": "#f4ecd8", "log_fg": "#3d2817",
    },
    "cyberpunk": {
        "label": "Cyberpunk",
        "bg": "#0a0014", "panel_bg": "#12002a", "panel_2": "#1a0a3a",
        "fg": "#f0e6ff", "muted": "#a07ec0",
        "accent": "#ff2a8a", "accent_fg": "#0a0014",
        "board_bg": "#0e0020", "cell_bg": "#1a0a3a", "border": "#3a1a6a",
        "pending": "#ffffff",
        "btn_bg": "#2a0a4a", "btn_fg": "#f0e6ff", "btn_act": "#3a1a6a",
        "log_bg": "#0e0020", "log_fg": "#f0e6ff",
    },
    "foret": {
        "label": "Forêt",
        "bg": "#0d1a0d", "panel_bg": "#152615", "panel_2": "#1e381e",
        "fg": "#d4f0d4", "muted": "#7aa87a",
        "accent": "#4ade80", "accent_fg": "#0d1a0d",
        "board_bg": "#0a140a", "cell_bg": "#1a2e1a", "border": "#2a4a2a",
        "pending": "#ffffff",
        "btn_bg": "#1e381e", "btn_fg": "#d4f0d4", "btn_act": "#2a4a2a",
        "log_bg": "#0d1a0d", "log_fg": "#d4f0d4",
    },
    "ocean": {
        "label": "Océan",
        "bg": "#03141e", "panel_bg": "#062030", "panel_2": "#0d3548",
        "fg": "#d0f0f5", "muted": "#5a9ba8",
        "accent": "#14b8a6", "accent_fg": "#03141e",
        "board_bg": "#041a26", "cell_bg": "#0a2a3a", "border": "#154a5c",
        "pending": "#ffffff",
        "btn_bg": "#0d3548", "btn_fg": "#d0f0f5", "btn_act": "#154a5c",
        "log_bg": "#03141e", "log_fg": "#d0f0f5",
    },
}


# ============================================================
#  PLATEAU
# ============================================================

@dataclass
class Square:
    name: str
    kind: str
    price: int = 0
    group: str = ""


BOARD: List[Square] = [
    Square("DÉPART", "start"),
    Square("NEO", "street", 60, "blue"),
    Square("PULSE", "street", 60, "blue"),
    Square("OPPORT.", "libre"),
    Square("VOLT", "street", 100, "green"),
    Square("FLUX", "street", 100, "green"),
    Square("CARTE", "carte"),
    Square("ORBIT", "street", 140, "yellow"),
    Square("SIGMA", "street", 140, "yellow"),
    Square("OPPORT.", "libre"),
    Square("HELIX", "street", 180, "red"),
    Square("QUANTA", "street", 180, "red"),
    Square("CARTE", "carte"),
    Square("NEXUS", "street", 220, "purple"),
    Square("ZENITH", "street", 220, "purple"),
    Square("OPPORT.", "libre"),
    Square("APEX", "street", 260, "orange"),
    Square("CROWN", "street", 260, "orange"),
    Square("CARTE", "carte"),
    Square("PRIME", "street", 300, "pink"),
    Square("TITAN", "street", 300, "pink"),
    Square("OPPORT.", "libre"),
    Square("REGAL", "street", 350, "cyan"),
    Square("ROYAL", "street", 400, "cyan"),
]


def grid_pos(i: int) -> Tuple[int, int]:
    if i == 0: return (6, 6)
    if 1 <= i <= 5: return (6, 6 - i)
    if i == 6: return (6, 0)
    if 7 <= i <= 11: return (6 - (i - 6), 0)
    if i == 12: return (0, 0)
    if 13 <= i <= 17: return (0, i - 12)
    if i == 18: return (0, 6)
    if 19 <= i <= 23: return (i - 18, 6)
    return (0, 0)


def cell_from_grid(row: int, col: int) -> Optional[int]:
    if row == 6 and col == 6: return 0
    if row == 6 and 1 <= col <= 5: return 6 - col
    if row == 6 and col == 0: return 6
    if 1 <= row <= 5 and col == 0: return 12 - row
    if row == 0 and col == 0: return 12
    if row == 0 and 1 <= col <= 5: return 12 + col
    if row == 0 and col == 6: return 18
    if 1 <= row <= 5 and col == 6: return 18 + row
    return None


# ============================================================
#  CARTES
# ============================================================

@dataclass
class Card:
    name: str
    description: str
    category: str
    effect: str
    value: int = 0


CARD_DECK: List[Card] = [
    Card("LEVÉE DE FONDS", "Recevez 400€.", "invest", "cash", 400),
    Card("ACHAT PRIVILÉGIÉ", "Achetez un terrain à -50%.", "invest", "discount_buy", 50),
    Card("MAISON OFFERTE", "Posez une maison gratuite.", "invest", "free_house", 0),
    Card("DÉVELOPPEMENT", "+1 maison sur toutes vos propriétés.", "invest", "upgrade_all", 1),
    Card("DIVIDENDES", "50€ par propriété possédée.", "invest", "dividend", 50),
    Card("ACQUISITION HOSTILE", "Prenez une propriété adverse (150% du prix).",
         "seize", "hostile_takeover", 150),
    Card("CONFISCATION", "Confisquez une propriété (50% au propriétaire).",
         "seize", "confiscate", 50),
    Card("BLOCUS", "Une cible passe son prochain tour.", "seize", "blocus", 1),
    Card("REDIRECTION", "Forcez une cible sur la case CARTE.", "seize", "redirect", 0),
    Card("AUDIT CROISÉ", "Détournez 100€ d'une cible.", "seize", "audit_cross", 100),
    Card("BONUS TRIMESTRIEL", "Encaissez 250€.", "money", "cash", 250),
    Card("HÉRITAGE", "Recevez 300€.", "money", "cash", 300),
    Card("SUBVENTION PUBLIQUE", "Recevez 200€.", "money", "cash", 200),
    Card("AMENDE RÉGLEMENTAIRE", "Payez 150€.", "money", "pay", 150),
    Card("AUDIT FISCAL", "Payez 200€.", "money", "pay", 200),
]


# ============================================================
#  MODÈLE
# ============================================================

class Player:
    def __init__(self, name: str, color: str, is_ai: bool = False, team: int = 0):
        self.name = name
        self.color = color
        self.is_ai = is_ai
        self.team = team
        self.money = 1500
        self.position = 0
        self.properties: List[int] = []
        self.hand: List[Card] = []
        self.alive = True
        self.turns_completed = 0
        self.skip_turns = 0


class Game:
    def __init__(self, configs: List[dict], seed: Optional[int] = None):
        self.players = [
            Player(c["name"], c["color"], c["is_ai"], c.get("team", 0))
            for c in configs
        ]
        self.current = 0
        self.owner: Dict[int, int] = {}
        self.houses: Dict[int, int] = {}
        self.copies: Dict[int, int] = {}
        self.dice = (0, 0)
        self.doubles = 0
        self.phase = "roll"
        self.log: List[str] = []
        self.game_over = False
        self.winner: Optional[Player] = None
        self.winning_team = 0
        self.turn_count = 1
        self.inflation_pct = 0
        self.inflation_turns = 0
        self.target = DEFAULT_TARGET
        self.max_turns = DEFAULT_MAX_TURNS
        self.extended = False
        # Mode PvP si tous les joueurs sont humains
        self.pvp_mode = all(not c["is_ai"] for c in configs)

        rng = random.Random(seed)
        self._rng = rng
        deck = list(CARD_DECK)
        rng.shuffle(deck)
        self.deck = deck
        self.deck_pos = 0
        self.drawn_history: List[Card] = []

    def add_log(self, msg: str):
        self.log.append(msg)
        if len(self.log) > 400:
            self.log.pop(0)

    def current_player(self) -> Player:
        return self.players[self.current]

    def roll_dice(self):
        d1 = self._rng.randint(1, 6)
        d2 = self._rng.randint(1, 6)
        self.dice = (d1, d2)
        return d1, d2

    def source(self, pos: int) -> Optional[int]:
        if BOARD[pos].kind == "libre":
            return self.copies.get(pos)
        return pos

    def move_player(self, p: Player, steps: int):
        old = p.position
        new = (old + steps) % 24
        if new < old:
            p.money += 200
            self.add_log(f"→ {p.name} franchit DÉPART (+200€)")
        p.position = new

    def rent_at_houses(self, pos: int, houses: int) -> int:
        src = self.source(pos)
        if src is None:
            return 0
        sq = BOARD[src]
        if sq.kind != "street":
            return 0
        if houses == 0: base = sq.price // 10
        elif houses == 1: base = sq.price // 3
        elif houses == 2: base = (sq.price * 3) // 5
        else: base = sq.price
        if self.inflation_turns > 0:
            base = int(base * (100 + self.inflation_pct) / 100)
            base = max(0, base)
        return base

    def compute_rent(self, pos: int) -> int:
        return self.rent_at_houses(pos, self.houses.get(pos, 0))

    def house_cost(self, pos: int) -> int:
        src = self.source(pos)
        if src is None:
            src = pos
        return BOARD[src].price // 2

    def net_worth(self, p: Player) -> int:
        total = p.money
        for pos in p.properties:
            src = self.source(pos)
            if src is None:
                src = pos
            total += BOARD[src].price
            total += self.houses.get(pos, 0) * (BOARD[src].price // 2)
        return total

    def pay(self, payer: Player, receiver: Optional[Player], amount: int):
        if amount <= 0:
            return
        while payer.money < amount and payer.properties:
            cheapest = None
            cheapest_price = float('inf')
            for pos in payer.properties:
                src = self.source(pos)
                if src is None:
                    src = pos
                price = BOARD[src].price
                if price < cheapest_price:
                    cheapest_price = price
                    cheapest = pos
            if cheapest is None:
                break
            real_src = self.source(cheapest)
            if real_src is None:
                real_src = cheapest
            refund = BOARD[real_src].price // 2
            name = BOARD[real_src].name
            payer.properties.remove(cheapest)
            payer.money += refund
            self.houses.pop(cheapest, None)
            self.owner.pop(cheapest, None)
            self.copies.pop(cheapest, None)
            self.add_log(f"💸 {payer.name} liquide {name} (+{refund}€)")

        if payer.money < amount:
            self.add_log(f"☠️ {payer.name} — FAILLITE")
            if receiver is not None:
                receiver.money += payer.money
                for pos in list(payer.properties):
                    self.owner[pos] = self.players.index(receiver)
                    receiver.properties.append(pos)
            payer.money = 0
            payer.properties = []
            payer.hand = []
            payer.alive = False
            self.check_game_over()
            return

        payer.money -= amount
        if receiver is not None:
            receiver.money += amount

    def buy(self, p: Player, pos: int, source_idx: Optional[int] = None,
            discount_pct: int = 0) -> bool:
        if pos in self.owner:
            return False
        sq = BOARD[pos]
        if sq.kind == "libre":
            if source_idx is None:
                return False
            base_price = BOARD[source_idx].price
        else:
            base_price = sq.price
            source_idx = None
        price = base_price
        if discount_pct > 0:
            price = base_price - (base_price * discount_pct // 100)
            price = max(0, price)
        if p.money < price:
            return False
        p.money -= price
        p.properties.append(pos)
        self.owner[pos] = self.players.index(p)
        if source_idx is not None:
            self.copies[pos] = source_idx
        return True

    def build_house(self, p: Player, pos: int) -> bool:
        if self.owner.get(pos) != self.players.index(p):
            return False
        src = self.source(pos)
        if src is None or BOARD[src].kind != "street":
            return False
        if self.houses.get(pos, 0) >= 3:
            return False
        cost = self.house_cost(pos)
        if p.money < cost:
            return False
        p.money -= cost
        self.houses[pos] = self.houses.get(pos, 0) + 1
        return True

    def place_free_house(self, p: Player, pos: int) -> bool:
        if self.owner.get(pos) != self.players.index(p):
            return False
        src = self.source(pos)
        if src is None or BOARD[src].kind != "street":
            return False
        if self.houses.get(pos, 0) >= 3:
            return False
        self.houses[pos] = self.houses.get(pos, 0) + 1
        return True

    def upgrade_all_properties(self, p: Player) -> int:
        added = 0
        for pos in p.properties:
            src = self.source(pos)
            if src is None or BOARD[src].kind != "street":
                continue
            if self.houses.get(pos, 0) >= 3:
                continue
            self.houses[pos] = self.houses.get(pos, 0) + 1
            added += 1
        return added

    def draw_card(self) -> Card:
        if self.deck_pos >= len(self.deck):
            self._rng.shuffle(self.deck)
            self.deck_pos = 0
        card = self.deck[self.deck_pos]
        self.deck_pos += 1
        self.drawn_history.append(card)
        return card

    def peek_deck_size(self) -> int:
        return len(self.deck) - self.deck_pos

    def next_turn(self):
        self.current_player().turns_completed += 1
        if self.inflation_turns > 0:
            self.inflation_turns -= 1
            if self.inflation_turns == 0:
                self.inflation_pct = 0
                self.add_log("📉 Fin de la période d'inflation")
        n = len(self.players)
        for _ in range(n):
            self.current = (self.current + 1) % n
            if self.players[self.current].alive:
                break
        self.phase = "roll"
        self.doubles = 0
        self.turn_count += 1

    def check_goal(self) -> Optional[Player]:
        for p in self.players:
            if p.alive and self.net_worth(p) >= self.target:
                return p
        return None

    def check_game_over(self):
        alive = [p for p in self.players if p.alive]
        if len(alive) <= 1:
            self.game_over = True
            self.winner = alive[0] if alive else None


# ============================================================
#  APPLICATION
# ============================================================

class DarkMonopolyApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("DarkMonopoly")
        self.root.geometry("1300x920")
        self.root.minsize(1200, 860)

        self.theme_key = "nuit_bleu"
        self.theme = THEMES[self.theme_key]

        self.session_id = 0
        self.game: Optional[Game] = None
        self.hovered_cell: Optional[int] = None

        self._build_menubar()
        self.show_menu()

    # --------------------------------------------------------
    #  Utilitaires
    # --------------------------------------------------------
    def _schedule(self, delay_sec: float, fn):
        sid = self.session_id
        def wrapper():
            if sid != self.session_id:
                return
            fn()
        self.root.after(int(delay_sec * 1000), wrapper)

    def clear_root(self):
        for w in self.root.winfo_children():
            if isinstance(w, tk.Menu):
                continue
            w.destroy()

    def _build_menubar(self):
        menubar = tk.Menu(self.root)

        m_file = tk.Menu(menubar, tearoff=0)
        m_file.add_command(label="Nouvelle partie", accelerator="Ctrl+N",
                           command=self.menu_new_game)
        m_file.add_command(label="Retour au menu", command=self.show_menu)
        m_file.add_separator()
        m_file.add_command(label="Exporter la partie…", accelerator="Ctrl+E",
                           command=self.export_game)
        m_file.add_separator()
        m_file.add_command(label="Quitter", accelerator="Ctrl+Q",
                           command=self.root.quit)
        menubar.add_cascade(label="Fichier", menu=m_file)

        m_opt = tk.Menu(menubar, tearoff=0)
        m_theme = tk.Menu(m_opt, tearoff=0)
        for key, th in THEMES.items():
            m_theme.add_command(label=th["label"],
                                command=lambda k=key: self.set_theme(k))
        m_opt.add_cascade(label="Thème", menu=m_theme)
        menubar.add_cascade(label="Options", menu=m_opt)

        m_help = tk.Menu(menubar, tearoff=0)
        m_help.add_command(label="Règles", accelerator="F1", command=self.show_rules)
        m_help.add_separator()
        m_help.add_command(label="À propos", command=self.show_about)
        menubar.add_cascade(label="Aide", menu=m_help)

        self.root.config(menu=menubar)

        self.root.bind("<Control-n>", lambda e: self.menu_new_game())
        self.root.bind("<Control-q>", lambda e: self.root.quit())
        self.root.bind("<Control-e>", lambda e: self.export_game())
        self.root.bind("<F1>", lambda e: self.show_rules())
        self.root.bind("<Escape>", lambda e: self.show_menu())
        self.root.bind("<space>", lambda e: self.action_roll())
        self.root.bind("<Return>", lambda e: self.action_end_turn())
        self.root.bind("<b>", lambda e: self.action_build())
        self.root.bind("<i>", lambda e: self.show_hovered_info())

    # --------------------------------------------------------
    #  Menu principal
    # --------------------------------------------------------
    def show_menu(self):
        self.session_id += 1
        self.game = None
        self.hovered_cell = None
        self.clear_root()
        self.root.title("DarkMonopoly")
        self._build_menu_screen()

    def _build_menu_screen(self):
        t = self.theme
        self.root.configure(bg=t["bg"])

        wrap = tk.Frame(self.root, bg=t["bg"])
        wrap.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(wrap, text="DARK", bg=t["bg"], fg=t["accent"],
                 font=("Segoe UI", 60, "bold")).pack()
        tk.Label(wrap, text="MONOPOLY", bg=t["bg"], fg=t["fg"],
                 font=("Segoe UI", 42, "bold")).pack()

        tk.Label(wrap, text="v7.0  ·  MODES  ·  MAINS PUBLIQUES EN PVP",
                 bg=t["bg"], fg=t["muted"],
                 font=("Segoe UI", 10)).pack(pady=(10, 40))

        for label, cmd in [
            ("▶   JOUER",     self.menu_new_game),
            ("⚙   OPTIONS",   self.menu_options),
            ("📖   RÈGLES",    self.show_rules),
            ("✕   QUITTER",   self.root.quit),
        ]:
            b = tk.Button(wrap, text=label, command=cmd,
                          bg=t["btn_bg"], fg=t["btn_fg"],
                          activebackground=t["accent"],
                          activeforeground=t["accent_fg"],
                          relief="flat", width=24, pady=10, cursor="hand2",
                          font=("Segoe UI", 13, "bold"),
                          bd=0, highlightthickness=0)
            b.pack(pady=4)

    def menu_new_game(self):
        if self.game is not None and not self.game.game_over:
            if not messagebox.askyesno(
                "Nouvelle partie",
                "Une partie est en cours. En démarrer une nouvelle ?",
                parent=self.root):
                return
        setup = self._ask_game_setup()
        if setup:
            self.start_game(setup)

    def _ask_game_setup(self) -> Optional[List[dict]]:
        t = self.theme
        win = tk.Toplevel(self.root)
        win.title("Configuration")
        win.configure(bg=t["panel_bg"])
        win.transient(self.root)
        win.grab_set()
        win.resizable(False, False)

        tk.Label(win, text="MODE DE JEU", bg=t["panel_bg"], fg=t["accent"],
                 font=("Segoe UI", 16, "bold")).pack(padx=30, pady=(20, 12))

        mode_var = tk.StringVar(value="solo")
        modes = [
            ("solo",     "Solo — 1 humain vs IA"),
            ("pvp",      "PvP local — 2 à 4 humains"),
            ("duel_2v2", "Duel 2v2 — 2 équipes (humains)"),
            ("coop",     "Coop — 2 humains vs 2 IA"),
        ]
        for key, label in modes:
            tk.Radiobutton(
                win, text=label, variable=mode_var, value=key,
                bg=t["panel_bg"], fg=t["fg"],
                activebackground=t["panel_bg"], activeforeground=t["fg"],
                selectcolor=t["btn_bg"],
                font=("Segoe UI", 10), anchor="w",
                padx=10, pady=4,
            ).pack(fill="x", padx=30)

        count_frame = tk.Frame(win, bg=t["panel_bg"])
        count_frame.pack(fill="x", padx=30, pady=(14, 6))
        tk.Label(count_frame, text="Nombre total :", bg=t["panel_bg"],
                 fg=t["muted"], font=("Segoe UI", 10)).pack(side="left")

        count_var = tk.IntVar(value=2)
        for k in (2, 3, 4):
            tk.Radiobutton(
                count_frame, text=str(k), variable=count_var, value=k,
                bg=t["panel_bg"], fg=t["fg"],
                activebackground=t["panel_bg"], activeforeground=t["fg"],
                selectcolor=t["btn_bg"], font=("Segoe UI", 10),
            ).pack(side="left", padx=4)

        tk.Label(win, text="(Nombre utilisé pour Solo et PvP seulement)",
                 bg=t["panel_bg"], fg=t["muted"],
                 font=("Segoe UI", 8, "italic")).pack(pady=(0, 12))

        result = {"configs": None}

        def validate():
            mode = mode_var.get()
            n = count_var.get()
            configs = []
            if mode == "solo":
                configs.append({"name": "VOUS", "color": COMPANY_COLORS[0],
                                "is_ai": False, "team": 0})
                for i in range(1, n):
                    configs.append({"name": COMPANIES[i], "color": COMPANY_COLORS[i],
                                    "is_ai": True, "team": 0})
            elif mode == "pvp":
                for i in range(n):
                    configs.append({"name": f"P{i+1}", "color": COMPANY_COLORS[i],
                                    "is_ai": False, "team": 0})
            elif mode == "duel_2v2":
                for i in range(4):
                    team = 1 if i < 2 else 2
                    configs.append({"name": f"P{i+1}", "color": COMPANY_COLORS[i],
                                    "is_ai": False, "team": team})
            elif mode == "coop":
                configs.append({"name": "P1", "color": COMPANY_COLORS[0],
                                "is_ai": False, "team": 1})
                configs.append({"name": "P2", "color": COMPANY_COLORS[1],
                                "is_ai": False, "team": 1})
                configs.append({"name": "IA-1", "color": COMPANY_COLORS[2],
                                "is_ai": True, "team": 2})
                configs.append({"name": "IA-2", "color": COMPANY_COLORS[3],
                                "is_ai": True, "team": 2})
            result["configs"] = configs
            win.destroy()

        row = tk.Frame(win, bg=t["panel_bg"])
        row.pack(padx=30, pady=(0, 20))
        tk.Button(row, text="LANCER", command=validate,
                  bg=t["accent"], fg=t["accent_fg"],
                  activebackground=t["btn_act"],
                  activeforeground=t["accent_fg"],
                  relief="flat", padx=24, pady=10, cursor="hand2",
                  font=("Segoe UI", 11, "bold"),
                  bd=0, highlightthickness=0).pack(side="left", padx=4)
        tk.Button(row, text="ANNULER", command=win.destroy,
                  bg=t["btn_bg"], fg=t["btn_fg"],
                  activebackground=t["btn_act"],
                  activeforeground=t["btn_fg"],
                  relief="flat", padx=24, pady=10, cursor="hand2",
                  font=("Segoe UI", 11),
                  bd=0, highlightthickness=0).pack(side="left", padx=4)

        win.update_idletasks()
        w, h = win.winfo_width(), win.winfo_height()
        x = (win.winfo_screenwidth() - w) // 2
        y = (win.winfo_screenheight() - h) // 2
        win.geometry(f"+{x}+{y}")

        self.root.wait_window(win)
        return result["configs"]

    def menu_options(self):
        t = self.theme
        win = tk.Toplevel(self.root)
        win.title("Options")
        win.configure(bg=t["panel_bg"])
        win.transient(self.root)
        win.grab_set()
        win.resizable(False, False)

        tk.Label(win, text="OPTIONS", bg=t["panel_bg"], fg=t["accent"],
                 font=("Segoe UI", 18, "bold")).pack(padx=30, pady=(20, 10))
        tk.Label(win, text="THÈME", bg=t["panel_bg"], fg=t["muted"],
                 font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=30, pady=(10, 6))

        theme_frame = tk.Frame(win, bg=t["panel_bg"])
        theme_frame.pack(fill="x", padx=30)

        for key, th in THEMES.items():
            is_current = (key == self.theme_key)
            prefix = "▶  " if is_current else "     "
            tk.Button(
                theme_frame,
                text=f"{prefix}{th['label']}",
                command=lambda k=key: self.set_theme(k),
                bg=t["accent"] if is_current else t["btn_bg"],
                fg=t["accent_fg"] if is_current else t["btn_fg"],
                activebackground=t["btn_act"],
                activeforeground=t["btn_fg"],
                relief="flat", anchor="w", padx=12, pady=6, cursor="hand2",
                font=("Segoe UI", 10),
                bd=0, highlightthickness=0,
            ).pack(fill="x", pady=1)

        tk.Button(win, text="Fermer", command=win.destroy,
                  bg=t["accent"], fg=t["accent_fg"],
                  activebackground=t["btn_act"],
                  activeforeground=t["accent_fg"],
                  relief="flat", padx=20, pady=8, cursor="hand2",
                  font=("Segoe UI", 10, "bold"),
                  bd=0, highlightthickness=0).pack(pady=(20, 20))

        win.update_idletasks()
        w, h = win.winfo_width(), win.winfo_height()
        x = (win.winfo_screenwidth() - w) // 2
        y = (win.winfo_screenheight() - h) // 2
        win.geometry(f"+{x}+{y}")

    def set_theme(self, name: str):
        if name not in THEMES:
            return
        self.theme_key = name
        self.theme = THEMES[name]
        if self.game is None:
            self.show_menu()
        else:
            self.clear_root()
            self._build_game_ui()
            self.refresh()

    # --------------------------------------------------------
    #  Démarrage
    # --------------------------------------------------------
    def start_game(self, configs: List[dict]):
        self.session_id += 1
        self.game = Game(configs)

        mode_str = self._describe_mode(configs)
        self.game.add_log("▓▓▓ DARKMONOPOLY v7.0 ▓▓▓")
        self.game.add_log(f"Mode : {mode_str}")
        self.game.add_log(f"Joueurs : {', '.join(p.name for p in self.game.players)}")
        self.game.add_log(f"Objectif : {DEFAULT_TARGET}€ nets · {DEFAULT_MAX_TURNS} tours")
        self.game.add_log(f"─── Tour 1 · {self.game.current_player().name} ───")

        self.clear_root()
        self._build_game_ui()
        self.refresh()
        self._schedule(0.5, self._maybe_auto_play)

    def _describe_mode(self, configs: List[dict]) -> str:
        humans = sum(1 for c in configs if not c["is_ai"])
        teams = set(c.get("team", 0) for c in configs)
        if teams == {0}:
            if humans == 1:
                return "Solo (1 humain vs IA)"
            elif humans == len(configs):
                return f"PvP local ({humans} humains)"
            return "Mixte"
        return "Équipes (Duel/Coop)"

    # --------------------------------------------------------
    #  UI de jeu
    # --------------------------------------------------------
    def _hand_height(self) -> int:
        """Hauteur dynamique du panneau main."""
        if self.game and self.game.pvp_mode:
            # En PvP : une ligne par joueur (~90px chaque)
            return 40 + 90 * len(self.game.players)
        return HAND_BASE_PX

    def _build_game_ui(self):
        t = self.theme
        self.root.configure(bg=t["bg"])

        main = tk.Frame(self.root, bg=t["bg"])
        main.pack(fill="both", expand=True, padx=12, pady=12)

        left = tk.Frame(main, bg=t["bg"])
        left.pack(side="left", fill="y")

        self.canvas = tk.Canvas(
            left, width=BOARD_PX, height=BOARD_PX,
            bg=t["board_bg"], highlightthickness=0,
        )
        self.canvas.pack()
        self.canvas.bind("<Motion>", self.on_canvas_motion)
        self.canvas.bind("<Leave>", self.on_canvas_leave)
        self.canvas.bind("<Button-1>", self.on_canvas_click)

        # Main
        hand_h = self._hand_height()
        hand_wrap = tk.Frame(left, bg=t["panel_bg"], height=hand_h)
        hand_wrap.pack(fill="x", pady=(10, 0))
        hand_wrap.pack_propagate(False)

        header = tk.Frame(hand_wrap, bg=t["panel_bg"])
        header.pack(fill="x", padx=10, pady=(6, 2))
        self.lbl_hand_title = tk.Label(header, text="🃏 MAIN",
                                       bg=t["panel_bg"], fg=t["muted"],
                                       font=("Segoe UI", 9, "bold"))
        self.lbl_hand_title.pack(side="left")
        self.lbl_hand_count = tk.Label(header, text="",
                                       bg=t["panel_bg"], fg=t["muted"],
                                       font=("Segoe UI", 9))
        self.lbl_hand_count.pack(side="right")

        self.hand_canvas = tk.Canvas(hand_wrap, bg=t["panel_bg"],
                                     highlightthickness=0, height=hand_h - 30)
        self.hand_canvas.pack(fill="both", expand=True, padx=10, pady=(0, 8))

        # Panneau droit
        panel = tk.Frame(main, bg=t["panel_bg"], width=520)
        panel.pack(side="right", fill="both", expand=True, padx=(14, 0))
        panel.pack_propagate(False)

        top_block = tk.Frame(panel, bg=t["panel_bg"])
        top_block.pack(fill="x", padx=16, pady=(14, 0))
        self.lbl_dot = tk.Label(top_block, text="●", bg=t["panel_bg"],
                                font=("Segoe UI", 20))
        self.lbl_dot.pack(side="left")
        self.lbl_player = tk.Label(top_block, text="—", bg=t["panel_bg"],
                                   fg=t["fg"], font=("Segoe UI", 16, "bold"),
                                   anchor="w")
        self.lbl_player.pack(side="left", padx=(4, 0))
        self.lbl_ai_tag = tk.Label(top_block, text="", bg=t["panel_bg"],
                                   fg=t["muted"], font=("Segoe UI", 10))
        self.lbl_ai_tag.pack(side="left", padx=(8, 0))

        self.lbl_turn = tk.Label(panel, text="", bg=t["panel_bg"],
                                 fg=t["muted"], anchor="w",
                                 font=("Segoe UI", 10))
        self.lbl_turn.pack(fill="x", padx=16, pady=(4, 0))

        money_row = tk.Frame(panel, bg=t["panel_bg"])
        money_row.pack(fill="x", padx=16, pady=(6, 0))
        self.lbl_money = tk.Label(money_row, text="", bg=t["panel_bg"],
                                  fg=t["accent"],
                                  font=("Consolas", 15, "bold"), anchor="w")
        self.lbl_money.pack(side="left")
        self.lbl_net = tk.Label(money_row, text="", bg=t["panel_bg"],
                                fg=t["muted"],
                                font=("Segoe UI", 10), anchor="e")
        self.lbl_net.pack(side="right")

        self.progress_canvas = tk.Canvas(panel, height=8, bg=t["panel_bg"],
                                         highlightthickness=0)
        self.progress_canvas.pack(fill="x", padx=16, pady=(6, 4))

        self.lbl_status = tk.Label(panel, text="", bg=t["panel_bg"],
                                   fg=t["accent"], anchor="w",
                                   font=("Segoe UI", 10, "italic"))
        self.lbl_status.pack(fill="x", padx=16, pady=(2, 0))

        tk.Frame(panel, bg=t["border"], height=1).pack(fill="x", padx=16, pady=(12, 12))

        dice_row = tk.Frame(panel, bg=t["panel_bg"])
        dice_row.pack(fill="x", padx=16)
        self.lbl_dice = tk.Label(dice_row, text="🎲 —", bg=t["panel_bg"],
                                 fg=t["fg"],
                                 font=("Consolas", 20, "bold"), anchor="w")
        self.lbl_dice.pack(side="left")
        self.lbl_inflation = tk.Label(dice_row, text="", bg=t["panel_bg"],
                                      fg=t["accent"],
                                      font=("Segoe UI", 10, "bold"), anchor="e")
        self.lbl_inflation.pack(side="right")

        tk.Frame(panel, bg=t["panel_bg"], height=8).pack()

        self.btn_roll = self._make_action_button(
            panel, "🎲  LANCER LES DÉS  (Espace)",
            self.action_roll, primary=True)
        self.btn_build = self._make_action_button(
            panel, "🏠  CONSTRUIRE  (B)",
            self.action_build, primary=False)
        self.btn_end = self._make_action_button(
            panel, "✔  TERMINER LE TOUR  (Entrée)",
            self.action_end_turn, primary=False)

        tk.Frame(panel, bg=t["border"], height=1).pack(fill="x", padx=16, pady=(14, 12))

        tk.Label(panel, text="ENTREPRISES", bg=t["panel_bg"], fg=t["muted"],
                 font=("Segoe UI", 9, "bold"), anchor="w").pack(fill="x", padx=16, pady=(0, 6))
        self.players_frame = tk.Frame(panel, bg=t["panel_bg"])
        self.players_frame.pack(fill="x", padx=16)

        tk.Frame(panel, bg=t["border"], height=1).pack(fill="x", padx=16, pady=(14, 12))

        tk.Label(panel, text="JOURNAL", bg=t["panel_bg"], fg=t["muted"],
                 font=("Segoe UI", 9, "bold"), anchor="w").pack(fill="x", padx=16, pady=(0, 6))

        log_wrap = tk.Frame(panel, bg=t["panel_bg"])
        log_wrap.pack(fill="both", expand=True, padx=16, pady=(0, 14))

        self.log_text = tk.Text(
            log_wrap, bg=t["log_bg"], fg=t["log_fg"],
            font=("Consolas", 9), relief="flat", wrap="word",
            state="disabled", bd=0, highlightthickness=0,
            padx=10, pady=8, spacing1=1, spacing3=1,
        )
        self.log_text.pack(side="left", fill="both", expand=True)

        sb = tk.Scrollbar(log_wrap, command=self.log_text.yview,
                          bg=t["panel_bg"], troughcolor=t["panel_bg"],
                          activebackground=t["btn_act"], bd=0,
                          highlightthickness=0, relief="flat")
        sb.pack(side="right", fill="y")
        self.log_text.configure(yscrollcommand=sb.set)

    def _make_action_button(self, parent, text, cmd, primary=False):
        t = self.theme
        b = tk.Button(
            parent, text=text, command=cmd,
            bg=t["accent"] if primary else t["btn_bg"],
            fg=t["accent_fg"] if primary else t["btn_fg"],
            activebackground=t["btn_act"],
            activeforeground=t["accent_fg"] if primary else t["btn_fg"],
            relief="flat", pady=11, cursor="hand2",
            font=("Segoe UI", 11, "bold"),
            bd=0, highlightthickness=0, anchor="w", padx=16,
        )
        b.pack(fill="x", padx=16, pady=3)
        return b

    # --------------------------------------------------------
    #  Canvas events
    # --------------------------------------------------------
    def on_canvas_motion(self, event):
        col = event.x // CELL
        row = event.y // CELL
        new_hover = None
        if 0 <= row < GRID and 0 <= col < GRID:
            new_hover = cell_from_grid(row, col)
        if new_hover != self.hovered_cell:
            self.hovered_cell = new_hover
            self.draw_board()

    def on_canvas_leave(self, event):
        if self.hovered_cell is not None:
            self.hovered_cell = None
            self.draw_board()

    def on_canvas_click(self, event):
        if self.game is None:
            return
        col = event.x // CELL
        row = event.y // CELL
        if 0 <= row < GRID and 0 <= col < GRID:
            idx = cell_from_grid(row, col)
            if idx is not None:
                self.show_cell_info(idx)

    def show_hovered_info(self):
        if self.hovered_cell is not None:
            self.show_cell_info(self.hovered_cell)

    # --------------------------------------------------------
    #  Info case
    # --------------------------------------------------------
    def show_cell_info(self, pos: int):
        if self.game is None:
            return
        sq = BOARD[pos]
        src = self.game.source(pos)
        owner_idx = self.game.owner.get(pos)
        current_houses = self.game.houses.get(pos, 0)

        t = self.theme
        win = tk.Toplevel(self.root)
        win.title("Détails de la case")
        win.configure(bg=t["panel_bg"])
        win.transient(self.root)
        win.grab_set()
        win.resizable(False, False)

        if sq.kind == "libre" and src is not None:
            title = f"{BOARD[src].name}  ⁂"
            subtitle = f"Terrain Libre · copie de {BOARD[src].name}"
        elif sq.kind == "libre":
            title = "OPPORT."
            subtitle = "Terrain Libre (non assigné)"
        else:
            title = sq.name
            type_map = {
                "start": "Case DÉPART — +200€ à chaque passage",
                "carte": "Case CARTE — pioche le deck",
                "street": f"Propriété · groupe {sq.group.upper() if sq.group else '—'}",
            }
            subtitle = type_map.get(sq.kind, sq.kind)

        tk.Label(win, text=title, bg=t["panel_bg"], fg=t["accent"],
                 font=("Segoe UI", 18, "bold")).pack(padx=30, pady=(20, 2))
        tk.Label(win, text=subtitle, bg=t["panel_bg"], fg=t["muted"],
                 font=("Segoe UI", 10)).pack(pady=(0, 12))
        tk.Frame(win, bg=t["border"], height=1).pack(fill="x", padx=30, pady=(0, 12))

        content = tk.Frame(win, bg=t["panel_bg"])
        content.pack(fill="x", padx=30)

        if sq.kind == "street" or (sq.kind == "libre" and src is not None):
            real_src = src if src is not None else pos
            price = BOARD[real_src].price
            house_cost = price // 2
            for label, val in [("Prix d'achat", f"{price}€"),
                               ("Coût d'une maison", f"{house_cost}€")]:
                r = tk.Frame(content, bg=t["panel_bg"])
                r.pack(fill="x", pady=(0, 4))
                tk.Label(r, text=label + " :", bg=t["panel_bg"],
                         fg=t["muted"], font=("Segoe UI", 10),
                         anchor="w").pack(side="left")
                tk.Label(r, text=val, bg=t["panel_bg"], fg=t["fg"],
                         font=("Consolas", 11, "bold")).pack(side="right")

            tk.Label(content, text="LOYERS", bg=t["panel_bg"], fg=t["accent"],
                     font=("Segoe UI", 10, "bold"), anchor="w").pack(fill="x", pady=(12, 6))

            rent_table = tk.Frame(content, bg=t["panel_2"])
            rent_table.pack(fill="x", pady=(0, 8))
            for c, h in enumerate(["Maisons", "Loyer", "Statut"]):
                tk.Label(rent_table, text=h, bg=t["panel_2"], fg=t["muted"],
                         font=("Segoe UI", 9, "bold"),
                         padx=10, pady=4).grid(row=0, column=c, sticky="ew")
            for c in range(3):
                rent_table.grid_columnconfigure(c, weight=1)
            for h in range(4):
                rent = self.game.rent_at_houses(pos, h)
                is_current = (h == current_houses and owner_idx is not None)
                is_next = (h == current_houses + 1 and owner_idx is not None)
                row_bg = t["panel_bg"] if h % 2 == 0 else t["panel_2"]
                fg_color = t["accent"] if is_current else t["fg"]
                weight = "bold" if is_current else "normal"
                label_h = f"{h} maison" + ("s" if h > 1 else "") if h > 0 else "Aucune"
                status = "◀ actuel" if is_current else ("→ prochain" if is_next else "")
                tk.Label(rent_table, text=label_h, bg=row_bg, fg=fg_color,
                         font=("Segoe UI", 10, weight),
                         padx=10, pady=3, anchor="w").grid(row=h + 1, column=0, sticky="ew")
                tk.Label(rent_table, text=f"{rent}€", bg=row_bg, fg=fg_color,
                         font=("Consolas", 10, weight),
                         padx=10, pady=3, anchor="e").grid(row=h + 1, column=1, sticky="ew")
                tk.Label(rent_table, text=status, bg=row_bg,
                         fg=t["accent"] if is_current else t["muted"],
                         font=("Segoe UI", 9, "italic"),
                         padx=10, pady=3, anchor="w").grid(row=h + 1, column=2, sticky="ew")

            if owner_idx is not None:
                owner = self.game.players[owner_idx]
                tk.Frame(content, bg=t["border"], height=1).pack(fill="x", pady=(10, 10))
                r = tk.Frame(content, bg=t["panel_bg"])
                r.pack(fill="x")
                tk.Label(r, text="Propriétaire :", bg=t["panel_bg"],
                         fg=t["muted"], font=("Segoe UI", 10),
                         anchor="w").pack(side="left")
                tk.Label(r, text=owner.name, bg=t["panel_bg"], fg=owner.color,
                         font=("Segoe UI", 11, "bold")).pack(side="right")
                current_rent = self.game.compute_rent(pos)
                if current_rent > 0:
                    r2 = tk.Frame(content, bg=t["panel_bg"])
                    r2.pack(fill="x", pady=(4, 0))
                    tk.Label(r2, text="Loyer actuel :", bg=t["panel_bg"],
                             fg=t["muted"], font=("Segoe UI", 10),
                             anchor="w").pack(side="left")
                    tk.Label(r2, text=f"{current_rent}€", bg=t["panel_bg"],
                             fg=t["accent"],
                             font=("Consolas", 12, "bold")).pack(side="right")
            else:
                first_rent = self.game.rent_at_houses(pos, 0)
                tk.Frame(content, bg=t["border"], height=1).pack(fill="x", pady=(10, 10))
                for label, val, val_color in [("Statut", "Libre", t["muted"]),
                                              ("Loyer si acheté", f"{first_rent}€", t["fg"])]:
                    r = tk.Frame(content, bg=t["panel_bg"])
                    r.pack(fill="x", pady=(4, 0))
                    tk.Label(r, text=label + " :", bg=t["panel_bg"],
                             fg=t["muted"], font=("Segoe UI", 10),
                             anchor="w").pack(side="left")
                    tk.Label(r, text=val, bg=t["panel_bg"], fg=val_color,
                             font=("Consolas", 11, "bold")).pack(side="right")

        elif sq.kind == "start":
            tk.Label(content, text="Chaque passage vous rapporte 200€.",
                     bg=t["panel_bg"], fg=t["fg"],
                     font=("Segoe UI", 11), wraplength=340).pack(pady=10)

        elif sq.kind == "carte":
            tk.Label(content, text="Pioche la carte suivante du deck.",
                     bg=t["panel_bg"], fg=t["fg"],
                     font=("Segoe UI", 11), wraplength=340).pack(pady=4)
            tk.Label(content,
                     text=f"Cartes restantes : {self.game.peek_deck_size()}/{len(self.game.deck)}",
                     bg=t["panel_bg"], fg=t["muted"],
                     font=("Segoe UI", 10)).pack(pady=(4, 8))
            cats = {"invest": 0, "seize": 0, "money": 0}
            for c in self.game.deck[self.game.deck_pos:]:
                cats[c.category] += 1
            for cat, count in cats.items():
                r = tk.Frame(content, bg=t["panel_bg"])
                r.pack(fill="x", pady=2)
                tk.Label(r, text="■", bg=t["panel_bg"], fg=CAT_COLORS[cat],
                         font=("Segoe UI", 12)).pack(side="left", padx=(0, 6))
                tk.Label(r, text=f"{CAT_LABELS[cat]} : {count}",
                         bg=t["panel_bg"], fg=t["fg"],
                         font=("Segoe UI", 10)).pack(side="left")

        elif sq.kind == "libre" and src is None:
            tk.Label(content, text="Aucune propriété copiée ici.",
                     bg=t["panel_bg"], fg=t["muted"],
                     font=("Segoe UI", 11)).pack(pady=10)
            tk.Label(content,
                     text="Le prochain joueur qui tombe dessus pourra copier\n"
                          "n'importe quelle rue en payant son prix.",
                     bg=t["panel_bg"], fg=t["fg"],
                     font=("Segoe UI", 10), justify="center").pack()

        tk.Button(win, text="Fermer", command=win.destroy,
                  bg=t["accent"], fg=t["accent_fg"],
                  activebackground=t["btn_act"],
                  activeforeground=t["accent_fg"],
                  relief="flat", padx=24, pady=8, cursor="hand2",
                  font=("Segoe UI", 10, "bold"),
                  bd=0, highlightthickness=0).pack(pady=(20, 20))

        win.update_idletasks()
        w = 440
        h = win.winfo_height()
        x = (win.winfo_screenwidth() - w) // 2
        y = (win.winfo_screenheight() - h) // 2
        win.geometry(f"{w}x{h}+{x}+{y}")

    # --------------------------------------------------------
    #  Rendu plateau
    # --------------------------------------------------------
    def draw_board(self):
        if self.game is None:
            return
        c = self.canvas
        c.delete("all")
        t = self.theme
        c.configure(bg=t["board_bg"])

        c.create_rectangle(CELL, CELL, BOARD_PX - CELL, BOARD_PX - CELL,
                           fill=t["board_bg"], outline="")

        c.create_text(BOARD_PX / 2, BOARD_PX / 2 - 16,
                      text="DARKMONOPOLY", fill=t["accent"],
                      font=("Segoe UI", 20, "bold"))
        c.create_text(BOARD_PX / 2, BOARD_PX / 2 + 14,
                      text=f"v7.0 · Objectif {self.game.target}€",
                      fill=t["muted"], font=("Segoe UI", 10))

        for i in range(24):
            self._draw_cell(c, i)
        self._draw_tokens(c)

    def _draw_cell(self, c, i):
        t = self.theme
        row, col = grid_pos(i)
        x1 = col * CELL
        y1 = row * CELL
        x2 = x1 + CELL
        y2 = y1 + CELL

        sq = BOARD[i]
        src = self.game.source(i)
        owner_idx = self.game.owner.get(i)

        if sq.kind == "libre" and src is not None:
            display = BOARD[src].name
            group = BOARD[src].group
        elif sq.kind == "libre":
            display = "· LIBRE ·"
            group = None
        else:
            display = sq.name
            group = sq.group

        if owner_idx is not None:
            bg = self.game.players[owner_idx].color
            fg = "#0a0a0a"
        elif sq.kind == "start":
            bg = t["accent"]
            fg = t["accent_fg"]
        elif sq.kind == "carte":
            bg = t["panel_2"]
            fg = t["accent"]
        elif group and group in GROUP_COLORS:
            bg = GROUP_COLORS[group]
            fg = "#0a0a0a"
        else:
            bg = t["cell_bg"]
            fg = t["muted"]

        c.create_rectangle(x1, y1, x2, y2, fill=bg,
                           outline=t["border"], width=1)

        # Cadre contrasté pour terrains sans propriétaire
        is_terrain = sq.kind in ("street", "libre")
        if is_terrain and owner_idx is None:
            c.create_rectangle(x1 + 4, y1 + 4, x2 - 4, y2 - 4,
                               outline=t["pending"], width=3)

        if i == self.hovered_cell:
            c.create_rectangle(x1 + 1, y1 + 1, x2 - 1, y2 - 1,
                               outline=t["accent"], width=3)

        if sq.kind == "libre" and src is not None:
            c.create_text(x2 - 10, y1 + 12, text="⁂", fill=t["accent"],
                          font=("Segoe UI", 11, "bold"))

        if sq.kind == "carte":
            c.create_text((x1 + x2) / 2, y1 + 20, text="⚡",
                          fill=t["accent"], font=("Segoe UI", 18, "bold"))

        short = display
        if len(short) > 11:
            short = short[:10] + "."
        c.create_text((x1 + x2) / 2, (y1 + y2) / 2 + 4,
                      text=short, fill=fg,
                      font=("Segoe UI", 10, "bold"),
                      width=CELL - 8, justify="center")

        if sq.kind == "street" and owner_idx is None:
            c.create_text((x1 + x2) / 2, (y1 + y2) / 2 + 24,
                          text=f"{sq.price}€", fill=fg,
                          font=("Segoe UI", 9))
        elif sq.kind == "libre" and owner_idx is None:
            c.create_text((x1 + x2) / 2, (y1 + y2) / 2 + 24,
                          text="libre", fill=fg,
                          font=("Segoe UI", 8, "italic"))
        elif owner_idx is not None:
            owner = self.game.players[owner_idx]
            c.create_text((x1 + x2) / 2, (y1 + y2) / 2 + 24,
                          text=owner.name, fill=fg,
                          font=("Segoe UI", 8, "bold"))

        houses = self.game.houses.get(i, 0)
        if houses > 0:
            for h in range(houses):
                hx = x1 + 12 + h * 12
                hy = y2 - 14
                color = "#ef4444" if houses == 3 else "#10b981"
                c.create_rectangle(hx, hy, hx + 8, hy + 8,
                                   fill=color, outline="#0a0a0a")

    def _draw_tokens(self, c):
        by_pos: Dict[int, list] = {}
        for idx, p in enumerate(self.game.players):
            if p.alive:
                by_pos.setdefault(p.position, []).append((idx, p))

        for pos, plist in by_pos.items():
            row, col = grid_pos(pos)
            x1 = col * CELL
            y1 = row * CELL
            cx = x1 + CELL / 2
            cy = y1 + CELL / 2

            n = len(plist)
            offsets = {
                1: [(0, 22)],
                2: [(-13, 22), (13, 22)],
                3: [(-13, 22), (13, 22), (0, 40)],
                4: [(-13, 22), (13, 22), (-13, 40), (13, 40)],
            }.get(n, [(0, 22)])

            for (idx, p), (dx, dy) in zip(plist, offsets):
                is_current = (idx == self.game.current)
                rad = 9 if is_current else 7
                c.create_oval(cx + dx - rad - 2, cy + dy - rad - 2,
                              cx + dx + rad + 2, cy + dy + rad + 2,
                              fill=self.theme["panel_bg"], outline="")
                c.create_oval(cx + dx - rad, cy + dy - rad,
                              cx + dx + rad, cy + dy + rad,
                              fill=p.color,
                              outline="#ffffff" if is_current else "#000000",
                              width=2 if is_current else 1)

    # --------------------------------------------------------
    #  Main de cartes — logique v7
    # --------------------------------------------------------
    def draw_hand(self):
        """Dessine la main selon le mode :
        - PvP (tous humains) : toutes les mains visibles
        - Sinon : main du joueur courant si humain, sinon rien
        """
        c = self.hand_canvas
        c.delete("all")
        if self.game is None:
            return
        t = self.theme

        if self.game.pvp_mode:
            self._draw_hand_pvp(c)
        else:
            self._draw_hand_solo(c)

    def _draw_hand_solo(self, c):
        """Mode Solo/Mixte : uniquement la main du joueur courant s'il est humain."""
        t = self.theme
        p = self.game.current_player()
        self.lbl_hand_title.configure(text=f"🃏 MAIN — {p.name}")

        if p.is_ai:
            self.lbl_hand_count.configure(text=f"{len(p.hand)} carte(s) (IA)")
            c.create_text(BOARD_PX / 2, 40,
                          text=f"🤖 {p.name} joue ses cartes automatiquement...",
                          fill=t["muted"], font=("Segoe UI", 11, "italic"))
            return

        self.lbl_hand_count.configure(text=f"{len(p.hand)} carte(s)")

        if not p.hand:
            c.create_text(BOARD_PX / 2, 40,
                          text="Aucune carte. Tombez sur une case ⚡ pour en piocher.",
                          fill=t["muted"], font=("Segoe UI", 10, "italic"))
            return

        can_play = (self.game.phase == "end" and not self.game.game_over)
        self._draw_hand_row(c, p, 0, can_play, clickable=True)

    def _draw_hand_pvp(self, c):
        """Mode PvP : toutes les mains affichées, une ligne par joueur."""
        t = self.theme
        self.lbl_hand_title.configure(text="🃏 MAINS DE TOUS LES JOUEURS (PvP)")

        all_cards = sum(len(p.hand) for p in self.game.players)
        self.lbl_hand_count.configure(text=f"{all_cards} carte(s) au total")

        current = self.game.current_player()
        can_current_play = (self.game.phase == "end"
                            and not self.game.game_over
                            and not current.is_ai)

        y = 8
        row_h = 82
        for pl in self.game.players:
            is_current = pl is current
            self._draw_hand_row_pvp(c, pl, y, is_current,
                                     clickable=is_current and can_current_play)
            y += row_h

    def _draw_hand_row(self, c, p: Player, y: int, can_play: bool, clickable: bool):
        """Dessine une ligne de cartes (utilisé en mode solo)."""
        t = self.theme
        card_w = 110
        card_h = 70
        pad = 6
        x = pad

        for idx, card in enumerate(p.hand):
            color = CAT_COLORS[card.category]
            is_clickable = clickable and can_play
            outline = color if is_clickable else t["border"]
            width = 3 if is_clickable else 1

            c.create_rectangle(x, y + 4, x + card_w, y + 4 + card_h,
                               fill=t["panel_2"], outline=outline, width=width)
            c.create_rectangle(x, y + 4, x + card_w, y + 16,
                               fill=color, outline="")
            c.create_text(x + card_w / 2, y + 10,
                          text=CAT_LABELS[card.category],
                          fill="#ffffff", font=("Segoe UI", 7, "bold"))
            short = card.name
            if len(short) > 16:
                short = short[:15] + "."
            c.create_text(x + card_w / 2, y + 4 + card_h / 2 + 4,
                          text=short, fill=t["fg"],
                          font=("Segoe UI", 9, "bold"),
                          width=card_w - 8, justify="center")
            if is_clickable:
                c.create_text(x + card_w / 2, y + 4 + card_h - 8,
                              text="CLIQUER", fill=t["muted"],
                              font=("Segoe UI", 7, "italic"))
                tag = f"hand_card_{idx}"
                c.create_rectangle(x, y + 4, x + card_w, y + 4 + card_h,
                                   outline="", fill="", tags=(tag,))
                c.tag_bind(tag, "<Button-1>",
                           lambda e, i=idx: self._on_hand_card_click(i))
            x += card_w + pad

    def _draw_hand_row_pvp(self, c, p: Player, y: int,
                            is_current: bool, clickable: bool):
        """Dessine la main d'un joueur (mode PvP) sur une ligne."""
        t = self.theme
        # Liseré gauche couleur joueur
        c.create_rectangle(2, y, 6, y + 78, fill=p.color, outline="")

        # Nom
        name_txt = f"{p.name}"
        if is_current:
            name_txt += "  ▶"
        c.create_text(14, y + 12, text=name_txt, fill=p.color,
                      anchor="w", font=("Segoe UI", 10, "bold"))
        c.create_text(14, y + 30, text=f"🃏 {len(p.hand)}",
                      fill=t["muted"], anchor="w", font=("Segoe UI", 9))

        # Cartes
        card_w = 90
        card_h = 60
        pad = 5
        x = 130
        max_x = BOARD_PX - 20

        for idx, card in enumerate(p.hand):
            if x + card_w > max_x:
                break
            color = CAT_COLORS[card.category]
            # Cliquable uniquement si c'est le joueur courant et son tour
            is_clickable = clickable and is_current
            outline = color if is_clickable else t["border"]
            width = 3 if is_clickable else 1

            c.create_rectangle(x, y + 10, x + card_w, y + 10 + card_h,
                               fill=t["panel_2"], outline=outline, width=width)
            c.create_rectangle(x, y + 10, x + card_w, y + 21,
                               fill=color, outline="")
            c.create_text(x + card_w / 2, y + 15,
                          text=CAT_LABELS[card.category][:10],
                          fill="#ffffff", font=("Segoe UI", 6, "bold"))
            short = card.name
            if len(short) > 14:
                short = short[:13] + "."
            c.create_text(x + card_w / 2, y + 10 + card_h / 2 + 4,
                          text=short, fill=t["fg"],
                          font=("Segoe UI", 8, "bold"),
                          width=card_w - 6, justify="center")

            if is_clickable:
                tag = f"hand_pvp_{p.name}_{idx}"
                c.create_rectangle(x, y + 10, x + card_w, y + 10 + card_h,
                                   outline="", fill="", tags=(tag,))
                c.tag_bind(tag, "<Button-1>",
                           lambda e, i=idx: self._on_hand_card_click(i))

            x += card_w + pad

        if not p.hand:
            c.create_text(130, y + 40, text="(vide)",
                          fill=t["muted"], anchor="w",
                          font=("Segoe UI", 9, "italic"))

    def _on_hand_card_click(self, idx: int):
        if self.game is None:
            return
        p = self.game.current_player()
        if p.is_ai:
            return
        if self.game.phase != "end":
            messagebox.showinfo(
                "Cartes",
                "Tu ne peux jouer des cartes qu'après avoir lancé les dés.",
                parent=self.root)
            return
        if idx >= len(p.hand):
            return
        card = p.hand[idx]
        self._open_play_card_dialog(p, idx, card)

    def _open_play_card_dialog(self, p: Player, idx: int, card: Card):
        t = self.theme
        cat_color = CAT_COLORS[card.category]

        win = tk.Toplevel(self.root)
        win.title("Carte")
        win.configure(bg=t["panel_bg"])
        win.transient(self.root)
        win.grab_set()
        win.resizable(False, False)

        tk.Frame(win, bg=cat_color, height=6).pack(fill="x")

        header = tk.Frame(win, bg=t["panel_bg"])
        header.pack(fill="x", padx=30, pady=(20, 0))
        tk.Label(header, text="⚡", bg=t["panel_bg"], fg=cat_color,
                 font=("Segoe UI", 22, "bold")).pack(side="left", padx=(0, 10))
        title_col = tk.Frame(header, bg=t["panel_bg"])
        title_col.pack(side="left", fill="x", expand=True, anchor="w")
        tk.Label(title_col, text=CAT_LABELS[card.category],
                 bg=t["panel_bg"], fg=cat_color,
                 font=("Segoe UI", 9, "bold"),
                 anchor="w").pack(fill="x")
        tk.Label(title_col, text=card.name, bg=t["panel_bg"], fg=t["fg"],
                 font=("Segoe UI", 15, "bold"),
                 anchor="w").pack(fill="x")

        tk.Label(win, text=card.description, bg=t["panel_bg"], fg=t["fg"],
                 font=("Segoe UI", 11), wraplength=380,
                 justify="left").pack(padx=30, pady=(18, 20), anchor="w")

        row = tk.Frame(win, bg=t["panel_bg"])
        row.pack(pady=(0, 22))

        def play():
            win.destroy()
            self._play_card(p, idx, card)

        def cancel():
            win.destroy()

        tk.Button(row, text="ACTIVER", command=play,
                  bg=t["accent"], fg=t["accent_fg"],
                  activebackground=t["btn_act"],
                  activeforeground=t["accent_fg"],
                  relief="flat", padx=24, pady=10, cursor="hand2",
                  font=("Segoe UI", 11, "bold"),
                  bd=0, highlightthickness=0).pack(side="left", padx=6)
        tk.Button(row, text="GARDER", command=cancel,
                  bg=t["btn_bg"], fg=t["btn_fg"],
                  activebackground=t["btn_act"],
                  activeforeground=t["btn_fg"],
                  relief="flat", padx=24, pady=10, cursor="hand2",
                  font=("Segoe UI", 11),
                  bd=0, highlightthickness=0).pack(side="left", padx=6)

        win.update_idletasks()
        w = 440
        h = win.winfo_height()
        x = (win.winfo_screenwidth() - w) // 2
        y = (win.winfo_screenheight() - h) // 2
        win.geometry(f"{w}x{h}+{x}+{y}")

        self.root.wait_window(win)

    def _play_card(self, p: Player, idx: int, card: Card):
        if idx >= len(p.hand):
            return
        p.hand.pop(idx)
        self.game.add_log(f"⚡ {p.name} joue : {card.name}")
        try:
            self._resolve_card(p, card)
        except Exception as e:
            self.game.add_log(f"⚠️ Erreur carte {card.name} : {e}")
        self.refresh()

    # --------------------------------------------------------
    #  Refresh
    # --------------------------------------------------------
    def refresh(self):
        if self.game is None:
            return
        self.draw_board()
        self.draw_hand()
        t = self.theme
        p = self.game.current_player()

        self.root.title(
            f"DarkMonopoly — {p.name} · Tour {self.game.turn_count}/{self.game.max_turns}")

        self.lbl_dot.configure(fg=p.color)
        self.lbl_player.configure(text=p.name, fg=p.color)
        self.lbl_ai_tag.configure(text="🤖 IA" if p.is_ai else "🧑 Humain")

        skip_info = f"  ·  ⏸️ paralysé {p.skip_turns}t" if p.skip_turns > 0 else ""
        team_info = f"  ·  Équipe {p.team}" if p.team > 0 else ""
        self.lbl_turn.configure(
            text=f"Tour {self.game.turn_count}/{self.game.max_turns}{team_info}{skip_info}")

        self.lbl_money.configure(text=f"{p.money}€")
        nw = self.game.net_worth(p)
        self.lbl_net.configure(text=f"Net : {nw}€ / {self.game.target}€")

        self._draw_progress(nw)

        if self.game.inflation_turns > 0:
            sign = "+" if self.game.inflation_pct >= 0 else ""
            self.lbl_inflation.configure(
                text=f"📈 {sign}{self.game.inflation_pct}% · {self.game.inflation_turns}t")
        else:
            self.lbl_inflation.configure(text="")

        if p.turns_completed == 0:
            self.lbl_status.configure(text="★ Premier tour — pas de loyer")
        else:
            self.lbl_status.configure(text="")

        d1, d2 = self.game.dice
        if d1 and d2:
            self.lbl_dice.configure(text=f"🎲  {d1} + {d2} = {d1 + d2}")
        else:
            self.lbl_dice.configure(text="🎲  —")

        human = (not p.is_ai) and (not self.game.game_over)
        can_roll = human and self.game.phase == "roll"
        can_end = human and self.game.phase == "end"
        can_build = can_end

        self.btn_roll.configure(state="normal" if can_roll else "disabled")
        self.btn_end.configure(state="normal" if can_end else "disabled")
        self.btn_build.configure(state="normal" if can_build else "disabled")

        # Liste joueurs
        for w in self.players_frame.winfo_children():
            w.destroy()
        for i, pl in enumerate(self.game.players):
            row = tk.Frame(self.players_frame, bg=t["panel_bg"])
            row.pack(fill="x", pady=2)
            marker = "▶" if (i == self.game.current and not self.game.game_over) else " "
            tk.Label(row, text=marker, bg=t["panel_bg"], fg=t["accent"],
                     font=("Segoe UI", 10, "bold"), width=2).pack(side="left")
            tk.Label(row, text="●", bg=t["panel_bg"], fg=pl.color,
                     font=("Segoe UI", 12)).pack(side="left", padx=(2, 6))

            tag = "" if pl.alive else "  ☠️"
            if pl.team > 0:
                tag += f"  [É{pl.team}]"
            # Cartes visibles seulement si PvP ou si c'est un humain (toujours public en PvP)
            if self.game.pvp_mode or not pl.is_ai:
                if pl.hand:
                    tag += f"  🃏{len(pl.hand)}"
            # IA : on cache le nombre de cartes
            tk.Label(row, text=f"{pl.name}{tag}", bg=t["panel_bg"],
                     fg=t["fg"] if pl.alive else t["muted"],
                     font=("Segoe UI", 10), anchor="w",
                     width=16).pack(side="left")

            tk.Label(row, text=f"{pl.money}€", bg=t["panel_bg"], fg=t["muted"],
                     font=("Consolas", 10, "bold"),
                     width=6).pack(side="left", padx=(0, 6))

            mini = tk.Canvas(row, height=6, width=70, bg=t["panel_2"],
                             highlightthickness=0)
            mini.pack(side="right", padx=(4, 0))
            nwp = self.game.net_worth(pl)
            pct = min(100, int(nwp * 100 / self.game.target))
            mini.create_rectangle(0, 0, int(70 * pct / 100), 6,
                                  fill=t["accent"], outline="")

        # Log
        self.log_text.configure(state="normal")
        self.log_text.delete("1.0", "end")
        for line in self.game.log[-100:]:
            self.log_text.insert("end", line + "\n")
        self.log_text.see("end")
        self.log_text.configure(state="disabled")

    def _draw_progress(self, nw: int):
        t = self.theme
        c = self.progress_canvas
        c.delete("all")
        c.update_idletasks()
        w = c.winfo_width()
        if w <= 1:
            w = 400
        c.create_rectangle(0, 0, w, 8, fill=t["panel_2"], outline="")
        pct = min(1.0, nw / self.game.target)
        c.create_rectangle(0, 0, int(w * pct), 8, fill=t["accent"], outline="")

    # --------------------------------------------------------
    #  Actions
    # --------------------------------------------------------
    def action_roll(self):
        if self.game is None or self.game.game_over:
            return
        p = self.game.current_player()
        if p.is_ai or self.game.phase != "roll":
            return
        self._do_roll()

    def action_end_turn(self):
        if self.game is None or self.game.game_over:
            return
        p = self.game.current_player()
        if p.is_ai or self.game.phase != "end":
            return
        self._end_turn()

    def action_build(self):
        if self.game is None:
            return
        p = self.game.current_player()
        if p.is_ai or self.game.game_over:
            return
        self._open_build_dialog(p)

    # --------------------------------------------------------
    #  Boucle de tour
    # --------------------------------------------------------
    def _do_roll(self):
        if self.game is None or self.game.game_over:
            return
        p = self.game.current_player()
        self.game.phase = "moving"
        self.refresh()

        d1, d2 = self.game.roll_dice()
        total = d1 + d2
        self.game.add_log(f"🎲 {p.name} : {d1}+{d2}={total}")

        if d1 == d2:
            self.game.doubles += 1
            if self.game.doubles >= 3:
                self.game.add_log(f"🚔 3 doubles — {p.name} redirigé vers CARTE")
                p.position = 6
                self.game.phase = "end"
                self.refresh()
                if not p.is_ai:
                    messagebox.showinfo(
                        "🚔 Trois doubles",
                        f"{p.name}, trois doubles d'affilée.\n"
                        "Redirigé vers CARTE. Tour perdu.",
                        parent=self.root)
                # FIX : l'IA joue sa main puis termine (via _end_turn)
                if p.is_ai:
                    self._schedule(0.8, self._end_turn)
                return

        self.game.move_player(p, total)
        self.refresh()
        self._schedule(0.35, lambda: self._after_move(p, d1 == d2))

    def _after_move(self, p: Player, is_double: bool):
        if self.game is None or self.game.game_over:
            return
        self._handle_landing(p)
        self.refresh()

        if self.game.game_over:
            self._end_game_natural()
            return

        winner = self.game.check_goal()
        if winner is not None:
            self.game.game_over = True
            self.game.winner = winner
            self.game.winning_team = winner.team
            self._end_game_natural()
            return

        if is_double:
            self.game.add_log(f"✨ Double — {p.name} rejoue")
            self.game.phase = "roll"
            self.refresh()
            if p.is_ai:
                self._schedule(0.8, self._do_roll)
            return

        self.game.phase = "end"
        self.refresh()
        # L'IA ne joue PLUS ses cartes ici : c'est _end_turn qui s'en charge.
        if p.is_ai:
            self._schedule(0.8, self._end_turn)

    def _handle_landing(self, p: Player):
        if self.game is None:
            return
        pos = p.position
        sq = BOARD[pos]
        src = self.game.source(pos)

        if sq.kind == "carte":
            self.game.add_log(f"⚡ {p.name} pioche une carte...")
        elif sq.kind == "libre" and src is None:
            self.game.add_log(f"➡️ {p.name} : Terrain Libre")
        elif sq.kind == "libre":
            self.game.add_log(f"➡️ {p.name} : {BOARD[src].name} ⁂")
        else:
            self.game.add_log(f"➡️ {p.name} : {sq.name}")

        if sq.kind == "carte":
            self._handle_card(p)
            return

        if sq.kind == "libre" and src is None:
            self._handle_libre(p, pos)
            return

        if sq.kind != "street":
            return

        owner_idx = self.game.owner.get(pos)
        if owner_idx is None:
            real_src = self.game.source(pos)
            if real_src is None:
                real_src = pos
            price = BOARD[real_src].price
            if p.money < price:
                self.game.add_log(f"❌ {p.name} : fonds insuffisants ({price}€)")
                return
            if p.is_ai:
                if p.money - price >= 150:
                    self.game.buy(p, pos)
                    self.game.add_log(
                        f"🏷️ {p.name} sécurise {BOARD[real_src].name} ({price}€)")
            else:
                self._ask_buy(p, pos, price, real_src)
            return

        if owner_idx == self.game.current:
            return

        rent = self.game.compute_rent(pos)
        if p.turns_completed == 0:
            if rent > 0:
                self.game.add_log(f"★ Premier tour — pas de loyer ({rent}€)")
            return
        if rent <= 0:
            return
        owner = self.game.players[owner_idx]
        self.game.add_log(f"💵 {p.name} paie {rent}€ à {owner.name}")
        self.game.pay(p, owner, rent)

    # --------------------------------------------------------
    #  Carte — pioche
    # --------------------------------------------------------
    def _handle_card(self, p: Player):
        card = self.game.draw_card()
        p.hand.append(card)
        self.game.add_log(f"🃏 {p.name} pioche : {card.name} ({CAT_LABELS[card.category]})")

        # Feedback visuel universel
        self.refresh()

        if not p.is_ai:
            self._show_card_popup(p, card)

    def _show_card_popup(self, p: Player, card: Card):
        t = self.theme
        cat_color = CAT_COLORS[card.category]

        win = tk.Toplevel(self.root)
        win.title("Nouvelle carte")
        win.configure(bg=t["panel_bg"])
        win.transient(self.root)
        win.grab_set()
        win.resizable(False, False)

        tk.Frame(win, bg=cat_color, height=6).pack(fill="x")

        header = tk.Frame(win, bg=t["panel_bg"])
        header.pack(fill="x", padx=30, pady=(20, 0))
        tk.Label(header, text="🃏", bg=t["panel_bg"], fg=cat_color,
                 font=("Segoe UI", 22, "bold")).pack(side="left", padx=(0, 10))
        title_col = tk.Frame(header, bg=t["panel_bg"])
        title_col.pack(side="left", fill="x", expand=True, anchor="w")
        tk.Label(title_col, text=f"NOUVELLE CARTE · {CAT_LABELS[card.category]}",
                 bg=t["panel_bg"], fg=cat_color,
                 font=("Segoe UI", 9, "bold"),
                 anchor="w").pack(fill="x")
        tk.Label(title_col, text=card.name, bg=t["panel_bg"], fg=t["fg"],
                 font=("Segoe UI", 15, "bold"),
                 anchor="w").pack(fill="x")

        tk.Label(win, text=card.description, bg=t["panel_bg"], fg=t["fg"],
                 font=("Segoe UI", 11), wraplength=380,
                 justify="left").pack(padx=30, pady=(18, 8), anchor="w")
        tk.Label(win,
                 text="→ Carte ajoutée à ta main (en bas du plateau).\n"
                      "→ Clique dessus pour l'activer quand tu veux.",
                 bg=t["panel_bg"], fg=t["muted"],
                 font=("Segoe UI", 9, "italic"), justify="left").pack(
                     padx=30, pady=(0, 12), anchor="w")

        tk.Button(win, text="OK", command=win.destroy,
                  bg=t["accent"], fg=t["accent_fg"],
                  activebackground=t["btn_act"],
                  activeforeground=t["accent_fg"],
                  relief="flat", padx=30, pady=10, cursor="hand2",
                  font=("Segoe UI", 11, "bold"),
                  bd=0, highlightthickness=0).pack(pady=(0, 22))

        win.update_idletasks()
        w = 440
        h = win.winfo_height()
        x = (win.winfo_screenwidth() - w) // 2
        y = (win.winfo_screenheight() - h) // 2
        win.geometry(f"{w}x{h}+{x}+{y}")

        self.root.wait_window(win)

    # --------------------------------------------------------
    #  Résolution des effets
    # --------------------------------------------------------
    def _resolve_card(self, p: Player, card: Card):
        eff = card.effect
        val = card.value

        if eff == "cash":
            p.money += val
            self.game.add_log(f"💰 {p.name} +{val}€")

        elif eff == "pay":
            self.game.pay(p, None, val)
            self.game.add_log(f"💸 {p.name} paie {val}€ à la banque")

        elif eff == "discount_buy":
            self._card_discount_buy(p, val)
        elif eff == "free_house":
            self._card_free_house(p)
        elif eff == "upgrade_all":
            added = self.game.upgrade_all_properties(p)
            if added > 0:
                self.game.add_log(f"🏠 {p.name} développe {added} propriété(s)")
            else:
                self.game.add_log("↩️ Aucune propriété à développer")
        elif eff == "dividend":
            total = val * len(p.properties)
            p.money += total
            self.game.add_log(f"💰 Dividendes : {p.name} +{total}€")
        elif eff == "hostile_takeover":
            self._card_hostile_takeover(p, val)
        elif eff == "confiscate":
            self._card_confiscate(p, val)
        elif eff == "blocus":
            self._card_blocus(p)
        elif eff == "redirect":
            self._card_redirect(p)
        elif eff == "audit_cross":
            self._card_audit_cross(p, val)
        else:
            self.game.add_log(f"⚠️ Effet inconnu : {eff}")

    def _card_discount_buy(self, p: Player, discount: int):
        candidates = [i for i, s in enumerate(BOARD)
                      if s.kind == "street" and i not in self.game.owner
                      and s.price - s.price * discount // 100 <= p.money]
        if not candidates:
            self.game.add_log("↩️ Aucun terrain abordable à acheter")
            return
        if p.is_ai:
            candidates.sort(key=lambda i: -BOARD[i].price)
            chosen = candidates[0]
            price = BOARD[chosen].price - BOARD[chosen].price * discount // 100
            self.game.buy(p, chosen, discount_pct=discount)
            self.game.add_log(f"🏷️ {p.name} achète {BOARD[chosen].name} à -{discount}% ({price}€)")
        else:
            chosen = self._choose_unowned_street(p, discount)
            if chosen is None:
                self.game.add_log("↩️ Achat annulé")
                return
            price = BOARD[chosen].price - BOARD[chosen].price * discount // 100
            self.game.buy(p, chosen, discount_pct=discount)
            self.game.add_log(f"🏷️ {p.name} achète {BOARD[chosen].name} à -{discount}% ({price}€)")

    def _card_free_house(self, p: Player):
        candidates = []
        for pos in p.properties:
            src = self.game.source(pos)
            if src is None:
                continue
            if BOARD[src].kind != "street":
                continue
            if self.game.houses.get(pos, 0) >= 3:
                continue
            candidates.append(pos)
        if not candidates:
            self.game.add_log("↩️ Aucune propriété où poser la maison")
            return
        if p.is_ai:
            chosen = max(candidates, key=lambda pp: BOARD[self.game.source(pp)].price)
        else:
            chosen = self._choose_your_property(p, candidates, "Maison offerte")
            if chosen is None:
                self.game.add_log("↩️ Maison non posée")
                return
        self.game.place_free_house(p, chosen)
        src = self.game.source(chosen)
        self.game.add_log(f"🏠 Maison offerte sur {BOARD[src].name}")

    def _card_hostile_takeover(self, p: Player, price_pct: int):
        opponents = [pl for pl in self.game.players if pl.alive and pl is not p]
        candidates = []
        for opp in opponents:
            for pos in opp.properties:
                src = self.game.source(pos)
                if src is None:
                    continue
                cost = BOARD[src].price * price_pct // 100
                if p.money >= cost:
                    candidates.append((pos, opp, cost))
        if not candidates:
            self.game.add_log("↩️ Aucune cible accessible")
            return
        if p.is_ai:
            pos, opp, cost = max(candidates,
                                  key=lambda x: BOARD[self.game.source(x[0])].price)
        else:
            result = self._choose_target_property(candidates, "Acquisition hostile")
            if result is None:
                self.game.add_log("↩️ Acquisition annulée")
                return
            pos, opp, cost = result
        opp.properties.remove(pos)
        opp.money += cost
        p.money -= cost
        p.properties.append(pos)
        self.game.owner[pos] = self.game.players.index(p)
        src = self.game.source(pos)
        self.game.add_log(f"⚔️ {p.name} prend {BOARD[src].name} à {opp.name} pour {cost}€")

    def _card_confiscate(self, p: Player, price_pct: int):
        opponents = [pl for pl in self.game.players if pl.alive and pl is not p]
        candidates = []
        for opp in opponents:
            for pos in opp.properties:
                src = self.game.source(pos)
                if src is None:
                    continue
                cost = BOARD[src].price * price_pct // 100
                candidates.append((pos, opp, cost))
        if not candidates:
            self.game.add_log("↩️ Aucune cible à confisquer")
            return
        candidates.sort(key=lambda x: x[0])
        pos, opp, cost = candidates[0]
        if p.money < cost:
            self.game.add_log(f"↩️ {p.name} ne peut pas payer {cost}€")
            return
        opp.properties.remove(pos)
        opp.money += cost
        p.money -= cost
        p.properties.append(pos)
        self.game.owner[pos] = self.game.players.index(p)
        src = self.game.source(pos)
        self.game.add_log(f"⚔️ {p.name} confisque {BOARD[src].name} à {opp.name} ({cost}€)")

    def _card_blocus(self, p: Player):
        opponents = [pl for pl in self.game.players if pl.alive and pl is not p]
        if not opponents:
            self.game.add_log("↩️ Aucune cible")
            return
        if p.is_ai:
            target = max(opponents, key=lambda pl: pl.money)
        else:
            target = self._choose_player_target(opponents, "Blocus — choisir la cible")
            if target is None:
                self.game.add_log("↩️ Blocus annulé")
                return
        target.skip_turns += 1
        self.game.add_log(f"🛑 {p.name} bloque {target.name} (1 tour)")

    def _card_redirect(self, p: Player):
        opponents = [pl for pl in self.game.players if pl.alive and pl is not p]
        if not opponents:
            self.game.add_log("↩️ Aucune cible")
            return
        if p.is_ai:
            target = max(opponents, key=lambda pl: pl.money)
        else:
            target = self._choose_player_target(opponents, "Redirection — choisir la cible")
            if target is None:
                self.game.add_log("↩️ Redirection annulée")
                return
        target.position = 6
        self.game.add_log(f"➡️ {p.name} redirige {target.name} vers CARTE")

    def _card_audit_cross(self, p: Player, amount: int):
        opponents = [pl for pl in self.game.players if pl.alive and pl is not p]
        if not opponents:
            self.game.add_log("↩️ Aucune cible")
            return
        if p.is_ai:
            target = max(opponents, key=lambda pl: pl.money)
        else:
            target = self._choose_player_target(opponents, "Audit croisé — choisir la cible")
            if target is None:
                self.game.add_log("↩️ Audit annulé")
                return
        taken = min(amount, target.money)
        target.money -= taken
        p.money += taken
        self.game.add_log(f"💻 {p.name} détourne {taken}€ de {target.name}")

    # --------------------------------------------------------
    #  Dialogues de sélection
    # --------------------------------------------------------
    def _choose_unowned_street(self, p: Player, discount: int) -> Optional[int]:
        candidates = [i for i, s in enumerate(BOARD)
                      if s.kind == "street" and i not in self.game.owner]
        affordable = [i for i in candidates
                      if BOARD[i].price - BOARD[i].price * discount // 100 <= p.money]
        if not affordable:
            return None
        t = self.theme
        win = tk.Toplevel(self.root)
        win.title("Achat privilégié")
        win.configure(bg=t["panel_bg"])
        win.transient(self.root)
        win.grab_set()
        win.geometry("500x500")
        tk.Label(win, text=f"ACHAT PRIVILÉGIÉ (-{discount}%)",
                 bg=t["panel_bg"], fg=t["accent"],
                 font=("Segoe UI", 14, "bold")).pack(pady=(18, 4))
        tk.Label(win, text=f"Solde : {p.money}€",
                 bg=t["panel_bg"], fg=t["muted"],
                 font=("Segoe UI", 10)).pack(pady=(0, 12))
        wrap = tk.Frame(win, bg=t["panel_bg"])
        wrap.pack(fill="both", expand=True, padx=16)
        canvas = tk.Canvas(wrap, bg=t["panel_bg"], highlightthickness=0)
        sb = tk.Scrollbar(wrap, orient="vertical", command=canvas.yview)
        inner = tk.Frame(canvas, bg=t["panel_bg"])
        inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=inner, anchor="nw")
        canvas.configure(yscrollcommand=sb.set)
        canvas.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")
        result = {"pos": None}
        def choose(i):
            result["pos"] = i
            win.destroy()
        for i in sorted(affordable, key=lambda ii: BOARD[ii].price):
            s = BOARD[i]
            price = s.price - s.price * discount // 100
            row = tk.Frame(inner, bg=t["panel_bg"])
            row.pack(fill="x", pady=1)
            gc = GROUP_COLORS.get(s.group, "#888")
            tk.Label(row, text="■", bg=t["panel_bg"], fg=gc,
                     font=("Segoe UI", 14)).pack(side="left", padx=(2, 8))
            tk.Button(row, text=f"{s.name}  —  {price}€",
                      command=lambda ii=i: choose(ii),
                      bg=t["btn_bg"], fg=t["btn_fg"],
                      activebackground=t["accent"],
                      activeforeground=t["accent_fg"],
                      relief="flat", anchor="w", padx=12, pady=8,
                      cursor="hand2", font=("Segoe UI", 10),
                      bd=0, highlightthickness=0).pack(side="left", fill="x", expand=True)
        tk.Button(win, text="PASSER", command=win.destroy,
                  bg=t["btn_bg"], fg=t["btn_fg"],
                  activebackground=t["btn_act"],
                  activeforeground=t["btn_fg"],
                  relief="flat", padx=20, pady=10, cursor="hand2",
                  font=("Segoe UI", 10, "bold"),
                  bd=0, highlightthickness=0).pack(pady=14)
        win.update_idletasks()
        x = (win.winfo_screenwidth() - 500) // 2
        y = (win.winfo_screenheight() - 500) // 2
        win.geometry(f"500x500+{x}+{y}")
        self.root.wait_window(win)
        return result["pos"]

    def _choose_your_property(self, p: Player, candidates: List[int],
                              title: str) -> Optional[int]:
        t = self.theme
        win = tk.Toplevel(self.root)
        win.title(title)
        win.configure(bg=t["panel_bg"])
        win.transient(self.root)
        win.grab_set()
        win.resizable(False, False)
        tk.Label(win, text=title, bg=t["panel_bg"], fg=t["accent"],
                 font=("Segoe UI", 14, "bold")).pack(padx=24, pady=(18, 12))
        result = {"pos": None}
        def choose(i):
            result["pos"] = i
            win.destroy()
        for pos in candidates:
            src = self.game.source(pos)
            s = BOARD[src]
            h = self.game.houses.get(pos, 0)
            tk.Button(win, text=f"{s.name}  ({h}/3)",
                      command=lambda pp=pos: choose(pp),
                      bg=t["btn_bg"], fg=t["btn_fg"],
                      activebackground=t["accent"],
                      activeforeground=t["accent_fg"],
                      relief="flat", anchor="w", padx=14, pady=8,
                      cursor="hand2", font=("Segoe UI", 10),
                      bd=0, highlightthickness=0,
                      width=30).pack(padx=24, pady=2)
        tk.Button(win, text="ANNULER", command=win.destroy,
                  bg=t["btn_bg"], fg=t["btn_fg"],
                  activebackground=t["btn_act"],
                  activeforeground=t["btn_fg"],
                  relief="flat", padx=20, pady=8, cursor="hand2",
                  font=("Segoe UI", 10),
                  bd=0, highlightthickness=0).pack(pady=(14, 18))
        win.update_idletasks()
        w = 340
        h = win.winfo_height()
        x = (win.winfo_screenwidth() - w) // 2
        y = (win.winfo_screenheight() - h) // 2
        win.geometry(f"{w}x{h}+{x}+{y}")
        self.root.wait_window(win)
        return result["pos"]

    def _choose_player_target(self, candidates: List[Player],
                              title: str) -> Optional[Player]:
        t = self.theme
        win = tk.Toplevel(self.root)
        win.title(title)
        win.configure(bg=t["panel_bg"])
        win.transient(self.root)
        win.grab_set()
        win.resizable(False, False)
        tk.Label(win, text=title, bg=t["panel_bg"], fg=t["accent"],
                 font=("Segoe UI", 13, "bold")).pack(padx=30, pady=(18, 12))
        result = {"target": None}
        def choose(target):
            result["target"] = target
            win.destroy()
        for c in candidates:
            nw = self.game.net_worth(c)
            tk.Button(win, text=f"{c.name}   ·   {c.money}€   ·   Net {nw}€",
                      command=lambda cc=c: choose(cc),
                      bg=t["btn_bg"], fg=t["btn_fg"],
                      activebackground=t["accent"],
                      activeforeground=t["accent_fg"],
                      relief="flat", padx=18, pady=10, cursor="hand2",
                      font=("Segoe UI", 10),
                      bd=0, highlightthickness=0,
                      width=32, anchor="w").pack(padx=24, pady=3)
        tk.Button(win, text="ANNULER", command=win.destroy,
                  bg=t["btn_bg"], fg=t["btn_fg"],
                  activebackground=t["btn_act"],
                  activeforeground=t["btn_fg"],
                  relief="flat", padx=20, pady=8, cursor="hand2",
                  font=("Segoe UI", 10),
                  bd=0, highlightthickness=0).pack(pady=(14, 18))
        win.update_idletasks()
        w = 360
        h = win.winfo_height()
        x = (win.winfo_screenwidth() - w) // 2
        y = (win.winfo_screenheight() - h) // 2
        win.geometry(f"{w}x{h}+{x}+{y}")
        self.root.wait_window(win)
        return result["target"]

    def _choose_target_property(self, candidates, title: str):
        t = self.theme
        win = tk.Toplevel(self.root)
        win.title(title)
        win.configure(bg=t["panel_bg"])
        win.transient(self.root)
        win.grab_set()
        win.resizable(False, False)
        tk.Label(win, text=title, bg=t["panel_bg"], fg=t["accent"],
                 font=("Segoe UI", 13, "bold")).pack(padx=30, pady=(18, 4))
        tk.Label(win, text="Choisir la propriété visée",
                 bg=t["panel_bg"], fg=t["muted"],
                 font=("Segoe UI", 10)).pack(pady=(0, 12))
        result = {"r": None}
        def choose(r):
            result["r"] = r
            win.destroy()
        candidates_sorted = sorted(
            candidates,
            key=lambda x: -BOARD[self.game.source(x[0]) or x[0]].price
        )
        for (pos, opp, cost) in candidates_sorted:
            src = self.game.source(pos) or pos
            name = BOARD[src].name
            text = f"{name}  ·  {opp.name}  ·  {cost}€"
            tk.Button(win, text=text,
                      command=lambda r=(pos, opp, cost): choose(r),
                      bg=t["btn_bg"], fg=t["btn_fg"],
                      activebackground=t["accent"],
                      activeforeground=t["accent_fg"],
                      relief="flat", padx=18, pady=8, cursor="hand2",
                      font=("Segoe UI", 10), anchor="w",
                      bd=0, highlightthickness=0,
                      width=36).pack(padx=24, pady=2)
        tk.Button(win, text="ANNULER", command=win.destroy,
                  bg=t["btn_bg"], fg=t["btn_fg"],
                  activebackground=t["btn_act"],
                  activeforeground=t["btn_fg"],
                  relief="flat", padx=20, pady=8, cursor="hand2",
                  font=("Segoe UI", 10),
                  bd=0, highlightthickness=0).pack(pady=(14, 18))
        win.update_idletasks()
        w = 420
        h = win.winfo_height()
        x = (win.winfo_screenwidth() - w) // 2
        y = (win.winfo_screenheight() - h) // 2
        win.geometry(f"{w}x{h}+{x}+{y}")
        self.root.wait_window(win)
        return result["r"]

    # --------------------------------------------------------
    #  Terrain libre
    # --------------------------------------------------------
    def _handle_libre(self, p: Player, pos: int):
        candidates = [i for i, s in enumerate(BOARD)
                      if s.kind == "street" and s.price <= p.money]
        if not candidates:
            self.game.add_log(f"❌ {p.name} : rien à copier")
            return
        if p.is_ai:
            candidates.sort(key=lambda i: -BOARD[i].price)
            src = candidates[0]
            self.game.buy(p, pos, src)
            self.game.add_log(f"🏷️ {p.name} copie {BOARD[src].name} ({BOARD[src].price}€)")
        else:
            src = self._open_copy_dialog(p, pos, candidates)
            if src is not None:
                self.game.buy(p, pos, src)
                self.game.add_log(f"🏷️ {p.name} copie {BOARD[src].name} ({BOARD[src].price}€)")
            else:
                self.game.add_log(f"↩️ {p.name} passe")

    def _ask_buy(self, p: Player, pos: int, price: int, real_src: int):
        t = self.theme
        win = tk.Toplevel(self.root)
        win.title("Achat")
        win.configure(bg=t["panel_bg"])
        win.transient(self.root)
        win.grab_set()
        win.resizable(False, False)
        tk.Label(win, text=BOARD[real_src].name, bg=t["panel_bg"], fg=t["accent"],
                 font=("Segoe UI", 16, "bold")).pack(padx=30, pady=(20, 6))
        tk.Label(win, text=f"Prix : {price}€\nSolde : {p.money}€",
                 bg=t["panel_bg"], fg=t["fg"],
                 font=("Segoe UI", 12)).pack(padx=30, pady=(0, 8))
        rent0 = self.game.rent_at_houses(pos, 0)
        tk.Label(win, text=f"Loyer de base : {rent0}€",
                 bg=t["panel_bg"], fg=t["muted"],
                 font=("Segoe UI", 10)).pack(padx=30, pady=(0, 14))
        result = {"buy": False}
        def yes():
            result["buy"] = True
            win.destroy()
        row = tk.Frame(win, bg=t["panel_bg"])
        row.pack(padx=30, pady=(0, 20))
        tk.Button(row, text="ACHETER", command=yes,
                  bg=t["accent"], fg=t["accent_fg"],
                  activebackground=t["btn_act"],
                  activeforeground=t["accent_fg"],
                  relief="flat", padx=22, pady=10, cursor="hand2",
                  font=("Segoe UI", 11, "bold"),
                  bd=0, highlightthickness=0).pack(side="left", padx=4)
        tk.Button(row, text="PASSER", command=win.destroy,
                  bg=t["btn_bg"], fg=t["btn_fg"],
                  activebackground=t["btn_act"],
                  activeforeground=t["btn_fg"],
                  relief="flat", padx=22, pady=10, cursor="hand2",
                  font=("Segoe UI", 11),
                  bd=0, highlightthickness=0).pack(side="left", padx=4)
        win.update_idletasks()
        w = 340
        h = win.winfo_height()
        x = (win.winfo_screenwidth() - w) // 2
        y = (win.winfo_screenheight() - h) // 2
        win.geometry(f"{w}x{h}+{x}+{y}")
        self.root.wait_window(win)
        if result["buy"]:
            self.game.buy(p, pos)
            self.game.add_log(f"🏷️ {p.name} achète {BOARD[real_src].name} ({price}€)")
            self.refresh()

    def _open_copy_dialog(self, p: Player, pos: int,
                          candidates: List[int]) -> Optional[int]:
        t = self.theme
        win = tk.Toplevel(self.root)
        win.title("Terrain Libre — Copier")
        win.configure(bg=t["panel_bg"])
        win.transient(self.root)
        win.grab_set()
        win.geometry("500x600")
        tk.Label(win, text="TERRAIN LIBRE", bg=t["panel_bg"], fg=t["accent"],
                 font=("Segoe UI", 16, "bold")).pack(pady=(18, 4))
        tk.Label(win, text=f"Copier une propriété  ·  {p.money}€ dispo",
                 bg=t["panel_bg"], fg=t["muted"],
                 font=("Segoe UI", 10)).pack(pady=(0, 12))
        wrap = tk.Frame(win, bg=t["panel_bg"])
        wrap.pack(fill="both", expand=True, padx=16)
        canvas = tk.Canvas(wrap, bg=t["panel_bg"], highlightthickness=0)
        sb = tk.Scrollbar(wrap, orient="vertical", command=canvas.yview)
        inner = tk.Frame(canvas, bg=t["panel_bg"])
        inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=inner, anchor="nw")
        canvas.configure(yscrollcommand=sb.set)
        canvas.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")
        result = {"src": None}
        def choose(i):
            result["src"] = i
            win.destroy()
        def sort_key(i):
            s = BOARD[i]
            return (s.group or "zzz", s.price)
        for i in sorted(candidates, key=sort_key):
            s = BOARD[i]
            row = tk.Frame(inner, bg=t["panel_bg"])
            row.pack(fill="x", pady=1)
            gc = GROUP_COLORS.get(s.group, "#888")
            tk.Label(row, text="■", bg=t["panel_bg"], fg=gc,
                     font=("Segoe UI", 14)).pack(side="left", padx=(2, 8))
            tk.Button(row, text=f"{s.name}   —   {s.price}€",
                      command=lambda ii=i: choose(ii),
                      bg=t["btn_bg"], fg=t["btn_fg"],
                      activebackground=t["accent"],
                      activeforeground=t["accent_fg"],
                      relief="flat", anchor="w",
                      padx=12, pady=8, cursor="hand2",
                      font=("Segoe UI", 10),
                      bd=0, highlightthickness=0).pack(side="left", fill="x", expand=True)
        tk.Button(win, text="PASSER", command=win.destroy,
                  bg=t["btn_bg"], fg=t["btn_fg"],
                  activebackground=t["btn_act"],
                  activeforeground=t["btn_fg"],
                  relief="flat", padx=20, pady=10, cursor="hand2",
                  font=("Segoe UI", 10, "bold"),
                  bd=0, highlightthickness=0).pack(pady=14)
        win.update_idletasks()
        x = (win.winfo_screenwidth() - 500) // 2
        y = (win.winfo_screenheight() - 600) // 2
        win.geometry(f"500x600+{x}+{y}")
        self.root.wait_window(win)
        return result["src"]

    # --------------------------------------------------------
    #  Construction
    # --------------------------------------------------------
    def _open_build_dialog(self, p: Player):
        buildable = []
        for pos in p.properties:
            src = self.game.source(pos)
            if src is None or BOARD[src].kind != "street":
                continue
            if self.game.houses.get(pos, 0) >= 3:
                continue
            cost = self.game.house_cost(pos)
            if p.money < cost:
                continue
            buildable.append((pos, BOARD[src].name, cost,
                              self.game.houses.get(pos, 0)))
        if not buildable:
            messagebox.showinfo(
                "Construction",
                "Aucune construction possible.\n\n"
                "• posséder une rue,\n"
                "• moins de 3 maisons dessus,\n"
                "• assez d'argent.",
                parent=self.root)
            return
        t = self.theme
        win = tk.Toplevel(self.root)
        win.title("Construire")
        win.configure(bg=t["panel_bg"])
        win.transient(self.root)
        win.grab_set()
        win.resizable(False, False)
        tk.Label(win, text="CONSTRUIRE", bg=t["panel_bg"], fg=t["accent"],
                 font=("Segoe UI", 16, "bold")).pack(padx=30, pady=(20, 4))
        tk.Label(win, text=f"Solde : {p.money}€", bg=t["panel_bg"], fg=t["fg"],
                 font=("Segoe UI", 11)).pack(pady=(0, 12))
        def do_build(pos):
            if self.game.build_house(p, pos):
                src = self.game.source(pos)
                self.game.add_log(f"🏠 {p.name} bâtit sur {BOARD[src].name} "
                                  f"({self.game.house_cost(pos)}€)")
                win.destroy()
                self.refresh()
        for pos, name, cost, houses in buildable:
            row = tk.Frame(win, bg=t["panel_bg"])
            row.pack(fill="x", padx=20, pady=2)
            current_rent = self.game.rent_at_houses(pos, houses)
            next_rent = self.game.rent_at_houses(pos, houses + 1)
            info = tk.Frame(row, bg=t["panel_bg"])
            info.pack(side="left", fill="x", expand=True, anchor="w")
            tk.Label(info, text=f"{name}  ({houses}/3)",
                     bg=t["panel_bg"], fg=t["fg"],
                     font=("Segoe UI", 10), anchor="w").pack(anchor="w")
            tk.Label(info, text=f"Loyer : {current_rent}€ → {next_rent}€",
                     bg=t["panel_bg"], fg=t["muted"],
                     font=("Segoe UI", 9), anchor="w").pack(anchor="w")
            tk.Button(row, text=f"+1 — {cost}€",
                      command=lambda pp=pos: do_build(pp),
                      bg=t["accent"], fg=t["accent_fg"],
                      activebackground=t["btn_act"],
                      activeforeground=t["accent_fg"],
                      relief="flat", padx=12, pady=6, cursor="hand2",
                      font=("Segoe UI", 10, "bold"),
                      bd=0, highlightthickness=0).pack(side="right")
        tk.Button(win, text="Fermer", command=win.destroy,
                  bg=t["btn_bg"], fg=t["btn_fg"],
                  activebackground=t["btn_act"],
                  activeforeground=t["btn_fg"],
                  relief="flat", padx=20, pady=8, cursor="hand2",
                  font=("Segoe UI", 10),
                  bd=0, highlightthickness=0).pack(pady=16)
        win.update_idletasks()
        w = 460
        h = win.winfo_height()
        x = (win.winfo_screenwidth() - w) // 2
        y = (win.winfo_screenheight() - h) // 2
        win.geometry(f"{w}x{h}+{x}+{y}")

    # --------------------------------------------------------
    #  Fin de tour / IA — CENTRALISÉ v7
    # --------------------------------------------------------
    def _end_turn(self):
        if self.game is None or self.game.game_over:
            return

        # === Point unique : l'IA joue sa main AVANT de passer le tour ===
        current = self.game.current_player()
        if current.is_ai and current.hand:
            self._play_ai_hand(current)

        winner = self.game.check_goal()
        if winner is not None:
            self.game.game_over = True
            self.game.winner = winner
            self.game.winning_team = winner.team
            self._end_game_natural()
            return

        if self.game.turn_count >= self.game.max_turns:
            self._end_by_turns()
            return

        self.game.next_turn()

        # Gestion des skips
        safety = 0
        p = self.game.current_player()
        while p.skip_turns > 0 and p.alive and safety < 8:
            p.skip_turns -= 1
            self.game.add_log(f"⏸️ {p.name} paralysé, tour sauté")
            self.game.next_turn()
            p = self.game.current_player()
            safety += 1
        if safety >= 8:
            self.game.add_log("⚠️ Blocage détecté, passage forcé")

        self.game.add_log(f"─── Tour {self.game.turn_count} · {p.name} ───")
        self.refresh()

        winner = self.game.check_goal()
        if winner is not None:
            self.game.game_over = True
            self.game.winner = winner
            self.game.winning_team = winner.team
            self._end_game_natural()
            return

        if self.game.turn_count >= self.game.max_turns:
            self._end_by_turns()
            return

        self._maybe_auto_play()

    def _play_ai_hand(self, p: Player):
        """Joue toutes les cartes de la main du bot (robuste aux exceptions)."""
        if not p.hand:
            return
        self.game.add_log(f"🤖 {p.name} active {len(p.hand)} carte(s)")
        safety = 0
        while p.hand and safety < 20:
            card = p.hand.pop(0)
            self.game.add_log(f"⚡ {p.name} joue : {card.name}")
            try:
                self._resolve_card(p, card)
            except Exception as e:
                self.game.add_log(f"⚠️ Erreur carte {card.name} : {e}")
            safety += 1
        self.refresh()

    def _maybe_auto_play(self):
        if self.game is None or self.game.game_over:
            if self.game is not None and self.game.game_over:
                self._end_game_natural()
            return
        p = self.game.current_player()
        if p.is_ai:
            self._schedule(0.8, self._do_roll)

    # --------------------------------------------------------
    #  Fin de partie
    # --------------------------------------------------------
    def _end_game_natural(self):
        if self.game is None:
            return
        w = self.game.winner
        if w is None:
            self._final_end(None)
            return
        if w.team > 0:
            team_winners = [p for p in self.game.players
                            if p.team == w.team and p.alive]
            names = ", ".join(p.name for p in team_winners)
            msg = (f"🏆 Équipe {w.team} gagne !\n"
                   f"Membres : {names}\n"
                   f"Meilleur : {w.name} avec {self.game.net_worth(w)}€ "
                   f"(tour {self.game.turn_count})")
        else:
            msg = (f"🏆 {w.name} atteint {self.game.net_worth(w)}€ nets\n"
                   f"Victoire au tour {self.game.turn_count}.")
        self.game.add_log("═══ OBJECTIF ATTEINT ═══")
        self.game.add_log(msg)
        self.refresh()

        if self.game.max_turns < EXTENDED_MAX_TURNS and not self.game.extended:
            extend = messagebox.askyesno(
                "Continuer ?",
                f"{msg}\n\n"
                f"Continuer jusqu'à {EXTENDED_MAX_TURNS} tours ?\n"
                f"(nouvel objectif : {self.game.target * 2}€)",
                parent=self.root)
            if extend:
                self._extend_game()
                return
        self._final_end(w)

    def _end_by_turns(self):
        if self.game is None:
            return
        self.game.game_over = True
        best = max(self.game.players,
                   key=lambda p: self.game.net_worth(p) if p.alive else -1)
        self.game.winner = best
        msg = (f"⏱️ Limite de {self.game.max_turns} tours atteinte.\n\n"
               f"🏆 {best.name} remporte la partie\n"
               f"avec {self.game.net_worth(best)}€ nets.")
        self.game.add_log("═══ LIMITE DE TOURS ═══")
        self.game.add_log(msg)
        self.refresh()

        if self.game.max_turns < EXTENDED_MAX_TURNS:
            extend = messagebox.askyesno(
                "Continuer ?",
                f"{msg}\n\n"
                f"Continuer jusqu'à {EXTENDED_MAX_TURNS} tours ?",
                parent=self.root)
            if extend:
                self._extend_game()
                return
        self._final_end(best)

    def _extend_game(self):
        if self.game is None:
            return
        self.game.max_turns = EXTENDED_MAX_TURNS
        self.game.target = self.game.target * 2
        self.game.extended = True
        self.game.game_over = False
        self.game.winner = None
        self.game.winning_team = 0
        self.game.add_log(f"⏩ PROLONGATION : {EXTENDED_MAX_TURNS} tours, "
                          f"objectif {self.game.target}€")
        self.refresh()
        self._maybe_auto_play()

    def _final_end(self, winner: Optional[Player]):
        if self.game is None:
            return
        self.game.game_over = True
        if winner is None:
            msg = "Partie terminée. Aucun survivant."
        else:
            nw = self.game.net_worth(winner)
            if winner.team > 0:
                msg = f"🏆 Équipe {winner.team} remporte la partie\n" \
                      f"({winner.name}, {nw}€ nets)"
            else:
                msg = f"🏆 {winner.name} remporte la partie\n" \
                      f"({nw}€ nets)"
        self.game.add_log("═══ FIN DE PARTIE ═══")
        self.game.add_log(msg)
        self.refresh()

        export = messagebox.askyesno(
            "Fin de partie",
            f"{msg}\n\nExporter le journal de la partie ?",
            parent=self.root)
        if export:
            self.export_game()
        self.show_menu()

    # --------------------------------------------------------
    #  Export
    # --------------------------------------------------------
    def export_game(self):
        if self.game is None:
            messagebox.showinfo("Export", "Aucune partie à exporter.",
                                parent=self.root)
            return
        default_name = f"darkmonopoly_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        path = filedialog.asksaveasfilename(
            parent=self.root,
            title="Exporter le journal de la partie",
            defaultextension=".txt",
            initialfile=default_name,
            filetypes=[("Fichiers texte", "*.txt"), ("Tous", "*.*")])
        if not path:
            return
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write("=" * 60 + "\n")
                f.write("DARKMONOPOLY v7.0 — Journal de partie\n")
                f.write("=" * 60 + "\n\n")
                f.write(f"Date : {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Mode : {'PvP local' if self.game.pvp_mode else 'Solo/Mixte'}\n")
                f.write(f"Tours joués : {self.game.turn_count}\n")
                f.write(f"Objectif : {self.game.target}€\n\n")

                f.write("JOUEURS\n")
                f.write("-" * 40 + "\n")
                for p in self.game.players:
                    status = "vivant" if p.alive else "FAILLITE"
                    team = f" [Équipe {p.team}]" if p.team > 0 else ""
                    nw = self.game.net_worth(p)
                    f.write(f"  {p.name}{team} : {p.money}€ cash, "
                            f"{nw}€ net, {len(p.properties)} propriétés, "
                            f"{len(p.hand)} cartes, {status}\n")
                f.write("\n")

                f.write("JOURNAL COMPLET\n")
                f.write("-" * 40 + "\n")
                for line in self.game.log:
                    f.write(line + "\n")
                f.write("\n")

                if self.game.drawn_history:
                    f.write("CARTES PIOCHÉES\n")
                    f.write("-" * 40 + "\n")
                    for c in self.game.drawn_history:
                        f.write(f"  [{CAT_LABELS[c.category]}] {c.name}\n")

            messagebox.showinfo("Export", f"Journal exporté vers :\n{path}",
                                parent=self.root)
        except Exception as e:
            messagebox.showerror("Export", f"Erreur lors de l'export :\n{e}",
                                 parent=self.root)

    # --------------------------------------------------------
    #  Aide
    # --------------------------------------------------------
    def show_rules(self):
        t = self.theme
        win = tk.Toplevel(self.root)
        win.title("Règles — v7.0")
        win.configure(bg=t["panel_bg"])
        win.transient(self.root)
        win.geometry("640x760")
        tk.Label(win, text="RÈGLES · v7.0",
                 bg=t["panel_bg"], fg=t["accent"],
                 font=("Segoe UI", 15, "bold")).pack(pady=(18, 12))
        txt = tk.Text(win, bg=t["log_bg"], fg=t["log_fg"],
                      font=("Consolas", 10), wrap="word",
                      relief="flat", padx=20, pady=14,
                      bd=0, highlightthickness=0)
        txt.pack(fill="both", expand=True, padx=16, pady=(0, 16))
        content = (
            "OBJECTIF\n════════\n"
            "Premier à 2500€ de patrimoine net.\n"
            "Limite : 40 tours. Sinon, plus haut patrimoine gagne.\n"
            "→ Prolongation possible jusqu'à 100 tours (objectif ×2).\n\n\n"

            "MODES\n══════\n"
            "• Solo — 1 humain vs IA\n"
            "• PvP local — 2-4 humains sur le même PC\n"
            "• Duel 2v2 — 2 équipes\n"
            "• Coop — 2 humains vs 2 IA\n\n"
            "En PvP, TOUTES les mains sont visibles en bas.\n"
            "En Solo, seule la main de l'humain est visible ;\n"
            "celle des IA reste cachée.\n\n\n"

            "MODE INVESTISSEUR\n═════════════════\n"
            "Chaque joueur incarne une entreprise.\n"
            "Pas de monopole. Construis librement sur tes rues.\n"
            "Max 3 maisons par case.\n\n"
            "Loyers :\n"
            "  0 maison : prix ÷ 10\n"
            "  1 maison : prix ÷ 3\n"
            "  2 maisons : 3 × prix ÷ 5\n"
            "  3 maisons : prix complet\n"
            "Coût maison : prix ÷ 2\n\n\n"

            "PREMIER TOUR\n═════════════\n"
            "Aucun loyer pendant ton premier tour.\n\n\n"

            "CARTES & MAIN\n══════════════\n"
            "3 cases CARTE (⚡). Deck déterministe.\n"
            "Les cartes piochées vont dans ta MAIN.\n"
            "Tu peux les garder et les jouer plus tard.\n\n"
            "Effets :\n"
            "  ■ INVESTISSEMENT — cash, achats réduits, maisons\n"
            "  ■ PRISE — vols, blocus, acquisitions\n"
            "  ■ ARGENT — bonus, héritages, amendes\n\n\n"

            "INFOS DES CASES\n════════════════\n"
            "Clic sur une case : prix, loyers à chaque palier,\n"
            "coût d'amélioration, propriétaire, projection.\n"
            "Cadre contrasté autour = terrain libre.\n\n\n"

            "EXPORT\n══════\n"
            "Fichier → Exporter la partie (Ctrl+E)\n\n"
        )
        txt.insert("1.0", content)
        txt.configure(state="disabled")
        tk.Button(win, text="Fermer", command=win.destroy,
                  bg=t["accent"], fg=t["accent_fg"],
                  activebackground=t["btn_act"],
                  activeforeground=t["accent_fg"],
                  relief="flat", padx=24, pady=8, cursor="hand2",
                  font=("Segoe UI", 10, "bold"),
                  bd=0, highlightthickness=0).pack(pady=(0, 16))
        win.update_idletasks()
        x = (win.winfo_screenwidth() - 640) // 2
        y = (win.winfo_screenheight() - 760) // 2
        win.geometry(f"640x760+{x}+{y}")

    def show_about(self):
        messagebox.showinfo(
            "À propos",
            "DarkMonopoly PC v7.0\n\n"
            "Fix IA cartes · Mains publiques PvP\n"
            "Thème clair contrasté · Export\n\n"
            "Python + Tkinter · Sans dépendances.",
            parent=self.root)


# ============================================================
#  MAIN
# ============================================================

def main():
    root = tk.Tk()
    app = DarkMonopolyApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()