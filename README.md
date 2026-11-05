# golf-s72-ring

Full colours, hole by hole, for the golf ring of the **Golf S72 Data+** watch face (Connect IQ store).

Without this, the ring is estimated from the score the watch gives (stroke play or Stableford setting). With it, the ring shows your real last round: eagles (purple), birdies (blue), pars (green), bogeys (yellow), double bogeys or worse (red).

How it works: every 30 minutes, GitHub reads your last round in Garmin Connect (free, on your own GitHub account) and writes `golf.json` here. The watch face reads that file through your phone. Only the counts are published, never the course, date or place. Your Garmin password is never stored: you log in once on your computer and paste a token in a GitHub secret.

## Steps (15 minutes, once)

1. **Fork this repository** to your GitHub account (button *Fork*, top right). Keep the name `golf-s72-ring` and keep it public (the watch reads the file without a password).
2. **Get your Garmin token**, on your computer, with Python 3.10 or newer:
   ```
   pip install garminconnect==0.3.20
   python get_token.py
   ```
   Enter your Garmin Connect email, password, and the code Garmin sends you if asked. Copy the long line it prints.
3. In your fork: **Settings > Secrets and variables > Actions > New repository secret**. Name: `GARMIN_TOKENS`, value: the line from step 2.
4. Tab **Actions**: click *I understand my workflows, go ahead and enable them*, then *Update golf ring* > *Enable workflow* > *Run workflow*. After a minute, `golf.json` shows your last round.
5. On your phone, **Connect IQ app > your watch > Watch faces > Golf S72 Data+ > Settings**:
   - Golf ring: *Full data*
   - Personal code: `your-github-name/golf-s72-ring`

The ring updates within 15 minutes, then after each new round.

Notes: this uses the unofficial library [python-garminconnect](https://github.com/cyberjunky/python-garminconnect), as Garmin has no public golf API. If Garmin ever refuses the login, redo steps 2 and 3. The workflow writes the date once a day so that GitHub keeps it running.

## En français

Même chose en bref : forker ce dépôt (public, même nom), lancer `python get_token.py` sur son ordinateur, coller la ligne obtenue dans le secret `GARMIN_TOKENS` (Settings > Secrets and variables > Actions), activer et lancer *Update golf ring* dans l'onglet Actions, puis dans l'appli Connect IQ, réglages du cadran : Rond golf = *Données complètes*, Code personnel = `votre-nom-github/golf-s72-ring`.
