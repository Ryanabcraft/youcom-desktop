[Setup]
AppName=You.com Desktop
AppVersion=1.0.0
AppPublisher=Ryanabcraft
AppPublisherURL=https://github.com/Ryanabcraft/youcom-desktop
AppSupportURL=https://github.com/Ryanabcraft/youcom-desktop/issues
DefaultDirName={localappdata}\You.com Desktop
DefaultGroupName=You.com Desktop
UninstallDisplayIcon={app}\YouCom.exe
UninstallDisplayName=You.com Desktop
OutputDir=dist_installer
OutputBaseFilename=YouCom-Setup
Compression=lzma2
SolidCompression=yes
PrivilegesRequired=lowest

[Languages]
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Files]
Source: "dist_py\YouCom.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{commondesktop}\You.com"; Filename: "{app}\YouCom.exe"; WorkingDir: "{app}"; Tasks: desktopicon
Name: "{group}\You.com Desktop"; Filename: "{app}\YouCom.exe"; WorkingDir: "{app}"
Name: "{group}\Desinstalar You.com Desktop"; Filename: "{uninstallexe}"

[Tasks]
Name: "desktopicon"; Description: "Criar atalho na &Área de Trabalho"; GroupDescription: "Atalhos:"; Flags: checkedonce

[Run]
Filename: "{app}\YouCom.exe"; Description: "Executar You.com Desktop"; Flags: postinstall nowait skipifsilent
