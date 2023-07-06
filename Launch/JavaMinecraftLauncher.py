from os import remove, system
from Modules.AgumentsBuilders.JavaMinecraftArgumentsBuilder import JavaMinecraftArgumentsBuilder
from Modules.Models.Launch.LaunchConfig import LaunchConfig
from Modules.Toolkits.GameCoreToolkit import GameCoreToolkit


class JavaMinecraftLauncher():
    def __init__(self, launchSetting: LaunchConfig, gameCoreToolkit: GameCoreToolkit, EnableIndependencyCore = False):
        self.LaunchSetting = launchSetting
        self.GameCoreToolkit = gameCoreToolkit
        self.EnableIndpendencyCore = EnableIndependencyCore

    def LaunchTaskAsync(self, id: str):
        javaMinecraftLauncher = JavaMinecraftArgumentsBuilder(
            self.GameCoreToolkit.Root,
            id, 
            self.LaunchSetting.JvmConfig[0], 
            self.LaunchSetting.JvmConfig[1], 
            self.LaunchSetting.Account, 
            self.LaunchSetting.GameWindowConfig[0], 
            self.LaunchSetting.GameWindowConfig[1])
        bat = open("run.bat", "w")
        bat.write(javaMinecraftLauncher.Launch())
        bat.close()
        system("run.bat")
        remove("run.bat")

    def Launch(self, id: str):
        pass
