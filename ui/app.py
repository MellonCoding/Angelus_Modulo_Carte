import tkinter as tk
from tkinter import ttk, messagebox
from deck import Deck
from pescata import Pescata


class App(tk.Tk):
    """Game-style interface for the Pescata demo."""

    BG = "#17151f"
    PANEL = "#211e2b"
    PANEL_2 = "#292535"
    TEXT = "#f2edf7"
    MUTED = "#aaa1b7"
    ACCENT = "#c9a86a"
    GREEN = "#8fc7a3"
    RED = "#d98f9a"
    BORDER = "#40394d"

    def __init__(self):
        super().__init__()
        self.title("PESCATA")
        self.geometry("1180x760")
        self.minsize(1000, 680)
        self.configure(bg=self.BG)

        self.deck = Deck()
        self.current_pescata = None
        self.card_vars = []

        self._configure_styles()
        self._build_ui()
        self._update_deck_label()

    def _configure_styles(self):
        style = ttk.Style(self)
        style.theme_use("clam")

        style.configure("TFrame", background=self.BG)
        style.configure("Panel.TFrame", background=self.PANEL)
        style.configure("Card.TFrame", background=self.PANEL_2)

        style.configure(
            "Title.TLabel",
            background=self.BG,
            foreground=self.TEXT,
            font=("TkDefaultFont", 28, "bold"),
        )
        style.configure(
            "Subtitle.TLabel",
            background=self.BG,
            foreground=self.MUTED,
            font=("TkDefaultFont", 10),
        )
        style.configure(
            "PanelTitle.TLabel",
            background=self.PANEL,
            foreground=self.TEXT,
            font=("TkDefaultFont", 13, "bold"),
        )
        style.configure(
            "Card.TLabel",
            background=self.PANEL_2,
            foreground=self.TEXT,
            font=("TkDefaultFont", 11),
        )
        style.configure(
            "Muted.TLabel",
            background=self.PANEL,
            foreground=self.MUTED,
            font=("TkDefaultFont", 9),
        )
        style.configure(
            "Score.TLabel",
            background=self.PANEL,
            foreground=self.TEXT,
            font=("TkDefaultFont", 25, "bold"),
        )
        style.configure(
            "TButton",
            background=self.ACCENT,
            foreground="#17151f",
            padding=(15, 9),
            font=("TkDefaultFont", 10, "bold"),
        )
        style.map(
            "TButton",
            background=[("disabled", "#4b4653"), ("active", "#dfc084")],
            foreground=[("disabled", "#aaa5af"), ("active", "#17151f")],
        )

    def _build_ui(self):
        header = ttk.Frame(self)
        header.pack(fill="x", padx=28, pady=(22, 10))

        title_box = ttk.Frame(header)
        title_box.pack(side="left")

        ttk.Label(title_box, text="PESCATA", style="Title.TLabel").pack(anchor="w")
        ttk.Label(
            title_box,
            text="Una lettura. Un seme. La fortuna decide.",
            style="Subtitle.TLabel",
        ).pack(anchor="w")

        self.deck_label = tk.Label(
            header,
            text="",
            bg=self.PANEL,
            fg=self.TEXT,
            font=("TkDefaultFont", 11, "bold"),
            padx=18,
            pady=12,
        )
        self.deck_label.pack(side="right")

        controls = tk.Frame(
            self,
            bg=self.PANEL,
            highlightbackground=self.BORDER,
            highlightthickness=1,
        )
        controls.pack(fill="x", padx=28, pady=8)

        tk.Label(
            controls,
            text="NUOVA PESCATA",
            bg=self.PANEL,
            fg=self.ACCENT,
            font=("TkDefaultFont", 10, "bold"),
        ).grid(row=0, column=0, columnspan=6, sticky="w", padx=18, pady=(14, 8))

        tk.Label(
            controls, text="Carte", bg=self.PANEL, fg=self.MUTED
        ).grid(row=1, column=0, padx=(18, 6), pady=(0, 16))

        self.number_var = tk.IntVar(value=5)
        self.number_spin = tk.Spinbox(
            controls,
            from_=1,
            to=78,
            textvariable=self.number_var,
            width=6,
            bg=self.PANEL_2,
            fg=self.TEXT,
            insertbackground=self.TEXT,
            buttonbackground=self.PANEL_2,
            relief="flat",
            font=("TkDefaultFont", 11),
        )
        self.number_spin.grid(row=1, column=1, padx=(0, 25), pady=(0, 16))

        tk.Label(
            controls, text="Seme", bg=self.PANEL, fg=self.MUTED
        ).grid(row=1, column=2, padx=(0, 6), pady=(0, 16))

        self.suit_var = tk.StringVar(value="Bastoni")
        self.suit_menu = ttk.Combobox(
            controls,
            textvariable=self.suit_var,
            values=["Bastoni", "Spade", "Denari", "Coppe"],
            state="readonly",
            width=13,
        )
        self.suit_menu.grid(row=1, column=3, padx=(0, 25), pady=(0, 16))

        self.draw_button = ttk.Button(
            controls, text="INIZIA PESCATA", command=self.start_pescata
        )
        self.draw_button.grid(row=1, column=4, padx=(0, 10), pady=(0, 16))

        self.new_button = ttk.Button(
            controls, text="NUOVA PARTITA", command=self.reset_game
        )
        self.new_button.grid(row=1, column=5, padx=(0, 18), pady=(0, 16))

        self.status_label = tk.Label(
            self,
            text="Scegli quante carte pescare e il seme della lettura.",
            bg=self.BG,
            fg=self.MUTED,
            font=("TkDefaultFont", 10),
            anchor="w",
        )
        self.status_label.pack(fill="x", padx=30, pady=(4, 8))

        main = tk.Frame(self, bg=self.BG)
        main.pack(fill="both", expand=True, padx=28, pady=(0, 18))

        # Left: cards
        cards_panel = tk.Frame(
            main,
            bg=self.PANEL,
            highlightbackground=self.BORDER,
            highlightthickness=1,
        )
        cards_panel.pack(side="left", fill="both", expand=True)

        tk.Label(
            cards_panel,
            text="CARTE SUL TAVOLO",
            bg=self.PANEL,
            fg=self.TEXT,
            font=("TkDefaultFont", 13, "bold"),
        ).pack(anchor="w", padx=16, pady=(14, 10))

        canvas_frame = tk.Frame(cards_panel, bg=self.PANEL)
        canvas_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.cards_canvas = tk.Canvas(
            canvas_frame,
            bg=self.PANEL,
            highlightthickness=0,
        )
        scrollbar = ttk.Scrollbar(
            canvas_frame, orient="vertical", command=self.cards_canvas.yview
        )
        self.cards_canvas.configure(yscrollcommand=scrollbar.set)

        self.cards_inner = tk.Frame(self.cards_canvas, bg=self.PANEL)
        self.cards_window = self.cards_canvas.create_window(
            (0, 0), window=self.cards_inner, anchor="nw"
        )

        self.cards_inner.bind(
            "<Configure>",
            lambda event: self.cards_canvas.configure(
                scrollregion=self.cards_canvas.bbox("all")
            ),
        )
        self.cards_canvas.bind(
            "<Configure>",
            lambda event: self.cards_canvas.itemconfigure(
                self.cards_window, width=event.width
            ),
        )

        self.cards_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Right: score/action panel
        side = tk.Frame(main, bg=self.BG, width=300)
        side.pack(side="right", fill="y", padx=(14, 0))
        side.pack_propagate(False)

        score_panel = tk.Frame(
            side,
            bg=self.PANEL,
            highlightbackground=self.BORDER,
            highlightthickness=1,
        )
        score_panel.pack(fill="x")

        tk.Label(
            score_panel,
            text="PUNTEGGIO",
            bg=self.PANEL,
            fg=self.TEXT,
            font=("TkDefaultFont", 13, "bold"),
        ).pack(anchor="w", padx=18, pady=(15, 12))

        self.upright_var = tk.StringVar(value="0")
        self.down_var = tk.StringVar(value="0")

        self._score_row(score_panel, "DRITTA", self.upright_var, self.GREEN)
        self._score_row(score_panel, "ROVESCIATA", self.down_var, self.RED)

        self.cheat_panel = tk.Frame(
            side,
            bg=self.PANEL,
            highlightbackground=self.BORDER,
            highlightthickness=1,
        )
        self.cheat_panel.pack(fill="x", pady=14)

        tk.Label(
            self.cheat_panel,
            text="CHEAT",
            bg=self.PANEL,
            fg=self.ACCENT,
            font=("TkDefaultFont", 13, "bold"),
        ).pack(anchor="w", padx=18, pady=(15, 4))

        tk.Label(
            self.cheat_panel,
            text="Seleziona una o più carte e ribaltale.",
            bg=self.PANEL,
            fg=self.MUTED,
            font=("TkDefaultFont", 9),
            wraplength=250,
            justify="left",
        ).pack(anchor="w", padx=18, pady=(0, 12))

        self.cheat_button = ttk.Button(
            self.cheat_panel,
            text="RIBALTA SELEZIONATE",
            command=self.cheat,
            state="disabled",
        )
        self.cheat_button.pack(fill="x", padx=18, pady=(0, 16))

        self.resolve_button = ttk.Button(
            side,
            text="RISOLVI PESCATA",
            command=self.resolve,
            state="disabled",
        )
        self.resolve_button.pack(fill="x")

    def _score_row(self, parent, label, variable, text_color):
        row = tk.Frame(parent, bg=self.PANEL)
        row.pack(fill="x", padx=18, pady=(0, 14))

        tk.Label(
            row,
            text=label,
            bg=self.PANEL,
            fg=text_color,
            font=("TkDefaultFont", 9, "bold"),
        ).pack(side="left")

        tk.Label(
            row,
            textvariable=variable,
            bg=self.PANEL,
            fg=self.TEXT,
            font=("TkDefaultFont", 25, "bold"),
        ).pack(side="right")

    def _update_deck_label(self):
        self.deck_label.config(text=f"DECK  {len(self.deck)} / 78")

    def _clear_cards(self):
        for child in self.cards_inner.winfo_children():
            child.destroy()
        self.card_vars.clear()

    def start_pescata(self):
        try:
            n = int(self.number_var.get())
        except (TypeError, ValueError):
            messagebox.showerror("Errore", "Inserisci un numero valido.")
            return

        if n < 1:
            messagebox.showerror("Errore", "Il numero di carte deve essere almeno 1.")
            return

        self._clear_cards()

        self.current_pescata = Pescata(
            deck=self.deck,
            chosen_seme=self.suit_var.get(),
            number_of_cards=n,
        )
        self.current_pescata.draw()
        self.current_pescata.reveal()
        self.current_pescata.calculate_totals()

        self._render_cards()
        self._update_totals()
        self._update_deck_label()

        self.status_label.config(
            text=(
                "Il deck è finito. La lettura continua normalmente con le carte rimaste."
                if self.current_pescata.deck_finished
                else "Le carte sono sul tavolo. Vuoi barare? Seleziona le carte da ribaltare."
            ),
            fg=self.ACCENT if self.current_pescata.deck_finished else self.MUTED,
        )

        self.cheat_button.config(state="normal")
        self.resolve_button.config(state="normal")
        self.draw_button.config(state="disabled")

    def _render_cards(self):
        for index, card in enumerate(self.current_pescata.drawn_cards):
            var = tk.BooleanVar(value=False)
            self.card_vars.append(var)

            card_frame = tk.Frame(
                self.cards_inner,
                bg=self.PANEL_2,
                highlightbackground=self.BORDER,
                highlightthickness=1,
            )
            card_frame.pack(fill="x", padx=6, pady=5)

            # Visual card number
            number_box = tk.Frame(card_frame, bg=self.ACCENT, width=42, height=58)
            number_box.pack(side="left", padx=10, pady=10)
            number_box.pack_propagate(False)

            tk.Label(
                number_box,
                text=str(index + 1),
                bg=self.ACCENT,
                fg=self.BG,
                font=("TkDefaultFont", 14, "bold"),
            ).pack(expand=True)

            content = tk.Frame(card_frame, bg=self.PANEL_2)
            content.pack(side="left", fill="both", expand=True, pady=10)

            value = card.calculate_value(self.current_pescata.chosen_seme)
            doubled = (
                card.arcana == "minor"
                and card.seme == self.current_pescata.chosen_seme
            )

            tk.Label(
                content,
                text=card.name,
                bg=self.PANEL_2,
                fg=self.TEXT,
                font=("TkDefaultFont", 11, "bold"),
                anchor="w",
            ).pack(fill="x")

            details = f"{card.orientation}   •   {value} punti"
            if doubled:
                details += "   •   SEME ×2"

            tk.Label(
                content,
                text=details,
                bg=self.PANEL_2,
                fg=self.ACCENT if doubled else self.MUTED,
                font=("TkDefaultFont", 9),
                anchor="w",
            ).pack(fill="x", pady=(4, 0))

            tk.Checkbutton(
                card_frame,
                variable=var,
                text="CHEAT",
                bg=self.PANEL_2,
                fg=self.TEXT,
                activebackground=self.PANEL_2,
                activeforeground=self.TEXT,
                selectcolor=self.PANEL,
                font=("TkDefaultFont", 8, "bold"),
                relief="flat",
            ).pack(side="right", padx=14)

    def _update_totals(self):
        p = self.current_pescata
        self.upright_var.set(str(p.upright_total))
        self.down_var.set(str(p.upside_down_total))

    def cheat(self):
        selected = [
            card
            for card, var in zip(self.current_pescata.drawn_cards, self.card_vars)
            if var.get()
        ]

        if not selected:
            self.status_label.config(
                text="Seleziona almeno una carta prima di usare il cheat.",
                fg=self.RED,
            )
            return

        self.current_pescata.cheat(selected)
        self._update_totals()
        self._refresh_cards()

        for var in self.card_vars:
            var.set(False)

        self.status_label.config(
            text=f"Hai ribaltato {len(selected)} carta/e. Il valore non è cambiato.",
            fg=self.ACCENT,
        )

    def _refresh_cards(self):
        # Rebuild card display after orientation changes.
        self._render_cards_without_destroying_selection()

    def _render_cards_without_destroying_selection(self):
        for child in self.cards_inner.winfo_children():
            child.destroy()

        old_vars = self.card_vars
        self.card_vars = []

        for index, card in enumerate(self.current_pescata.drawn_cards):
            var = tk.BooleanVar(value=False)
            self.card_vars.append(var)

            card_frame = tk.Frame(
                self.cards_inner,
                bg=self.PANEL_2,
                highlightbackground=self.BORDER,
                highlightthickness=1,
            )
            card_frame.pack(fill="x", padx=6, pady=5)

            number_box = tk.Frame(card_frame, bg=self.ACCENT, width=42, height=58)
            number_box.pack(side="left", padx=10, pady=10)
            number_box.pack_propagate(False)

            tk.Label(
                number_box,
                text=str(index + 1),
                bg=self.ACCENT,
                fg=self.BG,
                font=("TkDefaultFont", 14, "bold"),
            ).pack(expand=True)

            content = tk.Frame(card_frame, bg=self.PANEL_2)
            content.pack(side="left", fill="both", expand=True, pady=10)

            value = card.calculate_value(self.current_pescata.chosen_seme)
            doubled = card.arcana == "minor" and card.seme == self.current_pescata.chosen_seme

            tk.Label(
                content,
                text=card.name,
                bg=self.PANEL_2,
                fg=self.TEXT,
                font=("TkDefaultFont", 11, "bold"),
                anchor="w",
            ).pack(fill="x")

            details = f"{card.orientation}   •   {value} punti"
            if doubled:
                details += "   •   SEME ×2"

            tk.Label(
                content,
                text=details,
                bg=self.PANEL_2,
                fg=self.ACCENT if doubled else self.MUTED,
                font=("TkDefaultFont", 9),
                anchor="w",
            ).pack(fill="x", pady=(4, 0))

            tk.Checkbutton(
                card_frame,
                variable=var,
                text="CHEAT",
                bg=self.PANEL_2,
                fg=self.TEXT,
                activebackground=self.PANEL_2,
                activeforeground=self.TEXT,
                selectcolor=self.PANEL,
                font=("TkDefaultFont", 8, "bold"),
                relief="flat",
            ).pack(side="right", padx=14)

    def resolve(self):
        result = self.current_pescata.resolve()
        self._update_totals()
        self._update_deck_label()

        if result["winner"] == "Pareggio":
            title = "PAREGGIO"
            text = (
                "Nessun totale è maggiore.\n\n"
                "Tutte le carte tornano al centro del deck."
            )
        else:
            title = f"VINCE {result['winner'].upper()}"
            text = (
                f"Totale vincente: {max(result['upright_total'], result['upside_down_total'])} punti\n\n"
                f"Carte restituite al centro:\n"
                f"{', '.join(c.name for c in result['losing_cards']) or 'Nessuna'}\n\n"
                f"Carte scartate:\n"
                f"{', '.join(c.name for c in result['winning_cards']) or 'Nessuna'}"
            )

        messagebox.showinfo(title, text)

        if result.get("deck_rebuilt"):
            status_text = "Il deck è finito. È stato ricostruito e rimescolato con tutte le 78 carte."
            status_fg = self.ACCENT
        else:
            status_text = "Pescata risolta. Puoi iniziarne una nuova."
            status_fg = self.MUTED

        self.status_label.config(
            text=status_text,
            fg=status_fg,
        )
        self.cheat_button.config(state="disabled")
        self.resolve_button.config(state="disabled")
        self.draw_button.config(state="normal")

    def reset_game(self):
        self.deck = Deck()
        self.current_pescata = None
        self._clear_cards()
        self.upright_var.set("0")
        self.down_var.set("0")
        self.status_label.config(
            text="Nuova partita. Il deck contiene 78 carte.",
            fg=self.MUTED,
        )
        self.cheat_button.config(state="disabled")
        self.resolve_button.config(state="disabled")
        self.draw_button.config(state="normal")
        self._update_deck_label()


if __name__ == "__main__":
    App().mainloop()
