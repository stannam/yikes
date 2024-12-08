import SwiftUI

struct ContentView: View {
    @State private var text: String = "" // Holds the user input text
    @State private var inputMode: String = "IPA" // Variable for the input mode
    @State private var ignore: Bool = false // Flag for delete/backspace entered
    
    var body: some View {
        VStack(spacing: 4) {  // Vertical stack for textbox and status bar
            TextEditor(text: $text) // A simple, scrollable text editor
                .font(.body)
                .frame(minWidth: 250, maxWidth: .infinity,
                       minHeight: 20, maxHeight: .infinity)
                // when IPA mode and key changes, see if conversion needed
                .onChange(of: text) {
                    guard inputMode == "IPA", !ignore else {
                        ignore = false
                        return
                    }
                    
                    // Check last two characters (if text is long enough)
                    if text.count >= 2 {
                        let lastTwo = String(text.suffix(2))
                        if let replacement = mappings[lastTwo] {
                            // Remove the last two chars and append the replacement
                            text.removeLast(2)
                            text.append(replacement)
                        }
                    }
                }

            Text("Current mode (ESC to switch):   \(inputMode)")
                .frame(minWidth: 250, maxWidth: .infinity, alignment: .topLeading) // Make the status bar fill horizontally
                .font(.system(size: 12))
        }
        .padding()
        .background(Color.gray.opacity(0.2)) // Background color for entire window
        .frame(width: 500, height: 200) // Default window size
        .onAppear {
            setupKeyEventHandling()
        }
    }

    // Function to handle ESC key globally
    private func setupKeyEventHandling() {
        NSEvent.addLocalMonitorForEvents(matching: .keyDown) { event in
            if event.keyCode == 53 { // ESC key
                inputMode = (inputMode == "IPA") ? "Regular" : "IPA"
                return nil // Consume the event
            }
            if event.keyCode == 51 || event.keyCode == 117 {  // forward or backward delete
                ignore = true
            }
            return event // Pass other events through
        }
    }
}

#Preview {
    ContentView()
}
