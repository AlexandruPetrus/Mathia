# 🍎 Mathia × Supabase - Intégration SwiftUI

## 📱 Votre projet utilise SwiftUI (pas Flutter)

J'ai remarqué que votre app mobile est en **SwiftUI** (dans `mobile/MathiaApp/`), pas en Flutter.

Voici comment intégrer Supabase avec votre app **iOS native** existante ! 🚀

---

## 📦 Étape 1 : Installer le SDK Supabase Swift

### 1.1 Ouvrir votre projet Xcode

```bash
cd mobile
open MathiaApp.xcodeproj
# ou
open MathiaApp.xcworkspace
```

### 1.2 Ajouter le package Supabase

1. Dans **Xcode** → **File** → **Add Package Dependencies**
2. Entrez l'URL : `https://github.com/supabase/supabase-swift`
3. Version : **"Up to Next Major Version"** → `2.0.0`
4. Cliquez sur **Add Package**
5. Sélectionnez :
   - ✅ `Supabase`
   - ✅ `Auth`
   - ✅ `PostgREST`
   - ✅ `Realtime`
6. Cliquez sur **Add Package**

---

## ⚙️ Étape 2 : Configuration

### 2.1 Créer un fichier de configuration

Créez `mobile/MathiaApp/Config.swift` :

```swift
import Foundation

enum SupabaseConfig {
    static let url = URL(string: "https://xxxxxxxx.supabase.co")!
    static let anonKey = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

⚠️ **Important** : Remplacez avec vos vraies clés Supabase !

### 2.2 Initialiser Supabase

Dans `mobile/MathiaApp/MathiaApp.swift` :

```swift
import SwiftUI
import Supabase

@main
struct MathiaApp: App {
    
    // Client Supabase global
    static let supabase = SupabaseClient(
        supabaseURL: SupabaseConfig.url,
        supabaseKey: SupabaseConfig.anonKey
    )
    
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}
```

---

## 📦 Étape 3 : Créer les modèles

### 3.1 User Model

Remplacez `mobile/MathiaApp/Models/User.swift` :

```swift
import Foundation

struct User: Codable, Identifiable {
    let id: UUID
    let username: String
    let firstName: String?
    let lastName: String?
    let email: String
    let grade: String
    let role: String
    let totalPoints: Int
    let isActive: Bool
    let avatarUrl: String?
    let createdAt: Date
    
    enum CodingKeys: String, CodingKey {
        case id
        case username
        case firstName = "first_name"
        case lastName = "last_name"
        case email
        case grade
        case role
        case totalPoints = "total_points"
        case isActive = "is_active"
        case avatarUrl = "avatar_url"
        case createdAt = "created_at"
    }
    
    var fullName: String {
        [firstName, lastName]
            .compactMap { $0 }
            .joined(separator: " ")
    }
}
```

### 3.2 Course Model

Remplacez `mobile/MathiaApp/Models/Course.swift` :

```swift
import Foundation

struct Course: Codable, Identifiable {
    let id: UUID
    let title: String
    let description: String
    let content: String
    let grade: String
    let topic: String
    let difficulty: String
    let duration: Int?
    let isPublished: Bool
    let thumbnailUrl: String?
    let createdAt: Date
    
    enum CodingKeys: String, CodingKey {
        case id, title, description, content, grade, topic, difficulty, duration
        case isPublished = "is_published"
        case thumbnailUrl = "thumbnail_url"
        case createdAt = "created_at"
    }
    
    var difficultyEmoji: String {
        switch difficulty {
        case "facile": return "🟢"
        case "moyen": return "🟡"
        case "difficile": return "🔴"
        default: return "⚪"
        }
    }
}
```

### 3.3 Exercise Model

Remplacez `mobile/MathiaApp/Models/Exercise.swift` :

```swift
import Foundation

struct Exercise: Codable, Identifiable {
    let id: UUID
    let courseId: UUID
    let title: String
    let description: String?
    let question: String
    let answer: String
    let explanation: String?
    let difficulty: String
    let points: Int
    let type: String
    let hints: [String]
    let options: [String: String]?
    let isPublished: Bool
    
    enum CodingKeys: String, CodingKey {
        case id, title, description, question, answer, explanation, difficulty, points, type, hints, options
        case courseId = "course_id"
        case isPublished = "is_published"
    }
    
    var isQCM: Bool {
        type == "qcm"
    }
    
    var hasHints: Bool {
        !hints.isEmpty
    }
}
```

### 3.4 Attempt Model

Remplacez `mobile/MathiaApp/Models/Attempt.swift` :

```swift
import Foundation

struct Attempt: Codable, Identifiable {
    let id: UUID
    let userId: UUID
    let exerciseId: UUID
    let userAnswer: String
    let isCorrect: Bool
    let pointsEarned: Int
    let timeSpent: Int?
    let hintsUsed: Int
    let feedback: String?
    let createdAt: Date
    
    enum CodingKeys: String, CodingKey {
        case id
        case userId = "user_id"
        case exerciseId = "exercise_id"
        case userAnswer = "user_answer"
        case isCorrect = "is_correct"
        case pointsEarned = "points_earned"
        case timeSpent = "time_spent"
        case hintsUsed = "hints_used"
        case feedback
        case createdAt = "created_at"
    }
}
```

---

## 🔐 Étape 4 : Service d'authentification

Créez `mobile/MathiaApp/Services/SupabaseAuthService.swift` :

```swift
import Foundation
import Supabase
import Auth

@MainActor
class SupabaseAuthService: ObservableObject {
    private let supabase = MathiaApp.supabase
    
    @Published var currentUser: User?
    @Published var isAuthenticated = false
    @Published var isLoading = false
    @Published var errorMessage: String?
    
    init() {
        // Vérifier si l'utilisateur est déjà connecté
        Task {
            await checkSession()
        }
    }
    
    // Inscription
    func signUp(
        email: String,
        password: String,
        username: String,
        firstName: String,
        lastName: String,
        grade: String
    ) async throws {
        isLoading = true
        defer { isLoading = false }
        
        do {
            let response = try await supabase.auth.signUp(
                email: email,
                password: password,
                data: [
                    "username": .string(username),
                    "first_name": .string(firstName),
                    "last_name": .string(lastName),
                    "grade": .string(grade),
                    "role": .string("student")
                ]
            )
            
            guard let userId = response.user?.id else {
                throw NSError(domain: "", code: -1, userInfo: [NSLocalizedDescriptionKey: "Erreur d'inscription"])
            }
            
            // Récupérer le profil créé
            currentUser = try await getUserProfile(userId: userId)
            isAuthenticated = true
            
        } catch {
            errorMessage = error.localizedDescription
            throw error
        }
    }
    
    // Connexion
    func signIn(email: String, password: String) async throws {
        isLoading = true
        defer { isLoading = false }
        
        do {
            let response = try await supabase.auth.signIn(
                email: email,
                password: password
            )
            
            guard let userId = response.user?.id else {
                throw NSError(domain: "", code: -1, userInfo: [NSLocalizedDescriptionKey: "Email ou mot de passe incorrect"])
            }
            
            currentUser = try await getUserProfile(userId: userId)
            isAuthenticated = true
            
        } catch {
            errorMessage = error.localizedDescription
            throw error
        }
    }
    
    // Déconnexion
    func signOut() async throws {
        try await supabase.auth.signOut()
        currentUser = nil
        isAuthenticated = false
    }
    
    // Récupérer le profil
    func getUserProfile(userId: UUID) async throws -> User {
        let response = try await supabase
            .from("users")
            .select()
            .eq("id", value: userId.uuidString)
            .single()
            .execute()
        
        return try JSONDecoder().decode(User.self, from: response.data)
    }
    
    // Vérifier la session
    func checkSession() async {
        do {
            let session = try await supabase.auth.session
            if let userId = session.user.id {
                currentUser = try await getUserProfile(userId: userId)
                isAuthenticated = true
            }
        } catch {
            isAuthenticated = false
        }
    }
}
```

---

## 📚 Étape 5 : Service des cours

Créez `mobile/MathiaApp/Services/CourseService.swift` :

```swift
import Foundation
import Supabase

class CourseService {
    private let supabase = MathiaApp.supabase
    
    // Récupérer tous les cours
    func getCourses(
        grade: String? = nil,
        topic: String? = nil,
        difficulty: String? = nil
    ) async throws -> [Course] {
        var query = supabase
            .from("courses")
            .select()
            .eq("is_published", value: true)
            .order("order_num")
        
        if let grade = grade {
            query = query.eq("grade", value: grade)
        }
        if let topic = topic {
            query = query.eq("topic", value: topic)
        }
        if let difficulty = difficulty {
            query = query.eq("difficulty", value: difficulty)
        }
        
        let response = try await query.execute()
        return try JSONDecoder().decode([Course].self, from: response.data)
    }
    
    // Récupérer un cours par ID
    func getCourse(id: UUID) async throws -> Course {
        let response = try await supabase
            .from("courses")
            .select()
            .eq("id", value: id.uuidString)
            .single()
            .execute()
        
        return try JSONDecoder().decode(Course.self, from: response.data)
    }
    
    // Rechercher des cours
    func searchCourses(query: String) async throws -> [Course] {
        let response = try await supabase
            .rpc("search_courses", params: ["search_query": query])
            .execute()
        
        return try JSONDecoder().decode([Course].self, from: response.data)
    }
    
    // Ajouter aux favoris
    func addToFavorites(courseId: UUID) async throws {
        guard let userId = try await supabase.auth.session.user.id else {
            throw NSError(domain: "", code: -1, userInfo: [NSLocalizedDescriptionKey: "Non authentifié"])
        }
        
        try await supabase
            .from("favorites")
            .insert([
                "user_id": userId.uuidString,
                "course_id": courseId.uuidString
            ])
            .execute()
    }
}
```

---

## 📝 Étape 6 : Service des exercices

Créez `mobile/MathiaApp/Services/ExerciseService.swift` :

```swift
import Foundation
import Supabase

class ExerciseService {
    private let supabase = MathiaApp.supabase
    
    // Récupérer les exercices d'un cours
    func getExercises(courseId: UUID) async throws -> [Exercise] {
        let response = try await supabase
            .from("exercises")
            .select()
            .eq("course_id", value: courseId.uuidString)
            .eq("is_published", value: true)
            .order("order_num")
            .execute()
        
        return try JSONDecoder().decode([Exercise].self, from: response.data)
    }
    
    // Soumettre une tentative
    func submitAttempt(
        exerciseId: UUID,
        userAnswer: String,
        timeSpent: Int? = nil,
        hintsUsed: Int = 0
    ) async throws -> [String: Any] {
        let response = try await supabase
            .rpc("submit_attempt", params: [
                "p_exercise_id": exerciseId.uuidString,
                "p_user_answer": userAnswer,
                "p_time_spent": timeSpent as Any,
                "p_hints_used": hintsUsed
            ])
            .execute()
        
        guard let json = try? JSONSerialization.jsonObject(with: response.data) as? [[String: Any]],
              let result = json.first else {
            throw NSError(domain: "", code: -1, userInfo: [NSLocalizedDescriptionKey: "Erreur de soumission"])
        }
        
        return result
    }
    
    // Exercices recommandés
    func getRecommendedExercises(limit: Int = 5) async throws -> [Exercise] {
        guard let userId = try await supabase.auth.session.user.id else {
            throw NSError(domain: "", code: -1, userInfo: [NSLocalizedDescriptionKey: "Non authentifié"])
        }
        
        let response = try await supabase
            .rpc("get_recommended_exercises", params: [
                "user_uuid": userId.uuidString,
                "limit_count": limit
            ])
            .execute()
        
        return try JSONDecoder().decode([Exercise].self, from: response.data)
    }
}
```

---

## 📊 Étape 7 : Mettre à jour les vues

### 7.1 LoginView avec Supabase

Remplacez `mobile/MathiaApp/Views/Auth/LoginView.swift` :

```swift
import SwiftUI

struct LoginView: View {
    @StateObject private var authService = SupabaseAuthService()
    @State private var email = ""
    @State private var password = ""
    @State private var showError = false
    
    var body: some View {
        VStack(spacing: 20) {
            Text("Mathia")
                .font(.largeTitle)
                .bold()
            
            TextField("Email", text: $email)
                .textFieldStyle(.roundedBorder)
                .textInputAutocapitalization(.never)
                .keyboardType(.emailAddress)
            
            SecureField("Mot de passe", text: $password)
                .textFieldStyle(.roundedBorder)
            
            if authService.isLoading {
                ProgressView()
            } else {
                Button("Se connecter") {
                    Task {
                        do {
                            try await authService.signIn(email: email, password: password)
                        } catch {
                            showError = true
                        }
                    }
                }
                .buttonStyle(.borderedProminent)
            }
            
            if let error = authService.errorMessage {
                Text(error)
                    .foregroundColor(.red)
                    .font(.caption)
            }
        }
        .padding()
        .alert("Erreur", isPresented: $showError) {
            Button("OK") { showError = false }
        } message: {
            Text(authService.errorMessage ?? "Une erreur s'est produite")
        }
    }
}
```

### 7.2 CoursesListView avec Supabase

Remplacez `mobile/MathiaApp/Views/Courses/CoursesListView.swift` :

```swift
import SwiftUI

struct CoursesListView: View {
    @State private var courses: [Course] = []
    @State private var isLoading = true
    @State private var errorMessage: String?
    
    private let courseService = CourseService()
    
    var body: some View {
        NavigationView {
            Group {
                if isLoading {
                    ProgressView()
                } else if let error = errorMessage {
                    VStack {
                        Text("Erreur")
                            .font(.headline)
                        Text(error)
                            .font(.caption)
                            .foregroundColor(.red)
                        Button("Réessayer") {
                            Task { await loadCourses() }
                        }
                    }
                } else {
                    List(courses) { course in
                        NavigationLink(destination: CourseDetailView(courseId: course.id)) {
                            VStack(alignment: .leading, spacing: 8) {
                                HStack {
                                    Text(course.difficultyEmoji)
                                    Text(course.title)
                                        .font(.headline)
                                }
                                
                                Text(course.description)
                                    .font(.caption)
                                    .foregroundColor(.secondary)
                                    .lineLimit(2)
                                
                                HStack {
                                    Text(course.grade)
                                    Text("•")
                                    Text(course.topic)
                                }
                                .font(.caption2)
                                .foregroundColor(.secondary)
                            }
                            .padding(.vertical, 4)
                        }
                    }
                }
            }
            .navigationTitle("Cours")
            .task {
                await loadCourses()
            }
        }
    }
    
    private func loadCourses() async {
        isLoading = true
        do {
            courses = try await courseService.getCourses()
            errorMessage = nil
        } catch {
            errorMessage = error.localizedDescription
        }
        isLoading = false
    }
}
```

---

## ✅ Résumé de la migration

### Ce qui change dans votre code Swift :

1. ❌ **Supprimez** `mobile/MathiaApp/Services/APIService.swift` (ancien HTTP)
2. ✅ **Ajoutez** le package Supabase
3. ✅ **Créez** les nouveaux services (Auth, Course, Exercise)
4. ✅ **Mettez à jour** les vues pour utiliser les nouveaux services

### Avantages :

- ✅ Plus besoin du backend Express pour le CRUD
- ✅ Authentification native Supabase
- ✅ Temps réel disponible
- ✅ Code plus simple et plus maintenable

---

## 🧪 Test

1. Lancez votre app dans Xcode
2. Créez un compte
3. Connectez-vous
4. Consultez les cours

---

## 📖 Ressources

- [Supabase Swift SDK](https://github.com/supabase/supabase-swift)
- [Documentation Auth](https://supabase.com/docs/reference/swift/auth-signup)
- [Examples SwiftUI](https://github.com/supabase-community/supabase-swift-examples)

---

Créé avec ❤️ pour Mathia




