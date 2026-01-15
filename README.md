# STM32H563ZI Dual-Bank Bootloader

This repository contains a custom Bootloader and two sample applications designed for the **STM32H563ZI Nucleo-144** development board. The system utilizes the STM32H5's dual-bank flash memory to store and manage two separate firmware applications.

## 🚀 Features
* **Boot Selection:** Checks the state of the User Button (PC13) at startup.
    * **Button Released:** Jumps to **Application 1** (Bank 1).
    * **Button Pressed:** Jumps to **Application 2** (Bank 2).
* **Console Output:** Prints status and debug messages via USART3 (Virtual COM Port) at 115200 baud.
* **Memory Management:** Implements custom Linker Scripts to carve out specific flash regions for the Bootloader and Applications.
* **Cache Management:** Handles I-Cache invalidation before jumping to ensure stable application startup.

## 🛠 Hardware Used
* **Board:** NUCLEO-H563ZI
* **MCU:** STM32H563ZIT6 (Cortex-M33)
* **Interface:** USB ST-Link (Virtual COM Port on PD8/PD9)

## 💾 Memory Map
The 2MB Flash memory is partitioned as follows. We reserve the first 128KB for the bootloader.

| Component | Flash Bank | Start Address | Size Allocated |
| :--- | :--- | :--- | :--- |
| **Bootloader** | Bank 1 | `0x0800 0000` | 128 KB |
| **Application 1** | Bank 1 | `0x0802 0000` | 896 KB |
| **Application 2** | Bank 2 | `0x0810 0000` | 1024 KB |

## 📂 Project Structure
* **/Bootloader:** The main entry point code that handles logic and jumping.
* **/App1:** A sample application (e.g., Green LED Blink) linked to run from `0x08020000`.
* **/App2:** A secondary application (e.g., Yellow LED Blink) linked to run from `0x08100000`.
* **/Tools:** (Optional) Python scripts to merge binaries into a single production image.

## ⚙️ How to Build & Flash
1.  **Open Projects:** Import all three folders into **STM32CubeIDE**.
2.  **Configuration:** Ensure `Project > Properties > C/C++ Build > Settings > MCU Post build outputs` is set to generate **Binary (.bin)** files for all projects.
3.  **Flash Manually:**
    * Flash **Bootloader** to `0x08000000`.
    * Flash **App 1** to `0x08020000`.
    * Flash **App 2** to `0x08100000`.
4.  **Verify:** Open a Serial Terminal (115200 baud). Reset the board to see the boot messages.

## 📝 Usage
1.  Connect the Nucleo board to your PC via USB (ST-Link).
2.  Open a terminal (Tera Term, PuTTY) on the correct COM port @ 115200.
3.  **Default Boot:** Press the Black Reset button. The Bootloader will load App 1.
4.  **Alternate Boot:** Hold the Blue User Button + Press Reset. The Bootloader will load App 2.

## 👨‍💻 Author
**Rahul Shimpi** *Embedded Systems Engineer / Firmware Developer*
* **Portfolio:** [https://rahulshimpi.netlify.app](https://rahulshimpi.netlify.app)


## ⚠️ Important Notes
* **TrustZone:** This project assumes TZEN=0 (TrustZone Disabled).
* **Vector Table:** Each application must relocate the Vector Table Offset (VTOR) to its start address in `main()` or `SystemInit`.
