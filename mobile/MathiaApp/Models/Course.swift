import Foundation

struct Course: Codable, Identifiable {
    let id: Int
    let title: String
    let grade: String
    let chapter: String
    let description: String?
    let createdAt: String
    let updatedAt: String
    let exercises: [ExerciseSimple]?
}

struct ExerciseSimple: Codable, Identifiable {
    let id: Int
    let type: String
    let difficulty: String?
}

struct CoursesResponse: Codable {
    let success: Bool
    let data: CoursesData
}

struct CoursesData: Codable {
    let courses: [Course]
}

struct CourseDetailResponse: Codable {
    let success: Bool
    let data: CourseDetailData
}

struct CourseDetailData: Codable {
    let course: Course
}









