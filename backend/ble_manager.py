import asyncio
from bleak import BleakScanner, BleakClient
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BLEDeviceManager:
    def __init__(self):
        self.devices = {}  # 存储已发现的设备
        self.connected_devices = {}  # 存储已连接的设备
        self.device_data = {}  # 存储设备数据

    async def scan_devices(self, duration=5.0):
        """扫描附近的BLE设备"""
        logger.info("开始扫描BLE设备...")
        devices = await BleakScanner.discover(timeout=duration)
        
        for device in devices:
            if device.name:  # 只记录有名称的设备
                self.devices[device.address] = {
                    'name': device.name,
                    'address': device.address,
                    'rssi': device.rssi
                }
        
        return self.devices

    async def connect_device(self, device_address):
        """连接到特定设备"""
        try:
            client = BleakClient(device_address)
            await client.connect()
            self.connected_devices[device_address] = client
            logger.info(f"已连接到设备: {device_address}")
            return True
        except Exception as e:
            logger.error(f"连接设备失败: {str(e)}")
            return False

    async def read_device_data(self, device_address):
        """读取设备数据"""
        if device_address not in self.connected_devices:
            return None

        client = self.connected_devices[device_address]
        try:
            # 这里的特征值UUID需要根据具体设备类型来确定
            # 以下是一些常见的特征值UUID
            heart_rate_uuid = "00002a37-0000-1000-8000-00805f9b34fb"  # 心率
            battery_uuid = "00002a19-0000-1000-8000-00805f9b34fb"  # 电池电量

            data = {}
            
            try:
                heart_rate = await client.read_gatt_char(heart_rate_uuid)
                data['heart_rate'] = int(heart_rate[1])
            except:
                logger.warning("无法读取心率数据")

            try:
                battery = await client.read_gatt_char(battery_uuid)
                data['battery'] = int(battery[0])
            except:
                logger.warning("无法读取电池电量")

            # 记录数据
            self.device_data[device_address] = {
                'timestamp': datetime.now().isoformat(),
                'data': data
            }

            return data

        except Exception as e:
            logger.error(f"读取设备数据失败: {str(e)}")
            return None

    async def disconnect_device(self, device_address):
        """断开设备连接"""
        if device_address in self.connected_devices:
            client = self.connected_devices[device_address]
            await client.disconnect()
            del self.connected_devices[device_address]
            logger.info(f"已断开设备连接: {device_address}")
            return True
        return False

    def get_device_info(self, device_address):
        """获取设备信息"""
        return self.devices.get(device_address)

    def get_connected_devices(self):
        """获取所有已连接的设备"""
        return list(self.connected_devices.keys())

    def get_device_data_history(self, device_address):
        """获取设备的历史数据"""
        return self.device_data.get(device_address) 