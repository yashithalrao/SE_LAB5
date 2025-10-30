REFLECTIONS:
1. Which issues were easiest and hardest to fix?
Easiest: Formatting issues like long lines and missing docstrings, Ie comments and all because they only required quick edits.
Hardest: Logic and security issues (removing eval(), fixing the mutable default argument, replacing the bare except) because they needed actual code changes and understanding side effects.


2. Any false positives?
Pylint warned about the global keyword even though it was required to load data correctly. I kept the global and just added a justification comment.
3. How to use static analysis in real development?
Run tools locally before committing
Add Pylint, Flake8, and Bandit to CI so every push/PR is automatically checked


4. Improvements observed?
Code is safer (eval removed, proper validation)
No silent errors
Cleaner and easier to understand
Fully passes tools (Pylint 10/10)
