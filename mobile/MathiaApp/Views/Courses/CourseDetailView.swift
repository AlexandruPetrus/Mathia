import SwiftUI

struct CourseDetailView: View {
    @EnvironmentObject var authManager: AuthManager
    let course: Course
    
    @State private var exercises: [Exercise] = []
    @State private var isLoading = false
    @State private var errorMessage: String?
    
    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 20) {
                // En-tête du cours
                VStack(alignment: .leading, spacing: 12) {
                    HStack {
                        Text(course.grade)
                            .font(.headline)
                            .padding(.horizontal, 12)
                            .padding(.vertical, 6)
                            .background(Color.blue)
                            .foregroundColor(.white)
                            .cornerRadius(8)
                        
                        Text(course.chapter)
                            .font(.subheadline)
                            .foregroundColor(.secondary)
                    }
                    
                    Text(course.title)
                        .font(.title)
                        .fontWeight(.bold)
                    
                    if let description = course.description, !description.isEmpty {
                        Text(description)
                            .font(.body)
                            .foregroundColor(.secondary)
                    }
                }
                .padding()
                .background(Color(.systemBackground))
                .cornerRadius(12)
                .shadow(radius: 2)
                
                // Liste des exercices
                VStack(alignment: .leading, spacing: 12) {
                    Text("Exercices (\(exercises.count))")
                        .font(.title2)
                        .fontWeight(.semibold)
                        .padding(.horizontal)
                    
                    if isLoading {
                        ProgressView()
                            .frame(maxWidth: .infinity)
                            .padding()
                    } else if let error = errorMessage {
                        VStack(spacing: 12) {
                            Text(error)
                                .foregroundColor(.red)
                                .multilineTextAlignment(.center)
                            
                            Button("Réessayer") {
                                loadExercises()
                            }
                            .buttonStyle(.bordered)
                        }
                        .frame(maxWidth: .infinity)
                        .padding()
                    } else if exercises.isEmpty {
                        Text("Aucun exercice disponible pour ce cours")
                            .foregroundColor(.secondary)
                            .frame(maxWidth: .infinity)
                            .padding()
                    } else {
                        ForEach(exercises) { exercise in
                            NavigationLink(destination: QuizView(exercise: exercise)) {
                                ExerciseRow(exercise: exercise)
                            }
                            .buttonStyle(.plain)
                        }
                    }
                }
            }
            .padding()
        }
        .navigationTitle("Détails du cours")
        .navigationBarTitleDisplayMode(.inline)
        .onAppear {
            if exercises.isEmpty {
                loadExercises()
            }
        }
    }
    
    private func loadExercises() {
        guard let token = authManager.token else { return }
        
        isLoading = true
        errorMessage = nil
        
        Task {
            do {
                let response = try await APIService.shared.fetchExercises(
                    courseId: course.id,
                    token: token
                )
                await MainActor.run {
                    self.exercises = response.data.exercises
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

struct ExerciseRow: View {
    let exercise: Exercise
    
    var body: some View {
        HStack(spacing: 12) {
            // Icône selon le type
            Image(systemName: iconForType(exercise.type))
                .font(.title2)
                .foregroundColor(.blue)
                .frame(width: 40)
            
            VStack(alignment: .leading, spacing: 4) {
                Text(exercise.body)
                    .font(.body)
                    .lineLimit(2)
                
                HStack {
                    Text(exercise.type.uppercased())
                        .font(.caption2)
                        .padding(.horizontal, 6)
                        .padding(.vertical, 2)
                        .background(Color.blue.opacity(0.2))
                        .cornerRadius(4)
                    
                    if let difficulty = exercise.difficulty {
                        Text(difficulty)
                            .font(.caption2)
                            .padding(.horizontal, 6)
                            .padding(.vertical, 2)
                            .background(colorForDifficulty(difficulty).opacity(0.2))
                            .foregroundColor(colorForDifficulty(difficulty))
                            .cornerRadius(4)
                    }
                }
            }
            
            Spacer()
            
            Image(systemName: "chevron.right")
                .foregroundColor(.gray)
        }
        .padding()
        .background(Color(.systemGray6))
        .cornerRadius(12)
    }
    
    private func iconForType(_ type: String) -> String {
        switch type.lowercased() {
        case "qcm":
            return "checklist"
        case "libre":
            return "pencil.line"
        case "vrai-faux":
            return "checkmark.circle"
        case "calcul":
            return "number"
        default:
            return "questionmark.circle"
        }
    }
    
    private func colorForDifficulty(_ difficulty: String) -> Color {
        switch difficulty.lowercased() {
        case "facile":
            return .green
        case "moyen":
            return .orange
        case "difficile":
            return .red
        default:
            return .gray
        }
    }
}

#Preview {
    NavigationView {
        CourseDetailView(course: Course(
            id: 1,
            title: "Les fractions",
            grade: "6ème",
            chapter: "Arithmétique",
            description: "Apprendre les fractions simples",
            createdAt: "",
            updatedAt: "",
            exercises: nil
        ))
        .environmentObject(AuthManager.shared)
    }
}









