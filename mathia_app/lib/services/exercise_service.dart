import 'package:supabase_flutter/supabase_flutter.dart';
import '../models/exercise_model.dart';

class ExerciseService {
  final SupabaseClient _supabase = Supabase.instance.client;

  // Récupérer tous les exercices d'un cours
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
          .eq('is_published', true)
          .single();

      return ExerciseModel.fromJson(response);
    } catch (e) {
      throw Exception('Erreur lors de la récupération de l\'exercice: $e');
    }
  }

  // Récupérer les exercices avec filtres
  Future<List<ExerciseModel>> getExercises({
    String? courseId,
    String? difficulty,
    String? type,
    int? limit,
  }) async {
    try {
      dynamic query = _supabase
          .from('exercises')
          .select()
          .eq('is_published', true);

      // Ajouter les filtres optionnels
      if (courseId != null) {
        query = query.eq('course_id', courseId);
      }
      if (difficulty != null) {
        query = query.eq('difficulty', difficulty);
      }
      if (type != null) {
        query = query.eq('type', type);
      }

      // Ajouter l'ordre et la limite
      query = query.order('order_num');
      if (limit != null) {
        query = query.limit(limit);
      }

      final response = await query;
      
      return (response as List)
          .map((json) => ExerciseModel.fromJson(json))
          .toList();
    } catch (e) {
      throw Exception('Erreur lors de la récupération des exercices: $e');
    }
  }

  // Récupérer le prochain exercice d'un cours
  Future<ExerciseModel?> getNextExercise(String courseId, int currentOrder) async {
    try {
      final response = await _supabase
          .from('exercises')
          .select()
          .eq('course_id', courseId)
          .eq('is_published', true)
          .gt('order_num', currentOrder)
          .order('order_num')
          .limit(1);

      if (response.isEmpty) {
        return null;
      }

      return ExerciseModel.fromJson(response.first);
    } catch (e) {
      throw Exception('Erreur lors de la récupération du prochain exercice: $e');
    }
  }

  // Récupérer l'exercice précédent d'un cours
  Future<ExerciseModel?> getPreviousExercise(String courseId, int currentOrder) async {
    try {
      final response = await _supabase
          .from('exercises')
          .select()
          .eq('course_id', courseId)
          .eq('is_published', true)
          .lt('order_num', currentOrder)
          .order('order_num', ascending: false)
          .limit(1);

      if (response.isEmpty) {
        return null;
      }

      return ExerciseModel.fromJson(response.first);
    } catch (e) {
      throw Exception('Erreur lors de la récupération de l\'exercice précédent: $e');
    }
  }

  // Compter les exercices d'un cours
  Future<int> getExerciseCount(String courseId) async {
    try {
      final response = await _supabase
          .from('exercises')
          .select('id')
          .eq('course_id', courseId)
          .eq('is_published', true);

      return (response as List).length;
    } catch (e) {
      throw Exception('Erreur lors du comptage des exercices: $e');
    }
  }

  // Récupérer les exercices par difficulté
  Future<Map<String, int>> getExerciseCountByDifficulty(String courseId) async {
    try {
      final response = await _supabase
          .from('exercises')
          .select('difficulty')
          .eq('course_id', courseId)
          .eq('is_published', true);

      final Map<String, int> counts = {};
      for (final item in response) {
        final difficulty = item['difficulty'] as String;
        counts[difficulty] = (counts[difficulty] ?? 0) + 1;
      }

      return counts;
    } catch (e) {
      throw Exception('Erreur lors du comptage par difficulté: $e');
    }
  }

  // Rechercher des exercices
  Future<List<ExerciseModel>> searchExercises(String query) async {
    try {
      final response = await _supabase
          .from('exercises')
          .select()
          .eq('is_published', true)
          .or('title.ilike.%$query%,description.ilike.%$query%,question.ilike.%$query%')
          .order('order_num');

      return (response as List)
          .map((json) => ExerciseModel.fromJson(json))
          .toList();
    } catch (e) {
      throw Exception('Erreur lors de la recherche: $e');
    }
  }
}
