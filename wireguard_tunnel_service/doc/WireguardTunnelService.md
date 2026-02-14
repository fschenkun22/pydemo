## WireGuard Tunnel Service 开发文档（Windows + Python + uv）

## 1. 可行性评估
结论：可行，且可以按分阶段方式稳定落地。

可行性依据：
- Windows 平台可通过 WireGuard CLI 或 Windows Service 状态获取隧道运行状态。
- Python 可实现周期性健康检查、自动重连、日志记录、配置管理、UI 与系统托盘。
- 可使用 `uv` 进行依赖与环境管理，使用 `PyInstaller` 打包为 `exe`。
- 技术风险主要在“健康检查标准定义”和“重连策略误判”，可通过明确规则与测试规避。

## 2. 项目目标
构建一个 Windows 下的 WireGuard 隧道健康检查服务，具备：
1. 周期检测隧道状态。
2. 异常时自动重连。
3. 连接/断开历史与原因记录。
4. 检查周期、重试次数等参数可配置。
5. 图形界面 + 系统托盘驻留，便于实时查看与管理。
6. 最终产物为可执行 `exe`。

## 3. 范围定义
本期（MVP）包含：
- 单隧道监控与重连。
- 本地配置文件读写。
- 本地日志与历史记录展示。
- 托盘运行（最小化到托盘、托盘菜单操作）。
- 打包发布（Windows x64）。

后续可扩展（非 MVP）：
- 多隧道管理。
- 通知（Windows Toast、邮件、Webhook）。
- 远程状态上报与集中管理。

## 4. 技术选型
- Python: `3.12`（建议）
- 环境与依赖管理: `uv`
- UI: `PySide6`（含系统托盘支持）
- 调度与并发: `asyncio` + `qasync`（或 UI/后台线程隔离）
- 日志: `logging` + `RotatingFileHandler`
- 本地历史存储: `SQLite`（`sqlite3`）
- 配置管理: `pydantic-settings` + `TOML`
- 打包: `PyInstaller`
- 质量工具: `ruff`、`mypy`、`pytest`

## 5. 架构设计
核心模块建议：
- `core/health_checker.py`
  - 周期执行健康检查。
  - 提供健康判定结果（Healthy/Degraded/Disconnected）。
- `core/wireguard_controller.py`
  - 与 WireGuard/Windows Service 交互（查询、重连、重启）。
- `core/reconnect_policy.py`
  - 重试次数、退避策略、冷却时间控制。
- `core/state_store.py`
  - 保存当前状态与状态变更历史（SQLite）。
- `core/config.py`
  - 加载、校验、保存配置。
- `ui/main_window.py`
  - 主窗口：状态、历史、配置。
- `ui/tray.py`
  - 托盘图标、菜单、快速操作。

建议采用“UI 层”和“业务层”解耦，UI 不直接执行系统命令，只调用服务层接口。

## 6. 健康检查策略（关键）
建议组合判定，降低误判：
1. 隧道进程/服务是否运行。
2. 最近握手时间是否在阈值内（如 120 秒）。
3. 可选连通性探测（对对端内网地址做 ping）。

判定示例：
- `Healthy`: 服务运行 + 最近握手正常。
- `Degraded`: 服务运行但握手超时，触发观测与有限重试。
- `Disconnected`: 服务未运行或连续失败超过阈值，执行重连流程。

## 7. 自动重连策略
- 最大重试次数：`max_retries`（默认 3）。
- 重试间隔：`retry_interval_sec`（默认 10）。
- 指数退避：`10s -> 20s -> 40s`（可配置）。
- 冷却窗口：连续失败后进入冷却（如 5 分钟）避免频繁抖动。
- 所有动作写入日志和历史记录（含失败原因）。
- 运行策略：若检测 URL 连通性失败，先断开隧道；待网络恢复后再按重试策略重连隧道。

常见错误码（当前实现）：
- 服务查询类：`service_not_found`、`service_query_failed`、`service_state_parse_failed`

- 重连类：`reconnect_stop_failed`、`reconnect_stop_timeout`、`reconnect_start_failed`、`reconnect_start_timeout`

## 8. 配置设计（示例）
配置文件建议：`config/settings.toml`

```toml
[wireguard]
tunnel_name = ""
service_name = ""

healthcheck_url = "https://www.cloudflare.com/cdn-cgi/trace"
healthcheck_timeout_sec = 8
ping_target = "10.0.0.1"
enable_ping_check = true

[monitor]
check_interval_sec = 15
max_retries = 3
retry_interval_sec = 10
cooldown_sec = 300

[logging]
level = "INFO"
max_bytes = 1048576
backup_count = 5

[storage]
db_path = "data/state.db"
```

## 9. UI 功能清单
- 实时状态卡片（连接状态、最近握手、最近错误）。
- 历史记录表格（时间、事件、原因、动作结果）。
- 配置面板（隧道选择、检测 URL、检查频率、重试策略）。
- 操作按钮（立即检查、手动重连、打开日志目录）。
- 系统托盘（显示状态、快速重连、显示/隐藏窗口、退出）。

## 10. 工程结构（建议）
```text
wireguard_tunnel_service/
  pyproject.toml
  README.md
  src/wireguard_tunnel_service/
    __init__.py
    main.py
    core/
    ui/
    infra/
  tests/
    unit/
    integration/
  config/
    settings.toml
  scripts/
    build.ps1
  doc/
    WireguardTunnelService.md
```

## 11. 开发计划（里程碑）
1. 初始化工程
   - 用 `uv` 创建项目、依赖、代码规范与测试框架。
2. 实现核心服务
   - 状态检测、重连策略、日志与历史存储。
3. 实现 UI + 托盘
   - 状态展示、配置编辑、托盘交互。
4. 集成测试与稳定性测试
   - 模拟隧道断开、重连失败、配置异常。
5. 打包与发布
   - `PyInstaller` 生成 `exe`，整理发布说明。

## 12. 测试策略
- 单元测试：
  - 健康判定逻辑、重试退避逻辑、配置校验。
- 集成测试：
  - 与 WireGuard 命令交互（可 mock + 实机验证）。
- 稳定性测试：
  - 长时间运行（24h+），观察内存、句柄、日志滚动是否正常。
- 回归测试：
  - 修改策略后验证 UI 展示与状态机行为一致。

## 13. 打包与发布要求
- 使用 `PyInstaller` 生成 `onedir`（首选，问题定位更容易），稳定后可评估 `onefile`。
- 附带默认配置模板与日志目录说明。
- 需要管理员权限的操作需明确提示（首次安装或服务控制）。
- 输出版本号与构建时间，便于问题追踪。

## 14. 风险与应对
- 风险：握手时间判定不稳定。
  - 应对：握手 + ping 双信号判定，避免单点误判。
- 风险：Windows 权限导致服务控制失败。
  - 应对：启动时进行权限检查并给出引导。
- 风险：异常情况下频繁重连影响网络。
  - 应对：退避 + 冷却机制。

## 15. 结论
当前需求完整且可执行，建议按以上里程碑推进。  
下一步可直接进入“工程初始化（uv + 项目骨架 + 基础配置）”。

## 16. 当前可用启动命令
- 后台服务模式（无 UI）：`uv run wireguard-tunnel-service`
- 桌面 UI + 托盘模式：`uv run wireguard-tunnel-ui`



