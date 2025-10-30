class UserModel {
  final String id;
  final String username;
  final String? firstName;
  final String? lastName;
  final String email;
  final String grade;
  final String role;
  final int totalPoints;
  final bool isActive;
  final String? avatarUrl;
  final DateTime createdAt;

  UserModel({
    required this.id,
    required this.username,
    this.firstName,
    this.lastName,
    required this.email,
    required this.grade,
    required this.role,
    required this.totalPoints,
    required this.isActive,
    this.avatarUrl,
    required this.createdAt,
  });

  factory UserModel.fromJson(Map<String, dynamic> json) {
    return UserModel(
      id: json['id'] as String,
      username: json['username'] as String,
      firstName: json['first_name'] as String?,
      lastName: json['last_name'] as String?,
      email: json['email'] as String? ?? '',
      grade: json['grade'] as String,
      role: json['role'] as String,
      totalPoints: json['total_points'] as int? ?? 0,
      isActive: json['is_active'] as bool? ?? true,
      avatarUrl: json['avatar_url'] as String?,
      createdAt: DateTime.parse(json['created_at'] as String),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'username': username,
      'first_name': firstName,
      'last_name': lastName,
      'grade': grade,
      'role': role,
      'total_points': totalPoints,
      'is_active': isActive,
      'avatar_url': avatarUrl,
    };
  }

  String get fullName => '${firstName ?? ''} ${lastName ?? ''}'.trim();
}




