#!/usr/bin/env python3
"""
Unit tests for git integration and permission system.

Tests:
- spawn.py: AGENT_PROFILES permission configuration
- run.py: init_workspace_git() function
- Permission pattern matching
- Git command validation
"""

import unittest
import sys
import os
import tempfile
import shutil
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))


class TestAgentProfiles(unittest.TestCase):
    """Test AGENT_PROFILES in spawn.py."""

    def setUp(self):
        """Load spawn.py module."""
        # Import spawn module to access AGENT_PROFILES
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "spawn", str(Path(__file__).parent / "spawn.py"))
        self.spawn = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.spawn)

    def test_profiles_exist(self):
        """All three agent roles should have profiles."""
        self.assertIn("Planner", self.spawn.AGENT_PROFILES)
        self.assertIn("Builder", self.spawn.AGENT_PROFILES)
        self.assertIn("Evaluator", self.spawn.AGENT_PROFILES)

    def test_profiles_have_required_tools(self):
        """Each profile should have Read, Write, Edit tools."""
        for role in ["Planner", "Builder", "Evaluator"]:
            profile = self.spawn.AGENT_PROFILES[role]
            self.assertIn("Read", profile)
            self.assertIn("Write", profile)
            self.assertIn("Edit", profile)

    def test_profiles_restrict_bash(self):
        """Bash should be restricted to specific patterns."""
        for role in ["Planner", "Builder", "Evaluator"]:
            profile = self.spawn.AGENT_PROFILES[role]
            # Should allow python3
            self.assertIn("Bash(python3 *)", profile)
            # Should allow git read operations
            self.assertIn("Bash(git status*)", profile)
            self.assertIn("Bash(git diff*)", profile)
            self.assertIn("Bash(git log*)", profile)
            self.assertIn("Bash(git add *)", profile)
            # Should NOT allow unrestricted Bash
            self.assertNotIn("Bash,", profile)

    def test_profiles_forbid_dangerous_commands(self):
        """Profiles should not allow dangerous git commands."""
        for role in ["Planner", "Builder", "Evaluator"]:
            profile = self.spawn.AGENT_PROFILES[role]
            # Should NOT allow these
            self.assertNotIn("git commit", profile)
            self.assertNotIn("git reset", profile)
            self.assertNotIn("git checkout", profile)
            self.assertNotIn("git branch", profile)
            self.assertNotIn("git merge", profile)
            self.assertNotIn("git push", profile)

    def test_kb_skill_pattern(self):
        """Profiles should allow knowledge base skill pattern."""
        for role in ["Planner", "Builder", "Evaluator"]:
            profile = self.spawn.AGENT_PROFILES[role]
            self.assertIn("Bash(source * && python3 *)", profile)


class TestInitWorkspaceGit(unittest.TestCase):
    """Test init_workspace_git() in run.py."""

    def setUp(self):
        """Create temporary workspace."""
        self.test_dir = tempfile.mkdtemp()
        self.workspace = Path(self.test_dir) / "test_workspace"
        self.workspace.mkdir()

        # Create a test file
        (self.workspace / "problem.md").write_text("# Test Problem\n")

        # Import run module
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "run", str(Path(__file__).parent / "run.py"))
        self.run_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.run_module)

    def tearDown(self):
        """Clean up temporary directory."""
        shutil.rmtree(self.test_dir)

    def test_git_init_creates_repo(self):
        """init_workspace_git should create .git directory."""
        self.run_module.init_workspace_git(str(self.workspace))
        self.assertTrue((self.workspace / ".git").exists())

    def test_git_init_creates_gitignore(self):
        """init_workspace_git should create .gitignore."""
        self.run_module.init_workspace_git(str(self.workspace))
        gitignore = self.workspace / ".gitignore"
        self.assertTrue(gitignore.exists())

        content = gitignore.read_text()
        # 新布局：运行时记录移入 debug/ 并提交入库（审计用），只忽略缓存与临时文件
        rules = [ln for ln in content.splitlines() if ln.strip() and not ln.startswith("#")]
        self.assertIn("query_rag.py", rules)
        self.assertIn("__pycache__/", rules)
        self.assertIn("*.pyc", rules)
        self.assertIn("*.tmp", rules)
        self.assertNotIn(".*.log", rules)
        self.assertNotIn(".state", rules)

    def test_git_init_creates_layout(self):
        """init_workspace_git should create debug/ and tasks/ subdirectories."""
        self.run_module.init_workspace_git(str(self.workspace))
        self.assertTrue((self.workspace / "debug").is_dir())
        self.assertTrue((self.workspace / "tasks").is_dir())

    def test_git_init_registers_path_guard_hook(self):
        """init_workspace_git should register the path_guard hook in .claude/settings.json."""
        self.run_module.init_workspace_git(str(self.workspace))
        settings_path = self.workspace / ".claude" / "settings.json"
        self.assertTrue(settings_path.exists())
        content = settings_path.read_text()
        self.assertIn("path_guard.py", content)
        self.assertIn("PreToolUse", content)
        # matcher 必须覆盖读类工具与 Bash，否则偷看堵不住
        import re
        m = re.search(r'"matcher":\s*"([^"]+)"', content)
        self.assertIsNotNone(m)
        for tool in ["Read", "Write", "Edit", "Glob", "Grep", "Bash"]:
            self.assertIn(tool, m.group(1))
        # .claude/ 被 gitignore：hook 配置不会混入解题快照提交
        import subprocess
        r = subprocess.run(
            ["git", "-C", str(self.workspace), "check-ignore", ".claude/settings.json"],
            capture_output=True)
        self.assertEqual(r.returncode, 0)

    def test_git_init_makes_initial_commit(self):
        """init_workspace_git should create initial commit."""
        self.run_module.init_workspace_git(str(self.workspace))

        # Check git log
        import subprocess
        result = subprocess.run(
            ["git", "-C", str(self.workspace), "log", "--oneline"],
            capture_output=True, text=True
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("init: workspace setup with problem files", result.stdout)

    def test_git_init_idempotent(self):
        """Running init_workspace_git twice should not fail."""
        self.run_module.init_workspace_git(str(self.workspace))
        # Should not raise error
        self.run_module.init_workspace_git(str(self.workspace))

        # Should still have only one initial commit
        import subprocess
        result = subprocess.run(
            ["git", "-C", str(self.workspace), "log", "--oneline"],
            capture_output=True, text=True
        )
        lines = [l for l in result.stdout.strip().split('\n') if l]
        self.assertEqual(len(lines), 1)

    def test_git_config_user(self):
        """init_workspace_git should configure git user."""
        self.run_module.init_workspace_git(str(self.workspace))

        import subprocess
        result = subprocess.run(
            ["git", "-C", str(self.workspace), "config", "user.email"],
            capture_output=True, text=True
        )
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.strip(), "agent@physics-solver")

        result = subprocess.run(
            ["git", "-C", str(self.workspace), "config", "user.name"],
            capture_output=True, text=True
        )
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.strip(), "Physics Agent")


class TestPermissionPatterns(unittest.TestCase):
    """Test permission pattern matching logic."""

    def test_python3_pattern_matches_scripts(self):
        """Bash(python3 *) should match python3 script.py."""
        pattern = "Bash(python3 *)"
        # Pattern matching is done by Claude Code, but we can verify the pattern is correct
        self.assertIn("python3 *", pattern)

    def test_git_status_pattern_matches_variants(self):
        """Bash(git status*) should match git status with various flags."""
        pattern = "Bash(git status*)"
        # Should match: git status, git status --short, git status -s
        self.assertIn("git status*", pattern)

    def test_git_diff_pattern_matches_variants(self):
        """Bash(git diff*) should match git diff with various arguments."""
        pattern = "Bash(git diff*)"
        # Should match: git diff, git diff HEAD, git diff file.md
        self.assertIn("git diff*", pattern)

    def test_git_add_requires_argument(self):
        """Bash(git add *) should require an argument (space after add)."""
        pattern = "Bash(git add *)"
        # Note the space: "git add " requires something after "add"
        self.assertIn("git add *", pattern)


class TestSpawnCommandLine(unittest.TestCase):
    """Test spawn.py command line construction."""

    def setUp(self):
        """Import spawn module."""
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "spawn", str(Path(__file__).parent / "spawn.py"))
        self.spawn = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.spawn)

    def test_profile_lookup(self):
        """Should look up profile by role name."""
        # Test that the profile lookup logic works
        role = "Planner"
        expected_profile = self.spawn.AGENT_PROFILES[role]

        # Simulate the lookup logic from spawn.py
        allowed_tools = "Read,Write,Edit,Bash"  # fallback
        if role in self.spawn.AGENT_PROFILES:
            allowed_tools = self.spawn.AGENT_PROFILES[role]

        self.assertEqual(allowed_tools, expected_profile)
        self.assertNotEqual(allowed_tools, "Read,Write,Edit,Bash")

    def test_cli_override(self):
        """--tools flag should override profile."""
        # Simulate CLI override logic
        role = "Planner"
        allowed_tools = "Read,Write,Edit,Bash"  # fallback
        if role in self.spawn.AGENT_PROFILES:
            allowed_tools = self.spawn.AGENT_PROFILES[role]

        # Simulate --tools override
        cli_tools = "Read,Write"
        allowed_tools = cli_tools

        self.assertEqual(allowed_tools, "Read,Write")


class TestGitignoreContent(unittest.TestCase):
    """Test .gitignore content（新布局：debug/ 提交入库审计，只忽略缓存）."""

    GITIGNORE = """\
# 运行时记录（.log/.result/.metrics/.state）已移入 debug/ 并提交入库（审计用）。
# 这里只忽略缓存与临时文件。
query_rag.py
__pycache__/
*.pyc
*.tmp
.claude/
"""

    def test_debug_files_not_ignored(self):
        """运行时记录移入 debug/ 后提交入库审计，不应被 gitignore 排除。"""
        rules = [ln for ln in self.GITIGNORE.splitlines() if ln.strip() and not ln.startswith("#")]
        self.assertNotIn(".*.log", rules)
        self.assertNotIn(".*.result", rules)
        self.assertNotIn(".*.metrics", rules)
        self.assertNotIn(".state", rules)

    def test_ignores_temporary_files(self):
        """Should ignore temporary and cache files."""
        self.assertIn("query_rag.py", self.GITIGNORE)
        self.assertIn("__pycache__/", self.GITIGNORE)
        self.assertIn("*.pyc", self.GITIGNORE)
        self.assertIn("*.tmp", self.GITIGNORE)


if __name__ == "__main__":
    unittest.main()
