import Foundation

struct Attempt: Codable, Identifiable {
    let id: Int
    let exerciseId: Int
    let userAnswer: String
    let isCorrect: Bool
    let createdAt: String
}

struct AttemptRequest: Codable {
    let exerciseId: Int
    let userAnswer: String
}

struct AttemptResponse: Codable {
    let success: Bool
    let data: AttemptData
}

struct AttemptData: Codable {
    let attempt: Attempt
    let isCorrect: Bool
    let explanation: String?
    let correctAnswer: String?
}









