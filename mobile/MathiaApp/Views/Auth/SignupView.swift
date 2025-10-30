import SwiftUI

struct SignupView: View {
    @EnvironmentObject var authManager: AuthManager
    @Environment(\.dismiss) var dismiss
    
    @State private var name = ""
    @State private var email = ""
    @State private var password = ""
    @State private var confirmPassword = ""
    @State private var isLoading = false
    @State private var errorMessage: String?
    
    var body: some View {
        NavigationView {
            ZStack {
                // Fond dégradé
                LinearGradient(
                    colors: [Color.purple.opacity(0.6), Color.blue.opacity(0.4)],
                    startPoint: .topLeading,
                    endPoint: .bottomTrailing
                )
                .ignoresSafeArea()
                
                ScrollView {
                    VStack(spacing: 25) {
                        // Titre
                        VStack(spacing: 10) {
                            Image(systemName: "person.badge.plus")
                                .font(.system(size: 60))
                                .foregroundColor(.white)
                            
                            Text("Créer un compte")
                                .font(.system(size: 32, weight: .bold))
                                .foregroundColor(.white)
                        }
                        .padding(.top, 40)
                        .padding(.bottom, 20)
                        
                        // Formulaire
                        VStack(spacing: 20) {
                            // Nom
                            VStack(alignment: .leading, spacing: 8) {
                                Text("Nom complet")
                                    .font(.subheadline)
                                    .foregroundColor(.white)
                                
                                TextField("", text: $name)
                                    .textFieldStyle(RoundedTextFieldStyle())
                                    .textContentType(.name)
                            }
                            
                            // Email
                            VStack(alignment: .leading, spacing: 8) {
                                Text("Email")
                                    .font(.subheadline)
                                    .foregroundColor(.white)
                                
                                TextField("", text: $email)
                                    .textFieldStyle(RoundedTextFieldStyle())
                                    .textContentType(.emailAddress)
                                    .autocapitalization(.none)
                                    .keyboardType(.emailAddress)
                            }
                            
                            // Mot de passe
                            VStack(alignment: .leading, spacing: 8) {
                                Text("Mot de passe")
                                    .font(.subheadline)
                                    .foregroundColor(.white)
                                
                                SecureField("", text: $password)
                                    .textFieldStyle(RoundedTextFieldStyle())
                                    .textContentType(.newPassword)
                            }
                            
                            // Confirmation mot de passe
                            VStack(alignment: .leading, spacing: 8) {
                                Text("Confirmer le mot de passe")
                                    .font(.subheadline)
                                    .foregroundColor(.white)
                                
                                SecureField("", text: $confirmPassword)
                                    .textFieldStyle(RoundedTextFieldStyle())
                                    .textContentType(.newPassword)
                            }
                            
                            // Validation du mot de passe
                            if !password.isEmpty && password.count < 6 {
                                Text("Le mot de passe doit contenir au moins 6 caractères")
                                    .font(.caption)
                                    .foregroundColor(.yellow)
                            }
                            
                            if !confirmPassword.isEmpty && password != confirmPassword {
                                Text("Les mots de passe ne correspondent pas")
                                    .font(.caption)
                                    .foregroundColor(.red)
                            }
                            
                            // Message d'erreur
                            if let error = errorMessage {
                                Text(error)
                                    .font(.caption)
                                    .foregroundColor(.red)
                                    .padding()
                                    .background(Color.white.opacity(0.9))
                                    .cornerRadius(8)
                            }
                            
                            // Bouton d'inscription
                            Button(action: handleSignup) {
                                if isLoading {
                                    ProgressView()
                                        .progressViewStyle(CircularProgressViewStyle(tint: .purple))
                                } else {
                                    Text("S'inscrire")
                                        .font(.headline)
                                        .foregroundColor(.purple)
                                }
                            }
                            .frame(maxWidth: .infinity)
                            .frame(height: 50)
                            .background(Color.white)
                            .cornerRadius(12)
                            .disabled(!isFormValid || isLoading)
                            .opacity(isFormValid ? 1 : 0.6)
                        }
                        .padding(.horizontal, 40)
                        
                        Spacer()
                    }
                }
            }
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarLeading) {
                    Button("Annuler") {
                        dismiss()
                    }
                    .foregroundColor(.white)
                }
            }
        }
    }
    
    private var isFormValid: Bool {
        !name.isEmpty &&
        !email.isEmpty &&
        password.count >= 6 &&
        password == confirmPassword
    }
    
    private func handleSignup() {
        errorMessage = nil
        isLoading = true
        
        Task {
            do {
                try await authManager.signup(name: name, email: email, password: password)
                await MainActor.run {
                    dismiss()
                }
            } catch {
                await MainActor.run {
                    errorMessage = error.localizedDescription
                    isLoading = false
                }
            }
        }
    }
}

#Preview {
    SignupView()
        .environmentObject(AuthManager.shared)
}






