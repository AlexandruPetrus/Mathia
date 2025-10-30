import Foundation

struct User: Codable, Identifiable {
    let id: Int
    let name: String
    let email: String
    let createdAt: String
    let updatedAt: String
}

struct AuthResponse: Codable {
    let success: Bool
    let message: String?
    let data: AuthData
}

struct AuthData: Codable {
    let user: User
    let token: String
}









