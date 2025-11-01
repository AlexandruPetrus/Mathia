class UserModel {
  final String id;
  final String username;
  final String firstName;
  final String lastName;
  final String email;
  final String grade;
  final String role;
  final int totalPoints;
  final bool isActive;
  final String? avatarUrl;
  final DateTime? lastLogin;
  final DateTime createdAt;
  final DateTime updatedAt;

  UserModel({
    required this.id,
    required this.username,
    required this.firstName,
    required this.lastName,
    required this.email,
    required this.grade,
    required this.role,
    required this.totalPoints,
    required this.isActive,
    this.avatarUrl,
    this.lastLogin,
    required this.createdAt,
    required this.updatedAt,
  });

  factory UserModel.fromJson(Map<String, dynamic> json) {
    return UserModel(
      id: json['id'] as String,
      username: json['username'] as String,
      firstName: json['first_name'] as String? ?? '',
      lastName: json['last_name'] as String? ?? '',
      email: json['email'] as String,
      grade: json['grade'] as String,
      role: json['role'] as String? ?? 'student',
      totalPoints: json['total_points'] as int? ?? 0,
      isActive: json['is_active'] as bool? ?? true,
      avatarUrl: json['avatar_url'] as String?,
      lastLogin: json['last_login'] != null
          ? DateTime.parse(json['last_login'] as String)
          : null,
      createdAt: DateTime.parse(json['created_at'] as String),
      updatedAt: DateTime.parse(json['updated_at'] as String),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'username': username,
      'first_name': firstName,
      'last_name': lastName,
      'email': email,
      'grade': grade,
      'role': role,
      'total_points': totalPoints,
      'is_active': isActive,
      'avatar_url': avatarUrl,
      'last_login': lastLogin?.toIso8601String(),
    };
  }

  String get fullName => '$firstName $lastName'.trim();

  String get displayName => fullName.isNotEmpty ? fullName : username;

  bool get isStudent => role == 'student';
  bool get isTeacher => role == 'teacher';
  bool get isAdmin => role == 'admin';

  // Emoji pour le niveau
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
    return 'UserModel(id: $id, username: $username, grade: $grade, points: $totalPoints)';
  }

  @override
  bool operator ==(Object other) {
    if (identical(this, other)) return true;
    return other is UserModel && other.id == id;
  }

  @override
  int get hashCode => id.hashCode;

  // Méthode copyWith pour faciliter les mises à jour
  UserModel copyWith({
    String? username,
    String? firstName,
    String? lastName,
    String? email,
    String? grade,
    String? role,
    int? totalPoints,
    bool? isActive,
    String? avatarUrl,
    DateTime? lastLogin,
    DateTime? updatedAt,
  }) {
    return UserModel(
      id: id,
      username: username ?? this.username,
      firstName: firstName ?? this.firstName,
      lastName: lastName ?? this.lastName,
      email: email ?? this.email,
      grade: grade ?? this.grade,
      role: role ?? this.role,
      totalPoints: totalPoints ?? this.totalPoints,
      isActive: isActive ?? this.isActive,
      avatarUrl: avatarUrl ?? this.avatarUrl,
      lastLogin: lastLogin ?? this.lastLogin,
      createdAt: createdAt,
      updatedAt: updatedAt ?? this.updatedAt,
    );
  }
}
