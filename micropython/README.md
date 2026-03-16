# Flashing MicroPython on ESP32-C3 with Thonny / Flasher MicroPython sur l'ESP32-C3 avec Thonny

---

## 1. Install Thonny / Installer Thonny

- Download Thonny from https://thonny.org
- Install it normally (Windows, macOS or Linux)

---

- Télécharger Thonny sur https://thonny.org
- L'installer normalement (Windows, macOS ou Linux)

## 2. Prepare Thonny / Préparer Thonny

The La Machine board already runs Erlang/AtomVM firmware. The board does have BOOT and RESET buttons, but they are inside the enclosure — you would need to disassemble the machine to reach them. To avoid that, we'll use a quicker method: **switch S3** (the main button on top of the box, the one that normally triggers the arm) wakes the ESP32-C3 from deep sleep, which briefly makes the USB serial port visible. It disappears as soon as the movement is finished and the ESP32-C3 goes back to deep sleep. You need to be quick!

La carte La Machine contient déjà le firmware Erlang/AtomVM. La carte possède bien des boutons BOOT et RESET, mais ils sont à l'intérieur du boîtier — il faudrait démonter la machine pour y accéder. Pour éviter ça, on va utiliser une méthode plus rapide : **l'interrupteur S3** (le bouton principal sur le dessus de la boîte, celui qui déclenche normalement le bras) réveille l'ESP32-C3 du deep sleep, ce qui rend le port série USB brièvement visible. Il disparaît dès que le mouvement est terminé et que l'ESP32-C3 retourne en deep sleep. Il faut être rapide !

1. Plug the La Machine board via USB / Brancher la carte La Machine en USB
2. Open Thonny / Ouvrir Thonny
3. Go to **Tools > Options > Interpreter** / Aller dans **Outils > Options > Interpréteur**
4. Select **MicroPython (ESP32)** as interpreter / Sélectionner **MicroPython (ESP32)** comme interpréteur
5. Click **Install or update MicroPython (esptool)** / Cliquer sur **Installer ou mettre à jour MicroPython (esptool)**
6. In the install window, pre-configure everything **before** waking the machine:
   - **MicroPython family**: ESP32
   - **Variant**: Espressif ESP32-C3
   - Leave the latest version selected
   - Leave **Target port** for now

   Dans la fenêtre d'installation, pré-configurer tout **avant** de réveiller la machine :
   - **MicroPython family** : ESP32
   - **Variant** : Espressif ESP32-C3
   - Laisser la version la plus récente
   - Laisser **Target port** pour l'instant

## 3. Flash MicroPython (the tricky part!) / Flasher MicroPython (la partie délicate !)

This is a race against the clock: the serial port only stays active for a few seconds while the Erlang firmware runs a movement.

C'est une course contre la montre : le port série ne reste actif que quelques secondes pendant que le firmware Erlang exécute un mouvement.

1. **Get ready**: have the Thonny install window open with everything pre-configured (see step 2 above)
2. **Press the main button (S3)** on top of the box to wake up the machine
3. **Immediately** click the refresh button next to **Target port** — the serial port should appear (e.g. `/dev/cu.usbmodem...` on macOS, `COM3` on Windows)
4. **Select the port** and **click Install** as fast as possible
5. If the flash starts, you're good — `esptool` takes control of the ESP32 and the deep sleep timer no longer matters
6. Wait for flashing to complete (a few minutes)
7. Close the install window

---

1. **Se préparer** : avoir la fenêtre d'installation de Thonny ouverte avec tout pré-configuré (voir étape 2 ci-dessus)
2. **Actionner l'interrupteur S3** sur la boîte pour réveiller la machine
3. **Immédiatement** cliquer sur le bouton rafraîchir à côté de **Target port** — le port série devrait apparaître (ex : `/dev/cu.usbmodem...` sur macOS, `COM3` sur Windows)
4. **Sélectionner le port** et **cliquer Installer** le plus vite possible
5. Si le flashage démarre, c'est gagné — `esptool` prend le contrôle de l'ESP32 et le timer de deep sleep n'a plus d'effet
6. Attendre la fin du flashage (quelques minutes)
7. Fermer la fenêtre d'installation

> **Tip / Astuce**: If you miss the window, just press the main button (S3) again to wake the machine and retry. It may take a few attempts!
> Si vous ratez la fenêtre, appuyez à nouveau sur le bouton principal (S3) pour réveiller la machine et réessayez. Il faudra peut-être plusieurs tentatives !

## 4. Verify it works / Vérifier que ça fonctionne

1. Unplug and replug the USB cable / Débrancher et rebrancher le câble USB
2. In Thonny, the shell at the bottom should display / Dans Thonny, le shell en bas devrait afficher :

```
MicroPython v1.xx.x on xxxx-xx-xx; ESP32C3 module with ESP32C3
>>>
```

3. Type `print("hello")` in the shell to verify / Taper `print("hello")` dans le shell pour vérifier

> Now that MicroPython is flashed, the serial port stays active permanently (no more deep sleep race condition!).
> Maintenant que MicroPython est flashé, le port série reste actif en permanence (plus besoin de course contre la montre !).

## 5. Upload project files / Transférer les fichiers du projet

1. In Thonny, open `main.py` (**File > Open**, navigate to the `la-machine-DIY` folder)
2. Go to **File > Save as...**
3. Choose **MicroPython device** as destination
4. Name the file `main.py` (this name matters: MicroPython runs it automatically at startup)
5. Do the same for the sound file `sound.wav`:
   - In the **Files** panel in Thonny (**View > Files** if not visible)
   - Navigate to `sound.wav` on your computer (top panel)
   - Right-click `sound.wav` > **Upload to /**

> The WAV file must be: **16-bit, mono, 44100 Hz**. To convert an existing file, use Audacity or the command:
> ```
> ffmpeg -i my_sound.mp3 -ar 44100 -ac 1 -sample_fmt s16 sound.wav
> ```

---

1. Dans Thonny, ouvrir le fichier `main.py` (menu **Fichier > Ouvrir**, naviguer jusqu'au dossier `la-machine-DIY`)
2. Faire **Fichier > Enregistrer sous...**
3. Choisir **Périphérique MicroPython** comme destination
4. Nommer le fichier `main.py` (ce nom est important : MicroPython l'exécute automatiquement au démarrage)
5. Faire la même chose pour le fichier son `sound.wav` :
   - Dans le panneau **Fichiers** de Thonny (menu **Affichage > Fichiers** si pas visible)
   - Naviguer jusqu'au fichier `sound.wav` sur l'ordinateur (panneau du haut)
   - Clic droit sur `sound.wav` > **Transférer vers le périphérique**

> Le fichier WAV doit être : **16 bits, mono, 44100 Hz**. Pour convertir un fichier existant, utiliser Audacity ou la commande :
> ```
> ffmpeg -i mon_son.mp3 -ar 44100 -ac 1 -sample_fmt s16 sound.wav
> ```

## 6. Run the program / Lancer le programme

- Unplug and replug the USB cable (or click the Stop/Restart button in Thonny)
- `main.py` runs automatically at boot
- In Thonny, the shell displays `La Machine DIY - starting` then `Ready - waiting for button press...`
- Flip switch S3 to trigger the machine

---

- Débrancher et rebrancher le câble USB (ou cliquer sur le bouton Stop/Redémarrer dans Thonny)
- Le programme `main.py` se lance automatiquement au démarrage
- Dans Thonny, le shell affiche `La Machine DIY - starting` puis `Ready - waiting for button press...`
- Actionner l'interrupteur S3 pour déclencher la machine

## 7. Troubleshooting / Dépannage

| Problem / Problème | Solution |
|---------------------|----------|
| Serial port not detected / Port série non détecté | Install the USB driver (CH340 or CP2102 depending on the board). On macOS, try another USB cable (some are charge-only). / Installer le driver USB (CH340 ou CP2102 selon la carte). Sur macOS, essayer un autre câble USB (certains ne font que la charge). |
| `PWM is inactive` | Make sure you have the latest version of `main.py`. / Vérifier que vous avez la dernière version du `main.py`. |
| No sound / Pas de son | Check that `sound.wav` is on the device (Files panel). Check the format (16-bit mono 44100Hz). / Vérifier que `sound.wav` est bien sur le périphérique (panneau Fichiers). Vérifier le format (16-bit mono 44100Hz). |
| `ENOMEM` / Out of memory | The WAV file is too large for the filesystem. Shorten the sound or lower the sample rate to 22050Hz (and update `I2S_SAMPLE_RATE` in `main.py`). / Le fichier WAV est trop gros. Réduire la durée du son ou baisser le sample rate à 22050Hz (et modifier `I2S_SAMPLE_RATE` dans `main.py`). |
| Servo doesn't move / Le servo ne bouge pas | Check that the battery is charged (the boost circuit needs it). / Vérifier que la batterie est chargée (le boost circuit en a besoin). |
