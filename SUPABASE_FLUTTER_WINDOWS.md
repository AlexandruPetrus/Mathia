# 🪟 Mathia × Supabase × Flutter - Guide Windows

## 🎯 Vous êtes sur Windows

Bonne nouvelle : **Flutter fonctionne parfaitement sur Windows !** 🎉

---

## 📱 Flutter vs SwiftUI sur Windows

| Critère | SwiftUI | Flutter |
|---------|---------|---------|
| **Fonctionne sur Windows** | ❌ Non (Mac uniquement) | ✅ Oui |
| **Développer pour Android** | ❌ Non | ✅ Oui |
| **Développer pour iOS** | ❌ Impossible sans Mac | ✅ Oui (mais besoin Mac pour publier) |
| **Applications Web** | ❌ Non | ✅ Oui |
| **Windows Desktop** | ❌ Non | ✅ Oui |

**Verdict : Utilisez Flutter !** 🦋

---

## 🚀 Installation Flutter sur Windows

### Étape 1 : Télécharger Flutter (10 min)

1. Allez sur [https://flutter.dev](https://flutter.dev)
2. Cliquez sur **Get Started** → **Windows**
3. Téléchargez le SDK Flutter
4. Extrayez dans `C:\src\flutter` (ou autre dossier)

### Étape 2 : Configurer le PATH

1. Ouvrez **Paramètres Windows** → **Système** → **Informations système**
2. Cliquez sur **Paramètres système avancés**
3. Cliquez sur **Variables d'environnement**
4. Dans **Variables système**, trouvez `Path` → **Modifier**
5. Ajoutez : `C:\src\flutter\bin`
6. Cliquez sur **OK**

### Étape 3 : Vérifier l'installation

Ouvrez **PowerShell** ou **CMD** :

```bash
flutter doctor
```

Vous verrez quelque chose comme :

```
Doctor summary (to see all details, run flutter doctor -v):
[√] Flutter (Channel stable, 3.16.0, on Microsoft Windows)
[!] Android toolchain - develop for Android devices
[!] Chrome - develop for the web
[√] Visual Studio - develop Windows apps
[!] Android Studio (not installed)
[√] VS Code (version 1.85)
[√] Connected device (1 available)
```

### Étape 4 : Installer Android Studio (pour Android)

1. Téléchargez [Android Studio](https://developer.android.com/studio)
2. Installez-le
3. Ouvrez Android Studio
4. Allez dans **More Actions** → **SDK Manager**
5. Installez :
   - ✅ Android SDK
   - ✅ Android SDK Platform-Tools
   - ✅ Android SDK Build-Tools

6. Dans **SDK Tools**, installez :
   - ✅ Android SDK Command-line Tools
   - ✅ Google Play services

7. Créez un émulateur Android :
   - **More Actions** → **Virtual Device Manager**
   - **Create Device** → Choisissez un appareil → **Next**
   - Téléchargez une image système (ex: API 33) → **Next**
   - **Finish**

### Étape 5 : Accepter les licences Android

```bash
flutter doctor --android-licenses
```

Tapez `y` pour accepter toutes les licences.

### Étape 6 : Vérifier que tout fonctionne

```bash
flutter doctor
```

Vous devriez avoir :

```
[√] Flutter
[√] Android toolchain
[√] Chrome
[√] Visual Studio
[√] VS Code
[√] Connected device
```

---

## 🎨 Créer votre app Flutter Mathia

### Étape 1 : Créer le projet

```bash
cd C:\Users\petru\OneDrive\Desktop\Mathia
flutter create mathia_app
cd mathia_app
```

### Étape 2 : Installer Supabase

Dans `pubspec.yaml` :

```yaml
dependencies:
  flutter:
    sdk: flutter
  
  # Supabase
  supabase_flutter: ^2.3.0
  
  # Utilitaires
  flutter_dotenv: ^5.1.0
  
  # UI
  google_fonts: ^6.1.0
```

Puis :

```bash
flutter pub get
```

### Étape 3 : Configuration Supabase

Créez `.env` dans le dossier `mathia_app/` :

```env
SUPABASE_URL=https://xxxxxxxx.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

Dans `pubspec.yaml`, ajoutez :

```yaml
flutter:
  assets:
    - .env
```

### Étape 4 : Initialiser Supabase

Dans `lib/main.dart` :

```dart
import 'package:flutter/material.dart';
import 'package:supabase_flutter/supabase_flutter.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  // Charger .env
  await dotenv.load(fileName: ".env");
  
  // Initialiser Supabase
  await Supabase.initialize(
    url: dotenv.env['SUPABASE_URL']!,
    anonKey: dotenv.env['SUPABASE_ANON_KEY']!,
  );
  
  runApp(const MathiaApp());
}

// Raccourci global
final supabase = Supabase.instance.client;

class MathiaApp extends StatelessWidget {
  const MathiaApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Mathia',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.blue),
        useMaterial3: true,
      ),
      home: const HomePage(),
    );
  }
}

class HomePage extends StatelessWidget {
  const HomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Mathia'),
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Text(
              'Bienvenue sur Mathia !',
              style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: () async {
                // Test de connexion Supabase
                try {
                  final response = await supabase
                      .from('courses')
                      .select()
                      .limit(1);
                  
                  if (context.mounted) {
                    ScaffoldMessenger.of(context).showSnackBar(
                      const SnackBar(content: Text('✅ Connexion Supabase OK !')),
                    );
                  }
                } catch (e) {
                  if (context.mounted) {
                    ScaffoldMessenger.of(context).showSnackBar(
                      SnackBar(content: Text('❌ Erreur : $e')),
                    );
                  }
                }
              },
              child: const Text('Tester Supabase'),
            ),
          ],
        ),
      ),
    );
  }
}
```

### Étape 5 : Lancer l'app

#### Sur Windows (Desktop)

```bash
flutter run -d windows
```

#### Sur émulateur Android

```bash
# Démarrer l'émulateur dans Android Studio d'abord
# Puis :
flutter run
```

#### Sur navigateur Chrome

```bash
flutter run -d chrome
```

---

## 📦 Structure du projet Flutter

Suivez maintenant le guide complet Flutter :

👉 **[SUPABASE_FLUTTER_INTEGRATION.md](SUPABASE_FLUTTER_INTEGRATION.md)**

Ce guide contient :
- ✅ Tous les modèles de données (User, Course, Exercise, Attempt)
- ✅ Tous les services (Auth, Courses, Exercises, Stats)
- ✅ Exemples d'écrans complets
- ✅ Gestion de l'authentification
- ✅ Temps réel

---

## 🎨 Recommandations de design

Puisque vous aimez un design moderne [[memory:2978053]], voici quelques packages Flutter :

```yaml
dependencies:
  google_fonts: ^6.1.0           # Polices modernes
  flutter_svg: ^2.0.9            # Icônes SVG
  animations: ^2.0.11            # Animations fluides
  shimmer: ^3.0.0                # Effet de chargement élégant
```

---

## 🔧 Commandes utiles Flutter

```bash
# Créer un nouveau projet
flutter create mon_app

# Lancer l'app
flutter run

# Lancer sur un device spécifique
flutter run -d windows
flutter run -d chrome
flutter run -d [device-id]

# Lister les devices disponibles
flutter devices

# Hot reload (pendant l'exécution)
# Tapez 'r' dans le terminal

# Hot restart (pendant l'exécution)
# Tapez 'R' dans le terminal

# Build APK (Android)
flutter build apk --release

# Build App Bundle (Android - pour Play Store)
flutter build appbundle --release

# Build Web
flutter build web

# Build Windows
flutter build windows

# Nettoyer le projet
flutter clean

# Mettre à jour les dépendances
flutter pub get
flutter pub upgrade

# Analyser le code
flutter analyze

# Formater le code
flutter format .
```

---

## 📱 Développer pour iOS depuis Windows

### Problème

Vous **ne pouvez pas compiler pour iOS** directement depuis Windows. 😢

### Solutions

#### Option 1 : Utiliser Codemagic (CI/CD cloud) ⭐ RECOMMANDÉ

[Codemagic](https://codemagic.io) peut compiler votre app Flutter pour iOS dans le cloud.

1. Créez un compte Codemagic (gratuit)
2. Connectez votre repo Git
3. Configurez le build iOS
4. Codemagic compile dans le cloud
5. Téléchargez l'IPA

**Avantage** : Pas besoin de Mac !

#### Option 2 : Louer un Mac dans le cloud

Services comme [MacStadium](https://www.macstadium.com) ou [MacinCloud](https://www.macincloud.com).

#### Option 3 : Acheter un Mac Mini (d'occasion)

Pour ~400-500€, vous pouvez compiler localement.

#### Option 4 : Machine virtuelle macOS (non recommandé)

Techniquement possible mais :
- ❌ Contre les conditions d'Apple
- ❌ Lent
- ❌ Compliqué à configurer

---

## 🌐 Développer pour le Web (facile !)

Flutter Web fonctionne parfaitement sur Windows :

```bash
flutter run -d chrome
```

Déploiement :

```bash
flutter build web
```

Puis uploadez le dossier `build/web/` sur :
- Vercel
- Netlify
- Firebase Hosting
- GitHub Pages

---

## 📊 Comparaison : ce que vous pouvez faire sur Windows

| Platform | Développement | Build | Test | Publication |
|----------|---------------|-------|------|-------------|
| **Android** | ✅ Oui | ✅ Oui | ✅ Émulateur | ✅ Oui |
| **iOS** | ✅ Oui | ❌ Non (besoin Mac/cloud) | ❌ Non | ❌ Besoin Mac |
| **Web** | ✅ Oui | ✅ Oui | ✅ Chrome | ✅ Oui |
| **Windows** | ✅ Oui | ✅ Oui | ✅ Local | ✅ Oui |
| **Linux** | ✅ Oui | ❌ Non | ❌ Non | ❌ Non |
| **macOS** | ✅ Oui | ❌ Non | ❌ Non | ❌ Non |

**Résumé** : Vous pouvez développer pour **Android + Web + Windows** directement depuis Windows ! 🎉

---

## 🎯 Ordre recommandé pour vous

### Jour 1 : Configuration (2h)

1. ✅ Installer Flutter
2. ✅ Installer Android Studio
3. ✅ Configurer un émulateur Android
4. ✅ Créer le projet `mathia_app`
5. ✅ Tester que ça fonctionne

### Jour 2 : Supabase (1h)

1. ✅ Configurer Supabase (si pas déjà fait)
2. ✅ Exécuter les scripts SQL
3. ✅ Installer `supabase_flutter`
4. ✅ Tester la connexion

### Jour 3-4 : Développement (5-10h)

1. ✅ Créer les modèles
2. ✅ Créer les services
3. ✅ Créer les écrans (Auth, Courses, Exercises)
4. ✅ Implémenter la navigation
5. ✅ Ajouter le design

### Jour 5 : Tests (2h)

1. ✅ Tester sur émulateur Android
2. ✅ Tester sur Windows desktop
3. ✅ Tester sur Web (Chrome)

---

## 📚 Ressources Flutter

- [Documentation officielle](https://flutter.dev/docs)
- [Flutter Windows Setup](https://docs.flutter.dev/get-started/install/windows)
- [Codelabs Flutter](https://docs.flutter.dev/codelabs)
- [Flutter Packages](https://pub.dev)
- [Flutter Community](https://discord.gg/flutter)

---

## 🆘 Problèmes courants sur Windows

### Erreur : "flutter not recognized"

➡️ Vérifiez que `C:\src\flutter\bin` est dans votre PATH.

### Android licenses non acceptées

```bash
flutter doctor --android-licenses
```

### Visual Studio Build Tools manquants

Téléchargez [Visual Studio Build Tools](https://visualstudio.microsoft.com/downloads/)

### Émulateur Android lent

1. Activez la virtualisation dans le BIOS (Intel VT-x ou AMD-V)
2. Installez HAXM (Intel) ou WHV (Windows Hypervisor)
3. Allouez plus de RAM à l'émulateur

---

## ✅ Résumé pour vous

**Votre situation** :
- 🪟 Windows 10
- ❌ Pas de macOS → Pas de SwiftUI/Xcode
- ✅ Flutter fonctionne parfaitement !

**Ce que vous pouvez faire** :
- ✅ Développer pour Android, Web, Windows
- ✅ Compiler pour Android et Web directement
- ⚠️ Pour iOS : utiliser Codemagic (cloud)

**Prochaines étapes** :
1. Installer Flutter (guide ci-dessus)
2. Créer le projet `mathia_app`
3. Suivre [SUPABASE_FLUTTER_INTEGRATION.md](SUPABASE_FLUTTER_INTEGRATION.md)

---

🎉 Bienvenue dans le monde Flutter ! 🦋




