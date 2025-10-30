import Foundation

enum APIError: Error, LocalizedError {
    case invalidURL
    case networkError(Error)
    case invalidResponse
    case decodingError(Error)
    case serverError(String)
    case unauthorized
    
    var errorDescription: String? {
        switch self {
        case .invalidURL:
            return "URL invalide"
        case .networkError(let error):
            return "Erreur réseau: \(error.localizedDescription)"
        case .invalidResponse:
            return "Réponse invalide du serveur"
        case .decodingError(let error):
            return "Erreur de décodage: \(error.localizedDescription)"
        case .serverError(let message):
            return message
        case .unauthorized:
            return "Non autorisé. Veuillez vous reconnecter."
        }
    }
}

class APIService {
    static let shared = APIService()
    
    // Configuration de l'API
    private let baseURL = "http://localhost:3000/api"
    
    // Pour iOS Simulator qui accède au Mac localhost
    // private let baseURL = "http://127.0.0.1:3000/api"
    
    // Pour un appareil physique, utilisez l'IP de votre Mac
    // private let baseURL = "http://192.168.1.X:3000/api"
    
    private init() {}
    
    // MARK: - Helper Methods
    
    private func createRequest(
        endpoint: String,
        method: String = "GET",
        token: String? = nil,
        body: Data? = nil
    ) -> URLRequest? {
        guard let url = URL(string: "\(baseURL)\(endpoint)") else {
            return nil
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = method
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        if let token = token {
            request.setValue("Bearer \(token)", forHTTPHeaderField: "Authorization")
        }
        
        if let body = body {
            request.httpBody = body
        }
        
        return request
    }
    
    private func performRequest<T: Decodable>(
        _ request: URLRequest
    ) async throws -> T {
        let (data, response) = try await URLSession.shared.data(for: request)
        
        guard let httpResponse = response as? HTTPURLResponse else {
            throw APIError.invalidResponse
        }
        
        // Afficher la réponse pour debug
        if let jsonString = String(data: data, encoding: .utf8) {
            print("📥 Response (\(httpResponse.statusCode)): \(jsonString)")
        }
        
        switch httpResponse.statusCode {
        case 200...299:
            do {
                let decoded = try JSONDecoder().decode(T.self, from: data)
                return decoded
            } catch {
                print("❌ Decoding error: \(error)")
                throw APIError.decodingError(error)
            }
            
        case 401:
            throw APIError.unauthorized
            
        default:
            // Essayer de décoder le message d'erreur
            if let errorResponse = try? JSONDecoder().decode(ErrorResponse.self, from: data) {
                throw APIError.serverError(errorResponse.message)
            }
            throw APIError.serverError("Erreur HTTP \(httpResponse.statusCode)")
        }
    }
    
    // MARK: - Authentication
    
    func signup(name: String, email: String, password: String) async throws -> AuthResponse {
        let body = [
            "name": name,
            "email": email,
            "password": password
        ]
        
        let bodyData = try JSONEncoder().encode(body)
        
        guard let request = createRequest(
            endpoint: "/auth/signup",
            method: "POST",
            body: bodyData
        ) else {
            throw APIError.invalidURL
        }
        
        return try await performRequest(request)
    }
    
    func login(email: String, password: String) async throws -> AuthResponse {
        let body = [
            "email": email,
            "password": password
        ]
        
        let bodyData = try JSONEncoder().encode(body)
        
        guard let request = createRequest(
            endpoint: "/auth/login",
            method: "POST",
            body: bodyData
        ) else {
            throw APIError.invalidURL
        }
        
        return try await performRequest(request)
    }
    
    // MARK: - Courses
    
    func fetchCourses(token: String) async throws -> CoursesResponse {
        guard let request = createRequest(
            endpoint: "/courses",
            token: token
        ) else {
            throw APIError.invalidURL
        }
        
        return try await performRequest(request)
    }
    
    func fetchCourseDetail(id: Int, token: String) async throws -> CourseDetailResponse {
        guard let request = createRequest(
            endpoint: "/courses/\(id)",
            token: token
        ) else {
            throw APIError.invalidURL
        }
        
        return try await performRequest(request)
    }
    
    // MARK: - Exercises
    
    func fetchExercises(courseId: Int? = nil, difficulty: String? = nil, token: String) async throws -> ExercisesResponse {
        var endpoint = "/exercises?"
        
        if let courseId = courseId {
            endpoint += "courseId=\(courseId)&"
        }
        
        if let difficulty = difficulty {
            endpoint += "difficulty=\(difficulty)&"
        }
        
        // Retirer le dernier & ou ?
        if endpoint.hasSuffix("&") || endpoint.hasSuffix("?") {
            endpoint.removeLast()
        }
        
        guard let request = createRequest(
            endpoint: endpoint,
            token: token
        ) else {
            throw APIError.invalidURL
        }
        
        return try await performRequest(request)
    }
    
    // MARK: - Attempts
    
    func submitAttempt(exerciseId: Int, userAnswer: String, token: String) async throws -> AttemptResponse {
        let body = AttemptRequest(exerciseId: exerciseId, userAnswer: userAnswer)
        let bodyData = try JSONEncoder().encode(body)
        
        guard let request = createRequest(
            endpoint: "/attempts",
            method: "POST",
            token: token,
            body: bodyData
        ) else {
            throw APIError.invalidURL
        }
        
        return try await performRequest(request)
    }
}

// MARK: - Error Response Model

struct ErrorResponse: Codable {
    let success: Bool
    let message: String
}









