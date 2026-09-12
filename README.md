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

## 🙏 Remerciements

- À tous ceux qui jouent, cassent, et proposent des règles.
- À la communauté Python et à Tkinter, qui permettent de faire tenir un jeu complet dans un seul fichier.
