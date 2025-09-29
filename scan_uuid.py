import asyncio
from bleak import BleakClient

BOOST_MAC = "1A:2B:3C:4D:5E:6F" # Replace with real mac id of boost

async def scan_services():
    async with BleakClient(BOOST_MAC) as client:
        if client.is_connected:
            print("✅ Connected, discovering services...")
            for service in client.services:
                print(f"Service: {service.uuid}")
                for char in service.characteristics:
                    print(f"  Char: {char.uuid} - {char.properties}")

asyncio.run(scan_services())
