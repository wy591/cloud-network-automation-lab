云网络自动化运维平台 - 详细实施步骤
阶段一：底层网络环境搭建（EVE-NG）
🔹 步骤 1：搭建仿真拓扑

操作：在 EVE-NG 中创建实验，拖入 2 台华为 CE12800 交换机和 1 台 AR1000v 路由器，连接一个 Cloud 节点桥接到宿主机。

拓扑结构：CE1 (GE1/0/1) ↔ Cloud；CE1 (GE1/0/0) ↔ AR (G0/0/0)；CE2 (GE1/0/0) ↔ AR (G0/0/1)。

产出：EVE-NG 拓扑图


🔹 步骤 2：配置基础网络与路由

操作：给 CE1、CE2、AR 配置管理 IP 和互联 IP，并开启 OSPF，实现全网互通。

关键配置：

CE1 管理 IP：192.168.14.20/24（连接 Cloud）。

CE2 管理 IP：192.168.14.30/32（配置在 LoopBack0 上）。

AR 管理 IP：192.168.14.40/32（配置在 LoopBack0 上）。

产出：宿主机能 ping 通三台设备，全网路由打通。

🔹 步骤 3：配置设备 Telnet 登录

操作：由于 Ansible 和 Python 脚本需要远程连接，配置 VTY 使用密码认证，并赋予最高权限（注：该 CE 镜像最高用 3 级即可执行所有命令）。

关键命令：

bash
user-interface vty 0 4
authentication-mode password
set authentication password cipher Huawei@123
user privilege level 3
protocol inbound telnet
产出：宿主机可以通过 telnet 192.168.14.20 直接登录设备。

阶段二：CMDB 数据建模（NetBox）
🔹 步骤 4：部署 NetBox 系统

操作：在 Ubuntu 虚拟机上使用 Docker Compose 部署 NetBox（包含 PostgreSQL 和 Redis）。

创建文件：docker-compose.override.yml（配置端口映射为 8000）。

产出：浏览器能访问 http://192.168.14.130:8000/，NetBox 首页正常显示。

🔹 步骤 5：录入网络“通讯录”

操作：在 NetBox 中依次创建数据字典：站点（EVE-NG-Lab）、厂商（Huawei）、设备型号（CE12800/AR1000v）、设备角色（Core-Switch/Router）。

操作：录入三台设备，并在设备下创建接口（GE1/0/1 等），将管理 IP 绑定到接口，并勾选“设为首选 IP”。

产出：NetBox 设备列表展示了 3 台设备及对应的管理 IP（截图保存在 screenshots/netbox-devices.png）。

🔹 步骤 6：生成 API Token

操作：在 NetBox 个人资料中创建 API Token，用于后续自动化读取数据。

产出：获取到 nbt_cMP... 开头的 Token（已保存，后续用于测试 API 读取）。

阶段三：自动化配置下发（Python 脚本）
🔹 步骤 7：编写自动化配置脚本

操作：由于环境网络限制导致 Ansible 插件加载失败，改用原生 Python 的 telnetlib 库实现自动化。

创建文件：automation/batch_config.py。

脚本逻辑：

读取设备 IP 列表（后续可扩展为从 NetBox API 动态读取）。
依次 Telnet 登录设备。
输入密码 Huawei@123。
进入系统视图 system-view。
批量下发 vlan 100 和 vlan 200。
保存配置 save。
🔹 步骤 8：执行自动化并验证

操作：在宿主机运行 python3 batch_config.py。

产出：终端输出“配置成功！”，登录 CE1/CE2 使用 display vlan 能看到 VLAN 100 和 200 已被创建（截图保存在 screenshots/vlan-result.png）。

实现效果：将原本需要 10 分钟的手动配置缩短为 5 秒的自动化脚本执行。
