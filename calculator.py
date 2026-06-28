import tkinter as tk
from tkinter import font


class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Modern Calculator")
        self.root.geometry("450x650")
        self.root.resizable(False, False)
        
        # Configure colors
        self.bg_color = "#020617"
        self.card_bg = "#0f172a"
        self.button_bg = "rgba(148, 163, 184, 0.08)"
        self.text_color = "#e2e8f0"
        self.secondary_text = "#94a3b8"
        self.operator_bg = "#3b82f6"
        self.equals_bg = "#10b981"
        
        self.root.configure(bg=self.bg_color)
        
        # State
        self.state = {
            'value': '0',
            'operator': None,
            'previousValue': None,
            'waitingForOperand': False,
            'lastAction': None,
        }
        
        self.setup_ui()
    
    def setup_ui(self):
        """Create the calculator UI"""
        # Main container
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Calculator card
        card_frame = tk.Frame(main_frame, bg=self.card_bg, highlightthickness=1, 
                            highlightbackground="#94a3b8", highlightcolor="#94a3b8")
        card_frame.pack(fill=tk.BOTH, expand=True)
        card_frame.configure(relief=tk.FLAT)
        
        # Header
        header_frame = tk.Frame(card_frame, bg=self.card_bg)
        header_frame.pack(fill=tk.X, padx=20, pady=15)
        
        title_font = font.Font(family="Helvetica", size=14, weight="bold")
        subtitle_font = font.Font(family="Helvetica", size=10)
        
        title_label = tk.Label(header_frame, text="Modern Calculator", 
                             font=title_font, bg=self.card_bg, fg=self.text_color)
        title_label.pack(anchor="w")
        
        subtitle_label = tk.Label(header_frame, text="Clean, responsive, fast", 
                                font=subtitle_font, bg=self.card_bg, fg=self.secondary_text)
        subtitle_label.pack(anchor="w")
        
        # Screen
        screen_frame = tk.Frame(card_frame, bg=self.card_bg)
        screen_frame.pack(fill=tk.X, padx=20, pady=(10, 15))
        
        # History display
        self.history_var = tk.StringVar()
        history_label = tk.Label(screen_frame, textvariable=self.history_var,
                                font=("Helvetica", 12), bg=self.card_bg, 
                                fg=self.secondary_text, justify=tk.RIGHT, wraplength=350)
        history_label.pack(fill=tk.X, pady=(5, 0))
        
        # Value display
        self.display_var = tk.StringVar(value="0")
        display_font = font.Font(family="Helvetica", size=36, weight="bold")
        display_label = tk.Label(screen_frame, textvariable=self.display_var,
                                font=display_font, bg=self.card_bg,
                                fg=self.text_color, justify=tk.RIGHT)
        display_label.pack(fill=tk.BOTH, expand=True, pady=(0, 5))
        
        # Button grid
        button_frame = tk.Frame(card_frame, bg=self.card_bg)
        button_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Configure grid weights
        for i in range(4):
            button_frame.grid_columnconfigure(i, weight=1)
        for i in range(6):
            button_frame.grid_rowconfigure(i, weight=1)
        
        # Button layout
        buttons_layout = [
            [("AC", "clear", "control"), ("±", "toggle-sign", "control"), 
             ("%", "percent", "control"), ("÷", "divide", "operator")],
            [("7", "7", "digit"), ("8", "8", "digit"), 
             ("9", "9", "digit"), ("×", "multiply", "operator")],
            [("4", "4", "digit"), ("5", "5", "digit"), 
             ("6", "6", "digit"), ("−", "subtract", "operator")],
            [("1", "1", "digit"), ("2", "2", "digit"), 
             ("3", "3", "digit"), ("+", "add", "operator")],
            [("0", "0", "digit"), (".", "decimal", "digit"), 
             ("=", "equals", "equals")],
        ]
        
        for row_idx, row in enumerate(buttons_layout):
            for col_idx, (text, action, btn_type) in enumerate(row):
                if text == "0" and col_idx == 0:
                    # Zero button spans 2 columns
                    btn = self.create_button(button_frame, text, action, btn_type)
                    btn.grid(row=row_idx, column=col_idx, columnspan=2, 
                           sticky="nsew", padx=5, pady=5)
                elif text == "=" and col_idx == 2:
                    # Equals button spans 2 columns
                    btn = self.create_button(button_frame, text, action, btn_type)
                    btn.grid(row=row_idx, column=col_idx, columnspan=2, 
                           sticky="nsew", padx=5, pady=5)
                else:
                    btn = self.create_button(button_frame, text, action, btn_type)
                    btn.grid(row=row_idx, column=col_idx, sticky="nsew", padx=5, pady=5)
    
    def create_button(self, parent, text, action, btn_type):
        """Create a button with appropriate styling"""
        button_font = font.Font(family="Helvetica", size=14, weight="bold")
        
        if btn_type == "operator":
            bg = self.operator_bg
            fg = self.text_color
        elif btn_type == "equals":
            bg = self.equals_bg
            fg = self.text_color
        elif btn_type == "control":
            bg = "#475569"
            fg = self.text_color
        else:  # digit
            bg = "#334155"
            fg = self.text_color
        
        btn = tk.Button(parent, text=text, font=button_font, 
                       bg=bg, fg=fg, border=0, cursor="hand2",
                       command=lambda: self.handle_button_click(action))
        
        # Hover effect
        btn.bind("<Enter>", lambda e: btn.config(bg=self.lighten_color(bg)))
        btn.bind("<Leave>", lambda e: btn.config(bg=bg))
        
        return btn
    
    def lighten_color(self, hex_color):
        """Lighten a hex color for hover effect"""
        # Simple lightening by replacing with a slightly lighter shade
        lightness_map = {
            "#475569": "#5a6b7d",
            "#334155": "#4a5568",
            "#3b82f6": "#60a5fa",
            "#10b981": "#34d399",
        }
        return lightness_map.get(hex_color, hex_color)
    
    def handle_button_click(self, action):
        """Handle button click events"""
        if action.isdigit():
            self.input_digit(action)
        elif action == "decimal":
            self.input_decimal()
        elif action == "clear":
            self.clear_all()
        elif action == "toggle-sign":
            self.toggle_sign()
        elif action == "percent":
            self.apply_percent()
        elif action == "equals":
            self.handle_equals()
        elif action in ["add", "subtract", "multiply", "divide"]:
            self.handle_operator(action)
        
        self.update_display()
    
    def input_digit(self, digit):
        """Input a digit"""
        if self.state['waitingForOperand']:
            self.state['value'] = digit
            self.state['waitingForOperand'] = False
        else:
            self.state['value'] = digit if self.state['value'] == '0' else self.state['value'] + digit
    
    def input_decimal(self):
        """Input a decimal point"""
        if self.state['waitingForOperand']:
            self.state['value'] = '0.'
            self.state['waitingForOperand'] = False
            return
        if '.' not in self.state['value']:
            self.state['value'] += '.'
    
    def handle_operator(self, next_operator):
        """Handle operator button click"""
        value = float(self.state['value'])
        
        if self.state['operator'] and self.state['waitingForOperand']:
            self.state['operator'] = next_operator
            return
        
        if self.state['previousValue'] is None:
            self.state['previousValue'] = value
        elif self.state['operator']:
            result = self.calculate(self.state['previousValue'], value, self.state['operator'])
            self.state['previousValue'] = result
            self.state['value'] = str(result)
        
        self.state['waitingForOperand'] = True
        self.state['operator'] = next_operator
    
    def calculate(self, left, right, operator):
        """Perform calculation"""
        if operator == 'add':
            return left + right
        elif operator == 'subtract':
            return left - right
        elif operator == 'multiply':
            return left * right
        elif operator == 'divide':
            return 'Error' if right == 0 else left / right
        return right
    
    def clear_all(self):
        """Clear all values"""
        self.state['value'] = '0'
        self.state['operator'] = None
        self.state['previousValue'] = None
        self.state['waitingForOperand'] = False
        self.state['lastAction'] = None
    
    def toggle_sign(self):
        """Toggle sign of current value"""
        if self.state['value'] == '0':
            return
        self.state['value'] = self.state['value'][1:] if self.state['value'].startswith('-') else f"-{self.state['value']}"
    
    def apply_percent(self):
        """Apply percentage"""
        value = float(self.state['value'])
        self.state['value'] = str(value / 100)
    
    def handle_equals(self):
        """Handle equals button"""
        value = float(self.state['value'])
        
        if self.state['operator'] is None or self.state['previousValue'] is None:
            return
        
        result = self.calculate(self.state['previousValue'], value, self.state['operator'])
        self.state['value'] = str(result)
        self.state['previousValue'] = None
        self.state['operator'] = None
        self.state['waitingForOperand'] = True
    
    def update_display(self):
        """Update the display"""
        # Format the display value
        try:
            display_value = float(self.state['value'])
            # Remove unnecessary decimals
            if display_value == int(display_value):
                self.display_var.set(str(int(display_value)))
            else:
                self.display_var.set(str(display_value))
        except ValueError:
            self.display_var.set(self.state['value'])
        
        # Update history
        if self.state['operator']:
            operator_symbols = {
                'add': '+',
                'subtract': '−',
                'multiply': '×',
                'divide': '÷'
            }
            operator_text = operator_symbols.get(self.state['operator'], '')
            prev_val = str(int(self.state['previousValue'])) if isinstance(self.state['previousValue'], float) and self.state['previousValue'] == int(self.state['previousValue']) else str(self.state['previousValue'])
            self.history_var.set(f"{prev_val} {operator_text}")
        else:
            self.history_var.set("")


if __name__ == "__main__":
    root = tk.Tk()
    calculator = Calculator(root)
    root.mainloop()
