# Contribuer à DarkMonopoly

Merci de l'intérêt porté au projet ! Voici comment y participer proprement.

## 🌱 Philosophie du projet

- **Minimalisme** : un seul fichier tant que c'est possible.
- **Zéro dépendance** : uniquement la bibliothèque standard Python.
- **Lisible avant tout** : le code est pédagogique, pas optimisé à l'extrême.
- **Chaque commit laisse le jeu jouable** : pas de branche cassée longtemps.

## 🧭 Workflow Git

1. **Fork** le dépôt.
2. Crée une branche descriptive :
   ```bash
   git checkout -b feat/module-hack
   # ou
   git checkout -b fix/loyer-compagnies
   ```
3. Commits courts, au présent, en français ou anglais :
   ```
   feat: ajoute le module de falsification de titre
   fix: corrige le calcul du loyer des compagnies
   docs: précise la règle d'égalité de construction
   ```
4. **Push** puis ouvre une **Pull Request** vers `main`.

## 🏷️ Conventions de commit

Format inspiré de [Conventional Commits](https://www.conventionalcommits.org/) :

| Préfixe | Usage |
|---------|-------|
| `feat:` | nouvelle fonctionnalité |
| `fix:` | correction de bug |
| `docs:` | documentation seule |
| `refactor:` | refonte sans changement de comportement |
| `style:` | formatage, indentation |
| `test:` | ajout ou correction de tests |
| `chore:` | tâches diverses (build, gitignore…) |

## 🧪 Tests

Aucun framework de test n'est encore en place.  
En attendant, toute PR doit être vérifiée manuellement :

1. Lancer le jeu : `python darkmonopoly.py`
2. Tester les cas suivants :
   - achat d'une propriété,
   - loyer sur propriété adverse,
   - double → rejoue,
   - 3 doubles → prison,
   - faillite d'un joueur,
   - changement de thème.

## 📐 Style de code

- **PEP 8** appliqué raisonnablement.
- Noms de variables en **anglais** dans le code, **commentaires en français**.
- Typage indicatif accepté (`List[int]`, `-> bool`, etc.).
- Pas de print de debug laissé dans le code final.

## 🎨 UI / UX

- Toute nouvelle couleur passe par le dictionnaire `THEMES`.
- Aucune couleur codée en dur dans les widgets.
- Les 4 thèmes (clair, sombre, nuit_bleu, nuit_rouge) doivent rester **cohérents et lisibles**.

## 🐛 Signaler un bug

Ouvre une **issue** avec :

- titre clair et précis,
- version de Python,
- OS,
- étapes de reproduction,
- comportement attendu vs observé,
- capture ou message d'erreur.

## 💡 Proposer une fonctionnalité

Ouvre une **issue** avec le label `enhancement` et décris :

- **quoi** : la fonctionnalité en une phrase,
- **pourquoi** : le lien avec la vision économique du projet,
- **comment** : une ébauche d'idée d'implémentation (facultatif).

## 🤝 Code de conduite

En participant, tu t'engages à respecter le [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md).  
Sois respectueux, patient, et constructif. Les désaccords techniques sont normaux — les attaques personnelles ne le sont pas.