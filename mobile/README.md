# 📱 Mathia iOS App (SwiftUI)

Application iOS pour réviser les mathématiques, connectée au backend API Mathia.

## 🎯 Fonctionnalités

✅ **Authentification**
- Inscription avec nom, email et mot de passe
- Connexion avec email et mot de passe
- Stockage sécurisé du JWT dans UserDefaults
- Déconnexion

✅ **Cours**
- Liste de tous les cours disponibles
- Filtrage par niveau (6ème, 5ème, 4ème, 3ème)
- Affichage des détails d'un cours
- Nombre d'exercices par cours

✅ **Exercices**
- Liste des exercices par cours
- Support des QCM (questions à choix multiples)
- Support des questions libres
- Affichage de la difficulté (facile, moyen, difficile)

✅ **Quiz**
- Réponse aux exercices QCM
- Validation des réponses
- Affichage du résultat (correct/incorrect)
- Explication détaillée si la réponse est correcte
- Feedback visuel (vert pour correct, rouge pour incorrect)

✅ **Profil**
- Affichage des informations utilisateur
- Avatar avec initiales
- Date d'inscription
- Déconnexion

## 📁 Structure du projet

```
MathiaApp/
├── MathiaApp.swift          # Point d'entrée de l'app
├── Models/                  # Modèles de données
│   ├── User.swift
│   ├── Course.swift
│   ├── Exercise.swift
│   └── Attempt.swift
├── Services/                # Services réseau
│   ├── APIService.swift     # Appels API avec URLSession
│   └── AuthManager.swift    # Gestion de l'authentification
└── Views/                   # Vues SwiftUI
    ├── Auth/
    │   ├── LoginView.swift
    │   └── SignupView.swift
    ├── Courses/
    │   ├── CoursesListView.swift
    │   └── CourseDetailView.swift
    ├── Exercises/
    │   └── QuizView.swift
    └── Profile/
        └── ProfileView.swift
```

## 🚀 Installation

### 1. Ouvrir le projet dans Xcode

```bash
cd mobile/MathiaApp
open MathiaApp.xcodeproj
```

Si le fichier `.xcodeproj` n'existe pas encore, créez-le dans Xcode :
1. Ouvrir Xcode
2. File → New → Project
3. Choisir "iOS" → "App"
4. Nommer le projet "MathiaApp"
5. Interface: SwiftUI
6. Language: Swift
7. Copier tous les fichiers dans le projet

### 2. Configuration de l'API

Modifier `APIService.swift` pour pointer vers votre backend :

```swift
// Pour iOS Simulator sur Mac
private let baseURL = "http://localhost:3000/api"

// Pour un appareil physique, utilisez l'IP de votre Mac
// private let baseURL = "http://192.168.1.X:3000/api"
```

**Trouver l'IP de votre Mac** :
```bash
# Mac/Linux
ifconfig | grep "inet "

# Windows
ipconfig
```

### 3. Permissions réseau (iOS 14+)

Si vous utilisez `http://` (et non `https://`), ajoutez dans `Info.plist` :

```xml
<key>NSAppTransportSecurity</key>
<dict>
    <key>NSAllowsArbitraryLoads</key>
    <true/>
</dict>
```

**⚠️ Note** : En production, utilisez toujours HTTPS !

## 🎮 Utilisation

### 1. Démarrer le backend

```bash
cd ../
npm run dev
```

Le serveur doit tourner sur `http://localhost:3000`

### 2. Lancer l'app

1. Ouvrir le projet dans Xcode
2. Choisir un simulateur (iPhone 14 Pro recommandé)
3. Cliquer sur "Run" (⌘+R)

### 3. S'inscrire

1. Sur l'écran de connexion, cliquer sur "Inscrivez-vous"
2. Remplir le formulaire :
   - Nom complet
   - Email
   - Mot de passe (minimum 6 caractères)
   - Confirmation du mot de passe
3. Cliquer sur "S'inscrire"

### 4. Explorer les cours

1. L'onglet "Cours" affiche tous les cours disponibles
2. Cliquer sur un cours pour voir ses détails
3. Cliquer sur un exercice pour le résoudre

### 5. Répondre aux QCM

1. Lire la question
2. Sélectionner une réponse parmi les options
3. Cliquer sur "Valider"
4. Voir le résultat avec explication

## 🔧 Configuration avancée

### Changer l'URL de l'API

Éditez `APIService.swift` :

```swift
private let baseURL = "https://votre-api.com/api"
```

### Personnaliser les couleurs

Les couleurs sont définies dans les vues SwiftUI. Principales couleurs :
- **Bleu** : `.blue` - Couleur principale
- **Violet** : `.purple` - Couleur secondaire (écrans d'auth)
- **Vert** : `.green` - Réponses correctes
- **Rouge** : `.red` - Réponses incorrectes
- **Orange** : `.orange` - Niveau moyen

### Ajouter des icônes

Les icônes utilisent SF Symbols (intégrés à iOS) :
- `book.fill` - Cours
- `person.fill` - Profil
- `checklist` - QCM
- `function` - Logo Mathia

## 📊 Flux de données

```
1. Utilisateur se connecte
   ↓
2. JWT stocké dans AuthManager
   ↓
3. Récupération des cours depuis l'API
   ↓
4. Affichage des cours dans CoursesListView
   ↓
5. Sélection d'un cours
   ↓
6. Récupération des exercices du cours
   ↓
7. Affichage dans CourseDetailView
   ↓
8. Sélection d'un exercice
   ↓
9. Quiz dans QuizView
   ↓
10. Soumission de la réponse à l'API
    ↓
11. Affichage du résultat et explication
```

## 🐛 Dépannage

### Erreur "Connection refused"

**Problème** : L'app ne peut pas se connecter au backend

**Solutions** :
1. Vérifier que le backend tourne (`npm run dev`)
2. Vérifier l'URL dans `APIService.swift`
3. Sur appareil physique, utiliser l'IP du Mac au lieu de `localhost`
4. Vérifier les permissions réseau dans `Info.plist`

### Erreur "Invalid response"

**Problème** : Le backend renvoie une erreur

**Solutions** :
1. Vérifier les logs Xcode pour voir la réponse
2. Tester l'API avec curl ou Postman
3. Vérifier que le backend est à jour

### L'app ne s'affiche pas correctement

**Problème** : UI cassée ou manquante

**Solutions** :
1. Nettoyer le build : Product → Clean Build Folder (⌘+Shift+K)
2. Relancer le simulateur
3. Vérifier que tous les fichiers sont dans le projet

### JWT expiré

**Problème** : "Non autorisé. Veuillez vous reconnecter."

**Solutions** :
1. Se déconnecter et se reconnecter
2. Le JWT expire après 7 jours par défaut
3. Configurer `JWT_EXPIRES_IN` dans le backend

## 🎨 Personnalisation

### Modifier le thème

Dans chaque vue, les couleurs peuvent être changées :

```swift
// LoginView.swift
LinearGradient(
    colors: [Color.blue.opacity(0.6), Color.purple.opacity(0.4)],
    // Changer ces couleurs ↑
    startPoint: .topLeading,
    endPoint: .bottomTrailing
)
```

### Ajouter des animations

SwiftUI supporte les animations facilement :

```swift
.animation(.spring(), value: isSubmitted)
```

### Localisation (français)

Les textes sont déjà en français. Pour ajouter d'autres langues :
1. Project → Localizations → Add language
2. Utiliser `NSLocalizedString` pour les textes

## 📱 Compatibilité

- **iOS 15.0+** minimum
- **iPhone et iPad** supportés
- **Dark Mode** automatique
- **SwiftUI** natif

## 🚢 Déploiement

Pour déployer sur TestFlight :

1. Configurer l'URL de production dans `APIService.swift`
2. Changer le Bundle Identifier
3. Configurer les signing certificates
4. Archive → Distribute App → TestFlight

## 📚 Ressources

- [Documentation SwiftUI](https://developer.apple.com/documentation/swiftui/)
- [URLSession Guide](https://developer.apple.com/documentation/foundation/urlsession)
- [SF Symbols](https://developer.apple.com/sf-symbols/)
- [Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/)

---

✅ **App iOS complète et prête à l'emploi !**





