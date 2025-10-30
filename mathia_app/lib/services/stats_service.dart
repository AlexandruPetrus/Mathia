import 'package:supabase_flutter/supabase_flutter.dart';
import '../models/attempt_model.dart';

class StatsService {
  final SupabaseClient _supabase = Supabase.instance.client;

  // Récupérer les statistiques générales d'un utilisateur
  Future<Map<String, dynamic>> getUserStats(String userId) async {
    try {
      // Total des points
      final pointsResponse = await _supabase
          .from('users')
          .select('total_points')
          .eq('id', userId)
          .single();

      // Total des tentatives
      final attemptsResponse = await _supabase
          .from('attempts')
          .select('id')
          .eq('user_id', userId);

      // Tentatives réussies
      final successfulResponse = await _supabase
          .from('attempts')
          .select('id')
          .eq('user_id', userId)
          .eq('is_correct', true);

      // Moyenne du temps par exercice
      final avgTimeResponse = await _supabase
          .from('attempts')
          .select('time_spent')
          .eq('user_id', userId)
          .eq('is_correct', true);

      final totalAttempts = (attemptsResponse as List).length;
      final successfulAttempts = (successfulResponse as List).length;
      final successRate = totalAttempts > 0 ? (successfulAttempts / totalAttempts) * 100 : 0.0;

      // Calculer la moyenne du temps
      double avgTime = 0.0;
      if (avgTimeResponse.isNotEmpty) {
        final totalTime = avgTimeResponse
            .map((item) => item['time_spent'] as int)
            .reduce((a, b) => a + b);
        avgTime = totalTime / avgTimeResponse.length;
      }

      return {
        'totalPoints': pointsResponse['total_points'] ?? 0,
        'totalAttempts': totalAttempts,
        'successfulAttempts': successfulAttempts,
        'successRate': successRate.round(),
        'averageTime': avgTime.round(),
      };
    } catch (e) {
      throw Exception('Erreur lors de la récupération des statistiques: $e');
    }
  }

  // Récupérer les statistiques par cours
  Future<Map<String, dynamic>> getCourseStats(String userId, String courseId) async {
    try {
      // Tentatives dans ce cours
      final exerciseIds = await _getExerciseIdsForCourse(courseId);
      if (exerciseIds.isEmpty) {
        return {
          'totalAttempts': 0,
          'successfulAttempts': 0,
          'successRate': 0.0,
          'totalPoints': 0,
          'averageTime': 0.0,
        };
      }
      
      final attemptsResponse = await _supabase
          .from('attempts')
          .select('id, is_correct, time_spent, points_earned, exercise_id')
          .eq('user_id', userId);

      // Filtrer les tentatives pour ce cours
      final courseAttempts = (attemptsResponse as List)
          .where((attempt) => exerciseIds.contains(attempt['exercise_id']))
          .toList();

      final totalAttempts = courseAttempts.length;
      final successfulAttempts = courseAttempts.where((a) => a['is_correct'] == true).length;
      final successRate = totalAttempts > 0 ? (successfulAttempts / totalAttempts) * 100 : 0.0;

      // Points gagnés dans ce cours
      final totalPoints = courseAttempts
          .map((a) => a['points_earned'] as int)
          .fold(0, (sum, points) => sum + points);

      // Temps moyen
      double avgTime = 0.0;
      if (courseAttempts.isNotEmpty) {
        final totalTime = courseAttempts
            .map((a) => a['time_spent'] as int)
            .reduce((a, b) => a + b);
        avgTime = totalTime / courseAttempts.length;
      }

      return {
        'totalAttempts': totalAttempts,
        'successfulAttempts': successfulAttempts,
        'successRate': successRate.round(),
        'totalPoints': totalPoints,
        'averageTime': avgTime.round(),
      };
    } catch (e) {
      throw Exception('Erreur lors de la récupération des statistiques du cours: $e');
    }
  }

  // Récupérer l'historique des tentatives
  Future<List<AttemptModel>> getAttemptHistory({
    required String userId,
    String? courseId,
    String? exerciseId,
    int? limit,
  }) async {
    try {
      dynamic query = _supabase
          .from('attempts')
          .select()
          .eq('user_id', userId)
          .order('created_at', ascending: false);

      if (courseId != null) {
        final exerciseIds = await _getExerciseIdsForCourse(courseId);
        if (exerciseIds.isEmpty) {
          // Si aucun exercice trouvé, retourner une liste vide
          return [];
        }
        // Pour les exercices de ce cours, on va filtrer après récupération
        // car Supabase Flutter ne supporte pas bien in_ avec des listes dynamiques
      }

      if (exerciseId != null) {
        query = query.eq('exercise_id', exerciseId);
      }

      if (limit != null) {
        query = query.limit(limit);
      }

      final response = await query;
      
      List<AttemptModel> attempts = (response as List)
          .map((json) => AttemptModel.fromJson(json))
          .toList();

      // Filtrer par cours si nécessaire
      if (courseId != null) {
        final exerciseIds = await _getExerciseIdsForCourse(courseId);
        attempts = attempts.where((attempt) => exerciseIds.contains(attempt.exerciseId)).toList();
      }
      
      return attempts;
    } catch (e) {
      throw Exception('Erreur lors de la récupération de l\'historique: $e');
    }
  }

  // Récupérer les statistiques par difficulté
  Future<Map<String, Map<String, dynamic>>> getStatsByDifficulty(String userId) async {
    try {
      final response = await _supabase
          .from('attempts')
          .select('''
            is_correct,
            time_spent,
            points_earned,
            exercises!inner(difficulty)
          ''')
          .eq('user_id', userId);

      final Map<String, List<Map<String, dynamic>>> groupedByDifficulty = {};
      
      for (final item in response) {
        final difficulty = item['exercises']['difficulty'] as String;
        if (!groupedByDifficulty.containsKey(difficulty)) {
          groupedByDifficulty[difficulty] = [];
        }
        groupedByDifficulty[difficulty]!.add(item);
      }

      final Map<String, Map<String, dynamic>> result = {};
      
      for (final entry in groupedByDifficulty.entries) {
        final difficulty = entry.key;
        final attempts = entry.value;
        
        final totalAttempts = attempts.length;
        final successfulAttempts = attempts.where((a) => a['is_correct'] == true).length;
        final successRate = totalAttempts > 0 ? (successfulAttempts / totalAttempts) * 100 : 0.0;
        
        final totalPoints = attempts
            .map((a) => a['points_earned'] as int)
            .fold(0, (sum, points) => sum + points);
        
        final avgTime = attempts.isNotEmpty 
            ? attempts.map((a) => a['time_spent'] as int).reduce((a, b) => a + b) / attempts.length
            : 0.0;

        result[difficulty] = {
          'totalAttempts': totalAttempts,
          'successfulAttempts': successfulAttempts,
          'successRate': successRate.round(),
          'totalPoints': totalPoints,
          'averageTime': avgTime.round(),
        };
      }

      return result;
    } catch (e) {
      throw Exception('Erreur lors de la récupération des statistiques par difficulté: $e');
    }
  }

  // Récupérer le classement des utilisateurs
  Future<List<Map<String, dynamic>>> getLeaderboard({int limit = 10}) async {
    try {
      final response = await _supabase
          .from('users')
          .select('username, first_name, last_name, total_points, grade')
          .eq('is_active', true)
          .order('total_points', ascending: false)
          .limit(limit);

      return (response as List).cast<Map<String, dynamic>>();
    } catch (e) {
      throw Exception('Erreur lors de la récupération du classement: $e');
    }
  }

  // Méthode helper pour récupérer les IDs des exercices d'un cours
  Future<List<String>> _getExerciseIdsForCourse(String courseId) async {
    final response = await _supabase
        .from('exercises')
        .select('id')
        .eq('course_id', courseId);

    return (response as List).map((item) => item['id'] as String).toList();
  }

  // Récupérer les progrès quotidiens
  Future<List<Map<String, dynamic>>> getDailyProgress(String userId, {int days = 7}) async {
    try {
      final endDate = DateTime.now();
      final startDate = endDate.subtract(Duration(days: days));

      final response = await _supabase
          .from('attempts')
          .select('created_at, is_correct, points_earned')
          .eq('user_id', userId)
          .gte('created_at', startDate.toIso8601String())
          .lte('created_at', endDate.toIso8601String())
          .order('created_at');

      // Grouper par jour
      final Map<String, List<Map<String, dynamic>>> groupedByDay = {};
      
      for (final item in response) {
        final date = DateTime.parse(item['created_at'] as String).toIso8601String().split('T')[0];
        if (!groupedByDay.containsKey(date)) {
          groupedByDay[date] = [];
        }
        groupedByDay[date]!.add(item);
      }

      final List<Map<String, dynamic>> result = [];
      
      for (int i = 0; i < days; i++) {
        final date = endDate.subtract(Duration(days: i));
        final dateStr = date.toIso8601String().split('T')[0];
        
        final attempts = groupedByDay[dateStr] ?? [];
        final successfulAttempts = attempts.where((a) => a['is_correct'] == true).length;
        final totalPoints = attempts.map((a) => a['points_earned'] as int).fold(0, (sum, p) => sum + p);

        result.add({
          'date': dateStr,
          'attempts': attempts.length,
          'successfulAttempts': successfulAttempts,
          'points': totalPoints,
        });
      }

      return result.reversed.toList(); // Du plus ancien au plus récent
    } catch (e) {
      throw Exception('Erreur lors de la récupération des progrès quotidiens: $e');
    }
  }
}
