import 'package:supabase_flutter/supabase_flutter.dart';

class ExerciseModel {
  final String id;
  final String courseId;
  final String title;
  final String description;
  final String question;
  final String? answer;
  final List<String>? options; // Pour les QCM
  final String type; // 'qcm', 'libre', 'vrai-faux', 'calcul'
  final String difficulty; // 'facile', 'moyen', 'difficile'
  final int points;
  final int timeLimit; // en secondes
  final int orderNum;
  final bool isPublished;
  final DateTime createdAt;
  final DateTime updatedAt;

  ExerciseModel({
    required this.id,
    required this.courseId,
    required this.title,
    required this.description,
    required this.question,
    this.answer,
    this.options,
    required this.type,
    required this.difficulty,
    required this.points,
    required this.timeLimit,
    required this.orderNum,
    required this.isPublished,
    required this.createdAt,
    required this.updatedAt,
  });

  factory ExerciseModel.fromJson(Map<String, dynamic> json) {
    return ExerciseModel(
      id: json['id'] as String,
      courseId: json['course_id'] as String,
      title: json['title'] as String,
      description: json['description'] as String,
      question: json['question'] as String,
      answer: json['answer'] as String?,
      options: json['options'] != null 
          ? List<String>.from(json['options'] as List)
          : null,
      type: json['type'] as String,
      difficulty: json['difficulty'] as String,
      points: json['points'] as int,
      timeLimit: json['time_limit'] as int,
      orderNum: json['order_num'] as int,
      isPublished: json['is_published'] as bool,
      createdAt: DateTime.parse(json['created_at'] as String),
      updatedAt: DateTime.parse(json['updated_at'] as String),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'course_id': courseId,
      'title': title,
      'description': description,
      'question': question,
      'answer': answer,
      'options': options,
      'type': type,
      'difficulty': difficulty,
      'points': points,
      'time_limit': timeLimit,
      'order_num': orderNum,
      'is_published': isPublished,
      'created_at': createdAt.toIso8601String(),
      'updated_at': updatedAt.toIso8601String(),
    };
  }

  // Méthodes utilitaires
  bool get isQcm => type == 'qcm';
  bool get isTrueFalse => type == 'vrai-faux';
  bool get isFreeText => type == 'libre';
  bool get isCalculation => type == 'calcul';

  String get difficultyDisplayName {
    switch (difficulty) {
      case 'facile':
        return 'Facile';
      case 'moyen':
        return 'Moyen';
      case 'difficile':
        return 'Difficile';
      default:
        return difficulty;
    }
  }

  String get typeDisplayName {
    switch (type) {
      case 'qcm':
        return 'QCM';
      case 'vrai-faux':
        return 'Vrai/Faux';
      case 'libre':
        return 'Réponse libre';
      case 'calcul':
        return 'Calcul';
      default:
        return type;
    }
  }

  // Durée formatée (ex: "2 min")
  String get formattedTimeLimit {
    if (timeLimit < 60) {
      return '${timeLimit}s';
    } else {
      final minutes = timeLimit ~/ 60;
      return '${minutes} min';
    }
  }

  @override
  String toString() {
    return 'ExerciseModel(id: $id, title: $title, type: $type, difficulty: $difficulty)';
  }

  @override
  bool operator ==(Object other) {
    if (identical(this, other)) return true;
    return other is ExerciseModel && other.id == id;
  }

  @override
  int get hashCode => id.hashCode;
}
