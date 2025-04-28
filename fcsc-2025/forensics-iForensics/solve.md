# iForensics

## Description

As you pass through customs, the customs officer asks you to hand over your phone and its unlock code. The phone is returned to you a few hours later…

Suspicious, you send your phone to ANSSI’s CERT-FR for analysis. CERT-FR analysts carry out a collection on the phone, consisting of a sysdiagnose and a backup.

It seems that a flag has hidden itself in the place where crashes are stored on the phone…

This challenge is part of a serie.

## Solution

### 1 iCrash

Extract the archive file and open the `fcsc_intro.txt` under it. Then you can find the flag: `FCSC{7a1ca2d4f17d4e1aa8936f2e906f0be8}`.

### 2 iDevice

open `backup/info.plist` you can find the `Product Type` and `Build Version` which is the flag `FCSC{iPhone12,3|20A362}`.

### 3 iWiFi

use

```python
import sqlite3
import plistlib
import os
import re

conn = sqlite3.connect('backup/Manifest.db')
c = conn.cursor()

search_terms = ['Cloud', "mail", "com.apple.icloud"]

def search_for_emails_in_db(db_path):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # get all table name
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        found_emails = set()
        
        for table in tables:
            table_name = table[0]
            try:
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns = cursor.fetchall()
                
                for column in columns:
                    column_name = column[1]
                    if 'text' in str(column[2]).lower() or 'char' in str(column[2]).lower() or 'varchar' in str(column[2]).lower():
                        cursor.execute(f"SELECT {column_name} FROM {table_name} WHERE {column_name} LIKE '%@%'")
                        results = cursor.fetchall()
                        
                        for result in results:
                            if result[0]:
                                # use re to find email
                                emails = re.findall(email_pattern, str(result[0]))
                                found_emails.update(emails)
            except Exception as e:
                print(f"failed to search {table_name}: {e}")
                
        conn.close()
        return found_emails
    except Exception as e:
        print(f"failed to load {db_path}: {e}")
        return set()

c = conn.cursor()
c.execute("SELECT fileID, relativePath FROM Files WHERE relativePath LIKE '%.sqlite' OR relativePath LIKE '%.db'")
db_files = c.fetchall()

# search every database
for file_id, path in db_files:
    print(f"check database: {path}")
    db_path = os.path.join('./backup', file_id[:2], file_id)
    if os.path.exists(db_path):
        emails = search_for_emails_in_db(db_path)
        if emails:
            print(f"in {path} found emails: {emails}")

for term in search_terms:
    print(f"\nsearch file contain'{term}':")
    c.execute("SELECT fileID, relativePath FROM Files WHERE relativePath LIKE ?", (f'%{term}%',))
    results = c.fetchall()
    
    for file_id, path in results:
        potential_path = os.path.join("./backup", file_id[:2], file_id)
        if os.path.exists(potential_path):
            print(f"Try to read {potential_path}")
            with open(potential_path, 'rb') as f:
                data = f.read()
                print(f"result: {data[:100]}...")
                try:
                    plist_data = plistlib.loads(data)
                    if type(plist_data) is dict:
                        for key, value in plist_data.items():
                            if key == "CloudKitAccountInfoCache":
                                for a, b in value.items():
                                    plist_data[key][a] = plistlib.loads(b)
                    print(f"plist data: {plist_data}")
                except Exception as e:
                    print(f"non plist data: {e}")

c.execute("SELECT fileID, relativePath FROM Files WHERE relativePath LIKE '%wifi%'")
wifi_files = c.fetchall()

for file_id, path in wifi_files:
    print(f"potential WIFI file: {path} (ID: {file_id})")
    
    potential_path = os.path.join("./backup", file_id[:2], file_id)
    if os.path.exists(potential_path):
        print(f"Try to read: {potential_path}")
        with open(potential_path, 'rb') as f:
            data = f.read()
            print(f"result: {data[:100]}...")
            try:
                # try to parse it as plist
                plist_data = plistlib.loads(data)
                print(f"plist data: {plist_data}")
            except Exception as e:
                print(f"failed to parse plist: {e}")
    else:
        c.execute("SELECT data FROM Files WHERE fileID=?", (file_id,))
        encrypted_data = c.fetchone()[0]
        
        print(f"Encrypted: {encrypted_data[:100]}...")

```

then you can find the iCloud email is one of the email accounts and the WIFI named `FCSC` and it's BSSID which leads to the flag: `FCSC{FCSC|66:20:95:6c:9b:37|robertswigert@icloud.com}`.

### 5 iNvisible

This one need to find the SMS messages, thus we can use

```python
import sqlite3
import os
import plistlib

conn = sqlite3.connect('backup/Manifest.db')
cursor = conn.cursor()

cursor.execute("SELECT fileID, domain, relativePath FROM Files WHERE relativePath LIKE '%sms.db' OR domain LIKE '%sms%'")
message_files = cursor.fetchall()
print("potential files:", message_files)

for file_id, domain, relative_path in message_files:
    print(f"Found database: {relative_path} (ID: {file_id})")
    
    db_path = os.path.join('./backup', file_id[:2], file_id)
    if os.path.exists(db_path):
        print(f"try to read: {db_path}")
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM message")  # assume table is named message
            messages = cursor.fetchall()
            print(f"Found: {messages}")
            # print all table and columns
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            for table in tables:
                table_name = table[0]
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns = cursor.fetchall()
                print(f"Table {table_name} Col: {[column[1] for column in columns]}")
            for table in tables:
                table_name = table[0]
                cursor.execute(f"SELECT * FROM {table_name}")
                rows = cursor.fetchall()
                print(f"Table {table_name} Data: {rows}")
        except sqlite3.Error as e:
            print(f"Failed to load: {e}")
        finally:
            conn.close()
    else:
        print(f"Failed to load: {db_path}")

```

The email is pop up in the result: `FCSC{kristy.friedman@outlook.com}`.

### 6 iTreasure

In the last result, there is a hint message `Do you want to have my precious secret ?` and a suspicious attachment patch `~/Library/SMS/Attachments/9e/14/4C3DF366-1CE1-42F1-9570-C76206181041/679329D1-12E7-45F2-A082-1E58A6CB454F.HEIC`. We can find it's path in `backup` using:

```python
import sqlite3

conn = sqlite3.connect("backup/Manifest.db")
c = conn.cursor()
c.execute("SELECT fileID, relativePath FROM Files WHERE relativePath LIKE '%HEIC%'")
wifi_files = c.fetchall()

for file_id, path in wifi_files:
    print(f"found potential file: {path} (ID: {file_id})")
    
```

result:

```log
found potential file: Media/PhotoData/Thumbnails/V2/DCIM/100APPLE/IMG_0001.HEIC (ID: 791ed7f23ddbea801f075181c0f2e0b8d22935f3)
found potential file: Library/SMS/Attachments/9e/14/4C3DF366-1CE1-42F1-9570-C76206181041/679329D1-12E7-45F2-A082-1E58A6CB454F.HEIC (ID: 6f4e34098e00a80fde876c8638fb1d685be2318b)
found potential file: Media/PhotoData/Thumbnails/V2/DCIM/100APPLE/IMG_0001.HEIC/5005.JPG (ID: 964d0beaca615b9ab39f3093941320250d09c655)
found potential file: Media/PhotoData/CPL/storage/filecache/AWy/cplAWyozGucosYwEZjKZsvgRSmzuMit.heic (ID: bf2ce68a5deb520fbce2ceb103b44c7dbb9f8cad)
found potential file: Media/DCIM/100APPLE/IMG_0001.HEIC (ID: 78564230ecf97df163e76713ce779e028c679bb6)
```

It's is in `backup/6f/6f4e34098e00a80fde876c8638fb1d685be2318b` (actually any of these works) and the flag is in the image: `FCSC{511773550dca}`.

### 7 iBackDoor 1/2

I stuck on this one for a while since we don't have access with the wifi packets or memory dump. But somehow we can use  `grep -i "connection" *.txt` to search all connection crash under `CrashReporter`, I found

```log
> grep -i "connection" *.txt
kbdebug.txt:2025-04-07 15:04:47 +0000: Debug: [_UIKeyboardArbiter] Lost connection [<_UIKeyboardArbiterClientHandle: 0x281004dc0; PID 344: org.whispersystems.signal <<UIKBArbiterClientFocusContext: 0x2827ee380; contextID = d6ce337f; sceneIdentity = com.apple.frontboard.systemappservices::FBSceneManager:sceneID%3Aorg.whispersystems.signal-default >>; hosting PIDs {(
```

then go to the `ps.txt` and search `org.whispersystems.signal`, we can find

```log
mobile             501  1000   344     1  4004044   0.0  0.0   0  0        0      0 -        ??  ?s    7:56AM   0:00.00 /var/containers/Bundle/Application/4B6E715E-641B-4F43-B39B-CA9AE3E8B73B/Signal.app/Signal
root                 0    99   345   344  4004004   0.0  0.0   0  0        0      0 -        ??  ?     7:56AM   0:00.00 /var/containers/Bundle/Application/4B6E715E-641B-4F43-B39B-CA9AE3E8B73B/Signal.app/mussel dGNwOi8vOTguNjYuMTU0LjIzNToyOTU1Mg==
```

This is super malicious especially `dGNwOi8vOTguNjYuMTU0LjIzNToyOTU1Mg==` is `tcp://98.66.154.235:29552`. Therefore the flag is `FCSC{org.whispersystems.signal|344}`

### 8 iBackDoor 2/2

I didn't got the flag but here is my tries so far:  
Firstly I found this malicious behavior as in last step

```log
--- !logd statistics record
type  : Memory Rollover
time  : 2025-04-07 07:42:54-0700
total : 9733361
procs :
    - [    3117304,  32.0, /usr/libexec/backboardd ]
    - [    1161608,  11.9, /System/Library/CoreServices/SpringBoard.app/SpringBoard ]
    - [     616480,   6.3, /usr/libexec/runningboardd ]
    - [     521624,   5.4, /usr/libexec/locationd ]
    - [     422120,   4.3, /kernel ]
    - [     288544,   3.0, /usr/sbin/mediaserverd ]
    - [     230512,   2.4, /System/Library/PrivateFrameworks/TCC.framework/Support/tccd ]
    - [     221280,   2.3, /usr/libexec/UserEventAgent ]
    - [     208592,   2.1, /usr/libexec/remindd ]
    - [     188800,   1.9, /private/var/containers/Bundle/Application/4B6E715E-641B-4F43-B39B-CA9AE3E8B73B/Signal.app/Signal.hooked ]
    - [     176992,   1.8, /System/Library/PrivateFrameworks/CloudKitDaemon.framework/Support/cloudd ]
    - [     169712,   1.7, /System/Library/PrivateFrameworks/WallpaperKit.framework/PlugIns/CollectionsPoster.appex/CollectionsPoster ]
    - [     160880,   1.7, /System/Library/TextInput/kbd ]
    - [     145840,   1.5, /usr/sbin/bluetoothd ]
    - [     125576,   1.3, /usr/libexec/duetexpertd ]
    - [     115136,   1.2, /System/Library/PrivateFrameworks/IAP.framework/Support/iapd ]
    - [     114168,   1.2, /usr/libexec/symptomsd ]
    - [     103936,   1.1, /System/Library/PrivateFrameworks/CoreDuetContext.framework/Resources/contextstored ]
    - [      97592,   1.0, /private/var/containers/Bundle/Application/0B6E96CE-177D-4E4C-B85D-DDCE6B04FFD0/TrollStore.app/TrollStore ]
    - [      94409,   1.0, /usr/libexec/nesessionmanager ]
```


- `FCSC{com.opa334.TrollStore|/private/var/containers/Bundle/Application/0B6E96CE-177D-4E4C-B85D-DDCE6B04FFD0/TrollStore.app|2025-04-07 07:42:54}` no  
- `FCSC{com.opa334.TrollStore|/private/var/containers/Bundle/Application/4B6E715E-641B-4F43-B39B-CA9AE3E8B73B/Signal.app|2025-04-07 07:42:54}` no  

Then I found the `TrollDecrypt` behavior  

```log
0	96	-	0	1744033538	16877	501	501	/private/var/mobile/Library/TrollDecrypt/
0	96	-	0	1744033541	16877	501	501	/private/var/mobile/Library/TrollDecrypt/decrypted/
66605056	66603101	-	0	1744033541	33188	501	501	/private/var/mobile/Library/TrollDecrypt/decrypted/Signal_7.53_decrypted.ipa
```

- `FCSC{com.fiore.trolldecrypt|/private/var/mobile/Library/TrollDecrypt/decrypted/Signal_7.53_decrypted.ipa|2025-04-07 13:45:41}` no
- `FCSC{com.opa334.TrollStore|/private/var/mobile/Library/TrollDecrypt/decrypted/Signal_7.53_decrypted.ipa|2025-04-07 13:45:41}` no
- `FCSC{com.fiore.trolldecrypt|/private/var/containers/Bundle/Application/42E3BD65-87BB-4AF4-997A-8C4EEA5AE4A6|2025-04-07 07:43:55}` no

Then here are some uninstall and install logs:

```log
Mon Apr  7 07:40:47 2025 [446] <err> (0x16fc9b000) -[MIUninstaller performUninstallationByRevokingTemporaryReference:error:]: Failed to get children for org.whispersystems.signal : (null); ignoring
Mon Apr  7 07:40:47 2025 [446] <err> (0x16fc9b000) -[MIUninstaller performUninstallationByRevokingTemporaryReference:error:]: Failed to get parent of org.whispersystems.signal : (null); ignoring
Mon Apr  7 07:40:47 2025 [446] <err> (0x16fc9b000) -[MIUninstaller performUninstallationByRevokingTemporaryReference:error:]: Taking termination assertion on {(
    "org.whispersystems.signal"
)}
Mon Apr  7 07:40:47 2025 [446] <notice> (0x16fc9b000) -[MIUninstaller _uninstallBundleWithIdentity:linkedToChildren:waitForDeletion:uninstallReason:temporaryReference:wasLastReference:error:]: Uninstalling identifier org.whispersystems.signal
Mon Apr  7 07:40:47 2025 [446] <err> (0x16fc9b000) -[MIUninstaller _uninstallBundleWithIdentity:linkedToChildren:waitForDeletion:uninstallReason:temporaryReference:wasLastReference:error:]: Destroying container org.whispersystems.signal with persona (null) at /private/var/containers/Bundle/Application/1EC20F02-263B-4299-AE05-3F5D7A7744E9
Mon Apr  7 07:40:47 2025 [446] <err> (0x16fc9b000) -[MIUninstaller _uninstallBundleWithIdentity:linkedToChildren:waitForDeletion:uninstallReason:temporaryReference:wasLastReference:error:]: Destroying container org.whispersystems.signal with persona 8A4A857A-0269-4861-BE19-06B76B941887 at /private/var/mobile/Containers/Data/Application/99FCC994-C7C1-4F60-A797-0BFFB204453A
Mon Apr  7 07:40:47 2025 [446] <err> (0x16fc9b000) -[MIUninstaller _uninstallBundleWithIdentity:linkedToChildren:waitForDeletion:uninstallReason:temporaryReference:wasLastReference:error:]: Destroying container org.whispersystems.signal.shareextension with persona 8A4A857A-0269-4861-BE19-06B76B941887 at /private/var/mobile/Containers/Data/PluginKitPlugin/A9321276-4AF9-4BE5-8041-E399CA137541
Mon Apr  7 07:40:47 2025 [446] <err> (0x16fc9b000) -[MIUninstaller _uninstallBundleWithIdentity:linkedToChildren:waitForDeletion:uninstallReason:temporaryReference:wasLastReference:error:]: Destroying container org.whispersystems.signal.SignalNSE with persona 8A4A857A-0269-4861-BE19-06B76B941887 at /private/var/mobile/Containers/Data/PluginKitPlugin/30C28DF1-55B5-4F5D-8FAC-B9A1E8700E7D
Mon Apr  7 07:40:47 2025 [446] <notice> (0x16fc9b000) MIFetchUIDForRegistration_block_invoke: UID for registration: 501
Mon Apr  7 07:40:47 2025 [446] <err> (0x16fc9b000) -[MIUninstaller _onRegistrationQueue_registerUninstallationForRemovedInfo:error:]: Successfully unregistered <MIUninstallRecord: 0x104e1f200> for 501
Mon Apr  7 07:40:47 2025 [446] <notice> (0x16fd27000) -[MIClientConnection _uninstallIdentities:withOptions:completion:]: Uninstall requested by installcoordinationd (pid 123 (501/501)) for identity [org.whispersystems.signal/PersonalPersonaPlaceholderString] with options: {
    WaitForStorageDeletion = 0;
}
Mon Apr  7 07:40:47 2025 [446] <err> (0x16fd27000) -[MIUninstaller performUninstallationByRevokingTemporaryReference:error:]: Failed to get children for org.whispersystems.signal : (null); ignoring
Mon Apr  7 07:40:47 2025 [446] <err> (0x16fd27000) -[MIUninstaller performUninstallationByRevokingTemporaryReference:error:]: Failed to get parent of org.whispersystems.signal : (null); ignoring
Mon Apr  7 07:40:47 2025 [446] <err> (0x16fd27000) -[MIUninstaller performUninstallationByRevokingTemporaryReference:error:]: Taking termination assertion on {(
    "org.whispersystems.signal"
)}
```

- `FCSC{com.opa334.TrollStore|/private/var/mobile/Containers/Data/Application/99FCC994-C7C1-4F60-A797-0BFFB204453A|2025-04-07 07:40:47}` no

```log
Mon Apr  7 06:13:34 2025 [234] <notice> (0x16b48f000) -[MIClientConnection _doInstallationForURL:identity:domain:options:completion:]: Install of "/private/var/containers/Shared/SystemGroup/systemgroup.com.apple.installcoordinationd/Library/InstallCoordination/PromiseStaging/B6D2BE18-C74E-4BBE-A15F-C88A708E89A3/Signal.app" type Placeholder (LSInstallType = MIInstallationDomainDefault, Domain: 1) requested by installcoordinationd (pid 960 (501/501))
Mon Apr  7 06:13:34 2025 [234] <notice> (0x16b48f000) -[MIInstaller _installInstallable:containingSymlink:error:]: Installing <MIInstallableBundle ID=org.whispersystems.signal; Version=(null), ShortVersion=(null)>
Mon Apr  7 06:13:34 2025 [234] <notice> (0x16b48f000) -[MIContainer makeContainerLiveReplacingContainer:reason:waitForDeletion:withError:]: Made container live for org.whispersystems.signal at /private/var/mobile/Containers/Data/Application/7D8F45EA-CF9E-4074-910B-33CE7A8E196B
Mon Apr  7 06:13:34 2025 [234] <notice> (0x16b48f000) -[MIContainer makeContainerLiveReplacingContainer:reason:waitForDeletion:withError:]: Made container live for org.whispersystems.signal at /private/var/containers/Bundle/Application/9FE717E1-1A80-4973-B315-158AF5E4311E
Mon Apr  7 06:13:34 2025 [234] <err> (0x16b48f000) -[MIBundleContainer compatibilityLinkDestination]: Unable to determine SDK version for executable at /private/var/containers/Bundle/Application/9FE717E1-1A80-4973-B315-158AF5E4311E/Signal.app
Mon Apr  7 06:13:34 2025 [234] <err> (0x16b48f000) -[MIInstaller _onRegistrationQueue_registerInstalledInfo:error:]: Successfully registered [org.whispersystems.signal/PersonalPersonaPlaceholderString] for 501
Mon Apr  7 06:13:34 2025 [234] <notice> (0x16b48f000) -[MIInstaller performInstallationWithError:]: Install Successful for (Placeholder:org.whispersystems.signal); Staging: 0.01s; Waiting: 0.00s; Preflight/Patch: 0.00s, Verifying: 0.01s; Overall: 0.14s
Mon Apr  7 06:13:34 2025 [234] <notice> (0x16b48f000) -[MIClientConnection updatePlaceholderMetadataForApp:installType:failureReason:underlyingError:failureSource:completion:]: Update placeholder metadata requested by client installcoordinationd (pid 960 (501/501)) for app org.whispersystems.signal installType = 1 failureReason = 0 underlyingError = (null) failureSource = 0
```

- `FCSC{com.apple.installcoordinationd|/private/var/containers/Shared/SystemGroup/systemgroup.com.apple.installcoordinationd/Library/InstallCoordination/PromiseStaging/A920C941-DB60-4E99-92B9-26D5DCBE982B/Signal.app|2025-04-07 07:40:47}` no
- `FCSC{com.apple.installcoordinationd|/var/containers/Bundle/Application/4B6E715E-641B-4F43-B39B-CA9AE3E8B73B|2025-04-07 07:40:47}` no
- `FCSC{com.opa334.TrollStore|/private/var/containers/Shared/SystemGroup/systemgroup.com.apple.installcoordinationd/Library/InstallCoordination/PromiseStaging/A920C941-DB60-4E99-92B9-26D5DCBE982B/Signal.app|2025-04-07 07:40:47}` no
- `FCSC{com.apple.installcoordinationd|/private/var/containers/Bundle/Application/4B6E715E-641B-4F43-B39B-CA9AE3E8B73B/Signal.app|2025-04-07 07:40:47}` no

### 9 IC2

I didn't make it here is one of my guess: `tcp://98.66.154.235:29552` with `FCSC{Mussel|TCP|98.66.154.235|29552}`.

### 10 iCompromise

Didn't make it.
