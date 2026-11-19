# CCN Keypad

A one-page symbol keypad. Tap keys to build a string of math symbols and emoji, then **Send** it as JSON to a Wolfram Cloud API and read the reply.

**Live page (after you enable GitHub Pages):** `https://lossofgenerality.github.io/ccn-keypad/`

## What it does

The page follows the layout of the CCN String Diagrams editor: a toolbar and a drawing **canvas** on the left, and an **Input**, **Result** and **Selection** panel on the right.

- **Boxes and wires, from the editor:** + Box, + Box 𝟙 → X, + Box X → 𝟙, + Dot, + Crossing, + = and + Source / + Target ends. Drag a box to move it, drag from a port (○) to another port to draw an arc, scroll to zoom, and drag the background to pan. The toolbar also has Delete, Undo, Clear, Fit, Export SVG (with the © line), Save and Open (`.json`), the reading direction (bottom → top, as in the book) and colour labels. Boxes named `τ_{X,Y}` or `τ⁻¹_{Y,X}` on two lines are drawn as crossings. The canvas code is reused from CCN String Diagrams without the simplifier.
- **Selection** edits the selected box: label (`_` for a subscript), number of inputs and outputs, shape, and source and target colours.

- **Floating keypad, structured as in the editor:** tab buttons over an 8-column grid of keys, floating over the canvas. The tabs are
  - **Math:** ⋂ ⋃ ⨁ ⨂ ✖ ∂ ∈ ∉ ⊂ →
  - **Symbols:** 🫆 🔐 👥 🗣 𖤘 ⚲ 🗝 🔑 ⭔ ⛓️
  - **Faces:** 👶 👶🏻 🧑 👧🏻 🧕 🧕🏾 👩🏽‍🦱 👨 🧔🏽‍♂️ 🧑🏾‍🦱 👵🏻 👴🏻 😵
  - **Religious:** ✝️ 🕋 🕉️ 🛐
  - **Other:** 🪖 🧨 🔥 🇵🇸

  Every tab also has **space** and **⌫**. ⌫ removes one whole symbol, including skin-tone, ZWJ and flag emoji. Hover over a key to see its Unicode code point. The keys are listed in the `PADS` table in `src/keypad.html`, in the editor's format `[insert, label, class]`, where class `w2` or `w3` makes a key two or three columns wide.
- **Where keys go:** to the **Input** box. When a box is selected, they go to its label instead, so you can put symbols straight onto boxes. Clicking in any other Selection field, such as a colour, sends them there.
- **Moving it:** drag the keypad by its title bar; it stays inside the canvas. **–** minimises it and **×** hides it. The toolbar's **Floating keypad** button shows or hides it, and **Reset position** puts it back in the corner.
- **Send** posts the input to the API:

  ```js
  fetch("https://www.wolframcloud.com/obj/ccn2/freeform/ff/networks/tests/ffsimplefetch", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ ping: "<input text>" })
  });
  ```

- **Result** shows the reply, with **Copy result** and **Use as input**. For a one-field reply such as `{"ff": "..."}`, it shows just the value.

## Files

| File | Purpose |
|---|---|
| `index.html` | The page GitHub Pages serves. **Generated:** don't edit it by hand. |
| `src/keypad.html` | The source. Make your changes here. |
| `tools/build_csp.py` | Rebuilds `index.html` from the source and adds the security policy. |
| `.nojekyll` | Tells GitHub Pages to serve the files as they are. |
| `LICENSE.md` | CC BY-NC-SA 4.0 notice. |

## Put it on GitHub (website upload)

1. Unzip `ccn-keypad.zip`. You get a folder called `ccn-keypad`.
2. On GitHub, click **+ → New repository**. Name it `ccn-keypad`, make it **Public**, and leave every "Add a README / .gitignore / license" box unticked. Click **Create repository**.
3. On the new repo page, click **uploading an existing file**.
4. Open the `ccn-keypad` folder on your computer, select **everything inside it** (`index.html`, `README.md`, `LICENSE.md`, `.nojekyll`, and the `src` and `tools` folders), and drag it onto the upload area. Folders keep their structure.
   - `.nojekyll` is a hidden file. On a Mac, press **⌘ Shift .** in Finder to show it. On Windows, turn on **View → Show → Hidden items**. If it doesn't upload, see step 7.
5. Write a commit message such as `CCN Keypad v1` and click **Commit changes**.
6. Go to **Settings → Pages**. Under *Build and deployment*, set **Source: Deploy from a branch**, **Branch: main**, **Folder: / (root)**, and click **Save**.
7. If `.nojekyll` didn't upload, click **Add file → Create new file**, name it `.nojekyll`, leave it empty, and commit.
8. Wait about a minute, then open `https://lossofgenerality.github.io/ccn-keypad/`. The Pages settings screen shows the link once the site is live.

## Updating the page

1. Edit `src/keypad.html` (keys are in the `PADS` table, and the endpoint is `API_URL`).
2. Rebuild: `python3 tools/build_csp.py`. **This step is required:** the security policy only allows a script whose hash matches exactly, so an edited script is blocked until you rebuild.
3. Upload the new `index.html` (and `src/keypad.html`) with **Add file → Upload files** and commit.

If you change `API_URL` to a different host, also change `API_HOST` in `tools/build_csp.py`, or the browser will block the request.

## Security

- **Content-Security-Policy, hash-based.** Only the page's own script and stylesheet run. Everything else is blocked except Google Fonts and connections to `www.wolframcloud.com`. A nonce isn't used because it only works when a server makes a fresh one for every request, and GitHub Pages serves static files.
- No `innerHTML`, no `eval`, no inline event handlers. Input and replies only go into text-box values.
- Fetch sends no cookies (`credentials: "omit"`), no referrer, refuses redirects, and times out after 20 s.
- Input is limited to 5,000 characters and the reply to 100,000.
- Nothing is stored in the browser. Opened files are checked before they are drawn, and the Selection panel is built with DOM calls, not `innerHTML`.

## Notes on the API reply

The endpoint currently returns its text double-encoded and wrapped in Wolfram escape names (for example `\[CapitalATilde]\[Cent]…` for ⊕). The page decodes this. Returning the Association directly from the `APIFunction`, or using `ExportForm[…, "JSON"]` instead of `ExportString`, should fix it on the server side.

The page also runs as a claude.ai artifact. There, direct `fetch` to other sites is blocked, so it sends the same POST through the viewer's Wolfram connector instead.

© Computational Classnotes · CC BY-NC-SA 4.0
