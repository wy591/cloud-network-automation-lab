import telnetlib
import time

# 待管理的设备 IP 列表（后续可扩展为从 NetBox API 动态获取）
devices = ["192.168.14.20", "192.168.14.30"]

for host in devices:
    print(f"===== 配置 {host} =====")
    try:
        # 建立 Telnet 连接，超时时间 10 秒
        tn = telnetlib.Telnet(host, timeout=10)
        
        # 等待密码提示符并输入密码
        tn.read_until(b"Password:", timeout=5)
        tn.write(b"Huawei@123\n")
        time.sleep(2)
        
        # 进入系统视图
        tn.write(b"system-view\n")
        time.sleep(2)
        
        # 批量创建 VLAN 100 和 200
        tn.write(b"vlan 100\n")
        time.sleep(2)
        tn.write(b"vlan 200\n")
        time.sleep(2)
        
        # 返回用户视图并保存配置
        tn.write(b"return\n")
        time.sleep(1)
        tn.write(b"save\n")
        time.sleep(2)
        tn.write(b"y\n")
        time.sleep(2)
        
        print(f"{host} 配置完成！")
        tn.close()
    except Exception as e:
        print(f"{host} 配置失败: {e}")
