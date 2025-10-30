import SwiftUI

struct CoursesListView: View {
    @EnvironmentObject var authManager: AuthManager
    @State private var courses: [Course] = []
    @State private var isLoading = false
    @State private var errorMessage: String?
    
    var body: some View {
        NavigationView {
            ZStack {
                if isLoading {
                    ProgressView("Chargement des cours...")
                } else if let error = errorMessage {
                    VStack(spacing: 20) {
                        Image(systemName: "exclamationmark.triangle")
                            .font(.system(size: 50))
                            .foregroundColor(.orange)
                        
                        Text(error)
                            .multilineTextAlignment(.center)
                            .foregroundColor(.secondary)
                        
                        Button("Réessayer") {
                            loadCourses()
                        }
                        .buttonStyle(.bordered)
                    }
                    .padding()
                } else if courses.isEmpty {
                    VStack(spacing: 20) {
                        Image(systemName: "book.closed")
                            .font(.system(size: 50))
                            .foregroundColor(.gray)
                        
                        Text("Aucun cours disponible")
                            .font(.headline)
                            .foregroundColor(.secondary)
                    }
                } else {
                    List(courses) { course in
                        NavigationLink(destination: CourseDetailView(course: course)) {
                            CourseRow(course: course)
                        }
                    }
                    .listStyle(.plain)
                    .refreshable {
                        loadCourses()
                    }
                }
            }
            .navigationTitle("Mes Cours")
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button(action: loadCourses) {
                        Image(systemName: "arrow.clockwise")
                    }
                    .disabled(isLoading)
                }
            }
            .onAppear {
                if courses.isEmpty {
                    loadCourses()
                }
            }
        }
    }
    
    private func loadCourses() {
        guard let token = authManager.token else { return }
        
        isLoading = true
        errorMessage = nil
        
        Task {
            do {
                let response = try await APIService.shared.fetchCourses(token: token)
                await MainActor.run {
                    self.courses = response.data.courses
                    self.isLoading = false
                }
            } catch {
                await MainActor.run {
                    self.errorMessage = error.localizedDescription
                    self.isLoading = false
                }
            }
        }
    }
}

struct CourseRow: View {
    let course: Course
    
    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            // Titre et niveau
            HStack {
                Text(course.title)
                    .font(.headline)
                
                Spacer()
                
                Text(course.grade)
                    .font(.caption)
                    .padding(.horizontal, 8)
                    .padding(.vertical, 4)
                    .background(Color.blue.opacity(0.2))
                    .cornerRadius(8)
            }
            
            // Chapitre
            Text(course.chapter)
                .font(.subheadline)
                .foregroundColor(.secondary)
            
            // Description
            if let description = course.description, !description.isEmpty {
                Text(description)
                    .font(.caption)
                    .foregroundColor(.secondary)
                    .lineLimit(2)
            }
            
            // Nombre d'exercices
            if let exercises = course.exercises {
                HStack(spacing: 4) {
                    Image(systemName: "list.bullet.rectangle")
                        .font(.caption)
                    Text("\(exercises.count) exercice\(exercises.count > 1 ? "s" : "")")
                        .font(.caption)
                }
                .foregroundColor(.blue)
            }
        }
        .padding(.vertical, 8)
    }
}

#Preview {
    CoursesListView()
        .environmentObject(AuthManager.shared)
}









