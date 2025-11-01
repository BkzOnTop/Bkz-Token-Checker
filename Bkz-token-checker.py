import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import requests
import json
from PIL import Image, ImageTk
import os
import sys

# Configuration du style 3D professionnel
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class Professional3DTokenChecker:
    def __init__(self, root):
        self.root = root
        self.root.title("Check ur token with bkz checker")
        self.root.geometry("1200x800")
        self.root.configure(fg_color="#0f1a2b")
        
        # Variables pour les statistiques
        self.valid_count = 0
        self.locked_count = 0
        self.invalid_count = 0
        self.total_count = 0
        
        # Icônes personnalisées (à remplacer par vos propres images)
        self.icons = self.load_icons()
        
        self.setup_ui()
        
    def load_icons(self):
        # Création d'icônes basiques - Remplacez par vos propres images
        icons = {}
        try:
            # Icône valide (vert)
            valid_img = Image.new('RGB', (20, 20), color=(46, 204, 113))
            icons['valid'] = ImageTk.PhotoImage(valid_img)
            
            # Icône locké (orange)
            locked_img = Image.new('RGB', (20, 20), color=(243, 156, 18))
            icons['locked'] = ImageTk.PhotoImage(locked_img)
            
            # Icône invalide (rouge)
            invalid_img = Image.new('RGB', (20, 20), color=(231, 76, 60))
            icons['invalid'] = ImageTk.PhotoImage(invalid_img)
            
            # Icône chargement
            load_img = Image.new('RGB', (20, 20), color=(52, 152, 219))
            icons['load'] = ImageTk.PhotoImage(load_img)
            
        except Exception as e:
            print(f"Erreur chargement icônes: {e}")
            
        return icons
    
    def setup_ui(self):
        # Frame principal avec effet 3D
        self.main_frame = ctk.CTkFrame(
            self.root,
            fg_color="#1e2a3b",
            border_width=2,
            border_color="#34495e",
            corner_radius=15
        )
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header avec effet 3D prononcé
        self.setup_header()
        
        # Contenu principal
        self.setup_content()
        
        # Footer
        self.setup_footer()
    
    def setup_header(self):
        header_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="#2c3e50",
            border_width=3,
            border_color="#1abc9c",
            corner_radius=12,
            height=80
        )
        header_frame.pack(fill="x", padx=15, pady=15)
        header_frame.pack_propagate(False)
        
        # Titre avec effet 3D
        title_label = ctk.CTkLabel(
            header_frame,
            text="BKZ TOKEN CHECKER",
            font=("Arial", 24, "bold"),
            text_color="#1abc9c",
            fg_color="transparent"
        )
        title_label.pack(pady=20)
        
        # Sous-titre avec effet néon
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text=".",
            font=("Arial", 12, "italic"),
            text_color="#3498db",
            fg_color="transparent"
        )
        subtitle_label.pack(pady=5)
    
    def setup_content(self):
        content_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="transparent"
        )
        content_frame.pack(fill="both", expand=True, padx=15, pady=10)
        
        # Panneau gauche - Configuration
        self.setup_left_panel(content_frame)
        
        # Panneau droit - Résultats
        self.setup_right_panel(content_frame)
    
    def setup_left_panel(self, parent):
        left_panel = ctk.CTkFrame(
            parent,
            fg_color="#2c3e50",
            border_width=2,
            border_color="#34495e",
            corner_radius=12
        )
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Titre du panneau
        panel_title = ctk.CTkLabel(
            left_panel,
            text="TOKEN INPUT",
            font=("Arial", 16, "bold"),
            text_color="#ecf0f1"
        )
        panel_title.pack(pady=15)
        
        # Zone de texte avec style 3D
        text_frame = ctk.CTkFrame(
            left_panel,
            fg_color="#1e272e",
            border_width=2,
            border_color="#3f6a9c",
            corner_radius=8
        )
        text_frame.pack(fill="both", expand=True, padx=15, pady=10)
        
        self.token_text = ctk.CTkTextbox(
            text_frame,
            fg_color="#0f1a2b",
            text_color="#00cec9",
            border_width=2,
            border_color="#1abc9c",
            font=("Consolas", 11),
            corner_radius=6
        )
        self.token_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Boutons d'action avec effet 3D
        self.setup_buttons(left_panel)
        
        # Barre de progression
        self.setup_progress(left_panel)
        
        # Statistiques
        self.setup_stats(left_panel)
    
    def setup_buttons(self, parent):
        button_frame = ctk.CTkFrame(
            parent,
            fg_color="transparent"
        )
        button_frame.pack(fill="x", padx=15, pady=10)
        
        # Bouton Charger avec effet 3D
        self.load_btn = ctk.CTkButton(
            button_frame,
            text="LOAD TOKENS",
            command=self.load_tokens_from_file,
            font=("Arial", 12, "bold"),
            fg_color="#3498db",
            hover_color="#2980b9",
            border_width=2,
            border_color="#1abc9c",
            corner_radius=8,
            height=40
        )
        self.load_btn.pack(side="left", padx=(0, 10), fill="x", expand=True)
        
        # Bouton Vérifier avec effet 3D
        self.check_btn = ctk.CTkButton(
            button_frame,
            text="CHECK TOKENS",
            command=self.check_tokens_thread,
            font=("Arial", 12, "bold"),
            fg_color="#27ae60",
            hover_color="#219a52",
            border_width=2,
            border_color="#1abc9c",
            corner_radius=8,
            height=40
        )
        self.check_btn.pack(side="right", fill="x", expand=True)
    
    def setup_progress(self, parent):
        progress_frame = ctk.CTkFrame(
            parent,
            fg_color="transparent"
        )
        progress_frame.pack(fill="x", padx=15, pady=10)
        
        progress_label = ctk.CTkLabel(
            progress_frame,
            text="PROGRESSION:",
            font=("Arial", 11, "bold"),
            text_color="#bdc3c7"
        )
        progress_label.pack(anchor="w")
        
        self.progress_bar = ctk.CTkProgressBar(
            progress_frame,
            fg_color="#34495e",
            progress_color="#1abc9c",
            height=20,
            corner_radius=10
        )
        self.progress_bar.pack(fill="x", pady=5)
        self.progress_bar.set(0)
        
        self.progress_label = ctk.CTkLabel(
            progress_frame,
            text="0%",
            font=("Arial", 10, "bold"),
            text_color="#ecf0f1"
        )
        self.progress_label.pack(anchor="e")
    
    def setup_stats(self, parent):
        stats_frame = ctk.CTkFrame(
            parent,
            fg_color="#34495e",
            border_width=2,
            border_color="#2c3e50",
            corner_radius=10
        )
        stats_frame.pack(fill="x", padx=15, pady=15)
        
        self.stats_text = ctk.CTkLabel(
            stats_frame,
            text="Total: 0 | Valid: 0 | Locked: 0 | Invalid: 0",
            font=("Arial", 12, "bold"),
            text_color="#f1c40f"
        )
        self.stats_text.pack(pady=10)
    
    def setup_right_panel(self, parent):
        right_panel = ctk.CTkFrame(
            parent,
            fg_color="#2c3e50",
            border_width=2,
            border_color="#34495e",
            corner_radius=12
        )
        right_panel.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        # Titre du panneau résultats
        results_title = ctk.CTkLabel(
            right_panel,
            text="VALIDATION RESULTS",
            font=("Arial", 16, "bold"),
            text_color="#ecf0f1"
        )
        results_title.pack(pady=15)
        
        # Frame pour les résultats avec scroll
        results_container = ctk.CTkFrame(
            right_panel,
            fg_color="transparent"
        )
        results_container.pack(fill="both", expand=True, padx=15, pady=10)
        
        # Création d'un Treeview customisé
        self.setup_results_tree(results_container)
    
    def setup_results_tree(self, parent):
        # Style personnalisé pour le Treeview
        style = ttk.Style()
        style.theme_use('default')
        
        # Configuration du style 3D
        style.configure("3D.Treeview",
            background="#1e272e",
            foreground="#00cec9",
            fieldbackground="#1e272e",
            borderwidth=2,
            relief="groove",
            font=('Arial', 10)
        )
        
        style.configure("3D.Treeview.Heading",
            background="#34495e",
            foreground="#f1c40f",
            relief="raised",
            borderwidth=2,
            font=('Arial', 11, 'bold')
        )
        
        # Création du Treeview
        columns = ("status", "token", "username", "servers", "details")
        self.result_tree = ttk.Treeview(
            parent,
            columns=columns,
            show="headings",
            style="3D.Treeview",
            height=20
        )
        
        # Configuration des colonnes
        self.result_tree.heading("status", text="STATUS")
        self.result_tree.heading("token", text="TOKEN")
        self.result_tree.heading("username", text="USERNAME")
        self.result_tree.heading("servers", text="SERVERS")
        self.result_tree.heading("details", text="DETAILS")
        
        self.result_tree.column("status", width=100, anchor="center")
        self.result_tree.column("token", width=150)
        self.result_tree.column("username", width=120)
        self.result_tree.column("servers", width=80, anchor="center")
        self.result_tree.column("details", width=200)
        
        # Scrollbar
        scrollbar = ctk.CTkScrollbar(parent, command=self.result_tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.result_tree.configure(yscrollcommand=scrollbar.set)
        
        self.result_tree.pack(fill="both", expand=True)
        
        # Menu contextuel
        self.setup_context_menu()
    
    def setup_context_menu(self):
        self.context_menu = tk.Menu(self.root, tearoff=0, bg="#34495e", fg="white", font=("Arial", 10))
        self.context_menu.add_command(label="Copy Token", command=self.copy_token)
        self.context_menu.add_command(label="Copy Username", command=self.copy_username)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="View Details", command=self.view_details)
        
        self.result_tree.bind("<Button-3>", self.show_context_menu)
    
    def setup_footer(self):
        footer_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="#2c3e50",
            border_width=2,
            border_color="#34495e",
            corner_radius=10,
            height=50
        )
        footer_frame.pack(fill="x", padx=15, pady=15)
        footer_frame.pack_propagate(False)
        
        footer_text = ctk.CTkLabel(
            footer_frame,
            text="Developed by Bkz.py | Professional Token Analysis Tool",
            font=("Arial", 10, "italic"),
            text_color="#7f8c8d"
        )
        footer_text.pack(pady=15)
    
    def load_tokens_from_file(self):
        file_path = filedialog.askopenfilename(
            title="Select Token File",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    tokens = file.read()
                    self.token_text.delete("1.0", "end")
                    self.token_text.insert("1.0", tokens)
                messagebox.showinfo("Success", "File loaded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Load error: {str(e)}")
    
    def check_tokens_thread(self):
        if not self.token_text.get("1.0", "end-1c").strip():
            messagebox.showwarning("Warning", "No tokens to check!")
            return
            
        threading.Thread(target=self.check_tokens, daemon=True).start()
    
    def check_tokens(self):
        self.check_btn.configure(state="disabled", fg_color="#95a5a6")
        
        raw_text = self.token_text.get("1.0", "end-1c")
        tokens = [token.strip() for token in raw_text.splitlines() if token.strip()]
        
        # Réinitialisation
        self.valid_count = 0
        self.locked_count = 0
        self.invalid_count = 0
        self.total_count = len(tokens)
        
        # Clear previous results
        for item in self.result_tree.get_children():
            self.result_tree.delete(item)
        
        self.progress_bar.set(0)
        
        valid_tokens = []
        
        for i, token in enumerate(tokens):
            try:
                status, username, servers, details = self.verify_token(token)
                
                # Ajout au Treeview
                self.result_tree.insert("", "end", values=(status, f"{token[:25]}...", username, servers, details))
                
                # Mise à jour des compteurs
                if "VALID" in status:
                    self.valid_count += 1
                    valid_tokens.append(token)
                elif "LOCK" in status:
                    self.locked_count += 1
                else:
                    self.invalid_count += 1
                
                # Mise à jour de la progression
                progress = (i + 1) / len(tokens)
                self.progress_bar.set(progress)
                self.progress_label.configure(text=f"{progress*100:.1f}%")
                self.update_stats()
                
            except Exception as e:
                print(f"Error processing token: {e}")
        
        # Sauvegarde des tokens valides
        if valid_tokens:
            try:
                with open("valid_tokens_pro.txt", "w", encoding="utf-8") as f:
                    f.write("\n".join(valid_tokens))
            except Exception as e:
                print(f"Save error: {e}")
        
        self.check_btn.configure(state="normal", fg_color="#27ae60")
        messagebox.showinfo("Complete", f"Token validation completed!\nValid: {self.valid_count} | Locked: {self.locked_count} | Invalid: {self.invalid_count}")
    
    def verify_token(self, token):
        headers = {"Authorization": token}
        try:
            response = requests.get("https://discord.com/api/v10/users/@me", headers=headers, timeout=10)
            
            if response.status_code == 200:
                user_data = response.json()
                username = f"{user_data.get('username', 'N/A')}#{user_data.get('discriminator', '0000')}"
                
                # Récupération des serveurs admin
                admin_servers = self.get_admin_servers(token)
                servers_count = len(admin_servers)
                
                details = f"Admin on {servers_count} servers" if servers_count > 0 else "User account"
                
                return "✅ VALID", username, str(servers_count), details
                
            elif response.status_code == 403:
                return "🔒 LOCKED", "N/A", "0", "Account locked or no access"
            else:
                return "❌ INVALID", "N/A", "0", f"HTTP {response.status_code}"
                
        except Exception as e:
            return "❌ ERROR", "N/A", "0", str(e)
    
    def get_admin_servers(self, token):
        headers = {"Authorization": token}
        try:
            response = requests.get("https://discord.com/api/v10/users/@me/guilds", headers=headers, timeout=10)
            if response.status_code == 200:
                servers = response.json()
                admin_servers = []
                for server in servers:
                    if server.get("permissions") and (int(server["permissions"]) & 0x8):
                        admin_servers.append(server["name"])
                return admin_servers
        except:
            pass
        return []
    
    def update_stats(self):
        stats_text = f"Total: {self.total_count} | Valid: {self.valid_count} | Locked: {self.locked_count} | Invalid: {self.invalid_count}"
        self.stats_text.configure(text=stats_text)
    
    def show_context_menu(self, event):
        item = self.result_tree.identify_row(event.y)
        if item:
            self.result_tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)
    
    def copy_token(self):
        selected = self.result_tree.selection()
        if selected:
            item = self.result_tree.item(selected[0])
            # Implémentez la logique de copie du token complet
            self.root.clipboard_clear()
            self.root.clipboard_append("Token copied")
    
    def copy_username(self):
        selected = self.result_tree.selection()
        if selected:
            item = self.result_tree.item(selected[0])
            username = item['values'][2]
            self.root.clipboard_clear()
            self.root.clipboard_append(username)
    
    def view_details(self):
        selected = self.result_tree.selection()
        if selected:
            item = self.result_tree.item(selected[0])
            details = f"Status: {item['values'][0]}\nUser: {item['values'][2]}\nServers: {item['values'][3]}\nDetails: {item['values'][4]}"
            messagebox.showinfo("Token Details", details)

if __name__ == "__main__":
    # Configuration pour un rendu HD
    ctk.deactivate_automatic_dpi_awareness()
    
    root = ctk.CTk()
    app = Professional3DTokenChecker(root)
    root.mainloop()