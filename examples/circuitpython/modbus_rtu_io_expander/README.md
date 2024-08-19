# MODBUS RTU (RS485) IO Expander Example Code
This is the example code for using the IRIV IO Controller (IRIV-IOC) as a IO Expander Module. The code is written in CircuitPython and support the following features:
- MODBUS RTU (RS485) Compatible
- 11x Digital Inputs (5 of them can be configured as counter)
- 4x Digital Outpus
- 2x Analog Inputs (0-10V or 0-40mA)

The `source` folder contains the python source code in .py format. While the `bin` folder contains the pre-compiled .mpy files.<br>
Use the .mpy files if you don't want to expose the source code to the end user or you don't want the user to mess around with your code.

## Setting Up
1. Load the IRIV-IOC with the latest CircuitPython Firmware. It can be downloade from [here](https://circuitpython.org/board/cytron_iriv_io_controller/).
2. Connect the IRIV-IOC to the computer via USB-C. A USB drive called `CIRCUITPY` should be showing up.
3. Copy all files in either the `source` or `bin` folder to the CIRCUITPY drive.
4. Reboot the IRIV-IOC. The blue USR LED should be blinking if the code is running correctly.

## MODBUS RTU Configuration
1. Connect the IRIV-IOC to the computer via USB-C. A CIRCUITPY drive should be detected.
2. Edit the `settings.toml` file in the CIRCUITPY drive. You can change the RS485 Baudrate and MODBUS RTU slave ID here.<br>
```
# Baudrate for RS485.
# Maximum baudrate = 115200.
MODBUS_RTU_BAUDRATE = 9600

# MODBUS RTU Slave ID/Address.
# Valid Range = 1 to 247.
MODBUS_RTU_SLAVE_ADDRESS = 1
```
4. Save the file and **reboot**.

## MODBUS RTU Prototcol
### Function Code
| Function Code<br>HEX (DEC) | Description              |
| -------------------------- | ------------------------ |
| 0x01 (01)                  | Read Coils               |
| 0x02 (02)                  | Read Discrete Inputs     |
| 0x03 (03)                  | Read Holding Registers   |
| 0x04 (04)                  | Read Input Registers     |
| 0x05 (05)                  | Write Single Coil        |
| 0x06 (06)                  | Write Single Register    |
| 0x0F (15)                  | Write Multiple Coils     |
| 0x10 (16)                  | Write Multiple Registers |

### Registers Address
#### Digital Inputs:
<table>
  <tr align="center">
    <td><b>Adress<br>HEX (DEC)</b></td>
    <td><b>Description</b></td>
    <td><b>Read/Write</b></td>
    <td><b>Function Code</b></td>
  </tr>
  <tr>
    <td align="center" colspan="4"><b>Digital Inputs</b></td>
  <tr>
    <td>1x0000 (0)</td>
    <td>Digital Input - DI0</td>
    <td rowspan="11" align="center">R</td>
    <td rowspan="11">0x02: Read Discrete Inputs</td>
  </tr>
  <tr>
    <td>1x0001 (1)</td>
    <td>Digital Input - DI1</td>
  </tr>
  <tr>
    <td>1x0002 (2)</td>
    <td>Digital Input - DI2</td>
  </tr>
  <tr>
    <td>1x0003 (3)</td>
    <td>Digital Input - DI3</td>
  </tr>
  <tr>
    <td>1x0004 (4)</td>
    <td>Digital Input - DI4</td>
  </tr>
  <tr>
    <td>1x0005 (5)</td>
    <td>Digital Input - DI5</td>
  </tr>
  <tr>
    <td>1x0006 (6)</td>
    <td>Digital Input - DI6</td>
  </tr>
  <tr>
    <td>1x0007 (7)</td>
    <td>Digital Input - DI7</td>
  </tr>
  <tr>
    <td>1x0008 (8)</td>
    <td>Digital Input - DI8</td>
  </tr>
  <tr>
    <td>1x0009 (9)</td>
    <td>Digital Input - DI9</td>
  </tr>
  <tr>
    <td>1x000A (10)</td>
    <td>Digital Input - DI10</td>
  </tr>
  
  <tr>
    <td align="center" colspan="4"><b>Digital Outputs</b></td>
  <tr>
  <tr>
    <td>0x0100 (256)</td>
    <td>Digital Output - DO0</td>
    <td align="center" rowspan="4">R/W</td>
    <td rowspan="4">0x01: Read Coils<br>0x05: Write Single Coil<br>0x0F: Write Multiple Coils</td>
  </tr>
  <tr>
    <td>0x0101 (257)</td>
    <td>Digital Output - DO1</td>
  </tr>
  <tr>
    <td>0x0102 (258)</td>
    <td>Digital Output - DO2</td>
  </tr>
  <tr>
    <td>0x0103 (259)</td>
    <td>Digital Output - DO3</td>
  </tr>

  <tr>
    <td align="center" colspan="4"><b>Analog Inputs</b><br><i>* Voltage/Current mode must be selected correctly in hardware.</i></td>
  <tr>
  <tr>
    <td>3x0200 (512)</td>
    <td>Analog Input - AN0 (Voltage)<br><i>Range: 0 - 10560 mV</i></td>
    <td align="center" rowspan="4">R</td>
    <td rowspan="4">0x04: Read Input Registers</td>
  </tr>
  <tr>
    <td>3x0201 (513)</td>
    <td>Analog Input - AN1 (Voltage)<br><i>Range: 0 - 10560 mV</i></td>
  </tr>
  <tr>
    <td>3x0210 (528)</td>
    <td>Analog Input - AN0 (Current)<br><i>Range: 0 - 42580 uA</i></td>
  </tr>
  <tr>
    <td>3x0211 (529)</td>
    <td>Analog Input - AN1 (Current)<br><i>Range: 0 - 42580 uA</i></td>
  </tr>

  <tr>
    <td align="center" colspan="4"><b>Pulse Counters (Only available on DI1, DI3, DI5, DI7 and DI9)</b><br>
      <i>* Digital Input for the corresponding channel will be disabled if the counter is enabled.<br>
      * The counter value is 32-bit and it's recommended to read the higher and lower word in one go.</i></td>
  <tr>
  <tr>
    <td>0x0300 (768)</td>
    <td>Counter Enable bit for DI1</td>
    <td align="center" rowspan="10">R/W</td>
    <td rowspan="10">0x01: Read Coils<br>0x05: Write Single Coil<br>0x0F: Write Multiple Coils</td>
  </tr>
  <tr>
    <td>0x0301 (769)</td>
    <td>Counter Enable bit for DI3</td>
  </tr>
  <tr>
    <td>0x0302 (770)</td>
    <td>Counter Enable bit for DI5</td>
  </tr>
  <tr>
    <td>0x0303 (771)</td>
    <td>Counter Enable bit for DI7</td>
  </tr>
  <tr>
    <td>0x0304 (772)</td>
    <td>Counter Enable bit for DI9</td>
  </tr>
  <tr>
    <td>0x0310 (784)</td>
    <td>Counter Reset for DI1</td>
  </tr>
  <tr>
    <td>0x0311 (785)</td>
    <td>Counter Reset for DI3</td>
  </tr>
  <tr>
    <td>0x0312 (786)</td>
    <td>Counter Reset for DI5</td>
  </tr>
  <tr>
    <td>0x0313 (787)</td>
    <td>Counter Reset for DI7</td>
  </tr>
  <tr>
    <td>0x0314 (788)</td>
    <td>Counter Reset for DI9</td>
  </tr>

  <tr>
    <td>3x0400 (1024)</td>
    <td>Counter DI1 Higher Word</td>
    <td align="center" rowspan="10">R</td>
    <td rowspan="10">0x04: Read Input Registers</td>
  </tr>
  <tr>
    <td>3x0401 (1025)</td>
    <td>Counter DI1 Lower Word</td>
  </tr>
  <tr>
    <td>3x0402 (1026)</td>
    <td>Counter DI3 Higher Word</td>
  </tr>
  <tr>
    <td>3x0403 (1027)</td>
    <td>Counter DI3 Lower Word</td>
  </tr>
  <tr>
    <td>3x0404 (1028)</td>
    <td>Counter DI5 Higher Word</td>
  </tr>
  <tr>
    <td>3x0405 (1029)</td>
    <td>Counter DI5 Lower Word</td>
  </tr>
  <tr>
    <td>3x0406 (1030)</td>
    <td>Counter DI7 Higher Word</td>
  </tr>
  <tr>
    <td>3x0407 (1031)</td>
    <td>Counter DI7 Lower Word</td>
  </tr>
  <tr>
    <td>3x0408 (1032)</td>
    <td>Counter DI9 Higher Word</td>
  </tr>
  <tr>
    <td>3x0409 (1033)</td>
    <td>Counter DI9 Lower Word</td>
  </tr>

  <tr>
    <td align="center" colspan="4"><b>MISC</b></td>
  <tr>
  <tr>
    <td>3x0F00 (3840)</td>
    <td>Model Name 1 - Read as 0x494F ("IO")</td>
    <td align="center" rowspan="5">R</td>
    <td rowspan="5">0x04: Read Input Registers</td>
  </tr>
  <tr>
    <td>3x0F01 (3841)</td>
    <td>Model Name 2 - Read as 0x4300 ("C")</td>
  </tr>
  <tr>
    <td>3x0F10 (3856)</td>
    <td>Firmware Version - Major</td>
  </tr>
  <tr>
    <td>3x0F11 (3857)</td>
    <td>Firmware Version - Minor</td>
  </tr>
  <tr>
    <td>3x0F12 (3858)</td>
    <td>Firmware Version - Patch</td>
  </tr>
</table>

