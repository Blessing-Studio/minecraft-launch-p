from minecraft_launch.modules.models.download.download_api import DownloadAPI


class APIManager():
    current: DownloadAPI = DownloadAPI(
        host = "https://download.mcbbs.net",
        version_manifest = "https://download.mcbbs.net/mc/game/version_manifest.json",
        assets = "https://download.mcbbs.net/assets",
        libraries = "https://download.mcbbs.net/maven"
    )

    mojang: DownloadAPI = DownloadAPI(
        host = "https://launcher.mojang.com",
		version_manifest = "http://launchermeta.mojang.com/mc/game/version_manifest.json",
		assets = "http://resources.download.minecraft.net",
		libraries = "https://libraries.minecraft.net"
    )

    bmcl: DownloadAPI = DownloadAPI(
        host = "https://bmclapi2.bangbang93.com",
		version_manifest = "https://bmclapi2.bangbang93.com/mc/game/version_manifest.json",
		assets = "https://bmclapi2.bangbang93.com/assets",
		libraries = "https://bmclapi2.bangbang93.com/maven"
    )

    mcbbs: DownloadAPI = DownloadAPI(
        host = "https://download.mcbbs.net",
		version_manifest = "https://download.mcbbs.net/mc/game/version_manifest.json",
		assets = "https://download.mcbbs.net/assets",
		libraries = "https://download.mcbbs.net/maven"
    )

    forge_library_url_replace: dict[str, str] = {
		"https://maven.minecraftforge.net":
		"https://maven.minecraftforge.net" if current.host.__eq__(mojang.host) else (current.libraries if current.libraries != None else ""),
        "https://files.minecraftforge.net/maven":
		"https://maven.minecraftforge.net" if current.host.__eq__(mojang.host) else (current.libraries if current.libraries != None else "")
	}
    
    fabric_library_url_replace: dict[str, str] = {
        "https://maven.fabricmc.net":
	    "https://maven.fabricmc.net" if current.host.__eq__(mojang.host) else (current.libraries if current.libraries != None else ""),
		"https://meta.fabricmc.net":
		"https://meta.fabricmc.net" if current.host.__eq__(mojang.host) else (f"{current.host}/fabric-meta" if f"{current.host}/fabric-meta" != None else "")
    } 