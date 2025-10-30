import SwiftUI

struct QuizView: View {
    @EnvironmentObject var authManager: AuthManager
    @Environment(\.dismiss) var dismiss
    
    let exercise: Exercise
    
    @State private var selectedAnswer: String?
    @State private var isSubmitted = false
    @State private var attemptResult: AttemptData?
    @State private var isLoading = false
    @State private var errorMessage: String?
    
    var body: some View {
        ScrollView {
            VStack(spacing: 24) {
                // En-tête
                VStack(alignment: .leading, spacing: 12) {
                    HStack {
                        if let difficulty = exercise.difficulty {
                            DifficultyBadge(difficulty: difficulty)
                        }
                        
                        Spacer()
                        
                        Text(exercise.type.uppercased())
                            .font(.caption)
                            .fontWeight(.semibold)
                            .padding(.horizontal, 10)
                            .padding(.vertical, 5)
                            .background(Color.blue.opacity(0.2))
                            .foregroundColor(.blue)
                            .cornerRadius(8)
                    }
                    
                    if let courseInfo = exercise.course {
                        Text(courseInfo.title)
                            .font(.caption)
                            .foregroundColor(.secondary)
                    }
                }
                .padding()
                
                // Question
                VStack(alignment: .leading, spacing: 12) {
                    Text("Question")
                        .font(.headline)
                        .foregroundColor(.secondary)
                    
                    Text(exercise.body)
                        .font(.title3)
                        .fontWeight(.semibold)
                }
                .frame(maxWidth: .infinity, alignment: .leading)
                .padding()
                .background(Color.blue.opacity(0.1))
                .cornerRadius(12)
                
                // Options (pour QCM)
                if exercise.type.lowercased() == "qcm", let options = exercise.options {
                    VStack(spacing: 12) {
                        ForEach(exercise.sortedOptions, id: \.key) { option in
                            OptionButton(
                                key: option.key,
                                value: option.value,
                                isSelected: selectedAnswer == option.key,
                                isCorrect: attemptResult?.isCorrect == true && selectedAnswer == option.key,
                                isWrong: attemptResult?.isCorrect == false && selectedAnswer == option.key,
                                isDisabled: isSubmitted
                            ) {
                                if !isSubmitted {
                                    selectedAnswer = option.key
                                }
                            }
                        }
                    }
                } else {
                    // Input libre pour autres types
                    VStack(alignment: .leading, spacing: 8) {
                        Text("Votre réponse:")
                            .font(.headline)
                        
                        TextField("Entrez votre réponse", text: Binding(
                            get: { selectedAnswer ?? "" },
                            set: { selectedAnswer = $0 }
                        ))
                        .textFieldStyle(.roundedBorder)
                        .disabled(isSubmitted)
                    }
                    .padding()
                }
                
                // Résultat
                if let result = attemptResult {
                    ResultCard(result: result)
                }
                
                // Message d'erreur
                if let error = errorMessage {
                    Text(error)
                        .foregroundColor(.red)
                        .padding()
                        .background(Color.red.opacity(0.1))
                        .cornerRadius(8)
                }
                
                // Boutons
                HStack(spacing: 16) {
                    if !isSubmitted {
                        Button(action: submitAnswer) {
                            if isLoading {
                                ProgressView()
                            } else {
                                Text("Valider")
                            }
                        }
                        .buttonStyle(PrimaryButtonStyle())
                        .disabled(selectedAnswer == nil || selectedAnswer?.isEmpty == true || isLoading)
                    } else {
                        Button(action: { dismiss() }) {
                            Text("Retour")
                        }
                        .buttonStyle(SecondaryButtonStyle())
                    }
                }
                .padding(.vertical)
            }
            .padding()
        }
        .navigationTitle("Exercice")
        .navigationBarTitleDisplayMode(.inline)
    }
    
    private func submitAnswer() {
        guard let answer = selectedAnswer, !answer.isEmpty else { return }
        guard let token = authManager.token else { return }
        
        isLoading = true
        errorMessage = nil
        
        Task {
            do {
                let response = try await APIService.shared.submitAttempt(
                    exerciseId: exercise.id,
                    userAnswer: answer,
                    token: token
                )
                
                await MainActor.run {
                    self.attemptResult = response.data
                    self.isSubmitted = true
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

// MARK: - Components

struct DifficultyBadge: View {
    let difficulty: String
    
    var body: some View {
        Text(difficulty)
            .font(.caption)
            .fontWeight(.semibold)
            .padding(.horizontal, 10)
            .padding(.vertical, 5)
            .background(color.opacity(0.2))
            .foregroundColor(color)
            .cornerRadius(8)
    }
    
    private var color: Color {
        switch difficulty.lowercased() {
        case "facile": return .green
        case "moyen": return .orange
        case "difficile": return .red
        default: return .gray
        }
    }
}

struct OptionButton: View {
    let key: String
    let value: String
    let isSelected: Bool
    let isCorrect: Bool
    let isWrong: Bool
    let isDisabled: Bool
    let action: () -> Void
    
    var body: some View {
        Button(action: action) {
            HStack {
                Text(key)
                    .font(.title3)
                    .fontWeight(.bold)
                    .frame(width: 40, height: 40)
                    .background(backgroundColor)
                    .foregroundColor(foregroundColor)
                    .cornerRadius(8)
                
                Text(value)
                    .font(.body)
                    .foregroundColor(.primary)
                
                Spacer()
                
                if isCorrect {
                    Image(systemName: "checkmark.circle.fill")
                        .foregroundColor(.green)
                        .font(.title2)
                } else if isWrong {
                    Image(systemName: "xmark.circle.fill")
                        .foregroundColor(.red)
                        .font(.title2)
                }
            }
            .padding()
            .background(
                RoundedRectangle(cornerRadius: 12)
                    .stroke(borderColor, lineWidth: 2)
                    .background(
                        RoundedRectangle(cornerRadius: 12)
                            .fill(backgroundFill)
                    )
            )
        }
        .disabled(isDisabled)
        .buttonStyle(.plain)
    }
    
    private var backgroundColor: Color {
        if isCorrect { return .green }
        if isWrong { return .red }
        if isSelected { return .blue }
        return Color(.systemGray5)
    }
    
    private var foregroundColor: Color {
        if isCorrect || isWrong || isSelected { return .white }
        return .primary
    }
    
    private var borderColor: Color {
        if isCorrect { return .green }
        if isWrong { return .red }
        if isSelected { return .blue }
        return Color(.systemGray4)
    }
    
    private var backgroundFill: Color {
        if isCorrect { return .green.opacity(0.1) }
        if isWrong { return .red.opacity(0.1) }
        return .clear
    }
}

struct ResultCard: View {
    let result: AttemptData
    
    var body: some View {
        VStack(alignment: .leading, spacing: 16) {
            HStack {
                Image(systemName: result.isCorrect ? "checkmark.circle.fill" : "xmark.circle.fill")
                    .font(.title)
                    .foregroundColor(result.isCorrect ? .green : .red)
                
                Text(result.isCorrect ? "Bonne réponse !" : "Réponse incorrecte")
                    .font(.title3)
                    .fontWeight(.bold)
                
                Spacer()
            }
            
            if let explanation = result.explanation {
                VStack(alignment: .leading, spacing: 8) {
                    Text("Explication")
                        .font(.headline)
                    
                    Text(explanation)
                        .font(.body)
                        .foregroundColor(.secondary)
                }
            }
            
            if let correctAnswer = result.correctAnswer {
                HStack {
                    Text("Bonne réponse:")
                        .font(.subheadline)
                        .fontWeight(.semibold)
                    
                    Text(correctAnswer)
                        .font(.subheadline)
                        .foregroundColor(.green)
                }
            }
        }
        .padding()
        .background(
            RoundedRectangle(cornerRadius: 12)
                .fill(result.isCorrect ? Color.green.opacity(0.1) : Color.red.opacity(0.1))
        )
    }
}

// MARK: - Button Styles

struct PrimaryButtonStyle: ButtonStyle {
    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .font(.headline)
            .foregroundColor(.white)
            .frame(maxWidth: .infinity)
            .frame(height: 50)
            .background(Color.blue)
            .cornerRadius(12)
            .opacity(configuration.isPressed ? 0.8 : 1.0)
    }
}

struct SecondaryButtonStyle: ButtonStyle {
    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .font(.headline)
            .foregroundColor(.blue)
            .frame(maxWidth: .infinity)
            .frame(height: 50)
            .background(Color.blue.opacity(0.1))
            .cornerRadius(12)
            .opacity(configuration.isPressed ? 0.8 : 1.0)
    }
}

#Preview {
    NavigationView {
        QuizView(exercise: Exercise(
            id: 1,
            courseId: 1,
            type: "qcm",
            body: "Quelle est la moitié de 10?",
            options: ["A": "3", "B": "5", "C": "7", "D": "10"],
            answer: "B",
            explanation: "10 divisé par 2 égale 5",
            difficulty: "facile",
            tags: ["fractions"],
            createdAt: "",
            updatedAt: "",
            course: nil
        ))
        .environmentObject(AuthManager.shared)
    }
}






