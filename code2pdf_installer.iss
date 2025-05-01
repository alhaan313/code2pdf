[Setup]
AppName=Code2PDF
AppVersion=1.0
DefaultDirName={pf}\Code2PDF
DefaultGroupName=Code2PDF
OutputBaseFilename=Code2PDFInstaller
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\code2pdf.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "installers\pandoc-3.6.4-windows-x86_64.msi"; DestDir: "{tmp}"; Flags: deleteafterinstall
Source: "installers\basic-miktex-24.1-x64.exe"; DestDir: "{tmp}"; Flags: deleteafterinstall

[Icons]
Name: "{group}\Code2PDF"; Filename: "{app}\code2pdf.exe"
Name: "{group}\Uninstall Code2PDF"; Filename: "{uninstallexe}"

[Run]
; Install Pandoc silently
Filename: "msiexec.exe"; Parameters: "/i ""{tmp}\pandoc-3.6.4-windows-x86_64.msi"" /quiet"; StatusMsg: "Installing Pandoc..."

; Install MiKTeX silently in unattended mode
Filename: "{tmp}\basic-miktex-24.1-x64.exe"; Parameters: "--unattended"; StatusMsg: "Installing MiKTeX..."

; Small delay to ensure MiKTeX is fully initialized (optional but safer)
Filename: "ping.exe"; Parameters: "127.0.0.1 -n 6 > nul"; Flags: runhidden

[Registry]
Root: HKCU; Subkey: "Environment"; \
    ValueType: string; ValueName: "Path"; \
    ValueData: "{olddata};{app}"; Flags: preservestringtype uninsdeletevalue


