import os

# --- CONFIGURATION ---
BOOTLOADER_BIN = "bootloader.bin"
APP1_BIN       = "app1_LED.bin"
APP2_BIN       = "app2_LED.bin"
OUTPUT_FILE    = "Master_Factory_Image.bin"

# Memory Offsets (Must match your Linker Scripts!)
# Bootloader is at 0x0800 0000 (Offset 0)
APP1_OFFSET    = 0x020000  # 0x0802 0000 - 0x0800 0000 = 128KB
APP2_OFFSET    = 0x100000  # 0x0810 0000 - 0x0800 0000 = 1MB

def merge_binaries():
    # 1. Read the input files
    try:
        with open(BOOTLOADER_BIN, 'rb') as f:
            boot_data = f.read()
        with open(APP1_BIN, 'rb') as f:
            app1_data = f.read()
        with open(APP2_BIN, 'rb') as f:
            app2_data = f.read()
            
        print(f"Read {len(boot_data)} bytes from Bootloader")
        print(f"Read {len(app1_data)} bytes from App1")
        print(f"Read {len(app2_data)} bytes from App2")

    except FileNotFoundError as e:
        print(f"Error: {e}")
        return

    # 2. Calculate total size needed (End of App2)
    total_size = APP2_OFFSET + len(app2_data)
    
    # 3. Create a buffer filled with 0xFF (Erased Flash state)
    # Using 0xFF is crucial so we don't accidentally lock flash bits or slow down writing
    master_buffer = bytearray([0xFF] * total_size)

    # 4. Insert Bootloader at 0x00
    master_buffer[0:len(boot_data)] = boot_data

    # 5. Insert App 1 at 0x20000
    if len(boot_data) > APP1_OFFSET:
        print("Error: Bootloader is too big! It overlaps App 1.")
        return
    master_buffer[APP1_OFFSET:APP1_OFFSET+len(app1_data)] = app1_data

    # 6. Insert App 2 at 0x100000
    # Note: App 1 shouldn't be larger than (APP2_OFFSET - APP1_OFFSET)
    if (APP1_OFFSET + len(app1_data)) > APP2_OFFSET:
        print("Error: App 1 is too big! It overlaps App 2.")
        return
    master_buffer[APP2_OFFSET:APP2_OFFSET+len(app2_data)] = app2_data

    # 7. Write the output
    with open(OUTPUT_FILE, 'wb') as f:
        f.write(master_buffer)
        
    print(f"\nSuccess! Generated {OUTPUT_FILE}")
    print(f"Total Size: {len(master_buffer) / 1024:.2f} KB")

if __name__ == "__main__":
    merge_binaries()