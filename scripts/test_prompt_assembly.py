#!/usr/bin/env python3
"""Prompt 组装与控制台渲染回归测试（干测试，无 API 调用）。

覆盖：
1. 八条流水线的 Orchestrator prompt 组装：
   - 所有配置占位符（{pipeline}/{workspace}/{timeout_seconds}/...）必须被替换
   - 残留的 {...} 只允许是样板模板里由 Orchestrator/agent/spawn.py 填写的
     字面占位符（白名单），新增残留必须在此登记
2. 语义断言（deep_search v2 架构）：
   - deep_search.md 无"无条件放行"类措辞，含 PLAN: READY / PENDING /
     SUBTASKS / reentry_used，主脑流程不得出现 spawn Planner
   - verifier.md 无"拿不准时给 SOUND"，含"承担证明责任"
   - orchestrator.md 无"无条件放行"
3. 语义断言（auto 架构）：
   - auto.md 含 7 阶段封闭词表、四级难度决策表、长程脚手架键
     （spawn_count/phase_index/escalations_used）、永不放行；无动议机制
   - assessor.md 只评估不求解，四级难度词表
4. run.py 控制台策略：render_tool_lines 只渲染 spawn 派活事件，
   Orchestrator 自己的读写/轮询一律不上屏
5. run.py 自动续跑打转保护：newest_artifact_mtime 忽略框架自写文件
   （console.log/.runtime_seconds/.orchestrator*），真实产出照常计入

运行：python3 scripts/test_prompt_assembly.py -v
"""

import os
import re
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import run  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROMPTS = os.path.join(ROOT, "prompts")

ALL_PIPELINES = ["standard", "parallel", "iterative", "debate",
                 "tree_search", "adaptive", "deep_search", "auto"]

# run.py 组装时必须替换掉的配置占位符——残留即组装 bug
CONFIG_TOKENS = {
    "pipeline", "workspace", "project_root", "pipeline_config",
    "agents_list", "skills", "timeout_seconds", "max_concurrent_problems",
    "max_revisions", "max_iterations", "max_rounds", "num_planners",
    "ephemeral_timeout", "deep_timeout", "max_motions", "max_verify_rounds",
    "max_subtasks", "max_disputes", "max_concurrent_agents", "max_phases",
    "max_spawns", "max_escalations", "max_search_rounds", "max_debate_rounds",
}

# 合法残留：样板模板/agent prompt 里由 Orchestrator 写任务文件时填写、
# 或 spawn.py 在派活时替换（{task}）、或 LaTeX 花括号。新增残留须登记。
INTENTIONAL_TOKENS = {
    "task",                      # spawn.py 派活时替换为任务键
    "n", "N", "i", "k", "m",     # 轮次/编号字面量
    "id", "id2",                 # 任务/节点编号
    "expert_file", "id_namespace", "tree_table",
    "next_motion_id", "next_subtask_id", "subtasks_left",
    "iteration_number",          # explorer.md 假设模板
    "F", "const", "EllipticE", "EllipticF",   # LaTeX 花括号误匹配
}

TOKEN_RE = re.compile(r"\{([A-Za-z_][A-Za-z0-9_]*)\}")


def read_file(*parts):
    with open(os.path.join(*parts), encoding="utf-8") as f:
        return f.read()


class TestPromptAssembly(unittest.TestCase):
    def test_all_pipelines_assemble_cleanly(self):
        ws = os.path.join(tempfile.gettempdir(), "assembly_probe_ws")
        for p in ALL_PIPELINES:
            run.apply_pipeline_config(p)
            prompt = run.assemble_orchestrator_prompt(ws)
            tokens = set(TOKEN_RE.findall(prompt))

            leaked_config = tokens & CONFIG_TOKENS
            self.assertFalse(
                leaked_config,
                f"[{p}] 配置占位符未被替换: {sorted(leaked_config)}")

            unknown = tokens - INTENTIONAL_TOKENS
            self.assertFalse(
                unknown,
                f"[{p}] 出现未登记的残留占位符: {sorted(unknown)}"
                f"（合法字面量请登记进 INTENTIONAL_TOKENS）")

            self.assertIn(f"**Pipeline:** {p}", prompt)
            self.assertIn(ws, prompt)

    def test_task_token_documented_in_orchestrator(self):
        """agent prompt 里的 {task} 由 spawn.py 替换——
        orchestrator.md 必须向 Orchestrator 说明，免得它照抄。"""
        orch = read_file(PROMPTS, "orchestrator.md")
        self.assertIn("{task}", orch)
        self.assertIn("spawn.py", orch)


class TestDeepSearchSemantics(unittest.TestCase):
    def setUp(self):
        self.deep = read_file(PROMPTS, "pipelines", "deep_search.md")
        self.verifier = read_file(PROMPTS, "agents", "verifier.md")
        self.orch = read_file(PROMPTS, "orchestrator.md")

    def test_no_unconditional_pass(self):
        self.assertNotIn("第二次裁决无论是什么都放行", self.deep)
        self.assertNotIn("无条件放行", self.orch)
        # deep_search 的"永不放行"是正面措辞，允许存在
        self.assertIn("永不放行", self.deep)

    def test_routing_markers_present(self):
        for marker in ("PLAN: READY", "PENDING", "SUBTASKS", "reentry_used"):
            self.assertIn(marker, self.deep)

    def test_no_planner_mastermind(self):
        """主脑流程不得再 spawn Planner；仅子任务三连样板允许 agents/planner。"""
        self.assertNotIn("agents/planner_deep", self.deep)
        # spawn.py Planner 只应出现在子问题增援三连（agents/planner）
        for m in re.finditer(r"spawn\.py\s+Planner\b", self.deep):
            ctx = self.deep[m.start():m.start() + 120]
            self.assertIn("agents/planner", ctx,
                          f"疑似主脑 Planner 派活: {ctx!r}")

    def test_verifier_kill_power(self):
        self.assertNotIn("拿不准时给 SOUND", self.verifier)
        self.assertIn("承担证明责任", self.verifier)

    def test_parallel_branches_allowed(self):
        """运行时文件按派活隔离后，跨分支并行必须被允许。"""
        self.assertNotIn("各分支严格顺序处理", self.deep)
        self.assertIn("跨分支可以并行", self.deep)


class TestAutoSemantics(unittest.TestCase):
    """auto 流水线：封闭阶段词表 + 决策表 + 长程脚手架的骨架完整性。"""

    def setUp(self):
        self.auto = read_file(PROMPTS, "pipelines", "auto.md")
        self.assessor = read_file(PROMPTS, "agents", "assessor.md")

    def test_phase_vocabulary_complete(self):
        for phase in ("plan", "diverge", "search", "debate",
                      "synthesize", "gate", "final"):
            self.assertIn(f"`{phase}`", self.auto)

    def test_decision_table_levels(self):
        for lv in ("EASY", "MEDIUM", "HARD", "FRONTIER"):
            self.assertIn(lv, self.auto)
            self.assertIn(lv, self.assessor)

    def test_scaffolding_keys(self):
        for key in ("spawn_count", "phase_index", "escalations_used",
                    "auto_plan.md", "强制收尾", "检查点纪律"):
            self.assertIn(key, self.auto)

    def test_no_motions_in_auto(self):
        self.assertNotIn("task_motion", self.auto)

    def test_verifier_never_passes_in_auto(self):
        self.assertIn("永不放行", self.auto)

    def test_assessor_no_solving(self):
        self.assertIn("只评估，不求解", self.assessor)

    def test_debate_requires_expert_phases(self):
        """debate 的对象是专家分析文件，必须由 diverge/search 先产生。"""
        self.assertIn("`debate` 必须在 `diverge` 或 `search` 之后", self.auto)


class TestTaskKeyedNaming(unittest.TestCase):
    """所有面向调度者的文档必须使用按派活隔离的运行时文件命名。"""

    def test_orchestrator_uses_task_keyed_result(self):
        orch = read_file(PROMPTS, "orchestrator.md")
        self.assertIn(".<Role>_<任务名>.result", orch)

    def test_pipelines_no_role_keyed_result(self):
        # 除刻意保留的历史说明外，流水线模板不得再引用 .<Role>.result
        legacy = re.compile(r"debug/\.[A-Z][A-Za-z-]*\.result")
        for fn in os.listdir(os.path.join(PROMPTS, "pipelines")):
            text = read_file(PROMPTS, "pipelines", fn)
            hits = legacy.findall(text)
            self.assertFalse(hits, f"{fn} 仍含旧命名: {hits}")

    def test_agent_contracts_task_keyed(self):
        agents_dir = os.path.join(PROMPTS, "agents")
        legacy = re.compile(r"写入\s*[`\s]*\.?\{?Role\}?\.result|\.Verifier\.result")
        for fn in os.listdir(agents_dir):
            text = read_file(agents_dir, fn)
            self.assertFalse(legacy.search(text),
                             f"agents/{fn} 仍含旧契约行")
            self.assertIn("_<任务名>.result", text)


class TestConsoleRender(unittest.TestCase):
    """run.py 控制台策略：只有 sub-Agent 派活事件上屏。"""

    def setUp(self):
        self.ws = tempfile.mkdtemp(prefix="render_ws_")
        os.makedirs(os.path.join(self.ws, "tasks"), exist_ok=True)
        with open(os.path.join(self.ws, "tasks", "task_a1.md"),
                  "w", encoding="utf-8") as f:
            f.write("# Task a1\n说明：验证能量本征值的第一条路线\n")

    def render(self, name, inp):
        return run.render_tool_lines(name, inp, self.ws)
    def test_spawn_event_rendered_with_note(self):
        cmd = (f"python3 {ROOT}/scripts/spawn.py Builder {self.ws} "
               f"agents/builder task_a1 &\necho SPAWNED")
        lines = self.render("Bash", {"command": cmd})
        self.assertEqual(len(lines), 1)
        who, action = lines[0]
        self.assertTrue(who.startswith("Builder"))
        self.assertIn("task_a1", action)
        self.assertIn("验证能量本征值的第一条路线", action)

    def test_parallel_dispatch_all_roles_rendered(self):
        cmd = "\n".join([
            f"python3 {ROOT}/scripts/spawn.py Builder {self.ws} "
            f"agents/builder task_a1 &",
            f"python3 {ROOT}/scripts/spawn.py Builder {self.ws} "
            f"agents/builder task_a2 &",
            f"python3 {ROOT}/scripts/spawn.py Evaluator {self.ws} "
            f"agents/evaluator task_eval_a1 &",
        ])
        lines = self.render("Bash", {"command": cmd})
        self.assertEqual(len(lines), 3)

    def test_poll_loop_silenced(self):
        cmd = 'for i in $(seq 1 38); do sleep 15; done; echo ok'
        self.assertEqual(self.render("Bash", {"command": cmd}), [])

    def test_read_write_state_silenced(self):
        self.assertEqual(self.render("Read", {"file_path": f"{self.ws}/debug/.state"}), [])
        self.assertEqual(self.render("Write", {"file_path": f"{self.ws}/debug/.state",
                                               "content": "x"}), [])
        self.assertEqual(self.render("Edit", {"file_path": f"{self.ws}/tasks/task_x.md"}), [])

    def test_non_spawn_bash_silenced(self):
        self.assertEqual(self.render("Bash", {"command": "head -1 review.md"}), [])


class TestAutoResumeSpinGuard(unittest.TestCase):
    """自动续跑打转保护：newest_artifact_mtime 必须忽略运行框架自己写的文件
    （console.log / .runtime_seconds / .orchestrator*），否则零产出的续跑
    也会被误判为"有进展"，防打转机制失效。"""

    def setUp(self):
        self.ws = tempfile.mkdtemp(prefix="spin_ws_")
        os.makedirs(os.path.join(self.ws, "debug"), exist_ok=True)
        os.makedirs(os.path.join(self.ws, "tasks"), exist_ok=True)

    def touch(self, rel, content="x"):
        p = os.path.join(self.ws, rel)
        with open(p, "w", encoding="utf-8") as f:
            f.write(content)
        return p

    def test_self_written_files_excluded(self):
        self.touch("console.log", "[init]\n")
        self.touch("debug/.runtime_seconds", "123")
        self.touch("debug/.orchestrator_session", "sid")
        self.touch("debug/.orchestrator.log", "log")
        self.assertEqual(run.newest_artifact_mtime(self.ws), 0.0)

    def test_real_artifact_counted(self):
        self.touch("console.log")
        self.touch("debug/.runtime_seconds", "1")
        p = self.touch("debug/.Builder_task_a1.result", "HANDOFF")
        self.assertEqual(run.newest_artifact_mtime(self.ws),
                         os.path.getmtime(p))


if __name__ == "__main__":
    unittest.main(verbosity=2)
