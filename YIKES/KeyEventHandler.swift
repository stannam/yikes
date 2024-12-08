//
//  KeyEventHandler.swift
//  YIKES
//
//  Created by Stanley Nam on 2024-12-07.
//

import SwiftUI
import AppKit

class KeyEventHandlerView: NSView {
    let onKeyDown: (UInt16) -> Void

    init(onKeyDown: @escaping (UInt16) -> Void) {
        self.onKeyDown = onKeyDown
        super.init(frame: .zero)
        self.translatesAutoresizingMaskIntoConstraints = false
    }

    required init?(coder: NSCoder) {
        fatalError("init(coder:) has not been implemented")
    }

    override func keyDown(with event: NSEvent) {
        onKeyDown(event.keyCode)
    }

    override var acceptsFirstResponder: Bool {
        return true
    }

    override func becomeFirstResponder() -> Bool {
        true
    }
}
