import Foundation

struct Exercise: Codable, Identifiable {
    let id: Int
    let courseId: Int
    let type: String
    let body: String
    let options: [String: String]?
    let answer: String
    let explanation: String?
    let difficulty: String?
    let tags: [String]?
    let createdAt: String
    let updatedAt: String
    let course: CourseInfo?
}

struct CourseInfo: Codable {
    let id: Int
    let title: String
    let grade: String
    let chapter: String
}

struct ExercisesResponse: Codable {
    let success: Bool
    let data: ExercisesData
}

struct ExercisesData: Codable {
    let exercises: [Exercise]
}

// Extension pour obtenir les options sous forme de tableau trié
extension Exercise {
    var sortedOptions: [(key: String, value: String)] {
        guard let options = options else { return [] }
        return options.sorted { $0.key < $1.key }
    }
}









