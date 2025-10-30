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

      // Attendre un peu que le trigger se déclenche
      await Future.delayed(const Duration(seconds: 1));
      
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
          .maybeSingle(); // Utiliser maybeSingle() au lieu de single()

      if (response == null) {
        throw Exception('Profil utilisateur non trouvé. L\'utilisateur existe-t-il dans la table public.users ?');
      }

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

