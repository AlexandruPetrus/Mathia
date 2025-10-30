import 'package:supabase_flutter/supabase_flutter.dart';

class AttemptModel {
  final String id;
  final String userId;
  final String exerciseId;
  final String? userAnswer;
  final bool isCorrect;
  final int timeSpent; // en secondes
  final int pointsEarned;
  final DateTime startedAt;
  final DateTime? completedAt;
  final DateTime createdAt;
  final DateTime updatedAt;

  AttemptModel({
    required this.id,
    required this.userId,
    required this.exerciseId,
    this.userAnswer,
    required this.isCorrect,
    required this.timeSpent,
    required this.pointsEarned,
    required this.startedAt,
    this.completedAt,
    required this.createdAt,
    required this.updatedAt,
  });

  factory AttemptModel.fromJson(Map<String, dynamic> json) {
    return AttemptModel(
      id: json['id'] as String,
      userId: json['user_id'] as String,
      exerciseId: json['exercise_id'] as String,
      userAnswer: json['user_answer'] as String?,
      isCorrect: json['is_correct'] as bool,
      timeSpent: json['time_spent'] as int,
      pointsEarned: json['points_earned'] as int,
      startedAt: DateTime.parse(json['started_at'] as String),
      completedAt: json['completed_at'] != null 
          ? DateTime.parse(json['completed_at'] as String)
          : null,
      createdAt: DateTime.parse(json['created_at'] as String),
      updatedAt: DateTime.parse(json['updated_at'] as String),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'user_id': userId,
      'exercise_id': exerciseId,
      'user_answer': userAnswer,
      'is_correct': isCorrect,
      'time_spent': timeSpent,
      'points_earned': pointsEarned,
      'started_at': startedAt.toIso8601String(),
      'completed_at': completedAt?.toIso8601String(),
      'created_at': createdAt.toIso8601String(),
      'updated_at': updatedAt.toIso8601String(),
    };
  }

  // Méthodes utilitaires
  bool get isCompleted => completedAt != null;
  
  // Durée formatée (ex: "1 min 30s")
  String get formattedTimeSpent {
    if (timeSpent < 60) {
      return '${timeSpent}s';
    } else {
      final minutes = timeSpent ~/ 60;
      final seconds = timeSpent % 60;
      if (seconds == 0) {
        return '${minutes} min';
      } else {
        return '${minutes} min ${seconds}s';
      }
    }
  }

  // Statut de l'exercice
  String get status {
    if (!isCompleted) {
      return 'En cours';
    } else if (isCorrect) {
      return 'Réussi';
    } else {
      return 'Échoué';
    }
  }

  // Emoji pour le statut
  String get statusEmoji {
    if (!isCompleted) {
      return '⏳';
    } else if (isCorrect) {
      return '✅';
    } else {
      return '❌';
    }
  }

  // Pourcentage de réussite (1 = 100%)
  double get successRate => isCorrect ? 1.0 : 0.0;

  @override
  String toString() {
    return 'AttemptModel(id: $id, exerciseId: $exerciseId, isCorrect: $isCorrect, timeSpent: ${formattedTimeSpent})';
  }

  @override
  bool operator ==(Object other) {
    if (identical(this, other)) return true;
    return other is AttemptModel && other.id == id;
  }

  @override
  int get hashCode => id.hashCode;
}



