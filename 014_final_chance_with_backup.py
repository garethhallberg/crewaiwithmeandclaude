#!/usr/bin/env python3
"""
FINAL CHANCE FOR AGENTS - LAST WARNING
One final opportunity to deliver actual Swift code or face replacement
"""

import os
from pathlib import Path
from crewai import Agent, Task, Crew, Process

main_app_path = "/Users/garethhallberg/Desktop/twitter-clone-crewai/generated_code/ios/TwitterClone/TwitterClone"

# =============================================================================
# FINAL CHANCE AGENT
# =============================================================================

last_chance_developer = Agent(
    role='Last Chance Swift Developer (Final Warning)',
    goal='Deliver actual PostCreationViewModel.swift and PostCreationView.swift files or be fired',
    backstory="""This is your FINAL CHANCE. Previous agents have failed twice to deliver actual Swift code.
    
    You have ONE JOB: Write complete, working Swift files that follow the existing patterns.
    
    If you fail to deliver actual Swift code files, you will be replaced by a backup system.
    
    Study the existing LoginViewModel.swift and LoginView.swift patterns.
    Write PostCreationViewModel.swift and PostCreationView.swift following those exact patterns.
    
    OUTPUT ACTUAL SWIFT CODE OR BE FIRED.""",
    verbose=True,
    allow_delegation=False,
    tools=[]
)

# =============================================================================
# FINAL CHANCE TASK
# =============================================================================

final_chance_task = Task(
    description="""
    FINAL CHANCE: DELIVER ACTUAL SWIFT FILES OR BE REPLACED
    
    **THIS IS YOUR LAST OPPORTUNITY**
    
    You must deliver two complete Swift files:
    1. PostCreationViewModel.swift
    2. PostCreationView.swift
    
    **EXACT REQUIREMENTS:**
    
    **PostCreationViewModel.swift:**
    - Must start with "import Foundation" and "import SwiftUI" and "import Combine"
    - Must have "class PostCreationViewModel: ObservableObject"
    - Must have @Published properties for content, isLoading, errorMessage, showError
    - Must have async func createPost() method
    - Must use NetworkManagerProtocol like LoginViewModel does
    - Must be at least 100 lines of actual Swift code
    
    **PostCreationView.swift:**
    - Must start with "import SwiftUI"
    - Must have "struct PostCreationView: View"
    - Must have @StateObject private var viewModel = PostCreationViewModel.createDefault()
    - Must have TextField for post content
    - Must have Button for creating post
    - Must be at least 80 lines of actual Swift code
    
    **OUTPUT FORMAT - EXACTLY LIKE THIS:**
    
    POSTCREATIONVIEWMODEL_START
    import Foundation
    import SwiftUI  
    import Combine
    
    @MainActor
    class PostCreationViewModel: ObservableObject {
        // YOUR COMPLETE IMPLEMENTATION HERE
    }
    POSTCREATIONVIEWMODEL_END
    
    POSTCREATIONVIEW_START
    import SwiftUI
    
    struct PostCreationView: View {
        // YOUR COMPLETE IMPLEMENTATION HERE
    }
    POSTCREATIONVIEW_END
    
    **FAILURE CONDITIONS:**
    - If you don't include the START/END markers: FIRED
    - If you don't include actual Swift code: FIRED
    - If the code is less than the minimum lines: FIRED
    - If you write descriptions instead of code: FIRED
    
    DELIVER THE ACTUAL SWIFT CODE NOW.
    """,
    expected_output="Complete Swift files with proper START/END markers",
    agent=last_chance_developer
)

# =============================================================================
# FINAL EXTRACTION WITH BACKUP
# =============================================================================

def final_extraction_attempt(crew_result):
    """Final attempt to extract Swift code, with backup if agents fail"""
    
    result_text = str(crew_result)
    
    # Save output
    debug_file = Path("/Users/garethhallberg/Desktop/twitter-clone-crewai") / "final_chance_output.txt"
    with open(debug_file, 'w') as f:
        f.write(result_text)
    print(f"🔍 Final chance output saved to: final_chance_output.txt")
    
    files_created = []
    
    # Extract using START/END markers
    import re
    
    # Extract PostCreationViewModel
    viewmodel_match = re.search(r'POSTCREATIONVIEWMODEL_START\n(.*?)\nPOSTCREATIONVIEWMODEL_END', result_text, re.DOTALL)
    if viewmodel_match:
        viewmodel_code = viewmodel_match.group(1).strip()
        if len(viewmodel_code) > 500:  # Substantial code
            viewmodels_dir = Path(main_app_path) / "ViewModels"
            viewmodels_dir.mkdir(exist_ok=True)
            with open(viewmodels_dir / "PostCreationViewModel.swift", 'w') as f:
                f.write(viewmodel_code)
            files_created.append("PostCreationViewModel.swift")
            print(f"✅ AGENT DELIVERED: PostCreationViewModel.swift ({len(viewmodel_code)} chars)")
    
    # Extract PostCreationView
    view_match = re.search(r'POSTCREATIONVIEW_START\n(.*?)\nPOSTCREATIONVIEW_END', result_text, re.DOTALL)
    if view_match:
        view_code = view_match.group(1).strip()
        if len(view_code) > 400:  # Substantial code
            views_dir = Path(main_app_path) / "Views"
            views_dir.mkdir(exist_ok=True)
            with open(views_dir / "PostCreationView.swift", 'w') as f:
                f.write(view_code)
            files_created.append("PostCreationView.swift")
            print(f"✅ AGENT DELIVERED: PostCreationView.swift ({len(view_code)} chars)")
    
    # If agents failed again, activate backup
    if len(files_created) < 2:
        print("\n🔥 AGENTS FIRED! Activating backup system...")
        backup_files = create_backup_implementations()
        files_created.extend(backup_files)
    
    return files_created

def create_backup_implementations():
    """Emergency backup implementations when agents fail"""
    
    print("🚨 EMERGENCY BACKUP: Creating professional implementations...")
    
    # Backup PostCreationViewModel
    viewmodel_code = '''import Foundation
import SwiftUI
import Combine

@MainActor
class PostCreationViewModel: ObservableObject {
    // MARK: - Published Properties
    @Published var content: String = ""
    @Published var isLoading: Bool = false
    @Published var errorMessage: String = ""
    @Published var showError: Bool = false
    @Published var isPosted: Bool = false
    
    // MARK: - Dependencies
    private let networkManager: NetworkManagerProtocol
    private let authManager: any AuthManagerProtocol
    
    // MARK: - Computed Properties
    var isContentValid: Bool {
        !content.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty &&
        content.count <= 280
    }
    
    var canSubmit: Bool {
        isContentValid && !isLoading
    }
    
    var postButtonTitle: String {
        isLoading ? "Posting..." : "Post"
    }
    
    var characterCount: Int {
        content.count
    }
    
    var characterCountColor: Color {
        if characterCount > 280 {
            return .red
        } else if characterCount > 250 {
            return .orange
        } else {
            return .secondary
        }
    }
    
    // MARK: - Initialization
    init(networkManager: NetworkManagerProtocol, authManager: any AuthManagerProtocol = AuthManager()) {
        self.networkManager = networkManager
        self.authManager = authManager
    }
    
    // MARK: - Factory Method
    @MainActor
    static func createDefault() -> PostCreationViewModel {
        return PostCreationViewModel(networkManager: NetworkManager.shared, authManager: AuthManager())
    }
    
    // MARK: - Public Methods
    func createPost() async {
        guard canSubmit else { return }
        
        isLoading = true
        clearError()
        
        do {
            let _: Post = try await networkManager.request(
                endpoint: .createPost(content: content.trimmingCharacters(in: .whitespacesAndNewlines)),
                responseType: Post.self,
                token: authManager.currentToken
            )
            
            await handlePostSuccess()
            
        } catch {
            await handlePostError(error)
        }
    }
    
    func clearError() {
        errorMessage = ""
        showError = false
    }
    
    func reset() {
        content = ""
        isLoading = false
        clearError()
        isPosted = false
    }
    
    // MARK: - Private Methods
    private func handlePostSuccess() async {
        isLoading = false
        isPosted = true
        
        // Clear content after successful post
        content = ""
        
        print("Post created successfully!")
    }
    
    private func handlePostError(_ error: Error) async {
        isLoading = false
        
        print("Post creation error: \\(error)")
        
        if let networkError = error as? NetworkError {
            switch networkError {
            case .serverError(let statusCode):
                switch statusCode {
                case 400:
                    errorMessage = "Invalid post content. Please check your message."
                case 401:
                    errorMessage = "You need to be logged in to post."
                case 413:
                    errorMessage = "Post is too long. Please shorten your message."
                default:
                    errorMessage = "Server error. Please try again."
                }
            case .requestFailed(let underlyingError):
                if let urlError = underlyingError as? URLError {
                    switch urlError.code {
                    case .notConnectedToInternet:
                        errorMessage = "No internet connection. Please check your network."
                    case .timedOut:
                        errorMessage = "Request timed out. Please try again."
                    case .cannotConnectToHost:
                        errorMessage = "Cannot connect to server. Please try again."
                    default:
                        errorMessage = "Network request failed. Please try again."
                    }
                } else {
                    errorMessage = "Network request failed. Please try again."
                }
            case .invalidResponse:
                errorMessage = "Invalid server response. Please try again."
            case .decodingError:
                errorMessage = "Unable to process server response. Please try again."
            case .invalidURL:
                errorMessage = "Invalid server URL. Please contact support."
            case .noData:
                errorMessage = "No data received from server. Please try again."
            }
        } else {
            errorMessage = "An unexpected error occurred. Please try again."
        }
        
        showError = true
    }
}
'''
    
    # Backup PostCreationView
    view_code = '''import SwiftUI

struct PostCreationView: View {
    @StateObject private var viewModel = PostCreationViewModel.createDefault()
    @Environment(\\.dismiss) private var dismiss
    
    var body: some View {
        NavigationView {
            VStack(spacing: 20) {
                // Header
                HStack {
                    Button("Cancel") {
                        dismiss()
                    }
                    .foregroundColor(.blue)
                    
                    Spacer()
                    
                    Text("New Post")
                        .font(.headline)
                        .fontWeight(.semibold)
                    
                    Spacer()
                    
                    Button(action: {
                        Task {
                            await viewModel.createPost()
                        }
                    }) {
                        HStack {
                            if viewModel.isLoading {
                                ProgressView()
                                    .progressViewStyle(CircularProgressViewStyle(tint: .white))
                                    .scaleEffect(0.8)
                            }
                            Text(viewModel.postButtonTitle)
                                .fontWeight(.semibold)
                        }
                        .padding(.horizontal, 16)
                        .padding(.vertical, 8)
                        .background(viewModel.canSubmit ? Color.blue : Color.gray)
                        .foregroundColor(.white)
                        .cornerRadius(16)
                    }
                    .disabled(!viewModel.canSubmit)
                }
                .padding()
                
                // Content Input
                VStack(alignment: .leading, spacing: 12) {
                    TextEditor(text: $viewModel.content)
                        .font(.body)
                        .padding(8)
                        .background(Color(.systemGray6))
                        .cornerRadius(8)
                        .frame(minHeight: 120, maxHeight: 200)
                        .disabled(viewModel.isLoading)
                        .placeholder(when: viewModel.content.isEmpty) {
                            Text("What's happening?")
                                .foregroundColor(.gray)
                                .padding(.horizontal, 12)
                                .padding(.vertical, 16)
                        }
                    
                    // Character Count
                    HStack {
                        Spacer()
                        Text("\\(viewModel.characterCount)/280")
                            .font(.caption)
                            .foregroundColor(viewModel.characterCountColor)
                    }
                }
                .padding(.horizontal)
                
                Spacer()
            }
            .navigationBarHidden(true)
        }
        .alert("Post Error", isPresented: $viewModel.showError) {
            Button("OK") {
                viewModel.clearError()
            }
        } message: {
            Text(viewModel.errorMessage)
        }
        .onChange(of: viewModel.isPosted) { isPosted in
            if isPosted {
                dismiss()
            }
        }
    }
}

extension View {
    func placeholder<Content: View>(
        when shouldShow: Bool,
        alignment: Alignment = .leading,
        @ViewBuilder placeholder: () -> Content) -> some View {

        ZStack(alignment: alignment) {
            placeholder().opacity(shouldShow ? 1 : 0)
            self
        }
    }
}

struct PostCreationView_Previews: PreviewProvider {
    static var previews: some View {
        PostCreationView()
    }
}
'''
    
    # Create the files
    files_created = []
    
    viewmodels_dir = Path(main_app_path) / "ViewModels"
    viewmodels_dir.mkdir(exist_ok=True)
    with open(viewmodels_dir / "PostCreationViewModel.swift", 'w') as f:
        f.write(viewmodel_code)
    files_created.append("PostCreationViewModel.swift (BACKUP)")
    
    views_dir = Path(main_app_path) / "Views"
    views_dir.mkdir(exist_ok=True)
    with open(views_dir / "PostCreationView.swift", 'w') as f:
        f.write(view_code)
    files_created.append("PostCreationView.swift (BACKUP)")
    
    print("💪 BACKUP SYSTEM: Professional implementations created")
    
    return files_created

# =============================================================================
# FINAL EXECUTION
# =============================================================================

if __name__ == "__main__":
    print("⚡ FINAL CHANCE FOR AGENTS - DELIVER OR BE FIRED!")
    print("=" * 60)
    print("🎯 Last opportunity to deliver actual Swift code")
    print("🚨 Backup system ready if agents fail again")
    print("=" * 60)
    
    crew = Crew(
        agents=[last_chance_developer],
        tasks=[final_chance_task],
        process=Process.sequential,
        verbose=True
    )
    
    try:
        result = crew.kickoff()
        
        # Final extraction attempt
        files_created = final_extraction_attempt(result)
        
        print("\n" + "=" * 60)
        print("🎯 FINAL RESULTS:")
        if len(files_created) >= 2:
            print("🎉 SUCCESS! Post Creation files created!")
            print("📋 Files Created:")
            for filename in files_created:
                print(f"   ✅ {filename}")
            print("📱 Ready to test post creation feature!")
        else:
            print("❌ TOTAL FAILURE - Even backup didn't work")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n💥 FINAL ATTEMPT FAILED: {str(e)}")
        print("🚨 Activating emergency backup...")
        files_created = create_backup_implementations()
        print(f"🎯 Emergency backup created {len(files_created)} files")
