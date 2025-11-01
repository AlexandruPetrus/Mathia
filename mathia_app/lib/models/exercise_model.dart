class ExerciseModel {
  final String id;
  final String courseId;
  final String title;
  final String? description;
  final String question;
  final String type; // 'qcm', 'libre', 'vrai-faux', 'calcul'
  final Map<String, String>? options; // Pour les QCM: {"A": "...", "B": "..."}
  final String answer;
  final String? explanation;
  final String? difficulty; // 'facile', 'moyen', 'difficile'
  final int points;
  final List<String>? hints;
  final List<String>? tags;
  final int orderNum;
  final bool isPublished;
  final bool aiGenerated;
  final bool validatedByTeacher;
  final int usageCount;
  final double successRate;
  final String? createdBy;
  final DateTime createdAt;
  final DateTime updatedAt;

  ExerciseModel({
    required this.id,
    required this.courseId,
    required this.title,
    this.description,
    required this.question,
    required this.type,
    this.options,
    required this.answer,
    this.explanation,
    this.difficulty,
    required this.points,
    this.hints,
    this.tags,
    required this.orderNum,
    required this.isPublished,
    required this.aiGenerated,
    required this.validatedByTeacher,
    required this.usageCount,
    required this.successRate,
    this.createdBy,
    required this.createdAt,
    required this.updatedAt,
  });

  factory ExerciseModel.fromJson(Map<String, dynamic> json) {
    // Gérer le parsing de options (peut être Map ou null)
    Map<String, String>? parsedOptions;
    if (json['options'] != null) {
      final optionsData = json['options'];
      if (optionsData is Map) {
        parsedOptions = Map<String, String>.from(optionsData);
      }
    }

    // Gérer le parsing de hints (peut être List ou null)
    List<String>? parsedHints;
    if (json['hints'] != null && json['hints'] is List) {
      parsedHints = List<String>.from(json['hints']);
    }

    // Gérer le parsing de tags (peut être List ou null)
    List<String>? parsedTags;
    if (json['tags'] != null && json['tags'] is List) {
      parsedTags = List<String>.from(json['tags']);
    }

    return ExerciseModel(
      id: json['id'] as String,
      courseId: json['course_id'] as String,
      title: json['title'] as String,
      description: json['description'] as String?,
      question: json['question'] as String,
      type: json['type'] as String,
      options: parsedOptions,
      answer: json['answer'] as String,
      explanation: json['explanation'] as String?,
      difficulty: json['difficulty'] as String?,
      points: json['points'] as int? ?? 10,
      hints: parsedHints,
      tags: parsedTags,
      orderNum: json['order_num'] as int? ?? 0,
      isPublished: json['is_published'] as bool? ?? false,
      aiGenerated: json['ai_generated'] as bool? ?? false,
      validatedByTeacher: json['validated_by_teacher'] as bool? ?? false,
      usageCount: json['usage_count'] as int? ?? 0,
      successRate: (json['success_rate'] as num?)?.toDouble() ?? 0.0,
      createdBy: json['created_by'] as String?,
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
      'type': type,
      'options': options,
      'answer': answer,
      'explanation': explanation,
      'difficulty': difficulty,
      'points': points,
      'hints': hints,
      'tags': tags,
      'order_num': orderNum,
      'is_published': isPublished,
      'ai_generated': aiGenerated,
      'validated_by_teacher': validatedByTeacher,
      'usage_count': usageCount,
      'success_rate': successRate,
      'created_by': createdBy,
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
        return difficulty ?? 'Non défini';
    }
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

  // Emoji selon le type
  String get typeEmoji {
    switch (type) {
      case 'qcm':
        return '📝';
      case 'vrai-faux':
        return '✓✗';
      case 'libre':
        return '✍️';
      case 'calcul':
        return '🔢';
      default:
        return '❓';
    }
  }

  // Badge de qualité pour exercices IA
  String get qualityBadge {
    if (!aiGenerated) return '👨‍🏫'; // Créé par un prof
    if (validatedByTeacher) return '✅'; // IA validée
    return '🤖'; // IA non validée
  }

  // Taux de réussite formaté
  String get successRateText {
    return '${successRate.toStringAsFixed(1)}%';
  }

  // Liste des options pour QCM (retourne les clés triées)
  List<String> get optionKeys {
    if (options == null) return [];
    final keys = options!.keys.toList();
    keys.sort();
    return keys;
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
