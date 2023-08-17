#! /usr/bin/env python
'''
@Author: xiaobaiTser
@email : 807447312@qq.com
@Time  : 2023/7/4 21:14
@File  : MonitorCANBUS.py
'''

import can

# 定义CAN总线参数
can_interface = 'can0'  # CAN接口名称
can_bitrate = 500000  # CAN总线波特率

# 创建CAN总线对象
bus = can.interface.Bus(channel=can_interface, bitrate=can_bitrate)


# 获取整车所有ECU的ID
def get_all_ecu_ids():
    ecu_ids = set()  # 使用集合来存储唯一的ECU ID

    # 接收CAN总线上的所有帧
    for message in bus:
        ecu_id = message.arbitration_id

        # 将ECU ID添加到集合中
        ecu_ids.add(ecu_id)

        # 如果已经收集到所有ECU的ID，则退出循环
        if len(ecu_ids) == 255:
            break

    return ecu_ids


# 获取整车所有ECU的数据
def get_all_ecu_data():
    ecu_data = {}  # 使用字典来存每 接收CAN总线上的所有帧
    for message in bus:
        ecu_id = message.arbitration_id

        # 如果是新的ECU ID，则创建一个新的键值对
        if ecu_id not in ecu_data:
            ecu_data[ecu_id] = []

        # 将数据帧添加到对应的ECU数据
        ecu_data[ecu_id].append(message.data)

        # 如果已经收集数据退出
        if len(ecu_data) == 255:
            break

    return ecu_data


# 获取整车所有ECU的ID
all_ecu_ids = get_all_ecu_ids()
print("整车所有ECU的ID：", all_ecu_ids)

# 获取整车所有ECU的数据
all_ecu_data = get_all_ecu_data()
print("整车数据：", all_ecu_data)
