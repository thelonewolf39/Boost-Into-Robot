
import asyncio
from bleak import BleakClient, BleakScanner

# Set the MAC address of your Boost Move Hub
BOOST_MAC = "1A:2B:3C:4D:5E:6F"

async def scan_services_until_found(mac_address: str):
    """
    Continuously scan until the Boost hub is found,
    then connect and list its services and characteristics.
    """
    while True:
        print("🔍 Scanning for Boost hub...")
        devices = await BleakScanner.discover(timeout=5)
        hub_device = next((d for d in devices if d.address.upper() == mac_address.upper()), None)

        if not hub_device:
            print("❌ Hub not found, retrying in 3s...")
            await asyncio.sleep(3)
            continue

        print(f"✅ Found hub at {hub_device.address}, connecting...")
        try:
            async with BleakClient(hub_device) as client:
                if client.is_connected:
                    print("🤝 Connected! Listing services and characteristics...")
                    for service in client.services:
                        print(f"Service: {service.uuid}")
                        for char in service.characteristics:
                            print(f"  Char: {char.uuid} - {char.properties}")
                    return  # Stop after listing
                else:
                    print("❌ Could not stay connected, retrying...")
        except Exception as e:
            print(f"⚠️ Connection error: {e}")
        print("🔄 Retrying scan in 3s...")
        await asyncio.sleep(3)

if __name__ == "__main__":
    asyncio.run(scan_services_until_found(BOOST_MAC))
