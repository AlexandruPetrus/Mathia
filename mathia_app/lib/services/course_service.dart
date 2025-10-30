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
      // Construction de la requête
      dynamic query = _supabase
          .from('courses')
          .select()
          .eq('is_published', true);

      // Ajouter les filtres optionnels
      if (grade != null) {
        query = query.eq('grade', grade);
      }
      if (topic != null) {
        query = query.eq('topic', topic);
      }
      if (difficulty != null) {
        query = query.eq('difficulty', difficulty);
      }

      // Ajouter l'ordre et exécuter
      final response = await query.order('order_num');
      
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

