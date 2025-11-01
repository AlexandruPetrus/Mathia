# 📱 Mathia - Application Mobile Flutter

Application mobile de révision de mathématiques pour collégiens français (6ème à 3ème).

---

## 🎯 Fonctionnalités

✅ **Authentification sécurisée** avec Supabase
✅ **Centaines d'exercices** couvrant tout le programme
✅ **Types variés** : QCM, calcul, vrai/faux, réponse libre
✅ **Explications détaillées** pour chaque réponse
✅ **Suivi de progression** avec statistiques
✅ **Interface moderne** et intuitive
✅ **Mode hors-ligne** (avec cache)

---

## 📋 Prérequis

- **Flutter SDK 3.16+** ([Installation](https://flutter.dev/docs/get-started/install))
- **Dart 3.2+** (inclus avec Flutter)
- **Android Studio** ou **VS Code** avec extensions Flutter
- **Compte Supabase** ([Inscription gratuite](https://supabase.com))

---

## 🚀 Installation & Configuration

### 1. Installer Flutter

```bash
# Vérifier l'installation
flutter doctor

# Mettre à jour si nécessaire
flutter upgrade
```

### 2. Cloner et installer les dépendances

```bash
cd mathia_app
flutter pub get
```

### 3. Configurer Supabase

#### Créer un projet Supabase

1. Allez sur [supabase.com](https://supabase.com)
2. Créez un nouveau projet
3. Exécutez le script SQL depuis `/supabase_schema.sql`

#### Configurer les clés API

Créez un fichier `.env` dans `/mathia_app/` :

```env
SUPABASE_URL=https://votre-projet.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Où trouver ces clés ?**
- Supabase Dashboard → **Settings** → **API**

---

## 🔧 Développement

### Lancer l'app en mode dev

```bash
# Lister les appareils disponibles
flutter devices

# Lancer sur un émulateur/device
flutter run

# Lancer en mode debug avec hot reload
flutter run --debug

# Lancer en mode release
flutter run --release
```

### Structure du projet

```
mathia_app/
├── lib/
│   ├── main.dart                 # Point d'entrée
│   ├── models/                   # Modèles de données
│   │   ├── user_model.dart
│   │   ├── course_model.dart
│   │   ├── exercise_model.dart
│   │   └── attempt_model.dart
│   ├── screens/                  # Écrans de l'app
│   │   ├── auth/
│   │   │   ├── login_screen.dart
│   │   │   └── register_screen.dart
│   │   ├── home/
│   │   │   └── home_screen.dart
│   │   ├── course/
│   │   │   └── course_detail_screen.dart
│   │   ├── exercise/
│   │   │   └── exercise_screen.dart
│   │   └── profile/
│   │       └── profile_screen.dart
│   └── services/                 # Services API
│       ├── auth_service.dart
│       ├── course_service.dart
│       ├── exercise_service.dart
│       └── stats_service.dart
├── android/                      # Configuration Android
├── ios/                          # Configuration iOS
├── assets/                       # Images, icônes, etc.
└── .env                          # Configuration (ne pas committer!)
```

---

## 🏗️ Build pour Production

### Android (Play Store)

#### 1. Créer une keystore

```bash
keytool -genkey -v -keystore ~/mathia-upload-keystore.jks -storetype JKS -keyalg RSA -keysize 2048 -validity 10000 -alias upload
```

#### 2. Configurer la signature

Créez `android/key.properties` :

```properties
storePassword=VOTRE_MOT_DE_PASSE
keyPassword=VOTRE_MOT_DE_PASSE
keyAlias=upload
storeFile=/chemin/absolu/vers/mathia-upload-keystore.jks
```

#### 3. Build l'App Bundle (AAB)

```bash
flutter clean
flutter build appbundle --release

# Fichier généré :
# build/app/outputs/bundle/release/app-release.aab
```

### iOS (App Store)

```bash
flutter build ios --release

# Ouvrir dans Xcode pour la signature et upload
open ios/Runner.xcworkspace
```

---

## 🧪 Tests

### Tests unitaires

```bash
flutter test
```

### Tests d'intégration

```bash
flutter test integration_test
```

### Analyser le code

```bash
flutter analyze
```

---

## 📦 Dépendances Principales

| Package | Version | Usage |
|---------|---------|-------|
| `supabase_flutter` | ^2.0.0 | Backend & Auth |
| `flutter_dotenv` | ^5.1.0 | Variables d'environnement |
| `flutter_launcher_icons` | ^0.13.1 | Génération d'icônes |

Voir `pubspec.yaml` pour la liste complète.

---

## 🐛 Résolution de Problèmes

### L'app crash au démarrage

**Cause** : Fichier `.env` manquant ou mal configuré

**Solution** :
```bash
# Vérifier que .env existe
ls -la .env

# Vérifier le contenu
cat .env

# Reconstruire
flutter clean
flutter pub get
flutter run
```

### Erreur "Supabase not initialized"

**Cause** : `Supabase.initialize()` pas appelé avant `runApp()`

**Solution** : Vérifiez que `main.dart` contient :

```dart
Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await dotenv.load(fileName: ".env");
  await Supabase.initialize(
    url: dotenv.env['SUPABASE_URL']!,
    anonKey: dotenv.env['SUPABASE_ANON_KEY']!,
  );
  runApp(const MathiaApp());
}
```

### Erreur Gradle "Execution failed"

**Solution** :
```bash
cd android
./gradlew clean
cd ..
flutter clean
flutter pub get
flutter run
```

### Hot reload ne fonctionne pas

**Solution** :
```bash
# Relancer Flutter
r  # Dans le terminal où flutter run est actif

# Ou redémarrer complètement
R
```

---

## 🔐 Sécurité

### Fichiers à NE JAMAIS committer

❌ `.env` (contient les clés API Supabase)
❌ `android/key.properties` (mot de passe keystore)
❌ `*.jks`, `*.keystore` (clés de signature)
❌ `google-services.json` (si Firebase est utilisé)

✅ Ces fichiers sont déjà dans `.gitignore`

### Bonnes pratiques

- **Ne jamais** hardcoder les clés API dans le code
- **Toujours** utiliser des variables d'environnement (`.env`)
- **Sauvegarder** la keystore dans un endroit sûr (pas dans Git)
- **Activer** Row Level Security sur Supabase

---

## 📱 Compatibilité

### Versions Android supportées

- **Minimum** : Android 5.0 (API 21) - **98% des appareils**
- **Cible** : Android 14 (API 34)

### Versions iOS supportées

- **Minimum** : iOS 12.0
- **Cible** : iOS 17.0

---

## 🚀 Déploiement

### Play Store (Android)

Consultez le guide complet : `/DEPLOIEMENT_PLAY_STORE.md`

**Étapes résumées** :
1. Créer un compte Google Play Console (25 USD)
2. Configurer l'app (icône, captures, descriptions)
3. Build l'AAB : `flutter build appbundle --release`
4. Télécharger sur Play Console
5. Soumettre pour examen (1-7 jours)

### App Store (iOS)

1. Créer un compte Apple Developer (99 USD/an)
2. Configurer l'app dans App Store Connect
3. Build avec Xcode et upload
4. Soumettre pour examen (1-3 jours)

---

## 📈 Performances

### Optimisations appliquées

✅ **ProGuard** activé (minification du code)
✅ **Shrink Resources** activé (suppression des ressources inutilisées)
✅ **Multi-ABI support** (ARM, ARM64, x86_64)
✅ **Lazy loading** des images
✅ **Cache local** pour les données

### Taille de l'APK

- **Debug** : ~40 MB
- **Release (AAB)** : ~15-20 MB
- **Installée** : ~30-40 MB

---

## 🛠️ Scripts Utiles

```bash
# Vérifier la santé du projet
flutter doctor -v

# Nettoyer complètement
flutter clean
cd ios && rm -rf Pods Podfile.lock && cd ..
cd android && ./gradlew clean && cd ..

# Mettre à jour les dépendances
flutter pub upgrade

# Analyser les performances
flutter run --profile
flutter run --release --verbose

# Tester sur un device spécifique
flutter run -d <device-id>
```

---

## 📚 Ressources

### Documentation Flutter
- [Flutter Docs](https://docs.flutter.dev/)
- [Cookbook Flutter](https://docs.flutter.dev/cookbook)
- [Widget Catalog](https://docs.flutter.dev/ui/widgets)

### Documentation Supabase
- [Supabase Docs](https://supabase.com/docs)
- [Flutter Quickstart](https://supabase.com/docs/guides/getting-started/quickstarts/flutter)
- [Auth avec Supabase](https://supabase.com/docs/guides/auth)

### Communauté
- [Flutter Discord](https://discord.gg/flutter)
- [Supabase Discord](https://discord.supabase.com/)
- [Stack Overflow - Flutter](https://stackoverflow.com/questions/tagged/flutter)

---

## 📞 Support

### Problème avec l'app ?

1. Vérifiez la section **Résolution de Problèmes** ci-dessus
2. Consultez les logs : `flutter run --verbose`
3. Ouvrez une issue sur GitHub

### Contact

- **Email** : contact@mathia.app
- **GitHub** : [github.com/votre-username/mathia](https://github.com/votre-username/mathia)

---

## 📄 Licence

MIT License - Voir le fichier `LICENSE` pour plus de détails.

---

## ✅ Checklist Avant Production

Avant de déployer en production, vérifiez :

- [ ] Tests passent : `flutter test`
- [ ] Pas d'erreurs : `flutter analyze`
- [ ] `.env` configuré avec les vraies clés
- [ ] Keystore créée et sauvegardée
- [ ] `key.properties` configuré
- [ ] Version incrémentée dans `build.gradle`
- [ ] Icônes générées (512x512px)
- [ ] Captures d'écran préparées
- [ ] Description Play Store rédigée
- [ ] Politique de confidentialité publiée

---

**Bon développement ! 🚀**
