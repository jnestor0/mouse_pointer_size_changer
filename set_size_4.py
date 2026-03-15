import winreg
import ctypes

# Update accessibility preference (slider position)
key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Accessibility", 0, winreg.KEY_SET_VALUE)
winreg.SetValueEx(key, "CursorSize", 0, winreg.REG_DWORD, 4)
winreg.CloseKey(key)

# Update the actual cursor base size that SPI_SETCURSORS reads
# Windows maps size 1-15 to CursorBaseSize 32-128: round(32 + (size-1)*96/14)
# Size 4 -> 53
key2 = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Control Panel\Cursors", 0, winreg.KEY_SET_VALUE)
winreg.SetValueEx(key2, "CursorBaseSize", 0, winreg.REG_DWORD, 53)
winreg.CloseKey(key2)

# Reload cursors and broadcast the change to all windows
SPI_SETCURSORS = 0x0057
SPIF_UPDATEINIFILE = 0x01
SPIF_SENDCHANGE = 0x02
ctypes.windll.user32.SystemParametersInfoW(SPI_SETCURSORS, 0, None, SPIF_UPDATEINIFILE | SPIF_SENDCHANGE)

# Windows 10/11 Accessibility Cursor Scale (Undocumented API)
# This is explicitly required on modern Windows to scale the cursor visually
SPI_SETCURSORSIZE = 0x2029
ctypes.windll.user32.SystemParametersInfoW(SPI_SETCURSORSIZE, 0, 53, SPIF_UPDATEINIFILE | SPIF_SENDCHANGE)
