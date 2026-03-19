
try:
    print("Importing PyGithub...")
    from github import Github
    print("PyGithub imported successfully.")
    
    print("Initializing Github...")
    g = Github()
    print("Github initialized.")
    
except ImportError as e:
    print(f"IMPORT ERROR: {e}")
except Exception as e:
    print(f"GENERAL ERROR: {e}")
