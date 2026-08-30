#!/usr/bin/env python3
"""spawn.py 按派活隔离与彩色事件流的单元测试（干测试，无 API 调用）。

覆盖：
- task_key_of：任务键规范化（去 .md、非法字符替换、空名兜底）
- runtime_paths：keyed（.<Role>_<任务名>.*）与 legacy（.<Role>.*）两套命名
- branch_color：确定性哈希着色（跨进程稳定）
- describe_bash：bash 命令文字化（家务命令静默、脚本/知识库/内联分类）
- agent_event_line：控制台行渲染（bash 命令文字化后上屏、脚本创建上屏、
  workspace 内 md 写入静默、路线颜色标注）

运行：python3 scripts/test_spawn_keying.py -v
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import spawn  # noqa: E402


class TestTaskKeyOf(unittest.TestCase):
    def test_plain(self):
        self.assertEqual(spawn.task_key_of("tasks/task_a1.md"), "task_a1")

    def test_absolute_path(self):
        self.assertEqual(
            spawn.task_key_of("/abs/ws/tasks/task_final_builder.md"),
            "task_final_builder")

    def test_no_extension(self):
        self.assertEqual(spawn.task_key_of("task_x"), "task_x")

    def test_extension_case_insensitive(self):
        self.assertEqual(spawn.task_key_of("Task_X.MD"), "Task_X")

    def test_illegal_chars_replaced(self):
        self.assertEqual(spawn.task_key_of("weird name (v2).md"),
                         "weird_name__v2_")

    def test_empty_fallback(self):
        self.assertEqual(spawn.task_key_of(".md"), "task")
        self.assertEqual(spawn.task_key_of(""), "task")


class TestRuntimePaths(unittest.TestCase):
    def setUp(self):
        self.debug = "/ws/debug"

    def test_keyed_isolation(self):
        p = spawn.runtime_paths(self.debug, "Builder", "tasks/task_a1.md",
                                keyed=True)
        self.assertEqual(p["result"],
                         "/ws/debug/.Builder_task_a1.result")
        self.assertEqual(p["log"], "/ws/debug/.Builder_task_a1.log")
        self.assertEqual(p["session"], "/ws/debug/.Builder_task_a1.session")
        self.assertEqual(p["progress"], "/ws/debug/.Builder_task_a1.progress")
        self.assertEqual(p["metrics"], "/ws/debug/.Builder_task_a1.metrics")

    def test_two_dispatches_same_role_differ(self):
        p1 = spawn.runtime_paths(self.debug, "Builder", "tasks/task_a1.md",
                                 keyed=True)
        p2 = spawn.runtime_paths(self.debug, "Builder", "tasks/task_a2.md",
                                 keyed=True)
        self.assertNotEqual(p1["result"], p2["result"])

    def test_legacy_mode(self):
        p = spawn.runtime_paths(self.debug, "Builder", "tasks/task_a1.md",
                                keyed=False)
        self.assertEqual(p["result"], "/ws/debug/.Builder.result")
        self.assertEqual(p["progress"], "/ws/debug/.Builder.progress")

    def test_keys_complete(self):
        p = spawn.runtime_paths(self.debug, "Critic", "t.md", keyed=True)
        self.assertEqual(sorted(p), ["log", "metrics", "progress",
                                     "result", "session"])


class TestBranchColor(unittest.TestCase):
    def test_deterministic(self):
        for key in ("task_a1", "task_b2", "Builder", "x" * 100):
            self.assertEqual(spawn.branch_color(key), spawn.branch_color(key))

    def test_in_palette(self):
        for i in range(50):
            c = spawn.branch_color(f"task_{i}")
            self.assertIn(c, spawn.BRANCH_COLORS)

    def test_empty_key(self):
        self.assertIn(spawn.branch_color(""), spawn.BRANCH_COLORS)


class TestDescribeBash(unittest.TestCase):
    def test_housekeeping_returns_none(self):
        for cmd in ("ls tasks/", "cat debug/.state", "head -1 review.md",
                    "tail -3 x", "wc -c f", "grep foo bar", "find . -name x",
                    "echo SPAWNED", "pwd", "git status", "sleep 15",
                    "rm -f old.result", "mkdir -p scripts/builder",
                    "for i in $(seq 1 38); do sleep 15; done",
                    "[ -f x ] && echo ok", "cd tasks",
                    "export FOO=bar", "chmod +x run.py"):
            self.assertIsNone(spawn.describe_bash(cmd),
                              f"housekeeping not silenced: {cmd}")

    def test_python_script(self):
        self.assertEqual(
            spawn.describe_bash("python3 scripts/builder/task_a1/run.py"),
            "运行脚本 run.py")
        self.assertEqual(
            spawn.describe_bash("python3 check.py && echo DONE"),
            "运行脚本 check.py")
        self.assertEqual(
            spawn.describe_bash("cd /abs/ws && python3 calc.py"),
            "运行脚本 calc.py")

    def test_rag_query(self):
        cmd = ('cd /root/textbook && rag_env/bin/python '
               'rag_build/query_rag.py "查询"')
        self.assertEqual(spawn.describe_bash(cmd), "查询知识库")

    def test_inline_python(self):
        self.assertEqual(spawn.describe_bash('python3 -c "print(1)"'),
                         "运行内联 Python")

    def test_bash_script(self):
        self.assertEqual(spawn.describe_bash("bash setup.sh"),
                         "运行脚本 setup.sh")

    def test_executable(self):
        self.assertEqual(spawn.describe_bash("./solver --fast"), "执行 solver")

    def test_fallback(self):
        self.assertTrue(
            spawn.describe_bash("2>&1 weird | stuff").startswith("执行命令"))


class TestAgentEventLine(unittest.TestCase):
    WS = "/abs/ws"

    def test_bash_python_shown(self):
        line = spawn.agent_event_line("Builder", "task_a1",
                                      "Bash: python3 scripts/builder/task_a1/run.py")
        self.assertIn("[Builder·task_a1]", line)
        self.assertIn("运行脚本 run.py", line)

    def test_bash_housekeeping_silenced(self):
        for cmd in ("ls tasks/", "cat debug/.state", "head -1 review.md",
                    "tail -3 x", "wc -c f", "grep foo bar", "find . -name x",
                    "echo SPAWNED", "pwd", "git status"):
            self.assertEqual(
                spawn.agent_event_line("Builder", "t", f"Bash: {cmd}"), "",
                f"housekeeping not silenced: {cmd}")

    def test_write_py_shown_as_script(self):
        line = spawn.agent_event_line("Builder", "task_a1",
                                      "Write: /abs/ws/scripts/builder/task_a1/check.py")
        self.assertIn("脚本 check.py", line)
        self.assertIn("[Builder·task_a1]", line)

    def test_edit_py_shown_as_script(self):
        line = spawn.agent_event_line("Builder", "task_a1",
                                      "Edit: /abs/ws/scripts/builder/task_a1/check.py")
        self.assertIn("脚本 check.py", line)

    def test_write_workspace_md_silenced(self):
        self.assertEqual(
            spawn.agent_event_line(
                "Builder", "task_a1", "Write: /abs/ws/calculation_a1.md",
                workspace_abs=self.WS), "")

    def test_write_outside_workspace_shown(self):
        line = spawn.agent_event_line("Builder", "task_a1",
                                      "Write: /tmp/scratch.txt",
                                      workspace_abs=self.WS)
        self.assertIn("/tmp/scratch.txt", line)

    def test_read_and_other_silenced(self):
        self.assertEqual(
            spawn.agent_event_line("Builder", "t", "Read: /abs/ws/problem.md"), "")
        self.assertEqual(
            spawn.agent_event_line("Builder", "t", "thinking"), "")

    def test_color_annotation_present(self):
        line = spawn.agent_event_line("Builder", "task_a1",
                                      "Bash: python3 run.py")
        color = spawn.branch_color("task_a1")
        self.assertTrue(line.startswith(f"\033[1;{color}m[Builder·task_a1]"))
        self.assertTrue(line.endswith("\033[0m 运行脚本 run.py"))

    def test_branch_falls_back_to_role(self):
        line = spawn.agent_event_line("Critic", "", "Bash: python3 run.py")
        color = spawn.branch_color("Critic")
        self.assertIn(f"\033[1;{color}m[Critic·]", line)

    def test_cmd_truncated_to_first_line(self):
        line = spawn.agent_event_line("Builder", "t",
                                      "Bash: python3 a.py\necho done")
        self.assertNotIn("echo done", line)


if __name__ == "__main__":
    unittest.main(verbosity=2)
