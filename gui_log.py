import os
import re
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime, timedelta

README_PATH = "README.md"
SOLUTIONS_DIR = "solutions"

LANG_EXT_MAP = {
    "python": ".py",
    "c++": ".cpp",
    "java": ".java",
    "javascript": ".js",
    "typescript": ".ts",
    "go": ".go",
    "rust": ".rs",
    "sql": ".sql",
    "other": ".txt"
}

def get_current_date():
    return datetime.now().strftime("%Y-%m-%d")

def get_current_time():
    return datetime.now().strftime("%I:%M %p")

# Ensure solutions directory exists
if not os.path.exists(SOLUTIONS_DIR):
    os.makedirs(SOLUTIONS_DIR)

class PlacementPrepGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Placement Prep Log Assistant")
        self.root.geometry("900x650")
        self.root.minsize(800, 550)
        
        # Configure fonts & styles
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Colors
        self.bg_color = "#f5f6fa"
        self.primary_color = "#2f3640"
        self.accent_color = "#00a8ff"
        self.success_color = "#4cd137"
        
        self.root.configure(bg=self.bg_color)
        
        self.style.configure(".", font=("Segoe UI", 10), background=self.bg_color)
        self.style.configure("TLabel", foreground=self.primary_color)
        self.style.configure("Header.TLabel", font=("Segoe UI", 13, "bold"), foreground=self.primary_color)
        self.style.configure("Title.TLabel", font=("Segoe UI", 18, "bold"), foreground=self.primary_color)
        
        self.style.configure("TFrame", background=self.bg_color)
        self.style.configure("Sidebar.TFrame", background="#2f3640")
        self.style.configure("Sidebar.TLabel", background="#2f3640", foreground="white")
        
        # Main Layout: Sidebar (Dashboard) and Right Pane (Forms)
        self.main_container = ttk.Frame(self.root)
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Left Sidebar (Stats Dashboard)
        self.sidebar = tk.Frame(self.main_container, bg="#2f3640", width=250)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)
        
        # Right Notebook (Tabs for logging)
        self.notebook = ttk.Notebook(self.main_container)
        self.notebook.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Study session tracking state
        self.session_active = False
        self.session_start_dt = None
        self.session_questions_solved = []

        # Check if environment is already initialized
        if not os.path.exists(README_PATH):
            self.show_welcome_init_screen()
        else:
            self.load_main_dashboard()

    def show_welcome_init_screen(self):
        self.init_container = ttk.Frame(self.root, padding=30)
        self.init_container.pack(fill=tk.BOTH, expand=True)
        
        lbl_welcome = ttk.Label(self.init_container, text="👋 Welcome to Placement Prep Tracker!", font=("Segoe UI", 18, "bold"))
        lbl_welcome.pack(pady=(40, 15))
        
        desc = (
            "This application helps you track your coding problems, tech concept notes,\n"
            "and daily study logs directly inside a structured Markdown file (README.md).\n\n"
            "We detected that this folder is not initialized yet.\n"
            "Click the button below to automatically set up the prep environment:\n"
            "  1. A structured index file (README.md)\n"
            "  2. A solutions/ directory to store code files\n"
            "  3. A Git configuration helper (.gitignore)"
        )
        lbl_desc = ttk.Label(self.init_container, text=desc, font=("Segoe UI", 10), justify=tk.LEFT)
        lbl_desc.pack(pady=20)
        
        btn_init = tk.Button(self.init_container, text="🚀 Initialize Prep Environment", font=("Segoe UI", 11, "bold"),
                             bg="#4cd137", fg="white", activebackground="#44bd32", activeforeground="white",
                             bd=0, padx=25, pady=10, command=self.perform_initialization)
        btn_init.pack(pady=30)

    def perform_initialization(self):
        # 1. Create solutions/ dir
        if not os.path.exists(SOLUTIONS_DIR):
            os.makedirs(SOLUTIONS_DIR)
            
        # 2. Write fresh .gitignore
        if not os.path.exists(".gitignore"):
            with open(".gitignore", "w", encoding="utf-8") as f:
                f.write("__pycache__/\n*.pyc\nbuild/\ndist/\n*.spec\ngui_log.exe\n")
                
        # 3. Write fresh README.md
        fresh_readme_content = """# 🚀 Placement Prep Tracker

A centralized hub to track DSA coding problems, core CS concepts/technologies learned, and a detailed date-wise & time-wise study journal.

---

## 📊 Quick Dashboard

| Metric | Status / Value | Details |
| :--- | :--- | :--- |
| **Current Focus** | 🎯 Arrays & Dynamic Programming / DBMS | Core DSA + Core CS Subjects |
| **Questions Solved** | **0** | 🟢 Easy: `0` \\| 🟡 Medium: `0` \\| 🔴 Hard: `0` |
| **Days Active** | 📅 `0` Days | Current Streak: `0` Days |
| **Last Updated** | 🕒 *Never* | Automatically logged |

---

## 📚 Solved Questions Log

<!-- QUESTIONS_START -->
| Date | Platform | Problem Name & Link | Topic / Pattern | Language | Difficulty | Key Concept / Time Complexity | Code Solution |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
<!-- QUESTIONS_END -->

---

## 💻 Tech Learning Tracker

<!-- TECH_START -->
| Date | Technology / Domain | Topic / Concept Learned | Resources | Confidence | Key Takeaways |
| :--- | :--- | :--- | :--- | :--- | :--- |
<!-- TECH_END -->

---

## 🗓️ Time-Wise Study Journal

<!-- JOURNAL_START -->
| Date | Time Slot | Category | Activity Description | Focus / Key Takeaway | Next Steps |
| :--- | :--- | :--- | :--- | :--- | :--- |
<!-- JOURNAL_END -->

---

## 🛠️ How to Log Your Progress

You can manually edit this file, or use the interactive desktop GUI application.

### Launch Options:
* **Option 1 (Double-Click)**: Double-click the **`gui_log.exe`** application at the root of this workspace.
* **Option 2 (Terminal)**: Run the python script in your terminal:
  ```bash
  python gui_log.py
  ```

This helper tool will automatically:
1. Provide a graphical dashboard and tabs for easy data entry.
2. Allow you to write or paste solution code directly to save inside the `solutions/` folder.
3. Automatically commit your logged details and new code solutions to Git with structured commit messages.
4. Calculate and update dashboard metrics (Streak, Days Active, Solved Counts) instantly on submission.
"""
        with open(README_PATH, "w", encoding="utf-8") as f:
            f.write(fresh_readme_content.strip() + "\n")
            
        messagebox.showinfo("Success", "Workspace initialized successfully! Let's get preparing! 🚀")
        
        # Destroy welcome frame
        self.init_container.destroy()
        
        # Load main dashboard layout
        self.load_main_dashboard()

    def load_main_dashboard(self):
        # Main Layout: Sidebar (Dashboard) and Right Pane (Forms)
        self.main_container = ttk.Frame(self.root)
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Left Sidebar (Stats Dashboard)
        self.sidebar = tk.Frame(self.main_container, bg="#2f3640", width=250)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)
        
        # Right Notebook (Tabs for logging)
        self.notebook = ttk.Notebook(self.main_container)
        self.notebook.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        self.setup_sidebar()
        self.setup_tabs()
        
        # Load initially
        self.refresh_dashboard()

    # --- Git Integration Functions ---
    def is_git_repo(self):
        return os.path.exists(".git")

    def run_git_cmd(self, cmd):
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return True, result.stdout
        except subprocess.CalledProcessError as e:
            return False, e.stderr
        except Exception as e:
            return False, str(e)

    def handle_git_commit_and_push(self, committed_files, commit_msg, should_push=False):
        if not self.is_git_repo():
            init_repo = messagebox.askyesno("Git Repository Missing", 
                "This folder is not a Git repository. Would you like to initialize it and make the commit?")
            if init_repo:
                success, err = self.run_git_cmd(["git", "init"])
                if not success:
                    messagebox.showerror("Git Error", f"Failed to initialize Git repository:\n{err}")
                    return False
            else:
                return False

        # Add files
        for f in committed_files:
            if os.path.exists(f):
                self.run_git_cmd(["git", "add", f])
        
        # Commit
        success, out_err = self.run_git_cmd(["git", "commit", "-m", commit_msg])
        if not success:
            if "nothing to commit" in out_err.lower() or "no changes added" in out_err.lower():
                pass
            else:
                messagebox.showwarning("Git Commit Warning", f"Could not complete commit:\n{out_err}")
                return False

        # Push to GitHub
        if should_push:
            self.handle_git_push()

        return True

    def handle_git_push(self):
        # Check if remote is configured
        success, remote_out = self.run_git_cmd(["git", "remote"])
        if not success or not remote_out.strip():
            from tkinter import simpledialog
            url = simpledialog.askstring("Git Push - Setup Remote", 
                "GitHub remote repository is not configured.\n\nPlease enter your GitHub Repository URL\n(e.g., https://github.com/username/repo_name.git):")
            if not url:
                messagebox.showinfo("Git Push", "Push cancelled because no remote URL was configured.")
                return
            
            success_add, err_add = self.run_git_cmd(["git", "remote", "add", "origin", url.strip()])
            if not success_add:
                messagebox.showerror("Git Remote Error", f"Failed to add remote:\n{err_add}")
                return

        # Start asynchronous push thread so the GUI does not freeze
        import threading
        self.root.config(cursor="watch")
        
        def push_worker():
            try:
                # Use git push -u origin HEAD to push current branch and track
                success_push, out_err = self.run_git_cmd(["git", "push", "-u", "origin", "HEAD"])
            except Exception as e:
                success_push, out_err = False, str(e)
            
            self.root.after(0, lambda: self.on_push_complete(success_push, out_err))
            
        threading.Thread(target=push_worker, daemon=True).start()

    def on_push_complete(self, success, message):
        self.root.config(cursor="")
        if success:
            messagebox.showinfo("Git Push Success", "Successfully pushed all changes to GitHub! 🚀")
        else:
            hint = ""
            if "permission denied" in message.lower() or "could not read from remote" in message.lower() or "fatal: Authentication failed" in message or "access denied" in message.lower():
                hint = "\n\n💡 Hint: Ensure you have authenticated Git with GitHub (e.g. set up SSH keys or GitHub CLI Credential Helper)."
            elif "no upstream branch" in message.lower():
                hint = "\n\n💡 Hint: Upstream branch is not set. Try running 'git push -u origin main' manually."
            
            messagebox.showerror("Git Push Failed", f"Could not push to GitHub:\n\n{message}{hint}")

    # --- Data Parsing & Updating Logic ---
    def parse_markdown_table(self, content, start_marker, end_marker):
        pattern = re.compile(rf"{start_marker}\n(.*?)\n{end_marker}", re.DOTALL)
        match = pattern.search(content)
        if not match:
            return []
        table_content = match.group(1).strip()
        lines = [line.strip() for line in table_content.split("\n") if line.strip()]
        return lines

    def read_readme(self):
        if not os.path.exists(README_PATH):
            return ""
        with open(README_PATH, "r", encoding="utf-8") as f:
            return f.read()

    def write_readme(self, content):
        with open(README_PATH, "w", encoding="utf-8") as f:
            f.write(content)

    def update_dashboard_metrics(self, content):
        questions_lines = self.parse_markdown_table(content, "<!-- QUESTIONS_START -->", "<!-- QUESTIONS_END -->")
        
        actual_questions = []
        for line in questions_lines:
            if line.startswith("|") and not line.startswith("| :---") and not line.startswith("| Date") and "*Example*" not in line:
                actual_questions.append(line)
                
        total_solved = len(actual_questions)
        easy = 0
        medium = 0
        hard = 0
        unique_dates = set()
        
        for q in actual_questions:
            parts = [p.strip() for p in q.split("|")[1:-1]]
            if len(parts) >= 5:
                date_val = parts[0]
                if date_val and not date_val.startswith("*"):
                    unique_dates.add(date_val)
                    
                diff = parts[5].lower() if len(parts) >= 6 else parts[4].lower()
                if "easy" in diff or "🟢" in diff:
                    easy += 1
                elif "medium" in diff or "🟡" in diff:
                    medium += 1
                elif "hard" in diff or "🔴" in diff:
                    hard += 1

        tech_lines = self.parse_markdown_table(content, "<!-- TECH_START -->", "<!-- TECH_END -->")
        for line in tech_lines:
            if line.startswith("|") and not line.startswith("| :---") and not line.startswith("| Date") and "*Example*" not in line:
                parts = [p.strip() for p in line.split("|")[1:-1]]
                if len(parts) >= 1:
                    date_val = parts[0]
                    if date_val and not date_val.startswith("*"):
                        unique_dates.add(date_val)

        journal_lines = self.parse_markdown_table(content, "<!-- JOURNAL_START -->", "<!-- JOURNAL_END -->")
        for line in journal_lines:
            if line.startswith("|") and not line.startswith("| :---") and not line.startswith("| Date") and "*Example*" not in line:
                parts = [p.strip() for p in line.split("|")[1:-1]]
                if len(parts) >= 1:
                    date_val = parts[0]
                    if date_val and not date_val.startswith("*"):
                        unique_dates.add(date_val)

        days_active = len(unique_dates)
        
        # Streak Calculation
        sorted_dates = sorted(list(unique_dates), reverse=True)
        streak = 0
        if sorted_dates:
            today_str = get_current_date()
            yesterday_str = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")
            
            has_today = today_str in sorted_dates
            has_yesterday = yesterday_str in sorted_dates
            
            if has_today or has_yesterday:
                check_date = datetime.strptime(sorted_dates[0], "%Y-%m-%d")
                streak = 1
                for i in range(1, len(sorted_dates)):
                    prev_date = datetime.strptime(sorted_dates[i], "%Y-%m-%d")
                    if (check_date - prev_date).days == 1:
                        streak += 1
                        check_date = prev_date
                    else:
                        break
            else:
                streak = 0

        now_str = datetime.now().strftime("%Y-%m-%d %I:%M %p")
        
        # Find Current Focus
        focus_match = re.search(r"\|\s*\*\*Current Focus\*\*\s*\|\s*(.*?)\s*\|", content)
        current_focus = focus_match.group(1) if focus_match else "🎯 DSA & Development"
        
        dashboard_template = f"""## 📊 Quick Dashboard

| Metric | Status / Value | Details |
| :--- | :--- | :--- |
| **Current Focus** | {current_focus} | Core DSA + Core CS Subjects |
| **Questions Solved** | **{total_solved}** | 🟢 Easy: `{easy}` \| 🟡 Medium: `{medium}` \| 🔴 Hard: `{hard}` |
| **Days Active** | 📅 `{days_active}` Days | Current Streak: `{streak}` Days |
| **Last Updated** | 🕒 *{now_str}* | Automatically logged |"""

        content = re.sub(r"## 📊 Quick Dashboard\n\n.*?\n\n---", dashboard_template + "\n\n---", content, flags=re.DOTALL)
        return content

    # --- UI Setup: Left Sidebar (Dashboard) ---
    def setup_sidebar(self):
        # Title/Logo Area
        title_frame = tk.Frame(self.sidebar, bg="#1e222b", pady=20)
        title_frame.pack(fill=tk.X)
        
        lbl_title = tk.Label(title_frame, text="PLACEMENT PREP", font=("Segoe UI", 12, "bold"), fg="white", bg="#1e222b")
        lbl_title.pack()
        lbl_subtitle = tk.Label(title_frame, text="LOG ASSISTANT", font=("Segoe UI", 9), fg="#00a8ff", bg="#1e222b")
        lbl_subtitle.pack()
        
        # Study Session Frame
        self.session_frame = tk.Frame(self.sidebar, bg="#1e222b", padx=10, pady=15)
        self.session_frame.pack(fill=tk.X)
        
        lbl_sess_title = tk.Label(self.session_frame, text="⏱️ STUDY SESSION TIMER", font=("Segoe UI", 9, "bold"), fg="#7f8c8d", bg="#1e222b")
        lbl_sess_title.pack(pady=(0, 5))
        
        self.lbl_stopwatch = tk.Label(self.session_frame, text="00:00:00", font=("Segoe UI", 16, "bold"), fg="#00a8ff", bg="#1e222b")
        self.lbl_stopwatch.pack(pady=5)
        
        self.lbl_track_status = tk.Label(self.session_frame, text="Status: Idle", font=("Segoe UI", 8, "italic"), fg="#7f8c8d", bg="#1e222b")
        self.lbl_track_status.pack(pady=(0, 10))
        
        self.btn_session_toggle = tk.Button(self.session_frame, text="Start Study Session", font=("Segoe UI", 9, "bold"), bg="#4cd137", fg="white",
                                            activebackground="#44bd32", activeforeground="white", bd=0, pady=6, command=self.toggle_study_session)
        self.btn_session_toggle.pack(fill=tk.X)

        # Stats Frame
        self.stats_frame = tk.Frame(self.sidebar, bg="#2f3640", padx=15, pady=25)
        self.stats_frame.pack(fill=tk.BOTH, expand=True)
        
        # Labels will be updated by refresh_dashboard
        self.lbl_focus_val = tk.Label(self.stats_frame, text="-", font=("Segoe UI", 10, "italic"), fg="#f5f6fa", bg="#2f3640", wraplength=210, justify=tk.LEFT)
        self.lbl_solved_val = tk.Label(self.stats_frame, text="-", font=("Segoe UI", 16, "bold"), fg="#4cd137", bg="#2f3640")
        self.lbl_breakdown_val = tk.Label(self.stats_frame, text="-", font=("Segoe UI", 9), fg="#dcdde1", bg="#2f3640")
        self.lbl_days_val = tk.Label(self.stats_frame, text="-", font=("Segoe UI", 12, "bold"), fg="#f5f6fa", bg="#2f3640")
        self.lbl_streak_val = tk.Label(self.stats_frame, text="-", font=("Segoe UI", 12, "bold"), fg="#e1b12c", bg="#2f3640")
        self.lbl_updated_val = tk.Label(self.stats_frame, text="-", font=("Segoe UI", 8), fg="#7f8c8d", bg="#2f3640")
        
        # Pack layout in sidebar
        self.create_sidebar_stat("Target Focus:", self.lbl_focus_val)
        self.create_sidebar_stat("Solved Questions:", self.lbl_solved_val)
        self.lbl_breakdown_val.pack(anchor=tk.W, pady=(0, 15))
        
        self.create_sidebar_stat("Days Active:", self.lbl_days_val)
        self.create_sidebar_stat("Current Streak:", self.lbl_streak_val)
        self.create_sidebar_stat("Last Updated:", self.lbl_updated_val)

        # Refresh button at bottom of sidebar
        btn_refresh = tk.Button(self.sidebar, text="Sync Dashboard", font=("Segoe UI", 9, "bold"), bg="#1e222b", fg="white", 
                                activebackground="#00a8ff", activeforeground="white", bd=0, pady=8, command=self.refresh_dashboard)
        btn_refresh.pack(side=tk.BOTTOM, fill=tk.X, padx=15, pady=15)

    def create_sidebar_stat(self, header, val_lbl):
        lbl = tk.Label(self.stats_frame, text=header, font=("Segoe UI", 9, "bold"), fg="#7f8c8d", bg="#2f3640")
        lbl.pack(anchor=tk.W, pady=(10, 2))
        val_lbl.pack(anchor=tk.W, pady=(0, 10))

    def refresh_dashboard(self):
        content = self.read_readme()
        if not content:
            self.lbl_focus_val.configure(text="README.md not found")
            return
            
        # Parse Dashboard
        focus_match = re.search(r"\|\s*\*\*Current Focus\*\*\s*\|\s*(.*?)\s*\|", content)
        focus = focus_match.group(1) if focus_match else "-"
        self.lbl_focus_val.configure(text=focus)
        
        solved_match = re.search(r"\|\s*\*\*Questions Solved\*\*\s*\|\s*\*\*(\d+)\*\*\s*\|\s*(.*?)\s*\|", content)
        if solved_match:
            self.lbl_solved_val.configure(text=solved_match.group(1))
            self.lbl_breakdown_val.configure(text=solved_match.group(2).replace("\\|", " |"))
        else:
            self.lbl_solved_val.configure(text="-")
            self.lbl_breakdown_val.configure(text="-")
            
        days_match = re.search(r"\|\s*\*\*Days Active\*\*\s*\|\s*📅\s*`(\d+)`\s*Days\s*\|\s*Current Streak:\s*`(\d+)`\s*Days\s*\|", content)
        if days_match:
            self.lbl_days_val.configure(text=f"{days_match.group(1)} Days")
            self.lbl_streak_val.configure(text=f"{days_match.group(2)} Days 🔥")
        else:
            self.lbl_days_val.configure(text="-")
            self.lbl_streak_val.configure(text="-")
            
        updated_match = re.search(r"\|\s*\*\*Last Updated\*\*\s*\|\s*🕒\s*\*(.*?)\*\s*\|", content)
        updated = updated_match.group(1) if updated_match else "-"
        self.lbl_updated_val.configure(text=updated)

    # --- UI Setup: Right Forms Tabs ---
    def setup_tabs(self):
        # 1. Tab Coding Question
        self.tab_coding = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.tab_coding, text="Coding Question")
        self.build_coding_tab()
        
        # 2. Tab Tech Concept
        self.tab_tech = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.tab_tech, text="Tech Learning")
        self.build_tech_tab()
        
        # 3. Tab Study Journal
        self.tab_journal = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.tab_journal, text="Study Journal")
        self.build_journal_tab()

        # 4. Tab Goal/Focus
        self.tab_focus = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.tab_focus, text="Current Focus")
        self.build_focus_tab()

    # --- Tab Builders & Submit Handlers ---
    
    # 1. Coding Question Tab
    def build_coding_tab(self):
        row = 0
        
        # Header
        lbl_head = ttk.Label(self.tab_coding, text="Log Solved Coding Question", style="Header.TLabel")
        lbl_head.grid(row=row, column=0, columnspan=3, sticky=tk.W, pady=(5, 15))
        row += 1
        
        # Date & Platform
        ttk.Label(self.tab_coding, text="Date:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.ent_code_date = ttk.Entry(self.tab_coding, width=15)
        self.ent_code_date.insert(0, get_current_date())
        self.ent_code_date.grid(row=row, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(self.tab_coding, text="Platform:").grid(row=row, column=2, sticky=tk.W, padx=(20, 5), pady=5)
        self.cmb_code_platform = ttk.Combobox(self.tab_coding, values=["LeetCode", "GeeksforGeeks", "HackerRank", "CodeForces", "InterviewBit", "Other"], width=15)
        self.cmb_code_platform.set("LeetCode")
        self.cmb_code_platform.grid(row=row, column=3, sticky=tk.W, pady=5)
        row += 1
        
        # Problem Name & Link
        ttk.Label(self.tab_coding, text="Problem Name:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.ent_code_name = ttk.Entry(self.tab_coding, width=25)
        self.ent_code_name.grid(row=row, column=1, sticky=tk.W, pady=5)
        self.ent_code_name.bind("<KeyRelease>", self.on_problem_name_change)
        
        ttk.Label(self.tab_coding, text="Problem Link:").grid(row=row, column=2, sticky=tk.W, padx=(20, 5), pady=5)
        self.ent_code_link = ttk.Entry(self.tab_coding, width=25)
        self.ent_code_link.grid(row=row, column=3, sticky=tk.EW, pady=5)
        row += 1
        
        # Topic/Pattern & Language
        ttk.Label(self.tab_coding, text="Topic / Pattern:").grid(row=row, column=0, sticky=tk.W, pady=5)
        topics = [
            "Arrays", "Hashing", "Two Pointers", "Sliding Window", "Prefix Sum", 
            "Strings", "Stacks & Queues", "Linked Lists", "Recursion / Backtracking", 
            "Binary Search", "Trees & Binary Trees", "Graphs", "Heaps / Priority Queues", 
            "Dynamic Programming", "Greedy Algorithms", "Tries", "Bit Manipulation", 
            "Math & Geometry", "Other"
        ]
        self.cmb_code_topic = ttk.Combobox(self.tab_coding, values=topics, width=22)
        self.cmb_code_topic.set("Arrays")
        self.cmb_code_topic.grid(row=row, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(self.tab_coding, text="Language:").grid(row=row, column=2, sticky=tk.W, padx=(20, 5), pady=5)
        langs = ["Python", "C++", "Java", "JavaScript", "TypeScript", "Go", "Rust", "SQL", "Other"]
        self.cmb_code_lang = ttk.Combobox(self.tab_coding, values=langs, width=13)
        self.cmb_code_lang.set("Python")
        self.cmb_code_lang.grid(row=row, column=3, sticky=tk.W, pady=5)
        self.cmb_code_lang.bind("<<ComboboxSelected>>", self.on_problem_name_change)
        row += 1
        
        # Difficulty & Complexity
        ttk.Label(self.tab_coding, text="Difficulty:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.cmb_code_diff = ttk.Combobox(self.tab_coding, values=["🟢 Easy", "🟡 Medium", "🔴 Hard"], width=22, state="readonly")
        self.cmb_code_diff.set("🟡 Medium")
        self.cmb_code_diff.grid(row=row, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(self.tab_coding, text="Complexity/Takeaway:").grid(row=row, column=2, sticky=tk.W, padx=(20, 5), pady=5)
        self.ent_code_complexity = ttk.Entry(self.tab_coding, width=25)
        self.ent_code_complexity.insert(0, "Two Pointers / O(N)")
        self.ent_code_complexity.grid(row=row, column=3, sticky=tk.EW, pady=5)
        row += 1
        
        # Code paste box section
        ttk.Label(self.tab_coding, text="Solution Filename:").grid(row=row, column=0, sticky=tk.W, pady=(15, 5))
        self.ent_code_filename = ttk.Entry(self.tab_coding, width=25)
        self.ent_code_filename.grid(row=row, column=1, sticky=tk.W, pady=(15, 5))
        
        self.var_code_git = tk.BooleanVar(value=True)
        self.chk_code_git = ttk.Checkbutton(self.tab_coding, text="Auto Git Commit", variable=self.var_code_git)
        self.chk_code_git.grid(row=row, column=2, sticky=tk.W, padx=(20, 0), pady=(15, 5))
        
        self.var_code_push = tk.BooleanVar(value=True)
        self.chk_code_push = ttk.Checkbutton(self.tab_coding, text="and Push to GitHub", variable=self.var_code_push)
        self.chk_code_push.grid(row=row, column=3, sticky=tk.W, pady=(15, 5))
        row += 1
        
        ttk.Label(self.tab_coding, text="Paste Solution Code (Saved to solutions/):").grid(row=row, column=0, columnspan=4, sticky=tk.W, pady=5)
        row += 1
        
        self.txt_code_body = scrolledtext.ScrolledText(self.tab_coding, height=10, width=80, wrap=tk.NONE, font=("Consolas", 10))
        self.txt_code_body.grid(row=row, column=0, columnspan=4, sticky=tk.NSEW, pady=5)
        
        self.tab_coding.rowconfigure(row, weight=1)
        self.tab_coding.columnconfigure(1, weight=1)
        self.tab_coding.columnconfigure(3, weight=1)
        row += 1
        
        # Button Panel
        btn_panel = ttk.Frame(self.tab_coding)
        btn_panel.grid(row=row, column=0, columnspan=4, sticky=tk.E, pady=15)
        
        btn_submit = tk.Button(btn_panel, text="Save & Log Question", font=("Segoe UI", 10, "bold"), bg="#4cd137", fg="white", 
                               activebackground="#44bd32", activeforeground="white", bd=0, padx=15, pady=6, command=self.submit_coding_question)
        btn_submit.pack()

    def on_problem_name_change(self, event=None):
        name = self.ent_code_name.get().strip()
        lang = self.cmb_code_lang.get().strip().lower()
        
        # Convert name to clean snake_case filename
        clean_name = re.sub(r'[^a-zA-Z0-9\s_-]', '', name).strip().lower()
        filename = re.sub(r'[\s-]+', '_', clean_name)
        
        ext = LANG_EXT_MAP.get(lang, ".py")
        if filename:
            self.ent_code_filename.delete(0, tk.END)
            self.ent_code_filename.insert(0, f"{filename}{ext}")

    def submit_coding_question(self):
        date = self.ent_code_date.get().strip()
        platform = self.cmb_code_platform.get().strip()
        name = self.ent_code_name.get().strip()
        link = self.ent_code_link.get().strip()
        topic = self.cmb_code_topic.get().strip()
        lang = self.cmb_code_lang.get().strip()
        diff = self.cmb_code_diff.get()
        complexity = self.ent_code_complexity.get().strip()
        filename = self.ent_code_filename.get().strip()
        code_content = self.txt_code_body.get("1.0", tk.END).strip()
        
        if not name or not topic or not lang:
            messagebox.showerror("Validation Error", "Problem Name, Topic, and Language are required!")
            return
            
        if self.session_active:
            self.session_questions_solved.append(name)
            
        # 1. Save Code File if provided
        sol_link = "-"
        saved_files = [README_PATH]
        
        if code_content and filename:
            filepath = os.path.join(SOLUTIONS_DIR, filename)
            try:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(code_content)
                sol_link = f"[{filename}](file:///g:/Placement%20Prep/solutions/{filename})"
                saved_files.append(filepath)
            except Exception as e:
                messagebox.showerror("Write Error", f"Failed to save solution code:\n{str(e)}")
                return
        
        # Format problem name as link if link provided
        prob_formatted = f"[{name}]({link})" if link else name
        
        # Create row
        new_row = f"| {date} | {platform} | {prob_formatted} | {topic} | {lang} | {diff} | {complexity} | {sol_link} |"
        
        # 2. Update README.md
        content = self.read_readme()
        if not content:
            messagebox.showerror("Error", "README.md not found in the current workspace.")
            return
            
        lines = self.parse_markdown_table(content, "<!-- QUESTIONS_START -->", "<!-- QUESTIONS_END -->")
        lines.append(new_row)
        
        new_table_str = "<!-- QUESTIONS_START -->\n" + "\n".join(lines) + "\n<!-- QUESTIONS_END -->"
        content = re.sub(r"<!-- QUESTIONS_START -->.*?<!-- QUESTIONS_END -->", new_table_str, content, flags=re.DOTALL)
        
        content = self.update_dashboard_metrics(content)
        self.write_readme(content)
        
        # 3. Auto Git Commit & Push
        commit_success = True
        if self.var_code_git.get():
            commit_msg = f"docs: solve {name} on {platform}"
            should_push = self.var_code_push.get()
            commit_success = self.handle_git_commit_and_push(saved_files, commit_msg, should_push)
            
        self.refresh_dashboard()
        
        # Clear fields
        self.ent_code_name.delete(0, tk.END)
        self.ent_code_link.delete(0, tk.END)
        self.cmb_code_topic.set("Arrays")
        self.cmb_code_lang.set("Python")
        self.ent_code_filename.delete(0, tk.END)
        self.txt_code_body.delete("1.0", tk.END)
        
        msg = f"Logged question '{name}' successfully!"
        if self.var_code_git.get() and commit_success:
            msg += "\nChanges logged and committed to Git!"
        messagebox.showinfo("Success", msg)

    # 2. Tech Concept Tab
    def build_tech_tab(self):
        row = 0
        
        # Header
        lbl_head = ttk.Label(self.tab_tech, text="Log Technical Concept / Subject Learned", style="Header.TLabel")
        lbl_head.grid(row=row, column=0, columnspan=4, sticky=tk.W, pady=(5, 15))
        row += 1
        
        # Date & Technology
        ttk.Label(self.tab_tech, text="Date:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.ent_tech_date = ttk.Entry(self.tab_tech, width=15)
        self.ent_tech_date.insert(0, get_current_date())
        self.ent_tech_date.grid(row=row, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(self.tab_tech, text="Technology / Subject:").grid(row=row, column=2, sticky=tk.W, padx=(20, 5), pady=5)
        self.ent_tech_domain = ttk.Entry(self.tab_tech, width=25)
        self.ent_tech_domain.insert(0, "e.g., DBMS, Python, System Design")
        self.ent_tech_domain.grid(row=row, column=3, sticky=tk.EW, pady=5)
        row += 1
        
        # Topic & Resources
        ttk.Label(self.tab_tech, text="Topic / Concept:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.ent_tech_topic = ttk.Entry(self.tab_tech, width=30)
        self.ent_tech_topic.grid(row=row, column=1, columnspan=3, sticky=tk.EW, pady=5)
        row += 1
        
        ttk.Label(self.tab_tech, text="Resources Used:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.ent_tech_resource = ttk.Entry(self.tab_tech, width=30)
        self.ent_tech_resource.grid(row=row, column=1, columnspan=3, sticky=tk.EW, pady=5)
        row += 1
        
        # Confidence & Commit
        ttk.Label(self.tab_tech, text="Confidence Level:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.cmb_tech_confidence = ttk.Combobox(self.tab_tech, values=["🟢 5/5 - Mastery", "🔵 4/5 - Confident", "🟡 3/5 - Okay", "🟠 2/5 - Weak", "🔴 1/5 - Novice"], width=20, state="readonly")
        self.cmb_tech_confidence.set("🟡 3/5 - Okay")
        self.cmb_tech_confidence.grid(row=row, column=1, sticky=tk.W, pady=5)
        
        self.var_tech_git = tk.BooleanVar(value=True)
        self.chk_tech_git = ttk.Checkbutton(self.tab_tech, text="Auto Git Commit", variable=self.var_tech_git)
        self.chk_tech_git.grid(row=row, column=2, sticky=tk.W, padx=(20, 0), pady=5)
        
        self.var_tech_push = tk.BooleanVar(value=True)
        self.chk_tech_push = ttk.Checkbutton(self.tab_tech, text="and Push to GitHub", variable=self.var_tech_push)
        self.chk_tech_push.grid(row=row, column=3, sticky=tk.W, pady=5)
        row += 1
        
        # Summary Text area
        ttk.Label(self.tab_tech, text="Key Takeaways / Core Learnings Summary:").grid(row=row, column=0, columnspan=4, sticky=tk.W, pady=(15, 5))
        row += 1
        
        self.txt_tech_summary = scrolledtext.ScrolledText(self.tab_tech, height=12, width=80, wrap=tk.WORD, font=("Segoe UI", 10))
        self.txt_tech_summary.grid(row=row, column=0, columnspan=4, sticky=tk.NSEW, pady=5)
        
        self.tab_tech.rowconfigure(row, weight=1)
        self.tab_tech.columnconfigure(1, weight=1)
        self.tab_tech.columnconfigure(3, weight=1)
        row += 1
        
        # Button Panel
        btn_panel = ttk.Frame(self.tab_tech)
        btn_panel.grid(row=row, column=0, columnspan=4, sticky=tk.E, pady=15)
        
        btn_submit = tk.Button(btn_panel, text="Save & Log Concept", font=("Segoe UI", 10, "bold"), bg="#4cd137", fg="white", 
                               activebackground="#44bd32", activeforeground="white", bd=0, padx=15, pady=6, command=self.submit_tech_concept)
        btn_submit.pack()

    def submit_tech_concept(self):
        date = self.ent_tech_date.get().strip()
        tech = self.ent_tech_domain.get().strip()
        topic = self.ent_tech_topic.get().strip()
        resource = self.ent_tech_resource.get().strip()
        conf_str = self.cmb_tech_confidence.get()
        takeaways = self.txt_tech_summary.get("1.0", tk.END).strip()
        
        if not tech or not topic:
            messagebox.showerror("Validation Error", "Technology and Topic / Concept are required!")
            return
            
        # Parse confidence to output emoji format: e.g. "🟡 3/5"
        conf_emoji = conf_str.split(" - ")[0]
        
        new_row = f"| {date} | {tech} | {topic} | {resource} | {conf_emoji} | {takeaways.replace(chr(10), ' ')} |"
        
        content = self.read_readme()
        if not content:
            messagebox.showerror("Error", "README.md not found in the current workspace.")
            return
            
        lines = self.parse_markdown_table(content, "<!-- TECH_START -->", "<!-- TECH_END -->")
        lines.append(new_row)
        
        new_table_str = "<!-- TECH_START -->\n" + "\n".join(lines) + "\n<!-- TECH_END -->"
        content = re.sub(r"<!-- TECH_START -->.*?<!-- TECH_END -->", new_table_str, content, flags=re.DOTALL)
        
        content = self.update_dashboard_metrics(content)
        self.write_readme(content)
        
        # Git auto-commit & push
        commit_success = True
        if self.var_tech_git.get():
            commit_msg = f"docs: log study topic {topic} ({tech})"
            should_push = self.var_tech_push.get()
            commit_success = self.handle_git_commit_and_push([README_PATH], commit_msg, should_push)
            
        self.refresh_dashboard()
        
        # Clear fields
        self.ent_tech_domain.delete(0, tk.END)
        self.ent_tech_topic.delete(0, tk.END)
        self.ent_tech_resource.delete(0, tk.END)
        self.txt_tech_summary.delete("1.0", tk.END)
        
        msg = f"Logged concept '{topic}' successfully!"
        if self.var_tech_git.get() and commit_success:
            msg += "\nChanges logged and committed to Git!"
        messagebox.showinfo("Success", msg)

    # 3. Study Journal Tab
    def build_journal_tab(self):
        row = 0
        
        # Header
        lbl_head = ttk.Label(self.tab_journal, text="Log Chronological Study Session", style="Header.TLabel")
        lbl_head.grid(row=row, column=0, columnspan=4, sticky=tk.W, pady=(5, 15))
        row += 1
        
        # Date & Category
        ttk.Label(self.tab_journal, text="Date:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.ent_journ_date = ttk.Entry(self.tab_journal, width=15)
        self.ent_journ_date.insert(0, get_current_date())
        self.ent_journ_date.grid(row=row, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(self.tab_journal, text="Category:").grid(row=row, column=2, sticky=tk.W, padx=(20, 5), pady=5)
        self.cmb_journ_cat = ttk.Combobox(self.tab_journal, values=["DSA", "Development", "Core CS", "Aptitude", "Mock Interview", "Project Work", "Other"], width=18)
        self.cmb_journ_cat.set("DSA")
        self.cmb_journ_cat.grid(row=row, column=3, sticky=tk.W, pady=5)
        row += 1
        
        # Time Slots (Start Time & End Time)
        ttk.Label(self.tab_journal, text="Start Time:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.ent_journ_start = ttk.Entry(self.tab_journal, width=15)
        self.ent_journ_start.insert(0, get_current_time())
        self.ent_journ_start.grid(row=row, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(self.tab_journal, text="End Time (optional):").grid(row=row, column=2, sticky=tk.W, padx=(20, 5), pady=5)
        self.ent_journ_end = ttk.Entry(self.tab_journal, width=18)
        
        # Default end time to 1 hour from now
        default_end = (datetime.now() + timedelta(hours=1)).strftime("%I:%M %p")
        self.ent_journ_end.insert(0, default_end)
        self.ent_journ_end.grid(row=row, column=3, sticky=tk.W, pady=5)
        row += 1
        
        # Description
        ttk.Label(self.tab_journal, text="Activity Description:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.ent_journ_desc = ttk.Entry(self.tab_journal, width=50)
        self.ent_journ_desc.insert(0, "e.g., Practiced binary search medium questions, read B-trees")
        self.ent_journ_desc.grid(row=row, column=1, columnspan=3, sticky=tk.EW, pady=5)
        row += 1
        
        # Focus/Takeaway
        ttk.Label(self.tab_journal, text="Focus / Key Takeaway:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.ent_journ_takeaway = ttk.Entry(self.tab_journal, width=50)
        self.ent_journ_takeaway.grid(row=row, column=1, columnspan=3, sticky=tk.EW, pady=5)
        row += 1
        
        # Next Steps
        ttk.Label(self.tab_journal, text="Next Steps:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.ent_journ_next = ttk.Entry(self.tab_journal, width=50)
        self.ent_journ_next.grid(row=row, column=1, columnspan=3, sticky=tk.EW, pady=5)
        row += 1
        
        # Git Auto-commit option
        self.var_journ_git = tk.BooleanVar(value=True)
        self.chk_journ_git = ttk.Checkbutton(self.tab_journal, text="Auto Git Commit", variable=self.var_journ_git)
        self.chk_journ_git.grid(row=row, column=1, sticky=tk.W, pady=10)
        
        self.var_journ_push = tk.BooleanVar(value=True)
        self.chk_journ_push = ttk.Checkbutton(self.tab_journal, text="and Push to GitHub", variable=self.var_journ_push)
        self.chk_journ_push.grid(row=row, column=2, sticky=tk.W, pady=10)
        
        self.tab_journal.columnconfigure(1, weight=1)
        self.tab_journal.columnconfigure(3, weight=1)
        row += 1
        
        # Button Panel
        btn_panel = ttk.Frame(self.tab_journal)
        btn_panel.grid(row=row, column=0, columnspan=4, sticky=tk.E, pady=25)
        
        btn_submit = tk.Button(btn_panel, text="Save & Log Session", font=("Segoe UI", 10, "bold"), bg="#4cd137", fg="white", 
                               activebackground="#44bd32", activeforeground="white", bd=0, padx=15, pady=6, command=self.submit_journal_entry)
        btn_submit.pack()

    def submit_journal_entry(self):
        date = self.ent_journ_date.get().strip()
        cat = self.cmb_journ_cat.get().strip()
        start = self.ent_journ_start.get().strip()
        end = self.ent_journ_end.get().strip()
        desc = self.ent_journ_desc.get().strip()
        takeaway = self.ent_journ_takeaway.get().strip()
        next_steps = self.ent_journ_next.get().strip()
        
        if not desc:
            messagebox.showerror("Validation Error", "Activity Description is required!")
            return
            
        time_slot = f"{start} - {end}" if end else start
        
        new_row = f"| {date} | {time_slot} | {cat} | {desc} | {takeaway} | {next_steps} |"
        
        content = self.read_readme()
        if not content:
            messagebox.showerror("Error", "README.md not found in the current workspace.")
            return
            
        lines = self.parse_markdown_table(content, "<!-- JOURNAL_START -->", "<!-- JOURNAL_END -->")
        lines.append(new_row)
        
        new_table_str = "<!-- JOURNAL_START -->\n" + "\n".join(lines) + "\n<!-- JOURNAL_END -->"
        content = re.sub(r"<!-- JOURNAL_START -->.*?<!-- JOURNAL_END -->", new_table_str, content, flags=re.DOTALL)
        
        content = self.update_dashboard_metrics(content)
        self.write_readme(content)
        
        # Git auto-commit & push
        commit_success = True
        if self.var_journ_git.get():
            commit_msg = f"docs: log study session on {cat}"
            should_push = self.var_journ_push.get()
            commit_success = self.handle_git_commit_and_push([README_PATH], commit_msg, should_push)
            
        self.refresh_dashboard()
        
        # Clear fields
        self.ent_journ_desc.delete(0, tk.END)
        self.ent_journ_takeaway.delete(0, tk.END)
        self.ent_journ_next.delete(0, tk.END)
        
        msg = "Study session logged successfully!"
        if self.var_journ_git.get() and commit_success:
            msg += "\nChanges logged and committed to Git!"
        messagebox.showinfo("Success", msg)

    # 4. Current Focus Goal Tab
    def build_focus_tab(self):
        row = 0
        
        # Header
        lbl_head = ttk.Label(self.tab_focus, text="Update Target Prep Focus", style="Header.TLabel")
        lbl_head.grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=(5, 15))
        row += 1
        
        ttk.Label(self.tab_focus, text="Enter Focus Areas / Target Topics:").grid(row=row, column=0, sticky=tk.W, pady=5)
        row += 1
        
        self.ent_focus_value = ttk.Entry(self.tab_focus, width=60)
        self.ent_focus_value.grid(row=row, column=0, columnspan=2, sticky=tk.EW, pady=5)
        row += 1
        
        # Load current focus from README
        content = self.read_readme()
        if content:
            focus_match = re.search(r"\|\s*\*\*Current Focus\*\*\s*\|\s*(.*?)\s*\|", content)
            focus = focus_match.group(1) if focus_match else ""
            self.ent_focus_value.insert(0, focus)
            
        self.tab_focus.columnconfigure(1, weight=1)
        row += 1
        
        # Button Panel
        btn_panel = ttk.Frame(self.tab_focus)
        btn_panel.grid(row=row, column=0, columnspan=2, sticky=tk.E, pady=15)
        
        btn_submit = tk.Button(btn_panel, text="Update Focus Area", font=("Segoe UI", 10, "bold"), bg="#00a8ff", fg="white", 
                               activebackground="#0097e6", activeforeground="white", bd=0, padx=15, pady=6, command=self.submit_focus_goal)
        btn_submit.pack()
        row += 1

        # Separator line
        sep = ttk.Separator(self.tab_focus, orient=tk.HORIZONTAL)
        sep.grid(row=row, column=0, columnspan=2, sticky=tk.EW, pady=(15, 10))
        row += 1

        # Danger Zone
        lbl_danger_head = ttk.Label(self.tab_focus, text="⚠️ Danger Zone", style="Header.TLabel", foreground="#e84118")
        lbl_danger_head.grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=5)
        row += 1

        lbl_danger_desc = ttk.Label(self.tab_focus, text="Clears all your logged questions, tech learning concepts, and study journal logs from README.md.\nNote: This will reset all your dashboard stats back to 0. Solution code files in solutions/ are preserved.", font=("Segoe UI", 9, "italic"), justify=tk.LEFT)
        lbl_danger_desc.grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=5)
        row += 1

        btn_reset = tk.Button(self.tab_focus, text="Reset Prep Tracker Logs", font=("Segoe UI", 10, "bold"), bg="#e84118", fg="white",
                              activebackground="#c23616", activeforeground="white", bd=0, padx=15, pady=6, command=self.reset_workspace_logs)
        btn_reset.grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=10)

    def submit_focus_goal(self):
        new_focus = self.ent_focus_value.get().strip()
        if not new_focus:
            messagebox.showerror("Validation Error", "Focus target cannot be blank!")
            return
            
        # Clean pipes
        new_focus = new_focus.replace("|", "\\|")
        
        content = self.read_readme()
        if not content:
            messagebox.showerror("Error", "README.md not found in the current workspace.")
            return
            
        content = re.sub(r"(\|\s*\*\*Current Focus\*\*\s*\|\s*)(.*?)(\s*\|)", f"\\g<1>{new_focus}\\g<3>", content)
        
        # Re-calc last updated
        content = self.update_dashboard_metrics(content)
        self.write_readme(content)
        
        # Git Commit (always add/commit README when target focus shifts)
        self.handle_git_commit_and_push([README_PATH], f"docs: update placement focus goal to '{new_focus}'", should_push=True)
        
        self.refresh_dashboard()
        messagebox.showinfo("Success", f"Focus target updated successfully to:\n{new_focus}")

    def reset_workspace_logs(self):
        # Double Confirmation
        confirm1 = messagebox.askyesno("⚠️ Confirm Reset - Step 1 of 2", 
            "Are you sure you want to reset all tracker logs?\n\nThis will clear all solved questions, tech notes, and study journal entries in README.md, and reset dashboard statistics back to 0.")
        if not confirm1:
            return
            
        confirm2 = messagebox.askyesno("🚨 Final Warning - Step 2 of 2",
            "This action CANNOT be undone. Are you absolutely sure you want to wipe all logs from README.md clean?")
        if not confirm2:
            return
            
        content = self.read_readme()
        if not content:
            messagebox.showerror("Error", "README.md not found in the current workspace.")
            return
            
        # Clear tables by returning them to empty headers
        # 1. Questions Log
        content = re.sub(
            r"<!-- QUESTIONS_START -->.*?<!-- QUESTIONS_END -->", 
            "<!-- QUESTIONS_START -->\n| Date | Platform | Problem Name & Link | Topic / Pattern | Language | Difficulty | Key Concept / Time Complexity | Code Solution |\n| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n<!-- QUESTIONS_END -->", 
            content, 
            flags=re.DOTALL
        )
        
        # 2. Tech Tracker
        content = re.sub(
            r"<!-- TECH_START -->.*?<!-- TECH_END -->",
            "<!-- TECH_START -->\n| Date | Technology / Domain | Topic / Concept Learned | Resources | Confidence | Key Takeaways |\n| :--- | :--- | :--- | :--- | :--- | :--- |\n<!-- TECH_END -->",
            content,
            flags=re.DOTALL
        )
        
        # 3. Journal
        content = re.sub(
            r"<!-- JOURNAL_START -->.*?<!-- JOURNAL_END -->",
            "<!-- JOURNAL_START -->\n| Date | Time Slot | Category | Activity Description | Focus / Key Takeaway | Next Steps |\n| :--- | :--- | :--- | :--- | :--- | :--- |\n<!-- JOURNAL_END -->",
            content,
            flags=re.DOTALL
        )
        
        # Reset Dashboard stats
        content = self.update_dashboard_metrics(content)
        self.write_readme(content)
        
        # Commit & Push changes to github
        self.handle_git_commit_and_push([README_PATH], "chore: reset placement prep tracker logs and statistics", should_push=True)
        
        self.refresh_dashboard()
        messagebox.showinfo("Success", "Workspace logs reset successfully! Ready for a fresh start! 🚀")

    def toggle_study_session(self):
        if not self.session_active:
            self.session_active = True
            self.session_start_dt = datetime.now()
            self.session_questions_solved = []
            
            self.btn_session_toggle.configure(text="Stop Study Session", bg="#e84118", activebackground="#c23616")
            self.lbl_track_status.configure(text="Studying...", fg="#e1b12c")
            
            self.update_stopwatch()
        else:
            self.session_active = False
            
            self.btn_session_toggle.configure(text="Start Study Session", bg="#4cd137", activebackground="#44bd32")
            self.lbl_track_status.configure(text="Status: Idle", fg="#7f8c8d")
            self.lbl_stopwatch.configure(text="00:00:00")
            
            self.handle_session_stop()

    def update_stopwatch(self):
        if self.session_active:
            elapsed = datetime.now() - self.session_start_dt
            secs = int(elapsed.total_seconds())
            hours, remainder = divmod(secs, 3600)
            minutes, seconds = divmod(remainder, 60)
            time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            self.lbl_stopwatch.configure(text=time_str)
            
            self.root.after(1000, self.update_stopwatch)

    def handle_session_stop(self):
        end_dt = datetime.now()
        duration = end_dt - self.session_start_dt
        
        # Ignore sessions shorter than 10 seconds to avoid accidental clicks
        if duration.total_seconds() < 10:
            messagebox.showinfo("Session Cancelled", "Study session was too short to log.")
            return
            
        date = self.session_start_dt.strftime("%Y-%m-%d")
        time_slot = f"{self.session_start_dt.strftime('%I:%M %p')} - {end_dt.strftime('%I:%M %p')}"
        
        category = "DSA"
        if self.session_questions_solved:
            desc = f"Solved: {', '.join(self.session_questions_solved)}"
            category = "DSA"
        else:
            desc = "Self study session"
            category = "DSA"
                
        SessionSummaryDialog(self.root, date, time_slot, category, desc, self.save_session_log)

    def save_session_log(self, date, time_slot, category, desc, takeaway, next_steps, should_git):
        new_row = f"| {date} | {time_slot} | {category} | {desc} | {takeaway} | {next_steps} |"
        
        content = self.read_readme()
        if not content:
            messagebox.showerror("Error", "README.md not found in the current workspace.")
            return
            
        lines = self.parse_markdown_table(content, "<!-- JOURNAL_START -->", "<!-- JOURNAL_END -->")
        lines.append(new_row)
        
        new_table_str = "<!-- JOURNAL_START -->\n" + "\n".join(lines) + "\n<!-- JOURNAL_END -->"
        content = re.sub(r"<!-- JOURNAL_START -->.*?<!-- JOURNAL_END -->", new_table_str, content, flags=re.DOTALL)
        
        content = self.update_dashboard_metrics(content)
        self.write_readme(content)
        
        commit_success = True
        if should_git:
            commit_msg = f"docs: log study session on {category} via auto-tracker"
            commit_success = self.handle_git_commit_and_push([README_PATH], commit_msg, should_push=True)
            
        self.refresh_dashboard()
        
        msg = "Study session successfully saved to your journal!"
        if should_git and commit_success:
            msg += "\nChanges committed and pushed to GitHub!"
        messagebox.showinfo("Success", msg)

class SessionSummaryDialog(tk.Toplevel):
    def __init__(self, parent, date, time_slot, category, desc, save_callback):
        super().__init__(parent)
        self.title("Study Session Summary")
        self.geometry("500x380")
        self.resizable(False, False)
        self.configure(bg="#f5f6fa")
        self.transient(parent)
        self.grab_set()
        
        self.save_callback = save_callback
        
        self.columnconfigure(1, weight=1)
        
        ttk.Label(self, text="📝 Study Session Logged", font=("Segoe UI", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=15, padx=15, sticky=tk.W)
        
        ttk.Label(self, text="Date:").grid(row=1, column=0, padx=15, pady=5, sticky=tk.W)
        self.ent_date = ttk.Entry(self, width=30)
        self.ent_date.insert(0, date)
        self.ent_date.grid(row=1, column=1, padx=15, pady=5, sticky=tk.EW)
        
        ttk.Label(self, text="Time Slot:").grid(row=2, column=0, padx=15, pady=5, sticky=tk.W)
        self.ent_time = ttk.Entry(self, width=30)
        self.ent_time.insert(0, time_slot)
        self.ent_time.grid(row=2, column=1, padx=15, pady=5, sticky=tk.EW)
        
        ttk.Label(self, text="Category:").grid(row=3, column=0, padx=15, pady=5, sticky=tk.W)
        self.cmb_cat = ttk.Combobox(self, values=["DSA", "Development", "Core CS", "Aptitude", "Mock Interview", "Other"], width=28)
        self.cmb_cat.set(category)
        self.cmb_cat.grid(row=3, column=1, padx=15, pady=5, sticky=tk.EW)
        
        ttk.Label(self, text="Description:").grid(row=4, column=0, padx=15, pady=5, sticky=tk.W)
        self.ent_desc = ttk.Entry(self, width=30)
        self.ent_desc.insert(0, desc)
        self.ent_desc.grid(row=4, column=1, padx=15, pady=5, sticky=tk.EW)
        
        ttk.Label(self, text="Takeaway:").grid(row=5, column=0, padx=15, pady=5, sticky=tk.W)
        self.ent_takeaway = ttk.Entry(self, width=30)
        self.ent_takeaway.insert(0, "")
        self.ent_takeaway.grid(row=5, column=1, padx=15, pady=5, sticky=tk.EW)
        
        ttk.Label(self, text="Next Steps:").grid(row=6, column=0, padx=15, pady=5, sticky=tk.W)
        self.ent_next = ttk.Entry(self, width=30)
        self.ent_next.grid(row=6, column=1, padx=15, pady=5, sticky=tk.EW)
        
        self.var_git = tk.BooleanVar(value=True)
        self.chk_git = ttk.Checkbutton(self, text="Auto Git Commit & Push to GitHub", variable=self.var_git)
        self.chk_git.grid(row=7, column=1, padx=15, pady=10, sticky=tk.W)
        
        btn_frame = ttk.Frame(self)
        btn_frame.grid(row=8, column=0, columnspan=2, pady=15, padx=15, sticky=tk.E)
        
        btn_cancel = tk.Button(btn_frame, text="Discard", bg="#dcdde1", fg="#2f3640", bd=0, padx=12, pady=5, command=self.destroy)
        btn_cancel.pack(side=tk.RIGHT, padx=5)
        
        btn_save = tk.Button(btn_frame, text="Log to Journal", bg="#4cd137", fg="white", bd=0, padx=15, pady=5, command=self.on_save)
        btn_save.pack(side=tk.RIGHT, padx=5)

    def on_save(self):
        date = self.ent_date.get().strip()
        time_slot = self.ent_time.get().strip()
        category = self.cmb_cat.get().strip()
        desc = self.ent_desc.get().strip()
        takeaway = self.ent_takeaway.get().strip()
        next_steps = self.ent_next.get().strip()
        should_git = self.var_git.get()
        
        if not desc:
            messagebox.showerror("Error", "Description is required!")
            return
            
        self.save_callback(date, time_slot, category, desc, takeaway, next_steps, should_git)
        self.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = PlacementPrepGUI(root)
    root.mainloop()
