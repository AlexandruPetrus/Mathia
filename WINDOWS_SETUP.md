# 🪟 Configuration PostgreSQL sur Windows

Guide spécifique pour résoudre l'erreur de connexion PostgreSQL sur Windows.

## ❌ Erreur actuelle

```
ConnectionRefusedError [SequelizeConnectionRefusedError]
code: 'ECONNREFUSED'
```

**Signification** : PostgreSQL n'est pas accessible (pas installé ou pas démarré).

---

## ✅ Solution complète

### ÉTAPE 1 : Installer PostgreSQL

#### Option A : EDB Installer (recommandé)

1. **Télécharger** : https://www.postgresql.org/download/windows/
2. Cliquer sur **"Download the installer"** (lien EDB)
3. Choisir **PostgreSQL 16** (dernière version)
4. Télécharger le fichier `.exe`

#### Option B : Installer via Chocolatey

```powershell
# Dans PowerShell en administrateur
choco install postgresql
```

#### Installation

1. **Lancer l'installeur**
2. **Suivre l'assistant** :
   - Composants : Tout cocher (PostgreSQL Server, pgAdmin, Command Line Tools)
   - Dossier : Laisser par défaut (`C:\Program Files\PostgreSQL\16`)
   - **Port** : **5432** (IMPORTANT - ne pas changer)
   - **Mot de passe** : Choisir un mot de passe pour l'utilisateur `postgres` ⚠️ À RETENIR !
   - Locale : French, France
3. **Terminer** l'installation

---

### ÉTAPE 2 : Vérifier que PostgreSQL est démarré

#### Via Services Windows

1. Appuyer sur **Windows + R**
2. Taper **`services.msc`** et Entrée
3. Chercher **"postgresql-x64-16"** (ou version installée)
4. Si "Arrêté" → **Clic droit** → **Démarrer**
5. **Clic droit** → Propriétés → Type de démarrage : **Automatique**

#### Via PowerShell

```powershell
# Vérifier le statut
Get-Service -Name postgresql*

# Démarrer si nécessaire (PowerShell en admin)
Start-Service -Name postgresql-x64-16

# Ou via net start
net start postgresql-x64-16
```

#### Vérifier l'installation

```powershell
# Vérifier la version
psql --version
# Devrait afficher : psql (PostgreSQL) 16.x

# Vérifier le port
netstat -an | findstr :5432
# Devrait afficher : TCP    0.0.0.0:5432    0.0.0.0:0    LISTENING
```

---

### ÉTAPE 3 : Créer la base de données

```powershell
# Se connecter à PostgreSQL
psql -U postgres

# Entrer le mot de passe que vous avez défini lors de l'installation

# Une fois connecté (vous voyez postgres=#), créer la base :
CREATE DATABASE mathia;

# Vérifier
\l

# Vous devriez voir "mathia" dans la liste

# Quitter
\q
```

---

### ÉTAPE 4 : Créer le fichier .env

```powershell
# Dans PowerShell, à la racine du projet Mathia
@"
PORT=3000
DATABASE_URL=postgresql://postgres:VOTRE_MOT_DE_PASSE@localhost:5432/mathia
JWT_SECRET=super_secret_jwt_key_change_in_production
OPENAI_API_KEY=sk-xxxxxx
"@ | Out-File -FilePath .env -Encoding utf8
```

**⚠️ IMPORTANT** : Remplacez `VOTRE_MOT_DE_PASSE` par le mot de passe PostgreSQL que vous avez choisi lors de l'installation !

**Exemple** :
```env
DATABASE_URL=postgresql://postgres:monmotdepasse123@localhost:5432/mathia
```

#### Éditer le fichier .env

```powershell
# Ouvrir dans le bloc-notes
notepad .env

# Ou dans VS Code
code .env
```

**Le fichier doit contenir** :
```env
PORT=3000
DATABASE_URL=postgresql://postgres:VOTRE_VRAI_MOT_DE_PASSE@localhost:5432/mathia
JWT_SECRET=super_secret_jwt_key_change_in_production
OPENAI_API_KEY=sk-xxxxxx
```

---

### ÉTAPE 5 : Synchroniser la base de données

```powershell
npm run db:sync
```

**Sortie attendue** :
```
✅ Connexion à PostgreSQL établie avec succès
✅ Modèles synchronisés avec la base de données
```

---

### ÉTAPE 6 : Démarrer le serveur

```powershell
npm run dev
```

**Sortie attendue** :
```
✅ Connexion à PostgreSQL établie avec succès
✅ Modèles synchronisés avec la base de données
🚀 Serveur Mathia démarré avec succès
📍 URL: http://localhost:3000
```

🎉 **Ça fonctionne !**

---

## 🐛 Dépannage Windows

### ❌ "psql: command not found"

**Problème** : PostgreSQL n'est pas dans le PATH

**Solution** :
1. Ajouter PostgreSQL au PATH :
   - Windows + R → `sysdm.cpl` → Variables d'environnement
   - Path → Modifier
   - Ajouter : `C:\Program Files\PostgreSQL\16\bin`
   - OK → Redémarrer PowerShell

2. Ou utiliser le chemin complet :
```powershell
& "C:\Program Files\PostgreSQL\16\bin\psql.exe" -U postgres
```

### ❌ "password authentication failed"

**Problème** : Mauvais mot de passe dans .env

**Solution** :
1. Vérifier le mot de passe PostgreSQL
2. Modifier le fichier .env avec le bon mot de passe
3. Redémarrer le serveur

### ❌ "database 'mathia' does not exist"

**Problème** : Base de données pas créée

**Solution** :
```powershell
psql -U postgres -c "CREATE DATABASE mathia;"
```

### ❌ Port 5432 déjà utilisé

**Problème** : Une autre instance de PostgreSQL tourne

**Solution** :
```powershell
# Voir ce qui utilise le port
netstat -ano | findstr :5432

# Arrêter les autres services PostgreSQL
Get-Service postgresql* | Stop-Service
```

### ❌ "role 'user' does not exist"

**Problème** : Le .env utilise "user" au lieu de "postgres"

**Solution** : Modifier DATABASE_URL dans .env :
```env
DATABASE_URL=postgresql://postgres:votremotdepasse@localhost:5432/mathia
```

---

## 🎯 Commandes Windows spécifiques

### Gestion du service PostgreSQL

```powershell
# Statut
Get-Service postgresql*

# Démarrer
Start-Service postgresql-x64-16

# Arrêter
Stop-Service postgresql-x64-16

# Redémarrer
Restart-Service postgresql-x64-16

# Définir en automatique
Set-Service -Name postgresql-x64-16 -StartupType Automatic
```

### Se connecter à PostgreSQL

```powershell
# Méthode 1 : Via psql
psql -U postgres -d mathia

# Méthode 2 : Via pgAdmin
# Ouvrir pgAdmin 4 (installé avec PostgreSQL)
# Servers → PostgreSQL 16 → Databases → mathia
```

### Créer des cours de test

```powershell
# Depuis PowerShell
psql -U postgres -d mathia -c "
INSERT INTO courses (title, grade, chapter, description, \"createdAt\", \"updatedAt\")
VALUES 
  ('Les fractions', '6ème', 'Arithmétique', 'Apprendre les fractions', NOW(), NOW()),
  ('Géométrie', '6ème', 'Géométrie', 'Les formes géométriques', NOW(), NOW());
"
```

---

## ✅ Checklist Windows

- [ ] PostgreSQL installé (via EDB ou Chocolatey)
- [ ] Service PostgreSQL démarré
- [ ] Port 5432 accessible
- [ ] Base de données "mathia" créée
- [ ] Fichier .env créé et configuré avec le bon mot de passe
- [ ] Tables synchronisées (`npm run db:sync`)
- [ ] Serveur démarre sans erreur (`npm run dev`)

---

## 📝 Exemple complet de .env pour Windows

```env
PORT=3000
DATABASE_URL=postgresql://postgres:monmotdepasse123@localhost:5432/mathia
JWT_SECRET=dev_secret_key_for_local_testing_only_change_in_production
OPENAI_API_KEY=sk-xxxxxx
```

**Remplacez** :
- `monmotdepasse123` → Votre mot de passe PostgreSQL
- `sk-xxxxxx` → Votre clé OpenAI (optionnel)

---

## 🔧 Solution rapide (copier-coller)

```powershell
# 1. Démarrer PostgreSQL
Start-Service postgresql-x64-16

# 2. Créer la base de données
psql -U postgres -c "CREATE DATABASE mathia;"

# 3. Créer le .env (REMPLACEZ LE MOT DE PASSE !)
@"
PORT=3000
DATABASE_URL=postgresql://postgres:VOTRE_MOT_DE_PASSE_ICI@localhost:5432/mathia
JWT_SECRET=super_secret_jwt_key
OPENAI_API_KEY=sk-xxxxxx
"@ | Out-File -FilePath .env -Encoding utf8

# 4. Éditer le .env pour mettre le vrai mot de passe
notepad .env

# 5. Synchroniser
npm run db:sync

# 6. Démarrer
npm run dev
```

---

## 🆘 Si PostgreSQL n'est pas installé

### Installation rapide via Chocolatey

```powershell
# Dans PowerShell en ADMINISTRATEUR

# 1. Installer Chocolatey si pas déjà installé
Set-ExecutionPolicy Bypass -Scope Process -Force
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# 2. Installer PostgreSQL
choco install postgresql

# 3. Le mot de passe par défaut sera demandé
# Mot de passe : postgres (ou celui que vous choisissez)

# 4. Redémarrer PowerShell et continuer avec l'étape 2 ci-dessus
```

---

## ✅ Une fois PostgreSQL configuré

```powershell
npm run dev
```

Vous devriez voir :
```
✅ Connexion à PostgreSQL établie avec succès
✅ Modèles synchronisés avec la base de données
🚀 Serveur Mathia démarré avec succès
📍 URL: http://localhost:3000
```

🎉 **Problème résolu !**





