# 📱 Intégration Supabase dans Flutter - Guide Complet

## 📋 Vue d'ensemble

Ce guide vous montre comment intégrer Supabase dans votre application Flutter Mathia pour remplacer l'API Express traditionnelle.

### Avantages de l'intégration Flutter + Supabase :
- ✅ **Code simplifié** - Appels API directs sans couche backend
- ✅ **Temps réel** - Mises à jour instantanées
- ✅ **Authentification native** - Gestion complète des utilisateurs
- ✅ **Type-safe** - Modèles Dart fortement typés
- ✅ **Offline-first** - Cache automatique
- ✅ **Performance** - Requêtes optimisées

---

## 🚀 Étape 1 : Installation

### 1.1 Ajouter les dépendances

Dans `mobile/pubspec.yaml` :

```yaml
dependencies:
  flutter:
    sdk: flutter
  
  # Supabase
  supabase_flutter: ^2.3.0
  
  # Utilitaires
  flutter_dotenv: ^5.1.0
  shared_preferences: ^2.2.2
  
  # UI (si pas déjà présents)
  flutter_svg: ^2.0.9
  google_fonts: ^6.1.0
```

### 1.2 Installer les packages

```bash
cd mobile
flutter pub get
```

---

## ⚙️ Étape 2 : Configuration

### 2.1 Créer le fichier .env

Dans `mobile/.env` :

```env
SUPABASE_URL=https://xxxxxxxx.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

⚠️ **Important** : Ajoutez `.env` à votre `.gitignore` !

### 2.2 Charger le fichier .env

Dans `mobile/pubspec.yaml`, ajoutez :

```yaml
flutter:
  assets:
    - .env
```

### 2.3 Initialiser Supabase

Dans `mobile/lib/main.dart` :

```dart
import 'package:flutter/material.dart';
import 'package:supabase_flutter/supabase_flutter.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  // Charger les variables d'environnement
  await dotenv.load(fileName: ".env");
  
  // Initialiser Supabase
  await Supabase.initialize(
    url: dotenv.env['SUPABASE_URL']!,
    anonKey: dotenv.env['SUPABASE_ANON_KEY']!,
    authOptions: const FlutterAuthClientOptions(
      authFlowType: AuthFlowType.pkce, // Plus sécurisé
    ),
    realtimeClientOptions: const RealtimeClientOptions(
      logLevel: RealtimeLogLevel.info,
    ),
  );
  
  runApp(const MyApp());
}

// Shortcut pour accéder au client Supabase
final supabase = Supabase.instance.client;
```

---

## 🏗️ Étape 3 : Structure du projet

Créez cette structure dans `mobile/lib/` :

```
lib/
├── main.dart
├── config/
│   └── supabase_config.dart      # Configuration centralisée
├── models/
│   ├── user_model.dart
│   ├── course_model.dart
│   ├── exercise_model.dart
│   └── attempt_model.dart
├── services/
│   ├── auth_service.dart          # Authentification
│   ├── course_service.dart        # Gestion des cours
│   ├── exercise_service.dart      # Gestion des exercices
│   └── stats_service.dart         # Statistiques
├── providers/
│   ├── auth_provider.dart         # State management auth
│   └── app_provider.dart          # State global
└── screens/
    ├── auth/
    │   ├── login_screen.dart
    │   └── register_screen.dart
    ├── home/
    │   └── home_screen.dart
    ├── courses/
    │   ├── course_list_screen.dart
    │   └── course_detail_screen.dart
    └── profile/
        └── profile_screen.dart
```

---

## 📦 Étape 4 : Créer les modèles

### 4.1 User Model (`lib/models/user_model.dart`)

```dart
class UserModel {
  final String id;
  final String username;
  final String? firstName;
  final String? lastName;
  final String email;
  final String grade;
  final String role;
  final int totalPoints;
  final bool isActive;
  final String? avatarUrl;
  final DateTime createdAt;

  UserModel({
    required this.id,
    required this.username,
    this.firstName,
    this.lastName,
    required this.email,
    required this.grade,
    required this.role,
    required this.totalPoints,
    required this.isActive,
    this.avatarUrl,
    required this.createdAt,
  });

  factory UserModel.fromJson(Map<String, dynamic> json) {
    return UserModel(
      id: json['id'] as String,
      username: json['username'] as String,
      firstName: json['first_name'] as String?,
      lastName: json['last_name'] as String?,
      email: json['email'] as String? ?? '',
      grade: json['grade'] as String,
      role: json['role'] as String,
      totalPoints: json['total_points'] as int? ?? 0,
      isActive: json['is_active'] as bool? ?? true,
      avatarUrl: json['avatar_url'] as String?,
      createdAt: DateTime.parse(json['created_at'] as String),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'username': username,
      'first_name': firstName,
      'last_name': lastName,
      'grade': grade,
      'role': role,
      'total_points': totalPoints,
      'is_active': isActive,
      'avatar_url': avatarUrl,
    };
  }

  String get fullName => '${firstName ?? ''} ${lastName ?? ''}'.trim();
}
```

### 4.2 Course Model (`lib/models/course_model.dart`)

```dart
class CourseModel {
  final String id;
  final String title;
  final String description;
  final String content;
  final String grade;
  final String topic;
  final String difficulty;
  final int? duration;
  final bool isPublished;
  final String? thumbnailUrl;
  final DateTime createdAt;

  CourseModel({
    required this.id,
    required this.title,
    required this.description,
    required this.content,
    required this.grade,
    required this.topic,
    required this.difficulty,
    this.duration,
    required this.isPublished,
    this.thumbnailUrl,
    required this.createdAt,
  });

  factory CourseModel.fromJson(Map<String, dynamic> json) {
    return CourseModel(
      id: json['id'] as String,
      title: json['title'] as String,
      description: json['description'] as String,
      content: json['content'] as String,
      grade: json['grade'] as String,
      topic: json['topic'] as String,
      difficulty: json['difficulty'] as String,
      duration: json['duration'] as int?,
      isPublished: json['is_published'] as bool? ?? false,
      thumbnailUrl: json['thumbnail_url'] as String?,
      createdAt: DateTime.parse(json['created_at'] as String),
    );
  }

  String get difficultyEmoji {
    switch (difficulty) {
      case 'facile':
        return '🟢';
      case 'moyen':
        return '🟡';
      case 'difficile':
        return '🔴';
      default:
        return '⚪';
    }
  }
}
```

### 4.3 Exercise Model (`lib/models/exercise_model.dart`)

```dart
class ExerciseModel {
  final String id;
  final String courseId;
  final String title;
  final String? description;
  final String question;
  final String answer;
  final String? explanation;
  final String difficulty;
  final int points;
  final String type;
  final List<String> hints;
  final Map<String, dynamic>? options;
  final bool isPublished;

  ExerciseModel({
    required this.id,
    required this.courseId,
    required this.title,
    this.description,
    required this.question,
    required this.answer,
    this.explanation,
    required this.difficulty,
    required this.points,
    required this.type,
    required this.hints,
    this.options,
    required this.isPublished,
  });

  factory ExerciseModel.fromJson(Map<String, dynamic> json) {
    return ExerciseModel(
      id: json['id'] as String,
      courseId: json['course_id'] as String,
      title: json['title'] as String,
      description: json['description'] as String?,
      question: json['question'] as String,
      answer: json['answer'] as String,
      explanation: json['explanation'] as String?,
      difficulty: json['difficulty'] as String,
      points: json['points'] as int? ?? 10,
      type: json['type'] as String,
      hints: (json['hints'] as List<dynamic>?)?.cast<String>() ?? [],
      options: json['options'] as Map<String, dynamic>?,
      isPublished: json['is_published'] as bool? ?? true,
    );
  }

  bool get isQCM => type == 'qcm';
  bool get hasHints => hints.isNotEmpty;
}
```

### 4.4 Attempt Model (`lib/models/attempt_model.dart`)

```dart
class AttemptModel {
  final String id;
  final String userId;
  final String exerciseId;
  final String userAnswer;
  final bool isCorrect;
  final int pointsEarned;
  final int? timeSpent;
  final int hintsUsed;
  final String? feedback;
  final DateTime createdAt;

  AttemptModel({
    required this.id,
    required this.userId,
    required this.exerciseId,
    required this.userAnswer,
    required this.isCorrect,
    required this.pointsEarned,
    this.timeSpent,
    required this.hintsUsed,
    this.feedback,
    required this.createdAt,
  });

  factory AttemptModel.fromJson(Map<String, dynamic> json) {
    return AttemptModel(
      id: json['id'] as String,
      userId: json['user_id'] as String,
      exerciseId: json['exercise_id'] as String,
      userAnswer: json['user_answer'] as String,
      isCorrect: json['is_correct'] as bool,
      pointsEarned: json['points_earned'] as int? ?? 0,
      timeSpent: json['time_spent'] as int?,
      hintsUsed: json['hints_used'] as int? ?? 0,
      feedback: json['feedback'] as String?,
      createdAt: DateTime.parse(json['created_at'] as String),
    );
  }
}
```

---

## 🔐 Étape 5 : Service d'authentification

Créez `lib/services/auth_service.dart` :

```dart
import 'package:supabase_flutter/supabase_flutter.dart';
import '../models/user_model.dart';

class AuthService {
  final SupabaseClient _supabase = Supabase.instance.client;

  // Obtenir l'utilisateur actuel
  User? get currentUser => _supabase.auth.currentUser;
  
  // Stream d'authentification
  Stream<AuthState> get authStateChanges => _supabase.auth.onAuthStateChange;

  // Inscription
  Future<UserModel> signUp({
    required String email,
    required String password,
    required String username,
    required String firstName,
    required String lastName,
    required String grade,
  }) async {
    try {
      final response = await _supabase.auth.signUp(
        email: email,
        password: password,
        data: {
          'username': username,
          'first_name': firstName,
          'last_name': lastName,
          'grade': grade,
          'role': 'student',
        },
      );

      if (response.user == null) {
        throw Exception('Erreur lors de l\'inscription');
      }

      // Récupérer le profil créé automatiquement
      final profile = await getUserProfile(response.user!.id);
      return profile;
    } catch (e) {
      throw Exception('Erreur d\'inscription: $e');
    }
  }

  // Connexion
  Future<UserModel> signIn({
    required String email,
    required String password,
  }) async {
    try {
      final response = await _supabase.auth.signInWithPassword(
        email: email,
        password: password,
      );

      if (response.user == null) {
        throw Exception('Email ou mot de passe incorrect');
      }

      final profile = await getUserProfile(response.user!.id);
      return profile;
    } catch (e) {
      throw Exception('Erreur de connexion: $e');
    }
  }

  // Déconnexion
  Future<void> signOut() async {
    await _supabase.auth.signOut();
  }

  // Récupérer le profil utilisateur
  Future<UserModel> getUserProfile(String userId) async {
    try {
      final response = await _supabase
          .from('users')
          .select()
          .eq('id', userId)
          .single();

      return UserModel.fromJson(response);
    } catch (e) {
      throw Exception('Erreur lors de la récupération du profil: $e');
    }
  }

  // Mettre à jour le profil
  Future<UserModel> updateProfile({
    required String userId,
    String? firstName,
    String? lastName,
    String? grade,
    String? avatarUrl,
  }) async {
    try {
      final updates = <String, dynamic>{};
      if (firstName != null) updates['first_name'] = firstName;
      if (lastName != null) updates['last_name'] = lastName;
      if (grade != null) updates['grade'] = grade;
      if (avatarUrl != null) updates['avatar_url'] = avatarUrl;

      await _supabase
          .from('users')
          .update(updates)
          .eq('id', userId);

      return await getUserProfile(userId);
    } catch (e) {
      throw Exception('Erreur lors de la mise à jour: $e');
    }
  }

  // Réinitialiser le mot de passe
  Future<void> resetPassword(String email) async {
    try {
      await _supabase.auth.resetPasswordForEmail(email);
    } catch (e) {
      throw Exception('Erreur lors de la réinitialisation: $e');
    }
  }
}
```

---

## 📚 Étape 6 : Service des cours

Créez `lib/services/course_service.dart` :

```dart
import 'package:supabase_flutter/supabase_flutter.dart';
import '../models/course_model.dart';

class CourseService {
  final SupabaseClient _supabase = Supabase.instance.client;

  // Récupérer tous les cours
  Future<List<CourseModel>> getCourses({
    String? grade,
    String? topic,
    String? difficulty,
  }) async {
    try {
      var query = _supabase
          .from('courses')
          .select()
          .eq('is_published', true)
          .order('order_num');

      if (grade != null) query = query.eq('grade', grade);
      if (topic != null) query = query.eq('topic', topic);
      if (difficulty != null) query = query.eq('difficulty', difficulty);

      final response = await query;
      return (response as List)
          .map((json) => CourseModel.fromJson(json))
          .toList();
    } catch (e) {
      throw Exception('Erreur lors de la récupération des cours: $e');
    }
  }

  // Récupérer un cours par ID
  Future<CourseModel> getCourseById(String courseId) async {
    try {
      final response = await _supabase
          .from('courses')
          .select()
          .eq('id', courseId)
          .single();

      return CourseModel.fromJson(response);
    } catch (e) {
      throw Exception('Erreur lors de la récupération du cours: $e');
    }
  }

  // Rechercher des cours
  Future<List<CourseModel>> searchCourses(String query) async {
    try {
      final response = await _supabase.rpc(
        'search_courses',
        params: {'search_query': query},
      );

      return (response as List)
          .map((json) => CourseModel.fromJson(json))
          .toList();
    } catch (e) {
      throw Exception('Erreur de recherche: $e');
    }
  }

  // Cours populaires
  Future<List<CourseModel>> getPopularCourses({
    String? grade,
    int limit = 10,
  }) async {
    try {
      final response = await _supabase.rpc(
        'get_popular_courses',
        params: {
          'grade_filter': grade,
          'limit_count': limit,
        },
      );

      return (response as List)
          .map((json) => CourseModel.fromJson(json))
          .toList();
    } catch (e) {
      throw Exception('Erreur lors de la récupération des cours populaires: $e');
    }
  }

  // Ajouter aux favoris
  Future<void> addToFavorites(String courseId) async {
    try {
      await _supabase.from('favorites').insert({
        'user_id': _supabase.auth.currentUser!.id,
        'course_id': courseId,
      });
    } catch (e) {
      throw Exception('Erreur lors de l\'ajout aux favoris: $e');
    }
  }

  // Retirer des favoris
  Future<void> removeFromFavorites(String courseId) async {
    try {
      await _supabase
          .from('favorites')
          .delete()
          .eq('user_id', _supabase.auth.currentUser!.id)
          .eq('course_id', courseId);
    } catch (e) {
      throw Exception('Erreur lors de la suppression des favoris: $e');
    }
  }

  // Vérifier si un cours est favori
  Future<bool> isFavorite(String courseId) async {
    try {
      final response = await _supabase
          .from('favorites')
          .select()
          .eq('user_id', _supabase.auth.currentUser!.id)
          .eq('course_id', courseId);

      return response.isNotEmpty;
    } catch (e) {
      return false;
    }
  }
}
```

---

## 📝 Étape 7 : Service des exercices

Créez `lib/services/exercise_service.dart` :

```dart
import 'package:supabase_flutter/supabase_flutter.dart';
import '../models/exercise_model.dart';
import '../models/attempt_model.dart';

class ExerciseService {
  final SupabaseClient _supabase = Supabase.instance.client;

  // Récupérer les exercices d'un cours
  Future<List<ExerciseModel>> getExercisesByCourse(String courseId) async {
    try {
      final response = await _supabase
          .from('exercises')
          .select()
          .eq('course_id', courseId)
          .eq('is_published', true)
          .order('order_num');

      return (response as List)
          .map((json) => ExerciseModel.fromJson(json))
          .toList();
    } catch (e) {
      throw Exception('Erreur lors de la récupération des exercices: $e');
    }
  }

  // Récupérer un exercice par ID
  Future<ExerciseModel> getExerciseById(String exerciseId) async {
    try {
      final response = await _supabase
          .from('exercises')
          .select()
          .eq('id', exerciseId)
          .single();

      return ExerciseModel.fromJson(response);
    } catch (e) {
      throw Exception('Erreur lors de la récupération de l\'exercice: $e');
    }
  }

  // Soumettre une tentative
  Future<Map<String, dynamic>> submitAttempt({
    required String exerciseId,
    required String userAnswer,
    int? timeSpent,
    int hintsUsed = 0,
  }) async {
    try {
      final response = await _supabase.rpc(
        'submit_attempt',
        params: {
          'p_exercise_id': exerciseId,
          'p_user_answer': userAnswer,
          'p_time_spent': timeSpent,
          'p_hints_used': hintsUsed,
        },
      );

      return response[0] as Map<String, dynamic>;
    } catch (e) {
      throw Exception('Erreur lors de la soumission: $e');
    }
  }

  // Récupérer les tentatives de l'utilisateur
  Future<List<AttemptModel>> getMyAttempts({String? exerciseId}) async {
    try {
      var query = _supabase
          .from('attempts')
          .select()
          .eq('user_id', _supabase.auth.currentUser!.id)
          .order('created_at', ascending: false);

      if (exerciseId != null) {
        query = query.eq('exercise_id', exerciseId);
      }

      final response = await query;
      return (response as List)
          .map((json) => AttemptModel.fromJson(json))
          .toList();
    } catch (e) {
      throw Exception('Erreur lors de la récupération des tentatives: $e');
    }
  }

  // Exercices recommandés
  Future<List<ExerciseModel>> getRecommendedExercises({int limit = 5}) async {
    try {
      final response = await _supabase.rpc(
        'get_recommended_exercises',
        params: {
          'user_uuid': _supabase.auth.currentUser!.id,
          'limit_count': limit,
        },
      );

      return (response as List)
          .map((json) => ExerciseModel.fromJson(json))
          .toList();
    } catch (e) {
      throw Exception('Erreur lors de la récupération des recommandations: $e');
    }
  }
}
```

---

## 📊 Étape 8 : Service des statistiques

Créez `lib/services/stats_service.dart` :

```dart
import 'package:supabase_flutter/supabase_flutter.dart';

class StatsService {
  final SupabaseClient _supabase = Supabase.instance.client;

  // Statistiques de l'utilisateur
  Future<Map<String, dynamic>> getMyStats() async {
    try {
      final response = await _supabase.rpc('get_my_stats');
      return response[0] as Map<String, dynamic>;
    } catch (e) {
      throw Exception('Erreur lors de la récupération des stats: $e');
    }
  }

  // Progression dans un cours
  Future<Map<String, dynamic>> getCourseProgress(String courseId) async {
    try {
      final response = await _supabase.rpc(
        'get_user_course_progress',
        params: {
          'user_uuid': _supabase.auth.currentUser!.id,
          'course_uuid': courseId,
        },
      );

      return response[0] as Map<String, dynamic>;
    } catch (e) {
      throw Exception('Erreur lors de la récupération de la progression: $e');
    }
  }

  // Leaderboard
  Future<List<Map<String, dynamic>>> getLeaderboard({
    String? grade,
    int limit = 10,
  }) async {
    try {
      final response = await _supabase.rpc(
        'get_leaderboard',
        params: {
          'grade_filter': grade,
          'limit_count': limit,
        },
      );

      return (response as List).cast<Map<String, dynamic>>();
    } catch (e) {
      throw Exception('Erreur lors de la récupération du classement: $e');
    }
  }

  // Achievements
  Future<List<Map<String, dynamic>>> getMyAchievements() async {
    try {
      final response = await _supabase.rpc(
        'get_user_achievements',
        params: {'user_uuid': _supabase.auth.currentUser!.id},
      );

      return (response as List).cast<Map<String, dynamic>>();
    } catch (e) {
      throw Exception('Erreur lors de la récupération des achievements: $e');
    }
  }
}
```

---

## 🎯 Étape 9 : Exemples d'utilisation

### 9.1 Écran de connexion

```dart
import 'package:flutter/material.dart';
import '../services/auth_service.dart';

class LoginScreen extends StatefulWidget {
  @override
  _LoginScreenState createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final _authService = AuthService();
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  bool _isLoading = false;

  Future<void> _signIn() async {
    setState(() => _isLoading = true);
    
    try {
      await _authService.signIn(
        email: _emailController.text.trim(),
        password: _passwordController.text,
      );
      
      // Navigation vers l'écran principal
      Navigator.pushReplacementNamed(context, '/home');
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Erreur: $e')),
      );
    } finally {
      setState(() => _isLoading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Padding(
        padding: EdgeInsets.all(16),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            TextField(
              controller: _emailController,
              decoration: InputDecoration(labelText: 'Email'),
              keyboardType: TextInputType.emailAddress,
            ),
            SizedBox(height: 16),
            TextField(
              controller: _passwordController,
              decoration: InputDecoration(labelText: 'Mot de passe'),
              obscureText: true,
            ),
            SizedBox(height: 24),
            _isLoading
                ? CircularProgressIndicator()
                : ElevatedButton(
                    onPressed: _signIn,
                    child: Text('Se connecter'),
                  ),
          ],
        ),
      ),
    );
  }
}
```

### 9.2 Afficher la liste des cours

```dart
import 'package:flutter/material.dart';
import '../services/course_service.dart';
import '../models/course_model.dart';

class CourseListScreen extends StatefulWidget {
  @override
  _CourseListScreenState createState() => _CourseListScreenState();
}

class _CourseListScreenState extends State<CourseListScreen> {
  final _courseService = CourseService();
  List<CourseModel> _courses = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadCourses();
  }

  Future<void> _loadCourses() async {
    try {
      final courses = await _courseService.getCourses();
      setState(() {
        _courses = courses;
        _isLoading = false;
      });
    } catch (e) {
      setState(() => _isLoading = false);
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Erreur: $e')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_isLoading) {
      return Center(child: CircularProgressIndicator());
    }

    return ListView.builder(
      itemCount: _courses.length,
      itemBuilder: (context, index) {
        final course = _courses[index];
        return ListTile(
          leading: Text(course.difficultyEmoji, style: TextStyle(fontSize: 24)),
          title: Text(course.title),
          subtitle: Text('${course.grade} • ${course.topic}'),
          onTap: () {
            Navigator.pushNamed(
              context,
              '/course-detail',
              arguments: course.id,
            );
          },
        );
      },
    );
  }
}
```

---

## 🔔 Étape 10 : Temps réel (optionnel)

Pour écouter les changements en temps réel :

```dart
// Écouter les nouveaux cours
_supabase
    .from('courses')
    .stream(primaryKey: ['id'])
    .eq('is_published', true)
    .listen((List<Map<String, dynamic>> data) {
      setState(() {
        _courses = data.map((json) => CourseModel.fromJson(json)).toList();
      });
    });

// Écouter les mises à jour de points
_supabase
    .from('users')
    .stream(primaryKey: ['id'])
    .eq('id', _supabase.auth.currentUser!.id)
    .listen((List<Map<String, dynamic>> data) {
      // Mettre à jour l'UI avec les nouveaux points
    });
```

---

## ✅ Checklist de migration

- [ ] Installer `supabase_flutter`
- [ ] Créer le fichier `.env` avec les clés
- [ ] Initialiser Supabase dans `main.dart`
- [ ] Créer les modèles de données
- [ ] Créer les services (auth, courses, exercises, stats)
- [ ] Mettre à jour les écrans pour utiliser les services
- [ ] Tester l'authentification
- [ ] Tester les cours et exercices
- [ ] Tester la soumission de tentatives
- [ ] Implémenter les statistiques
- [ ] Ajouter le temps réel (optionnel)
- [ ] Supprimer l'ancien code HTTP

---

## 🎉 Résultat

Vous avez maintenant une application Flutter moderne qui :
- ✅ Communique directement avec Supabase
- ✅ Gère l'authentification nativement
- ✅ Bénéficie de Row Level Security
- ✅ Peut utiliser le temps réel
- ✅ A des modèles fortement typés
- ✅ Est plus simple et maintenable

**Plus besoin de backend Express pour le CRUD !** 🎊

---

Créé avec ❤️ pour Mathia




