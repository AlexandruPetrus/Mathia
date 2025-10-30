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

  String get durationText {
    if (duration == null) return '';
    if (duration! < 60) return '$duration min';
    final hours = duration! ~/ 60;
    final minutes = duration! % 60;
    return minutes > 0 ? '${hours}h${minutes}min' : '${hours}h';
  }
}




