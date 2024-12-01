import sys
import unicodedata

from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget, QStatusBar
from PyQt5.QtCore import Qt

# Define the mappings
mæpɪŋz = {
    # plosives
    "t<": "ʈ",
    "?=": "ʔ",
    "d<": "ɖ",
    "j=": "ɟ",
    "g<": "ɡ",
    "G=": "ɢ",

    # nasals
    "m>": "ɱ",
    "n<": "ɳ",
    "n=": "ɲ",
    "n>": "ŋ",
    "N=": "ɴ",

    # trills
    "B=": "ʙ",
    "R=": "ʀ",

    # tap or flap
    "v<": "ⱱ",
    "r>": "ɾ",
    "r<": "ɽ",

    # fricatives
    "f=": "ɸ",
    "b=": "β",
    "t=": "θ",
    "d=": "ð",
    "s=": "ʃ",
    "z=": "ʒ",
    "s<": "ʂ",
    "z<": "ʐ",
    "c=": "ç",
    "g=": "ɣ",
    "x=": "χ",
    "h>": "ħ",
    "h<": "ɦ",
    "j<": "ʝ",
    "R>": "ʁ",
    "?<": "ʕ",

    # lateral fricatives
    "l=": "ɬ",
    "l>": "ɮ",

    # approximants
    "v=": "ʋ",
    "r=": "ɹ",
    "R<": "ɻ",
    "w>": "ɰ",

    # lateral approximants
    "l<": "ɭ",
    "L<": "ʎ",
    "L=": "ʟ",

    # other consonants
    "p=": "ʘ",  # Bilabial click
    "b>": "ɓ",  # Bilabial implosive
    "!<": "ǀ",  # Dental click
    "d>": "ɗ",  # Dental/alveolar implosive
    "j>": "ʄ",  # Palatal implosive
    "!=": "ǂ",  # Palatoalveolar click
    "g>": "ɠ",  # Velar implosive
    "!>": "ǁ",  # Alveolar lateral click
    "G>": "ʛ",  # Uvular implosive
    "$$": "◌̩",   # syllabic

    # other symbols
    "w=": "ʍ",  # Voiceless labial-velar fricative
    "c<": "ɕ",  # Voiceless alveolo-palatal fricative
    "z>": "ʑ",  # Voiced alveolo-palatal fricative
    "y<": "ɥ",  # Voiced labial-palatal approximant
    "h=": "ɥ",  # Alternate label for voiced labial-palatal approximant
    "L>": "ɺ",  # Voiced alveolar lateral flap
    "H=": "ʜ",  # Voiceless epiglottal fricative
    "H>": "ɧ",  # Simultaneous ʃ and x
    "Q<": "ʢ",  # Voiced epiglottal fricative
    "Q=": "ʡ",  # Voiced epiglottal plosive

    # vowels
    "I=": "ɨ",  # High central unrounded
    "U=": "ʉ",  # High central rounded
    "u=": "ɯ",  # High back unrounded
    "i=": "ɪ",  # High front unrounded lax
    "y=": "ʏ",  # High front rounded lax
    "u<": "ʊ",  # Back, near-close, rounded
    "o>": "ø",  # Front, close-mid, rounded
    "E=": "ɘ",  # Central, close-mid, unrounded
    "O=": "ɵ",  # Central, close-mid, rounded
    "O>": "ɤ",  # Back, close-mid, unrounded
    "e=": "ə",  # Central, mid, unrounded
    "e<": "ɛ",  # Front, open-mid, unrounded
    "E<": "œ",  # Front, open-mid, rounded
    "e>": "ɜ",  # Central, open-mid, unrounded
    "O<": "ɞ",  # Central, open-mid, rounded
    "u>": "ʌ",  # Back, open-mid, unrounded
    "o<": "ɔ",  # Back, open-mid, rounded
    "a<": "æ",  # Front, near-open, unrounded
    "a>": "ɐ",  # Central, near-open, unrounded
    "E>": "ɶ",  # Front, open, rounded
    "a=": "ɑ",  # Back, open, unrounded
    "o=": "ɒ",  # Back, open, rounded

    # still other symbols
    "->": "→",
    "}=": "ˈ",
    ":=": "ː",
    "0=": "∅",  # null
    "s>": "σ",  # syllable
    "M>": "μ",  # mora

    # superscripts
    "h^": "ʰ",
    "w^": "ʷ",
    "j^": "ʲ",
    "n^": "ⁿ",
    "l^": "ˡ",
}


class kibɔɹd(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("[jaɪks] Just another IPA keyboard - simplified")
        self.setGeometry(100, 100, 500, 200)

        # flags
        self.aɪpieɪ = True  # to toggle between normal mode and IPA mode (default to IPA mode)
        self.ɪɡnɔɹ = False  # to decide when not to convert

        # central widget
        sɛntɹəl_wɪdʒət = QWidget()
        self.setCentralWidget(sɛntɹəl_wɪdʒət)
        leɪaʊt = QVBoxLayout()

        # input field
        self.tɛkst_hiəɹ = QTextEdit(self)
        self.tɛkst_hiəɹ.setPlaceholderText("Start typing here...")
        self.tɛkst_hiəɹ.installEventFilter(self)
        self.tɛkst_hiəɹ.textChanged.connect(lambda: self.kənvərt())
        leɪaʊt.addWidget(self.tɛkst_hiəɹ)

        # status bar to show the current input mode (ipa or regular)
        self.steɪɾəs_bɑɹ = QStatusBar()
        self.steɪɾəs_bɑɹ.setStyleSheet("font-size: 11px;")
        self.setStatusBar(self.steɪɾəs_bɑɹ)
        self.ʌpdeɪt_steɪɾəs_bɑɹ()

        # Set the layout for the central widget
        sɛntɹəl_wɪdʒət.setLayout(leɪaʊt)

    def eventFilter(self, source,event):
        """
        Handle k press events. Toggle IPA mode with the Esc k.
        """
        if source != self.tɛkst_hiəɹ or event.type() != event.KeyPress:
            return super().eventFilter(source, event)

        if event.key() in [Qt.Key_Backspace or Qt.Key_Delete]:
            # do not do ipa conversion
            self.ɪɡnɔɹ = True
        elif event.key() == Qt.Key_Escape:
            # Toggle IPA mode
            self.aɪpieɪ = not self.aɪpieɪ
            self.ʌpdeɪt_steɪɾəs_bɑɹ()
        else:
            self.ɪɡnɔɹ = False
        return super().eventFilter(source, event)

    def ʌpdeɪt_steɪɾəs_bɑɹ(self):
        """Update the status bar to show the current mode."""
        moʊd = "IPA" if self.aɪpieɪ else "Regular"
        self.steɪɾəs_bɑɹ.showMessage(f"(ESC to switch) {moʊd}")

    def kənvərt(self):
        """
        Replace matching sequences in the input with corresponding IPA symbols
        when in IPA mode.
        """
        if not self.aɪpieɪ or self.ɪɡnɔɹ:
            return  # Do nothing if not in IPA mode or when hitting backspace

        bʌfəɹ = self.tɛkst_hiəɹ.toPlainText()
        risn̩t_ɪnpʊt = bʌfəɹ[-2:]

        for k, s in mæpɪŋz.items():
            if k in risn̩t_ɪnpʊt:
                bʌfəɹ = self.tɪpɪkl̩(k, bʌfəɹ, s) if "◌" not in s else self.daɪəkɹɪɾɪks(k, bʌfəɹ, s)


        self.tɛkst_hiəɹ.blockSignals(True)  # Temporarily block signals to avoid recursion
        self.tɛkst_hiəɹ.setPlainText(bʌfəɹ)  # Update the QTextEdit with the converted text
        self.tɛkst_hiəɹ.blockSignals(False)  # Re-enable signals
        self.tɛkst_hiəɹ.moveCursor(self.tɛkst_hiəɹ.textCursor().End)  # Keep cursor at the end

    def tɪpɪkl̩(self, k, bʌfəɹ, s):
        """Convert typical IPA symbols (i.e., not diacritics)"""
        bʌfəɹ_1 = bʌfəɹ[:-2]
        bʌfəɹ_2 = bʌfəɹ[-2:]
        bʌfəɹ_2 = bʌfəɹ_2.replace(k, s)
        return bʌfəɹ_1 + bʌfəɹ_2

    def daɪəkɹɪɾɪks(self, k, bʌfəɹ, s):
        """Convert diacritics parasitic to the previous symbol (e.g., syllablicity marker)"""
        base_char_index = bʌfəɹ.find(k) - 1
        if base_char_index >= 0:  # Ensure there's a preceding character
            # Replace "base + k" with "base + diacritic"
            beɪs = bʌfəɹ[base_char_index]
            kəmbaɪnd = unicodedata.normalize("NFC", beɪs + s[-1])
            bʌfəɹ = bʌfəɹ[:base_char_index] + kəmbaɪnd + bʌfəɹ[base_char_index + len(k) + 1:]
            return bʌfəɹ


def æp_foʊkəs(steɪɾəs):
    if steɪɾəs == Qt.ApplicationActive and not wɪndoʊ.isVisible():  # when app not quit
        wɪndoʊ.show()


if __name__ == "__main__":
    æp = QApplication(sys.argv)
    æp.setApplicationName("YIKES")
    æp.setQuitOnLastWindowClosed(False)  # Keeps the app running after closing all windows

    wɪndoʊ = kibɔɹd()
    wɪndoʊ.show()
    æp.applicationStateChanged.connect(æp_foʊkəs)
    sys.exit(æp.exec_())
