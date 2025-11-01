# 🚀 Guide de Déploiement - Mathia sur le Play Store

Guide complet pour déployer l'application Mathia sur le Google Play Store en moins de 2 heures.

---

## 📋 Prérequis

### Outils nécessaires
- [ ] Flutter SDK 3.16+ installé ([flutter.dev](https://flutter.dev))
- [ ] Android Studio installé
- [ ] Compte Google Play Console ([play.google.com/console](https://play.google.com/console)) - **25 USD** d'inscription
- [ ] Compte Supabase ([supabase.com](https://supabase.com)) - Plan gratuit

### Fichiers à préparer
- [ ] Logo de l'app (512x512px, PNG)
- [ ] Icône de lancement (1024x1024px, PNG)
- [ ] Captures d'écran (minimum 2, format 16:9)
- [ ] Description de l'app (court et long)
- [ ] Politique de confidentialité (URL publique)

---

## 🎯 ÉTAPE 1 : Configurer Supabase (15 min)

### 1.1 Créer un projet Supabase

1. Allez sur [supabase.com](https://supabase.com)
2. Créez un nouveau projet :
   - **Nom** : Mathia
   - **Mot de passe de la base de données** : Générer automatiquement (notez-le !)
   - **Région** : Frankfurt (Europe) pour la France
3. Attendez 2-3 minutes que le projet soit prêt

### 1.2 Créer le schéma de base de données

1. Dans votre projet Supabase, allez dans **SQL Editor**
2. Copiez le contenu de `/supabase_schema.sql`
3. Collez-le dans l'éditeur SQL
4. Cliquez sur **Run** ▶️
5. Vérifiez que tout est créé : allez dans **Table Editor**, vous devriez voir :
   - `users`
   - `courses`
   - `exercises`
   - `attempts`
   - `favorites`
   - `progress`

### 1.3 Récupérer les clés API

1. Allez dans **Settings** → **API**
2. Notez ces deux valeurs :
   ```
   SUPABASE_URL=https://xxxxx.supabase.co
   SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
   ```

### 1.4 Activer l'authentification par email

1. Allez dans **Authentication** → **Providers**
2. Activez **Email** (devrait être activé par défaut)
3. Désactivez **Confirm email** pour simplifier (optionnel)

### 1.5 Insérer des données de test (OPTIONNEL)

```sql
-- Cours de démonstration
INSERT INTO public.courses (title, description, grade, topic, difficulty, is_published, order_num)
VALUES
  ('Introduction aux fractions', 'Apprendre les bases des fractions avec des exercices simples', '6ème', 'Arithmétique', 'facile', true, 1),
  ('Les équations du premier degré', 'Résoudre des équations simples à une inconnue', '3ème', 'Algèbre', 'moyen', true, 2),
  ('Géométrie : les triangles', 'Propriétés et construction des triangles', '5ème', 'Géométrie', 'moyen', true, 3);

-- Exercices pour le premier cours (récupérer l'ID du cours d'abord)
INSERT INTO public.exercises (course_id, title, description, question, type, options, answer, explanation, difficulty, points, is_published, order_num)
SELECT
  (SELECT id FROM public.courses WHERE title = 'Introduction aux fractions' LIMIT 1),
  'Addition de fractions',
  'Calculer la somme de deux fractions',
  'Calculez : 1/2 + 1/4 = ?',
  'qcm',
  '{"A": "1/4", "B": "2/6", "C": "3/4", "D": "1"}'::jsonb,
  'C',
  'Pour additionner des fractions, il faut un dénominateur commun. 1/2 = 2/4, donc 2/4 + 1/4 = 3/4',
  'facile',
  10,
  true,
  1;
```

---

## 📱 ÉTAPE 2 : Configurer l'App Flutter (20 min)

### 2.1 Créer le fichier .env

Dans `/mathia_app/`, créez un fichier `.env` :

```env
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

Remplacez par vos vraies valeurs récupérées à l'étape 1.3.

### 2.2 Installer les dépendances Flutter

```bash
cd mathia_app
flutter pub get
flutter pub upgrade
```

### 2.3 Tester l'app en local

```bash
# Démarrer un émulateur Android ou connecter un téléphone
flutter devices

# Lancer l'app
flutter run
```

✅ **Vérifiez que** :
- L'app se lance sans erreur
- Vous pouvez créer un compte
- Vous pouvez voir les cours (si vous avez inséré des données de test)

---

## 🔧 ÉTAPE 3 : Configurer pour le Play Store (30 min)

### 3.1 Modifier le package name

Éditez `/mathia_app/android/app/build.gradle` :

```gradle
android {
    namespace "com.mathia.app"  // ← Ligne 3, changez ceci
    // ...
    defaultConfig {
        applicationId "com.mathia.app"  // ← Ligne 50, changez ceci
        minSdkVersion 21
        targetSdkVersion flutter.targetSdkVersion
        versionCode 1           // ← Incrémentez pour chaque release
        versionName "1.0.0"     // ← Version visible par les utilisateurs
    }
}
```

### 3.2 Modifier l'AndroidManifest.xml

Éditez `/mathia_app/android/app/src/main/AndroidManifest.xml` :

```xml
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    <!-- Permissions nécessaires -->
    <uses-permission android:name="android.permission.INTERNET"/>

    <application
        android:label="Mathia"  <!-- ← Nom de l'app -->
        android:name="${applicationName}"
        android:icon="@mipmap/ic_launcher">  <!-- ← Icône -->

        <activity
            android:name=".MainActivity"
            android:exported="true"
            android:launchMode="singleTop"
            android:theme="@style/LaunchTheme"
            android:configChanges="orientation|keyboardHidden|keyboard|screenSize|smallestScreenSize|locale|layoutDirection|fontScale|screenLayout|density|uiMode"
            android:hardwareAccelerated="true"
            android:windowSoftInputMode="adjustResize">

            <intent-filter>
                <action android:name="android.intent.action.MAIN"/>
                <category android:name="android.intent.category.LAUNCHER"/>
            </intent-filter>
        </activity>

        <meta-data
            android:name="flutterEmbedding"
            android:value="2" />
    </application>
</manifest>
```

### 3.3 Créer l'icône de l'app

#### Option A : Utiliser flutter_launcher_icons (RECOMMANDÉ)

1. Ajoutez dans `/mathia_app/pubspec.yaml` :

```yaml
dev_dependencies:
  flutter_launcher_icons: ^0.13.1

flutter_launcher_icons:
  android: true
  image_path: "assets/icon/app_icon.png"  # Créez ce fichier (512x512px)
  adaptive_icon_foreground: "assets/icon/app_icon_foreground.png"
  adaptive_icon_background: "#0066FF"  # Couleur de fond
```

2. Placez votre logo dans `/mathia_app/assets/icon/app_icon.png` (512x512px)

3. Générez les icônes :

```bash
flutter pub get
flutter pub run flutter_launcher_icons
```

#### Option B : Manuellement avec Android Studio

1. Clic droit sur `/mathia_app/android/app/src/main/res/`
2. **New** → **Image Asset**
3. Sélectionnez votre image (1024x1024px)
4. Générez toutes les tailles

### 3.4 Créer une keystore pour signer l'APK

```bash
# Sur macOS/Linux
keytool -genkey -v -keystore ~/mathia-upload-keystore.jks -storetype JKS -keyalg RSA -keysize 2048 -validity 10000 -alias upload

# Sur Windows (PowerShell)
keytool -genkey -v -keystore $env:USERPROFILE\mathia-upload-keystore.jks -storetype JKS -keyalg RSA -keysize 2048 -validity 10000 -alias upload
```

**Remplissez** :
- Mot de passe du keystore : choisissez un mot de passe fort et **NOTEZ-LE**
- Nom et prénom : Votre nom
- Unité organisationnelle : Mathia
- Organisation : Votre société
- Ville, État, Pays : Vos informations

### 3.5 Configurer la signature de l'app

Créez `/mathia_app/android/key.properties` :

```properties
storePassword=VOTRE_MOT_DE_PASSE_KEYSTORE
keyPassword=VOTRE_MOT_DE_PASSE_KEYSTORE
keyAlias=upload
storeFile=/Users/vous/mathia-upload-keystore.jks
```

⚠️ **IMPORTANT** : Remplacez le chemin `storeFile` par le chemin absolu vers votre keystore.

Éditez `/mathia_app/android/app/build.gradle` :

```gradle
// AVANT android {
def keystoreProperties = new Properties()
def keystorePropertiesFile = rootProject.file('key.properties')
if (keystorePropertiesFile.exists()) {
    keystoreProperties.load(new FileInputStream(keystorePropertiesFile))
}

android {
    // ...

    signingConfigs {
        release {
            keyAlias keystoreProperties['keyAlias']
            keyPassword keystoreProperties['keyPassword']
            storeFile keystoreProperties['storeFile'] ? file(keystoreProperties['storeFile']) : null
            storePassword keystoreProperties['storePassword']
        }
    }

    buildTypes {
        release {
            signingConfig signingConfigs.release
            minifyEnabled true
            shrinkResources true
        }
    }
}
```

---

## 📦 ÉTAPE 4 : Construire l'APK/AAB (10 min)

### 4.1 Build pour le Play Store (AAB)

```bash
cd mathia_app

# Nettoyer le build précédent
flutter clean
flutter pub get

# Construire l'App Bundle (AAB) - OBLIGATOIRE pour Play Store
flutter build appbundle --release

# Le fichier sera généré ici :
# build/app/outputs/bundle/release/app-release.aab
```

### 4.2 Vérifier la taille de l'app

```bash
ls -lh build/app/outputs/bundle/release/app-release.aab

# Devrait être entre 15-30 MB
```

### 4.3 (OPTIONNEL) Build APK pour test

```bash
# APK pour installer directement sur un téléphone
flutter build apk --release

# Le fichier sera ici :
# build/app/outputs/flutter-apk/app-release.apk
```

---

## 🎮 ÉTAPE 5 : Créer une fiche Play Store (25 min)

### 5.1 Créer l'application sur Google Play Console

1. Allez sur [play.google.com/console](https://play.google.com/console)
2. Cliquez sur **Créer une application**
3. Remplissez :
   - **Nom** : Mathia - Révision de Maths
   - **Langue par défaut** : Français (France)
   - **Type** : Application
   - **Gratuite ou payante** : Gratuite
4. Acceptez les conditions

### 5.2 Remplir la fiche de l'application

#### Informations principales

1. **Catégorie** : Éducation
2. **Balises** : Mathématiques, Éducation, Collège, Révision

#### Description courte (max 80 caractères)

```
Révisez les maths du collège avec des exercices interactifs
```

#### Description complète (max 4000 caractères)

```
Mathia est l'application parfaite pour réviser les mathématiques du collège (6ème à 3ème) !

🎯 FONCTIONNALITÉS

✓ Des centaines d'exercices couvrant tout le programme
✓ Exercices interactifs : QCM, calcul, vrai/faux
✓ Explications détaillées pour chaque réponse
✓ Progression sauvegardée automatiquement
✓ Statistiques de réussite en temps réel
✓ Interface moderne et intuitive

📚 PROGRAMME COMPLET

• 6ème : Fractions, Géométrie, Décimaux
• 5ème : Calcul littéral, Aires et périmètres, Proportionnalité
• 4ème : Équations, Pythagore, Statistiques
• 3ème : Fonctions, Trigonométrie, Probabilités

🌟 POURQUOI CHOISIR MATHIA ?

- Contenu aligné sur le programme officiel français
- Exercices progressifs du facile au difficile
- Système de points et badges pour motiver
- Aucune publicité intrusive
- Fonctionne hors ligne une fois les cours téléchargés

🎓 PARFAIT POUR

- Réviser avant un contrôle
- S'entraîner pendant les vacances
- Approfondir un chapitre difficile
- Gagner en confiance en mathématiques

📈 SUIVEZ VOTRE PROGRESSION

Consultez vos statistiques détaillées :
- Taux de réussite par chapitre
- Temps passé sur chaque exercice
- Points gagnés et classement

Mathia rend les maths amusantes et accessibles à tous les collégiens !

🔒 CONFIDENTIALITÉ

Nous respectons votre vie privée. Toutes vos données sont sécurisées et ne sont jamais partagées avec des tiers.
```

### 5.3 Captures d'écran

Vous devez fournir **AU MINIMUM 2 captures**, **maximum 8** :

**Formats acceptés** :
- Téléphone : 16:9 ou 9:16
- Tablette (7 pouces) : 16:9 ou 9:16
- Tablette (10 pouces) : 16:9 ou 9:16

**Comment créer des captures** :

1. Lancez l'app dans un émulateur Flutter :
   ```bash
   flutter run
   ```

2. Capturez depuis l'émulateur (Android Studio) :
   - Utilisez l'outil **Camera** dans Android Studio
   - Ou utilisez `adb shell screencap -p /sdcard/screen.png`

3. **Captures recommandées** :
   - Écran de connexion
   - Liste des cours
   - Exercice QCM en cours
   - Résultat d'un exercice
   - Profil avec statistiques

### 5.4 Icône de l'application

- **Format** : PNG (32-bit)
- **Taille** : 512 x 512 pixels
- **Transparence** : Non autorisée (arrière-plan opaque)

### 5.5 Bannière (Feature Graphic)

- **Format** : PNG ou JPG
- **Taille** : 1024 x 500 pixels
- **Poids** : < 1 MB

**Astuce** : Utilisez Canva ou Figma pour créer une bannière attractive.

### 5.6 Coordonnées

- **Email de contact** : Votre email (sera visible publiquement)
- **Site web** : (optionnel) Votre site
- **Politique de confidentialité** : **OBLIGATOIRE** (voir section suivante)

---

## 🔒 ÉTAPE 6 : Politique de confidentialité (10 min)

### Option A : Générer avec un outil en ligne (RAPIDE)

1. Allez sur [app-privacy-policy-generator.firebaseapp.com](https://app-privacy-policy-generator.firebaseapp.com/)
2. Remplissez :
   - **Nom de l'app** : Mathia
   - **Email de contact** : Votre email
   - **Collecte de données** :
     - ✅ Email
     - ✅ Prénom/Nom
     - ✅ Progression (exercices)
   - **Services tiers** : Supabase (pour l'hébergement)
3. Cliquez sur **Generate**
4. Téléchargez le fichier HTML

### Option B : Héberger sur GitHub Pages (GRATUIT)

1. Créez un dépôt GitHub : `mathia-privacy-policy`
2. Ajoutez le fichier `index.html` avec votre politique
3. Activez GitHub Pages : **Settings** → **Pages** → **Source: main**
4. URL : `https://votre-username.github.io/mathia-privacy-policy/`

### Option C : Texte minimaliste

```markdown
# Politique de Confidentialité - Mathia

**Date de mise à jour** : [DATE]

## Collecte de données

Mathia collecte les données suivantes :
- Adresse email (pour l'authentification)
- Prénom et nom (pour la personnalisation)
- Progression des exercices (pour le suivi)

## Utilisation des données

Les données sont utilisées uniquement pour :
- Permettre l'authentification
- Sauvegarder la progression
- Afficher des statistiques personnalisées

## Hébergement

Les données sont hébergées sur Supabase (https://supabase.com) et
sont sécurisées par des protocoles SSL/TLS.

## Partage de données

Nous ne partageons JAMAIS vos données avec des tiers.

## Contact

Pour toute question : contact@mathia.app
```

Hébergez ce fichier sur n'importe quel service (GitHub Pages, Netlify, Vercel, etc.).

---

## 🚀 ÉTAPE 7 : Télécharger l'AAB sur Play Store (10 min)

### 7.1 Créer une version

1. Dans Google Play Console, allez dans **Production** → **Créer une version**
2. Cliquez sur **Télécharger** et sélectionnez `app-release.aab`
3. Attendez l'analyse automatique (1-2 min)

### 7.2 Remplir les notes de version

```
Version 1.0.0

🎉 Première version de Mathia !

✓ Centaines d'exercices de mathématiques
✓ Programme complet du collège (6ème à 3ème)
✓ Explications détaillées
✓ Suivi de progression
✓ Interface moderne et intuitive

Des questions ? Contactez-nous à contact@mathia.app
```

### 7.3 Soumettre pour examen

1. Cliquez sur **Enregistrer** puis **Examiner la version**
2. Vérifiez que tout est rempli (icône, captures, descriptions)
3. Cliquez sur **Commencer le déploiement en production**

⏱️ **Temps d'examen** : 1 à 7 jours (généralement 24-48h)

---

## ✅ ÉTAPE 8 : Checklist finale

Avant de soumettre, vérifiez :

### Application
- [ ] L'app se lance sans erreur
- [ ] L'inscription fonctionne
- [ ] La connexion fonctionne
- [ ] Les cours s'affichent correctement
- [ ] Les exercices fonctionnent
- [ ] Les statistiques se mettent à jour

### Play Store
- [ ] Nom de l'app défini
- [ ] Description courte (≤ 80 caractères)
- [ ] Description longue (bien formatée)
- [ ] Minimum 2 captures d'écran
- [ ] Icône 512x512px téléchargée
- [ ] Bannière 1024x500px téléchargée (optionnel)
- [ ] Catégorie sélectionnée
- [ ] Email de contact renseigné
- [ ] Politique de confidentialité (URL valide)
- [ ] Fichier AAB téléchargé
- [ ] Notes de version rédigées

### Technique
- [ ] Package name unique (com.mathia.app)
- [ ] versionCode = 1
- [ ] versionName = "1.0.0"
- [ ] Keystore sauvegardé en lieu sûr
- [ ] Mot de passe du keystore noté
- [ ] Fichier .env configuré avec vraies clés Supabase

---

## 🎉 Après la publication

### Une fois approuvée (1-7 jours)

1. **Partagez votre app** :
   ```
   https://play.google.com/store/apps/details?id=com.mathia.app
   ```

2. **Suivez les métriques** :
   - Installations
   - Désinstallations
   - Avis utilisateurs
   - Crashs

3. **Répondez aux avis** :
   - Remerciez les avis positifs
   - Résolvez les problèmes des avis négatifs

### Mises à jour futures

Pour publier une mise à jour :

1. Incrémentez `versionCode` et `versionName` dans `build.gradle`
   ```gradle
   versionCode 2           // Était 1
   versionName "1.0.1"     // Était 1.0.0
   ```

2. Rebuild l'AAB :
   ```bash
   flutter clean
   flutter build appbundle --release
   ```

3. Téléchargez sur Play Console → **Production** → **Créer une version**

---

## 🆘 Résolution de problèmes

### Erreur : "DexArchiveMergerException"

```bash
cd mathia_app/android
./gradlew clean
cd ../..
flutter clean
flutter pub get
flutter build appbundle --release
```

### Erreur : "Keystore not found"

Vérifiez que le chemin dans `key.properties` est **absolu** :
```properties
storeFile=/Users/VOUS/mathia-upload-keystore.jks  # Chemin absolu !
```

### L'app crash au démarrage

1. Vérifiez que le fichier `.env` existe et contient les bonnes clés Supabase
2. Vérifiez que Supabase est bien configuré (schéma créé)
3. Lancez `flutter run` pour voir les logs détaillés

### "Politique de confidentialité requise"

Vous devez fournir une URL publique. Utilisez GitHub Pages ou créez une page HTML simple sur n'importe quel hébergeur.

### Rejet pour "contenu inapproprié"

Assurez-vous que :
- Les captures d'écran sont claires
- La description ne contient pas de fautes
- L'icône est professionnelle

---

## 📞 Support

Pour toute question sur ce guide :
- **Documentation Flutter** : [flutter.dev/docs](https://flutter.dev/docs)
- **Documentation Supabase** : [supabase.com/docs](https://supabase.com/docs)
- **Play Console Help** : [support.google.com/googleplay](https://support.google.com/googleplay)

---

## 🎯 Récapitulatif des temps

| Étape | Durée estimée |
|-------|---------------|
| Configurer Supabase | 15 min |
| Configurer Flutter | 20 min |
| Configurer Play Store | 30 min |
| Build AAB | 10 min |
| Fiche Play Store | 25 min |
| Politique de confidentialité | 10 min |
| Télécharger AAB | 10 min |
| **TOTAL** | **~2 heures** |

+ 1-7 jours d'attente pour l'examen Google

---

**Bonne chance pour votre lancement ! 🚀**
