import Foundation
import SwiftUI

class AuthManager: ObservableObject {
    static let shared = AuthManager()
    
    @Published var isAuthenticated = false
    @Published var currentUser: User?
    @Published var token: String?
    
    private let tokenKey = "auth_token"
    private let userKey = "current_user"
    
    private init() {
        loadSavedAuth()
    }
    
    // MARK: - Authentication
    
    func login(email: String, password: String) async throws {
        let response = try await APIService.shared.login(email: email, password: password)
        
        await MainActor.run {
            self.token = response.data.token
            self.currentUser = response.data.user
            self.isAuthenticated = true
            saveAuth()
        }
    }
    
    func signup(name: String, email: String, password: String) async throws {
        let response = try await APIService.shared.signup(name: name, email: email, password: password)
        
        await MainActor.run {
            self.token = response.data.token
            self.currentUser = response.data.user
            self.isAuthenticated = true
            saveAuth()
        }
    }
    
    func logout() {
        token = nil
        currentUser = nil
        isAuthenticated = false
        clearAuth()
    }
    
    // MARK: - Persistence
    
    private func saveAuth() {
        if let token = token {
            UserDefaults.standard.set(token, forKey: tokenKey)
        }
        
        if let user = currentUser {
            if let encoded = try? JSONEncoder().encode(user) {
                UserDefaults.standard.set(encoded, forKey: userKey)
            }
        }
    }
    
    private func loadSavedAuth() {
        if let savedToken = UserDefaults.standard.string(forKey: tokenKey) {
            self.token = savedToken
            
            if let savedUser = UserDefaults.standard.data(forKey: userKey),
               let user = try? JSONDecoder().decode(User.self, from: savedUser) {
                self.currentUser = user
                self.isAuthenticated = true
            }
        }
    }
    
    private func clearAuth() {
        UserDefaults.standard.removeObject(forKey: tokenKey)
        UserDefaults.standard.removeObject(forKey: userKey)
    }
}









