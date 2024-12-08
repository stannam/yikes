//
//  YIKESApp.swift
//  YIKES
//
//  Created by Stanley Nam on 2024-12-07.
//

import SwiftUI

@main
struct YIKESApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
        .defaultSize(width: 500, height: 200) // Set the default window size
        .windowResizability(.contentSize) // Ensure content-resizable behavior

    }
}
