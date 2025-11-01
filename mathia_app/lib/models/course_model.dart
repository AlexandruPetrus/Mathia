class CourseModel {
  final String id;
  final String title;
  final String? description;
  final String? content;
  final String grade;
  final String topic;
  final String? difficulty;
  final int? duration;
  final int orderNum;
  final bool isPublished;
  final String? thumbnailUrl;
  final String? createdBy;
  final DateTime createdAt;
  final DateTime updatedAt;

  CourseModel({
    required this.id,
    required this.title,
    this.description,
    this.content,
    required this.grade,
    required this.topic,
    this.difficulty,
    this.duration,
    required this.orderNum,
    required this.isPublished,
    this.thumbnailUrl,
    this.createdBy,
    required this.createdAt,
    required this.updatedAt,
  });

  factory CourseModel.fromJson(Map<String, dynamic> json) {
    return CourseModel(
      id: json['id'] as String,
      title: json['title'] as String,
      description: json['description'] as String?,
      content: json['content'] as String?,
      grade: json['grade'] as String,
      topic: json['topic'] as String,
      difficulty: json['difficulty'] as String?,
      duration: json['duration'] as int?,
      orderNum: json['order_num'] as int? ?? 0,
      isPublished: json['is_published'] as bool? ?? false,
      thumbnailUrl: json['thumbnail_url'] as String?,
      createdBy: json['created_by'] as String?,
      createdAt: DateTime.parse(json['created_at'] as String),
      updatedAt: DateTime.parse(json['updated_at'] as String),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'title': title,
      'description': description,
      'content': content,
      'grade': grade,
      'topic': topic,
      'difficulty': difficulty,
      'duration': duration,
      'order_num': orderNum,
      'is_published': isPublished,
      'thumbnail_url': thumbnailUrl,
      'created_by': createdBy,
    };
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

  String get durationText {
    if (duration == null) return '';
    if (duration! < 60) return '$duration min';
    final hours = duration! ~/ 60;
    final minutes = duration! % 60;
    return minutes > 0 ? '${hours}h${minutes}min' : '${hours}h';
  }

  // Emoji pour le niveau scolaire
  String get gradeEmoji {
    switch (grade) {
      case '6ème':
        return '🔵';
      case '5ème':
        return '🟢';
      case '4ème':
        return '🟡';
      case '3ème':
        return '🔴';
      default:
        return '⚪';
    }
  }

  @override
  String toString() {
    return 'CourseModel(id: $id, title: $title, grade: $grade, topic: $topic)';
  }

  @override
  bool operator ==(Object other) {
    if (identical(this, other)) return true;
    return other is CourseModel && other.id == id;
  }

  @override
  int get hashCode => id.hashCode;
}
