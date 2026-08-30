#!/usr/bin/env python3
"""spawn.py 按派活隔离与彩色事件流的单元测试（干测试，无 API 调用）。

覆盖：
- task_key_of：任务键规范化（去 .md、非法字符替换、空名兜底）
- runtime_paths：keyed（.<Role>_<任务名>.*）与 legacy（.<Role>.*）两套命名
- branch_color：确定性哈希着色（跨进程稳定）
- describe_bash：bash 命令文字化（家务命令静默、脚本/知识库/内联分类）
- heartbeat_text：.progress 心跳同套文字化（原始命令不进进度播报）
- agent_event_line：控制台行渲染（bash 命令文字化后上屏、脚本创建上屏、
  workspace 内 md 写入静默、路线颜色标注）
- 即时失败回执：派活前任务文件/角色 prompt 缺失 → 立刻写 BLOCKED .result
  （后台派活的报错被 shell 吞掉，Orchestrator 只认 .result）

运行：python3 scripts/test_spawn_keying.py -v
"""

import os
import subprocess
import sys
import tempfile
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
            "script 执行：run.py")
        self.assertEqual(
            spawn.describe_bash("python3 check.py && echo DONE"),
            "script 执行：check.py")
        self.assertEqual(
            spawn.describe_bash("cd /abs/ws && python3 calc.py"),
            "script 执行：calc.py")

    def test_rag_query(self):
        cmd = ('cd /root/textbook && rag_env/bin/python '
               'rag_build/query_rag.py "查询"')
        self.assertEqual(spawn.describe_bash(cmd), "script 执行：查询知识库")

    def test_inline_python(self):
        self.assertEqual(spawn.describe_bash('python3 -c "print(1)"'),
                         "script 执行：内联 Python")

    def test_bash_script(self):
        self.assertEqual(spawn.describe_bash("bash setup.sh"),
                         "script 执行：setup.sh")

    def test_executable(self):
        self.assertEqual(spawn.describe_bash("./solver --fast"),
                         "script 执行：solver")

    def test_timeout_wrapper_stripped(self):
        """timeout/nohup 等前缀包装器不得伪装成可执行文件上报。"""
        self.assertEqual(
            spawn.describe_bash("timeout 120 python3 scripts/x/run.py 2>&1"),
            "script 执行：run.py")
        self.assertEqual(
            spawn.describe_bash("cd /abs/ws && timeout 900 python3 calc.py"),
            "script 执行：calc.py")
        self.assertIsNone(spawn.describe_bash("timeout 60 cat x.md"))

    def test_untranslatable_suppressed(self):
        self.assertIsNone(spawn.describe_bash("2>&1 weird | stuff"))


class TestHeartbeatText(unittest.TestCase):
    """.progress 心跳与上屏行同一套文字化，原始命令不进进度播报。"""

    def test_bash_textified(self):
        self.assertEqual(
            spawn.heartbeat_text("Bash: timeout 120 python3 scripts/x/run.py"),
            "script 执行：run.py")

    def test_bash_housekeeping_generic(self):
        self.assertEqual(spawn.heartbeat_text("Bash: cat debug/.state"),
                         "执行命令")

    def test_write_py(self):
        self.assertEqual(
            spawn.heartbeat_text("Write: /ws/scripts/builder/t/check.py"),
            "写脚本 check.py")

    def test_write_md(self):
        self.assertEqual(
            spawn.heartbeat_text("Write: /ws/calculation_a1.md"),
            "写 calculation_a1.md")

    def test_other_passthrough(self):
        self.assertEqual(spawn.heartbeat_text("Read: /ws/problem.md"),
                         "Read: /ws/problem.md")


class TestAgentEventLine(unittest.TestCase):
    WS = "/abs/ws"

    def test_bash_python_shown(self):
        line = spawn.agent_event_line("Builder", "task_a1",
                                      "Bash: python3 scripts/builder/task_a1/run.py")
        self.assertIn("[Builder·task_a1]", line)
        self.assertIn("script 执行：run.py", line)

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
        self.assertTrue(line.endswith("\033[0m script 执行：run.py"))

    def test_branch_falls_back_to_role(self):
        line = spawn.agent_event_line("Critic", "", "Bash: python3 run.py")
        color = spawn.branch_color("Critic")
        self.assertIn(f"\033[1;{color}m[Critic·]", line)

    def test_cmd_truncated_to_first_line(self):
        line = spawn.agent_event_line("Builder", "t",
                                      "Bash: python3 a.py\necho done")
        self.assertNotIn("echo done", line)


class TestMissingFileReceipt(unittest.TestCase):
    """派活前文件缺失必须立刻写 BLOCKED 回执：后台派活（&）的报错会被
    shell 吞掉，Orchestrator 只认 .result——没有回执它会空转满整个轮询
    周期（I510 实测烧过 9.5 分钟才发现 NOT_STARTED）。"""

    SPAWN = os.path.join(os.path.dirname(os.path.abspath(spawn.__file__)),
                         "spawn.py")

    def setUp(self):
        self.ws = tempfile.mkdtemp(prefix="spawn_fail_ws_")
        os.makedirs(os.path.join(self.ws, "debug"), exist_ok=True)
        os.makedirs(os.path.join(self.ws, "tasks"), exist_ok=True)

    def run_spawn(self, args, extra_env=None):
        env = os.environ.copy()
        env.pop("SOLVER_PIPELINE", None)
        if extra_env:
            env.update(extra_env)
        return subprocess.run([sys.executable, self.SPAWN] + args,
                              capture_output=True, text=True, env=env,
                              timeout=120)

    def read(self, rel):
        with open(os.path.join(self.ws, rel), encoding="utf-8") as f:
            return f.read()

    def test_missing_task_writes_blocked_result(self):
        # 未设 SPAWN_RUNTIME_BY_TASK → 旧命名 .<Role>.result
        r = self.run_spawn(["Builder", self.ws, "agents/builder", "task_ghost"])
        self.assertEqual(r.returncode, 1)
        content = self.read("debug/.Builder.result")
        self.assertIn("HANDOFF", content)
        self.assertIn("STATUS: BLOCKED", content)
        self.assertIn("任务文件不存在", content)
        self.assertIn("失败", self.read("console.log"))

    def test_missing_task_keyed_naming(self):
        r = self.run_spawn(["Evaluator", self.ws, "agents/evaluator", "task_x"],
                           extra_env={"SPAWN_RUNTIME_BY_TASK": "1"})
        self.assertEqual(r.returncode, 1)
        self.assertTrue(os.path.exists(
            os.path.join(self.ws, "debug", ".Evaluator_task_x.result")))

    def test_missing_prompt_writes_blocked_result(self):
        with open(os.path.join(self.ws, "tasks", "task_y.md"), "w",
                  encoding="utf-8") as f:
            f.write("# t\n")
        r = self.run_spawn(["Builder", self.ws, "agents/no_such_prompt", "task_y"])
        self.assertEqual(r.returncode, 1)
        content = self.read("debug/.Builder.result")
        self.assertIn("角色 prompt 不存在", content)


if __name__ == "__main__":
    unittest.main(verbosity=2)
