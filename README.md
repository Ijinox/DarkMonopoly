# DarkMonopoly

> Un Monopoly classique européen, jouable hors-ligne, en un seul fichier Python — pensé comme un **laboratoire d'expériences de pensée économiques**.  
> Le but à terme : bidouiller les règles du Monopoly pour tester des modèles réalistes (inflation, UBI, taxe foncière, marché noir, corruption, crypto…).

![statut](https://img.shields.io/badge/statut-prototype-orange)
![python](https://img.shields.io/badge/python-3.10%2B-blue)
![license](https://img.shields.io/badge/license-MIT-green)
![plateforme](https://img.shields.io/badge/plateforme-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)

---

## 🎯 Vision

**DarkMonopoly** n'est pas « juste » un Monopoly. C'est un bac à sable pour :

- simuler des **modèles économiques alternatifs** (UBI, taxe foncière, monnaie parallèle, marchés noirs) ;
- observer l'émergence de **dynamiques réalistes** : inflation, concentration du capital, inégalités (Gini), faillites en chaîne ;
- laisser le joueur (ou une IA) **exploiter des failles** du règlement — comme un hacker qui cherche à comprendre un système en le cassant.

Le projet est développé de manière **itérative et minimaliste** : un seul fichier, des dépendances quasi nulles, un prototype jouable à chaque commit.

---

## ✨ État actuel — v1

- ✅ Monopoly classique **édition européenne / française** (40 cases, noms FR)
- ✅ 2 à 4 joueurs — 1 humain + IA (achètent avec marge de sécurité)
- ✅ Dés, doubles (3 doubles → prison), prison (payer 50 €)
- ✅ Achats, loyers (×2 si monopole, gares dégressives, compagnies ×4/×10)
- ✅ Construction de maisons (max 5, règle d'égalité approximative)
- ✅ Hypothèque automatique + faillite avec transfert de patrimoine
- ✅ Cartes **Chance** et **Caisse de Communauté**
- ✅ **4 thèmes graphiques** : Clair, Sombre, Nuit Bleu, Nuit Rouge — changeables en direct
- ✅ Journal de partie intégré

---

## 🗺️ Feuille de route

| Version | Contenu prévu |
|---------|---------------|
| **v1.x** | Corrections de bugs, IA plus fine, sauvegarde JSON |
| **v2**   | Module **hack** : falsifier un titre, détourner un loyer, injecter de la monnaie, détection/risque |
| **v2.x** | Métriques économiques : Gini, masse monétaire, inflation |
| **v3**   | Panneau « Dark Rules » : activer/désactiver UBI, taxe foncière, crypto, corruption |
| **v3.x** | Agents IA avancés, négociation, coalitions |
| **v4**   | Mode simulation automatique (headless) + export des résultats |

---

## 🚀 Installation & lancement

### Prérequis

- **Python 3.10 ou supérieur** (obligatoire pour `dataclasses` + typage `List[int]`)
- **Tkinter** (inclus par défaut dans l'installateur Windows et la plupart des distributions Linux)
- Aucune autre dépendance externe.

### Étapes

```bash
git clone https://github.com/<ton-pseudo>/DarkMonopoly.git
cd DarkMonopoly
python darkmonopoly.py
```

> Sur Windows 11, tu peux aussi double-cliquer sur `darkmonopoly.py` après avoir associé le `.py` à `python.exe`.

### Vérification de Tkinter

```bash
python -c "import tkinter; print(tkinter.TkVersion)"
```

Si une erreur apparaît sous Linux :

```bash
sudo apt install python3-tk
```

---

## 🎮 Comment jouer

1. Au démarrage, choisis le **nombre de joueurs** (2 à 4).
   - **Joueur 1** = toi (humain).
   - **Joueurs 2, 3, 4** = IA.
2. Clique sur **🎲 Lancer les dés**.
   - Propriété libre → dialogue d'achat.
   - Propriété adverse → loyer payé automatiquement.
   - Chance / Caisse → carte tirée automatiquement.
3. Clique sur **✔ Terminer le tour** (sauf si tu fais un double : tu rejoues).
4. **🏠 Construire une maison** est actif en fin de tour si tu as un monopole de couleur et assez d'argent.
5. Change de thème à tout moment via la barre du haut.

---

## 🖼️ Thèmes

| Nom | Description |
|-----|-------------|
| **Clair** | Fond clair, texte sombre — proche du Monopoly papier |
| **Sombre** | Fond gris foncé, contrastes doux — pour la nuit |
| **Nuit Bleu** | Ambiance cyber / terminal, dominante bleue |
| **Nuit Rouge** | Ambiance alerte / hack, dominante rouge |

Le thème par défaut est **Nuit Bleu**.

---

## 🧱 Architecture

Le projet est volontairement **mono-fichier** (`darkmonopoly.py`) :

```
darkmonopoly.py
├── DONNÉES
│   ├── SQUARES           # les 40 cases du plateau
│   ├── CHANCE_CARDS      # cartes Chance
│   ├── CHEST_CARDS       # cartes Caisse de Communauté
│   ├── GROUP_COLORS      # couleurs des groupes de rues
│   ├── GROUP_HOUSE_COST  # coût de construction par groupe
│   └── THEMES            # 4 palettes graphiques
├── MODÈLE
│   ├── Player            # un joueur
│   └── Game              # moteur de jeu (état + règles + tours)
└── UI
    └── DarkMonopolyApp   # interface Tkinter
```

Aucune dépendance externe. Aucun package à installer. Un seul fichier à copier pour lancer le jeu.

---

## 🛠️ Contribuer

Les contributions sont bienvenues, surtout sur :

- les **règles économiques alternatives** (UBI, taxe foncière progressive, marché noir…) ;
- les **agents IA** (heuristiques, minimax, RL) ;
- les **métriques** (Gini, inflation, masse monétaire, vélocité) ;
- l'**internationalisation** (README + interface en anglais).

Voir [`CONTRIBUTING.md`](CONTRIBUTING.md) pour le détail du workflow.

---

## 🐛 Signaler un bug

Ouvre une **issue** en utilisant le template prévu à cet effet. Inclus :

- ta version de Python (`python --version`) ;
- ton OS (Windows / Linux / macOS) ;
- une **capture** ou le **message d'erreur exact** ;
- la **seed** ou la séquence d'actions qui a déclenché le bug si possible.

---

## 📜 Licence

Distribué sous licence **MIT**. Voir [`LICENSE`](LICENSE).

---

## ⚠️ Avertissement

DarkMonopoly est un **projet éducatif et expérimental**.  
Il ne prétend pas modéliser fidèlement une économie réelle, ni fournir de conseil financier, économique ou politique.  
Les « failles » du jeu sont des **métaphores pédagogiques**, pas des incitations à quoi que ce soit dans la vie réelle.

---

## 👤 Auteur

**Adrian** — développeur indépendant.  
Projet né d'une envie de faire de l'**expérience de pensée économique** en s'amusant avec un Monopoly qu'on peut casser.

> « Le Monopoly est un jeu où l'on apprend vite que le hasard et la rente valent mieux que le travail. DarkMonopoly, c'est voir ce qu'on peut en faire quand on triche avec le règlement. »

---


Voici la description prête à copier-coller dans un **GitHub Release** (ou en haut du README). Je l'ai écrite dans le format standard des releases GitHub.

---

# 🌃 DarkMonopoly v7.0 — Mains publiques en PvP

**Date de sortie :** Octobre 2026
**Compatibilité :** Python 3.10+ · Windows / Linux / macOS
**Type :** Release majeure (correctifs + nouvelles fonctionnalités)

---

## 📖 À propos

**DarkMonopoly** est un laboratoire d'expériences économiques sous forme de Monopoly modifiable. Chaque joueur incarne une entreprise, le monopole est aboli, et les cartes Cheat permettent de hacker le système pour tester des modèles économiques alternatifs.

Prototype en un seul fichier Python. Aucune dépendance externe.

---

## ✨ Nouveautés v7.0

### 🎴 Mains publiques en mode PvP

Quand tous les joueurs sont humains (mode PvP local), **toutes les mains sont affichées** en bas du plateau. Une ligne par joueur, avec sa couleur, son nombre de cartes et ses cartes visibles.

- **Mode Solo/Mixte** : seule la main de l'humain courant reste visible. Les cartes des IA sont cachées.
- **Mode PvP** : transparence totale — utile pour jouer à plusieurs sur un même PC.
- **Clic sur une carte** (ligne du joueur courant uniquement) → popup d'activation ou de conservation.

### 🎨 Thème "Clair" retravaillé

Le thème clair manquait de contraste. Les boutons passent d'un gris pastel à un **gris franc** (`#d1d5db`), avec bordures renforcées (`#94a3b8`). Le cadre des terrains libres devient foncé (`#1f2937`) pour rester lisible sur fond blanc.

### 🧠 Refonte du système de cartes IA

La gestion des cartes est maintenant **centralisée** dans `_end_turn()`, point unique de passage garanti pour tous les joueurs.

---

## 🐛 Correctifs

### Bug critique : blocage sur case CARTE (IA)

**Symptôme** : un bot tombait sur une case CARTE, piochait, mais ne jouait jamais sa main. Les cartes s'accumulaient. Dans certains cas (double + 3 doubles d'affilée), le jeu se figeait complètement.

**Cause** : la résolution des cartes IA était éparpillée dans plusieurs méthodes avec des `return` prématurés qui court-circuitaient l'appel de fin.

**Correctif** :
- Nouvelle méthode `_play_ai_hand()` appelée **uniquement** depuis `_end_turn()`
- `try/except` sur chaque effet de carte → aucune exception ne peut plus figer le jeu
- `refresh()` systématique après chaque pioche (IA incluse)
- Suppression de l'ancienne logique redondante `_ai_play_cards_then_end()`

### Bug secondaire : absence de feedback visuel

Lorsqu'un bot piochait une carte, rien ne bougeait à l'écran. Maintenant, `refresh()` est appelé immédiatement après chaque pioche.

---

## 🔧 Notes techniques

| Aspect | Détail |
|---|---|
| **Fichier unique** | `darkmonopoly_v7.py` (~2700 lignes) |
| **Dépendances** | Aucune (Tkinter inclus dans Python) |
| **Architecture** | Modèle (Game/Player) · Vue (Canvas) · Contrôleur (boutons/clavier) |
| **Déterminisme** | Deck mélangé une seule fois avec un RNG dédié (`random.Random(seed)`) |
| **Reproductibilité** | Même seed → mêmes dés, mêmes cartes |
| **Protection callbacks** | `session_id` invalide les callbacks fantômes |
| **Hauteur dynamique** | Le panneau main s'adapte au nombre de joueurs en PvP |

---

## 🎮 Modes de jeu disponibles

| Mode | Description |
|---|---|
| **Solo** | 1 humain vs 2-3 IA |
| **PvP local** | 2 à 4 humains sur le même PC (mains publiques) |
| **Duel 2v2** | 2 équipes de 2 humains |
| **Coop** | 2 humains vs 2 IA (équipes) |

---

## ⚙️ Règles principales

- **Objectif** : premier à 2500€ de patrimoine net (extensible à 100 tours / objectif 5000€)
- **Mode Investisseur** : pas de monopole, constructions libres, max 3 maisons par case
- **Premier tour** : aucun loyer pendant le premier tour de chaque joueur
- **Terrains Libres** : possibilité de copier une propriété existante en payant son prix
- **3 doubles** : envoi forcé sur la case CARTE et perte du tour

---

## 🚀 Installation

```bash
# Cloner le dépôt
git clone https://github.com/Ijinox/DarkMonopoly.git
cd DarkMonopoly

# Lancer (aucune dépendance à installer)
python darkmonopoly_v7.py
```

**Raccourcis clavier :**
- `Espace` → Lancer les dés
- `Entrée` → Terminer le tour
- `B` → Construire
- `I` → Info case survolée
- `F1` → Règles
- `Ctrl+E` → Exporter le journal
- `Ctrl+N` → Nouvelle partie
- `Échap` → Retour au menu

---

## ⚠️ Limitations connues

- **PvP local** : pas de système "passe le clavier". Les dialogues s'affichent à tour de rôle sans vérification. Chaque joueur doit faire attention à ne pas cliquer pour les autres.
- **Pas de sauvegarde de partie** (l'export se limite au journal texte).
- **IA basique** : prend ses décisions de manière déterministe (pas de stratégie adaptative).
- **Rendu naïf** : le plateau est redessiné intégralement à chaque changement d'état. Fluide pour 24 cases, mais non optimisé pour un plateau plus grand.

---

## 🗺️ Feuille de route v8+

- [ ] Sauvegarde / chargement de partie en JSON
- [ ] IA personnalisables (agressive / prudente / opportuniste)
- [ ] Métriques de fin (Gini, inflation, concentration)
- [ ] Mode "passe le clavier" pour le vrai PvP local
- [ ] Statistiques post-partie avec courbes
- [ ] Version web (PWA) pour mobile

---

## 🧪 Testé sur

- Windows 11 · Python 3.12
- Linux Ubuntu 24.04 · Python 3.11
- Tkinter 8.6+

---

## 📜 Licence

MIT — voir [`LICENSE`](LICENSE)

---

## 👤 Auteur

**Adrian Daniel ANTONIAK** ([@Ijinox](https://github.com/Ijinox))

Projet né d'une envie de faire de l'expérience de pensée économique en s'amusant avec un Monopoly qu'on peut casser.

> *"Le Monopoly est un jeu où l'on apprend vite que le hasard et la rente valent mieux que le travail. DarkMonopoly, c'est voir ce qu'on peut en faire quand on triche avec le règlement."*

---

## 🙏 Contribuer

Les retours, idées et Pull Requests sont bienvenus. Voir [`CONTRIBUTING.md`](CONTRIBUTING.md) pour le workflow.

**Signaler un bug** → ouvrir une issue avec le template dédié (version Python, OS, étapes de reproduction).

---

**Changelog complet** : voir [`CHANGELOG.md`](CHANGELOG.md)

---

### 🏷️ Tags

`python` `tkinter` `game` `simulation` `economy` `serious-game` `open-source` `monopoly` `pvp` `strategy`

---

Tu peux copier ce texte directement :

- **Comme GitHub Release** : va dans `Releases → Draft a new release`, colle le contenu, coche "Set as latest release"
- **Comme README** : remplace la section actuelle en gardant les liens vers `LICENSE`, `CONTRIBUTING.md`, etc.
- **Comme post LinkedIn** : garde uniquement les sections **"Nouveautés"** et **"Correctifs"** — ça fait un post court et percutant

Tu veux que je te prépare aussi le **CHANGELOG.md** mis à jour avec toutes les versions depuis la v1 ?
## 🙏 Remerciements

- À tous ceux qui jouent, cassent, et proposent des règles.
- À la communauté Python et à Tkinter, qui permettent de faire tenir un jeu complet dans un seul fichier.
