# CS2 Keychain Extractor

A tiny tool to extract CS2 keychain coordinates (x, y, z) directly from the browser when generating an inspect link on cs2inspects.com.

It intercepts the network payload via a native browser extension and sends the coordinates to a local Python script to automatically copy them to your clipboard.

Works on Linux (Wayland/X11), Windows, and macOS.

## Contributing
Got a sick charm placement? Add it to the public archive!
1. Fork the repo.
2. Drop your screenshot in the `images/` folder (e.g., `glock18-grip.png`).
3. Add your image and X/Y/Z coordinates to the "Common Placements" list below.
4. Open a PR.

## Setup

### 1. Start the Clipboard Server
Run the Python script in a terminal. It listens for the extension and handles clipboard copying. No dependencies required.
```bash
python3 server.py
```
*(Linux: make sure `wl-clipboard` or `xclip` is installed)*

### 2. Install the Extension

#### Temporary 
1. Open Firefox / Zen Browser and go to `about:debugging`.
2. Click **This Firefox** on the left.
3. Click **Load Temporary Add-on...**
4. Select the `manifest.json` file inside the `extension/` folder.

#### Permanent
1. Go to `about:config`.
2. Search for `xpinstall.signatures.required` and set it to `false`.
3. Drag and drop `cs2-extractor.xpi` into your browser window and click **Add**.

## Usage
1. Keep `server.py` running.
2. Go to cs2inspects.com and set up your weapon.
3. Click the **Inspect In-Game** button.
4. Your coordinates are instantly copied to your clipboard: `!charm_set <x> <y> <z>`

---

## Common Placements

Don't want to use the extractor? Here's a master list of common charm placements. 

**Jump to Weapon:**
- [Rifles](#rifles)
  - [AK-47](#ak-47)
  - [M4A1-S](#m4a1-s)

---

### Rifles

#### AK-47

##### Top UP
![AK-47 Top UP](images/ak47-TopUP.png)

- **X:** `24.32`
- **Y:** `0.23`
- **Z:** `4.08`
> **Command:** `!charm_set 24.32 0.23 4.08`

*(Add more placements here)*

---

#### M4A1-S
*(Add M4A1-S placements here)*
