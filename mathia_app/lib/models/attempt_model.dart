class AttemptModel {
  final String id;
  final String userId;
  final String exerciseId;
  final String userAnswer;
  final bool isCorrect;
  final int pointsEarned;
  final int? timeSpent; // en secondes
  final int hintsUsed;
  final int attemptNumber;
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
    required this.attemptNumber,
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
      attemptNumber: json['attempt_number'] as int? ?? 1,
      feedback: json['feedback'] as String?,
      createdAt: DateTime.parse(json['created_at'] as String),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'user_id': userId,
      'exercise_id': exerciseId,
      'user_answer': userAnswer,
      'is_correct': isCorrect,
      'points_earned': pointsEarned,
      'time_spent': timeSpent,
      'hints_used': hintsUsed,
      'attempt_number': attemptNumber,
      'feedback': feedback,
      'created_at': createdAt.toIso8601String(),
    };
  }

  // Méthodes utilitaires

  // Durée formatée (ex: "1 min 30s")
  String get formattedTimeSpent {
    if (timeSpent == null) return 'N/A';
    if (timeSpent! < 60) {
      return '${timeSpent}s';
    } else {
      final minutes = timeSpent! ~/ 60;
      final seconds = timeSpent! % 60;
      if (seconds == 0) {
        return '${minutes} min';
      } else {
        return '${minutes} min ${seconds}s';
      }
    }
  }

  // Statut de la tentative
  String get status {
    return isCorrect ? 'Réussi' : 'Échoué';
  }

  // Emoji pour le statut
  String get statusEmoji {
    return isCorrect ? '✅' : '❌';
  }

  // Couleur du statut (pour l'UI)
  String get statusColor {
    return isCorrect ? 'green' : 'red';
  }

  // Message de feedback selon le résultat
  String get defaultFeedback {
    if (feedback != null) return feedback!;

    if (isCorrect) {
      if (hintsUsed == 0) {
        return 'Parfait ! Vous avez réussi du premier coup sans aide.';
      } else if (hintsUsed == 1) {
        return 'Bien joué ! Vous avez utilisé 1 indice.';
      } else {
        return 'Correct ! Vous avez utilisé $hintsUsed indices.';
      }
    } else {
      if (attemptNumber == 1) {
        return 'Pas tout à fait. Réessayez !';
      } else {
        return 'Toujours pas correct. Tentative n°$attemptNumber.';
      }
    }
  }

  // Score en pourcentage (1 = 100%)
  double get successRate => isCorrect ? 1.0 : 0.0;

  // Badge selon la performance
  String get performanceBadge {
    if (!isCorrect) return '💔';
    if (hintsUsed == 0 && timeSpent != null && timeSpent! < 60) {
      return '🏆'; // Excellent
    } else if (hintsUsed == 0) {
      return '🌟'; // Très bien
    } else if (hintsUsed <= 2) {
      return '👍'; // Bien
    } else {
      return '✓'; // Correct
    }
  }

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

  // Méthode copyWith pour faciliter les mises à jour
  AttemptModel copyWith({
    String? userAnswer,
    bool? isCorrect,
    int? pointsEarned,
    int? timeSpent,
    int? hintsUsed,
    int? attemptNumber,
    String? feedback,
  }) {
    return AttemptModel(
      id: id,
      userId: userId,
      exerciseId: exerciseId,
      userAnswer: userAnswer ?? this.userAnswer,
      isCorrect: isCorrect ?? this.isCorrect,
      pointsEarned: pointsEarned ?? this.pointsEarned,
      timeSpent: timeSpent ?? this.timeSpent,
      hintsUsed: hintsUsed ?? this.hintsUsed,
      attemptNumber: attemptNumber ?? this.attemptNumber,
      feedback: feedback ?? this.feedback,
      createdAt: createdAt,
    );
  }
}
