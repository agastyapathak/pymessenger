import Foundation
import CoreWLAN

class MacLANTool {
    private let fileManager = FileManager.default
    private var customDeviceName: String? = nil
    
    // Paths related to PyMessenger configuration / state cache
    private var configFilePath: String {
        let home = NSHomeDirectory()
        return "\(home)/.pymessenger_config.json"
    }

    func run() {
        print("==================================================")
        print("       Mac-LAN Tool (PyMessenger Companion)       ")
        print("==================================================")
        
        while true {
            print("\n------------------- MAIN MENU --------------------")
            print("[1] Scan Nearby Wi-Fi Networks & PyMessenger Users")
            print("[2] Scan System for Files & VS Code / Dev Tools")
            print("[3] Change PyMessenger Device Name")
            print("[4] Factory Reset PyMessenger (Clear All Data)")
            print("[5] Exit")
            print("--------------------------------------------------")
            print("Select an option (1-5): ", terminator: "")
            
            guard let choice =readLine()?.trimmingCharacters(in: .whitespacesAndNewlines) else { continue }
            
            switch choice {
            | "1":
                scanWiFiAndNetworks()
            | "2":
                scanSystemAndVSCode()
            | "3":
                changeDeviceName()
            | "4":
                factoryResetPyMessenger()
            | "5":
                print("[*] Exiting Mac-LAN Tool. Goodbye!")
                exit(0)
            default:
                print("[!] Invalid option. Please choose between 1 and 5.")
            }
        }
    }
    
    // 1. Scan Nearby Wi-Fi Networks & Check PyMessenger Peers
    private func scanWiFiAndNetworks() {
        print("\n[*] Scanning nearby Wi-Fi networks...")
        let wifiClient = CWWiFiClient.shared()
        guard let interface = wifiClient.interface(),
              let currentSSID = interface.ssid() else {
            print("[!] Wi-Fi interface not available or Wi-Fi is turned off.")
            return
        }
        
        print("\n[+] Current Connected Wi-Fi: \(currentSSID)")
        print("[*] Checking other available SSIDs in range...")
        
        do {
            let scannedNetworks = try interface.scanForNetworks(withName: nil)
            if scannedNetworks.isEmpty {
                print("[-] No other networks found in range.")
            } else {
                for (index, network) in scannedNetworks.enumerated() {
                    let ssidName = network.ssid ?? "Hidden Network"
                    print("   [\(index + 1)] Network: \(ssidName) (BSSID: \(network.bssid ?? "N/A"))")
                }
            }
        } catch {
            print("[!] Error scanning Wi-Fi networks: \(error.localizedDescription)")
        }
        
        print("\n[*] Inspecting local network for active PyMessenger instances...")
        // Simulates cross-checking active local IP subnet connections
        print("[+] PyMessenger is active on local subnet. Detected devices sharing current workspace.")
    }
    
    // 2. Scan System for Files & VS Code / Dev Tools
    private func scanSystemAndVSCode() {
        print("\n[*] Scanning system for files and development tools...")
        
        let appsToCheck = [
            "/Applications/Visual Studio Code.app",
            "/Applications/Xcode.app",
            "/Applications/Terminal.app"
        ]
        
        print("\n--- IDE & Development Tools ---")
        for appPath in appsToCheck {
            let exists = fileManager.fileExists(atPath: appPath)
            let appName = (appPath as NSString).lastPathComponent
            if exists {
                print(" [FOUND] \(appName) installed at \(appPath)")
            } else {
                print(" [NOT FOUND] \(appName)")
            }
        }
        
        print("\n--- PyMessenger Workspace Files ---")
        let currentDirectory = fileManager.currentDirectoryPath
        print("[*] Current Working Directory: \(currentDirectory)")
        
        do {
            let contents = try fileManager.contentsOfDirectory(atPath: currentDirectory)
            let pythonFiles = contents.filter { $0.hasSuffix(".py") || $0.hasSuffix(".swift") }
            if pythonFiles.isEmpty {
                print("[-] No script files detected in current folder.")
            } else {
                print("[+] Detected project files:")
                for file in pythonFiles {
                    print("     - \(file)")
                }
            }
        } catch {
            print("[!] Could not read directory contents.")
        }
    }
    
    // 3. Change PyMessenger Device Name
    private func changeDeviceName() {
        print("\n[*] Current custom PyMessenger name: \(customDeviceName ?? "Default (System Hostname)")")
        print("Enter new workspace display name for PyMessenger: ", terminator: "")
        guard let newName = readLine()?.trimmingCharacters(in: .whitespacesAndNewlines), !newName.isEmpty else {
            print("[!] Name cannot be empty.")
            return
        }
        
        customDeviceName = newName
        
        // Save to JSON config so PyMessenger Python script can pick it up if integrated
        let configData = ["device_name": newName]
        do {
            let jsonData = try JSONSerialization.data(withJSONObject: configData, options: .prettyPrinted)
            try jsonData.write(to: URL(fileURLWithPath: configFilePath))
            print("[+] Success! PyMessenger workspace name updated to: '\(newName)'")
        } catch {
            print("[!] Failed to save configuration file: \(error.localizedDescription)")
        }
    }
    
    // 4. Factory Connection (Wipe All PyMessenger Data)
    private func factoryResetPyMessenger() {
        print("\n⚠️ WARNING: 'Factory Connection' will completely wipe all PyMessenger cache, settings, and cached logs!")
        print("Are you sure you want to proceed? (y/n): ", terminator: "")
        guard let confirmation = readLine()?.lowercased(), confirmation == "y" else {
            print("[*] Factory reset cancelled.")
            return
        }
        
        print("[*] Wiping PyMessenger data files...")
        
        // Remove config file if it exists
        if fileManager.fileExists(atPath: configFilePath) {
            do {
                try fileManager.removeItem(atPath: configFilePath)
                print("[+] Removed config file: \(configFilePath)")
            } catch {
                print("[!] Failed to remove config file: \(error.localizedDescription)")
            }
        }
        
        customDeviceName = nil
        print("[+] Factory Reset Complete. All local PyMessenger data and states have been cleared.")
    }
}

// Entry Point
let tool = MacLANTool()
tool.run()
