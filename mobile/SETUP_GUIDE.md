# 🚀 Guide de configuration - Mathia iOS

Guide étape par étape pour configurer et lancer l'application iOS.

## 📋 Prérequis

### Requis

- ✅ **macOS** (pour Xcode)
- ✅ **Xcode 14+** ([Télécharger](https://apps.apple.com/app/xcode/id497799835))
- ✅ **Backend Mathia** fonctionnel

### Optionnel

- iPhone ou iPad physique (sinon le Simulator suffit)

## 🛠️ Installation complète

### Étape 1 : Créer le projet Xcode

1. **Ouvrir Xcode**

2. **File → New → Project**

3. **Choisir le template** :
   - Platform: iOS
   - Template: App
   - Cliquer sur "Next"

4. **Configuration** :
   - Product Name: `MathiaApp`
   - Team: None (ou votre Apple ID)
   - Organization Identifier: `com.mathia` (ou votre propre identifiant)
   - Interface: **SwiftUI**
   - Language: **Swift**
   - Storage: **None**
   - Include Tests: Non
   - Cliquer sur "Next"

5. **Choisir l'emplacement** :
   - Naviguer vers `mobile/`
   - Cliquer sur "Create"

### Étape 2 : Organiser les fichiers

1. **Créer les dossiers** dans Xcode :
   - Clic droit sur "MathiaApp" → New Group → "Models"
   - Clic droit sur "MathiaApp" → New Group → "Services"
   - Clic droit sur "MathiaApp" → New Group → "Views"
   - Dans "Views", créer : "Auth", "Courses", "Exercises", "Profile"

2. **Ajouter les fichiers Swift** :
   - Glisser-déposer chaque fichier `.swift` dans son dossier correspondant
   - OU : Clic droit sur le dossier → Add Files to "MathiaApp"

### Étape 3 : Configuration réseau

1. **Ouvrir `Info.plist`** (ou `Info` dans Project Settings)

2. **Ajouter l'exception HTTP** pour localhost :
   - Clic droit dans Info.plist → Add Row
   - Key: `App Transport Security Settings` (NSAppTransportSecurity)
   - Expand → Add Row
   - Key: `Allow Arbitrary Loads` (NSAllowsArbitraryLoads)
   - Value: YES

**Format XML direct** :
```xml
<key>NSAppTransportSecurity</key>
<dict>
    <key>NSAllowsArbitraryLoads</key>
    <true/>
</dict>
```

### Étape 4 : Configurer l'URL de l'API

**Ouvrir `APIService.swift`** et configurer selon votre situation :

#### Option A : Simulator iOS sur le même Mac

```swift
private let baseURL = "http://localhost:3000/api"
```

✅ Simple et fonctionne directement

#### Option B : Appareil physique (iPhone/iPad)

1. **Trouver l'IP de votre Mac** :
```bash
ifconfig | grep "inet "
# Exemple de résultat : inet 192.168.1.10
```

2. **Mettre à jour l'URL** :
```swift
private let baseURL = "http://192.168.1.10:3000/api"
```

⚠️ **Important** : iPhone et Mac doivent être sur le même réseau WiFi !

#### Option C : Backend en production

```swift
private let baseURL = "https://your-api.com/api"
```

✅ Utilisez HTTPS en production

### Étape 5 : Lancer le backend

```bash
cd ..  # Revenir à la racine du projet
npm run dev
```

Attendez de voir :
```
✅ Connexion à PostgreSQL établie avec succès
🚀 Serveur Mathia démarré avec succès
📍 URL: http://localhost:3000
```

### Étape 6 : Lancer l'app iOS

1. **Sélectionner un simulator** :
   - En haut d'Xcode : MathiaApp > **iPhone 14 Pro** (recommandé)

2. **Lancer l'app** :
   - Cliquer sur le bouton "Play" (▶️)
   - Ou : Product → Run (⌘+R)

3. **Attendre le build** (première fois peut prendre 1-2 minutes)

4. **L'app s'ouvre** sur l'écran de connexion 🎉

## 🧪 Test rapide

### 1. Créer un compte

1. Cliquer sur "Pas encore de compte ? **Inscrivez-vous**"
2. Remplir :
   - Nom: "Test User"
   - Email: "test@example.com"
   - Mot de passe: "test123"
   - Confirmer: "test123"
3. Cliquer sur "S'inscrire"

→ Vous devriez voir l'écran "Mes Cours"

### 2. Tester les cours

Si aucun cours n'apparaît, créez-en un via l'API :

```bash
# D'abord, récupérer le token depuis l'app (voir les logs Xcode)
# Ou se connecter via l'API :

curl -X POST http://localhost:3000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "test123"
  }'

# Copier le token, puis créer un cours en SQL :
psql -U postgres -d mathia_db -c "
INSERT INTO courses (title, grade, chapter, description, \"createdAt\", \"updatedAt\")
VALUES ('Les fractions', '6ème', 'Arithmétique', 'Apprendre les fractions', NOW(), NOW())
RETURNING id;
"
```

### 3. Créer un exercice

```bash
export TOKEN="votre_token_ici"

curl -X POST http://localhost:3000/api/admin/exercises \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "courseId": 1,
    "type": "qcm",
    "body": "Quelle est la moitié de 10?",
    "options": {"A": "3", "B": "5", "C": "7", "D": "10"},
    "answer": "B",
    "explanation": "10 divisé par 2 égale 5",
    "difficulty": "facile",
    "tags": ["fractions"]
  }'
```

### 4. Pull to refresh

Dans l'app, tirez vers le bas pour rafraîchir la liste des cours.

### 5. Résoudre un exercice

1. Cliquer sur un cours
2. Cliquer sur un exercice
3. Sélectionner une réponse
4. Cliquer sur "Valider"

→ Vous verrez le résultat avec l'explication !

## 🐛 Problèmes courants

### ❌ "Connection refused" / "Failed to connect"

**Causes possibles** :
1. Backend pas démarré
2. Mauvaise URL configurée
3. Firewall bloque le port 3000

**Solutions** :
```bash
# 1. Vérifier que le backend tourne
lsof -i :3000
# Devrait afficher "node"

# 2. Tester l'API manuellement
curl http://localhost:3000/api/health

# 3. Sur appareil physique, pinguer le Mac
ping 192.168.1.X
```

### ❌ Build failed

**Erreur commune** : "Cannot find 'X' in scope"

**Solution** :
1. Product → Clean Build Folder (⌘+Shift+K)
2. File → Close Workspace
3. Rouvrir Xcode
4. Product → Build (⌘+B)

### ❌ "App Transport Security" erreur

**Solution** : Vérifier `Info.plist` contient :
```xml
<key>NSAppTransportSecurity</key>
<dict>
    <key>NSAllowsArbitraryLoads</key>
    <true/>
</dict>
```

### ❌ L'app se lance mais écran blanc

**Causes** :
1. Fichier principal mal configuré
2. @main manquant dans MathiaApp.swift

**Solution** :
Vérifier que `MathiaApp.swift` a la structure :
```swift
@main
struct MathiaApp: App {
    // ...
}
```

### ❌ "Invalid response" lors de l'appel API

**Debug** :
1. Ouvrir la Console Xcode (⌘+Shift+C)
2. Chercher les logs qui commencent par "📥"
3. Vérifier la réponse du serveur

**Solution** :
- Vérifier que le backend renvoie du JSON valide
- Tester l'endpoint avec curl/Postman

## 📱 Configuration avancée

### Déployer sur un iPhone physique

1. **Connecter l'iPhone** via USB

2. **Trust this computer** sur l'iPhone

3. **Configurer le Team** :
   - Project Settings → Signing & Capabilities
   - Team: Choisir votre Apple ID
   - Signing Certificate: Automatic

4. **Sélectionner l'appareil** en haut d'Xcode

5. **Run** (⌘+R)

6. **Sur l'iPhone** : Settings → General → VPN & Device Management → Trust developer

### Dark Mode

L'app supporte automatiquement le Dark Mode iOS.

Pour forcer un mode :
```swift
// Dans MathiaApp.swift
.preferredColorScheme(.dark) // ou .light
```

### Logs de debug

Pour voir les réponses API, vérifier `APIService.swift` ligne ~75 :
```swift
if let jsonString = String(data: data, encoding: .utf8) {
    print("📥 Response (\(httpResponse.statusCode)): \(jsonString)")
}
```

## ✅ Checklist finale

Avant de dire que tout fonctionne :

- [ ] Backend démarré sur port 3000
- [ ] URL configurée dans APIService.swift
- [ ] Info.plist configure les permissions HTTP
- [ ] App se build sans erreurs
- [ ] App se lance sur le Simulator
- [ ] Peut créer un compte
- [ ] Peut se connecter
- [ ] Peut voir la liste des cours (si disponibles)
- [ ] Peut ouvrir un cours
- [ ] Peut répondre à un exercice
- [ ] Le résultat s'affiche correctement
- [ ] Peut se déconnecter

## 🎓 Prochaines étapes

Une fois que tout fonctionne :

1. **Ajouter des cours et exercices** via l'API ou le script IA
2. **Personnaliser les couleurs** et le design
3. **Ajouter des fonctionnalités** (historique, badges, etc.)
4. **Tester sur iPhone physique**
5. **Préparer pour TestFlight**

---

✅ **Votre app iOS est prête !**

Besoin d'aide ? Consultez `README.md` pour plus de détails.





