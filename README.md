# golf-s72-ring

Real hole-by-hole colours for the golf ring of the **Golf S72 Data+** watch face: birdies (blue), pars (green), bogeys (yellow), double bogeys or worse (red), from your Garmin Connect account. Free, 5 minutes, all in your browser.

## 4 steps, once

1. **GitHub account**: free at [github.com/signup](https://github.com/signup) (email only).
2. On this page, click **Use this template > Create a new repository**. Name: `golf-s72-ring`, **Public**, then *Create repository*.
3. In your new repository: **Settings > Secrets and variables > Actions > New repository secret**, twice:
   - Name `GARMIN_EMAIL`, secret: your Garmin Connect email
   - Name `GARMIN_PASSWORD`, secret: your Garmin Connect password
4. On your phone, **Connect IQ app > your watch > Watch faces > Golf S72 Data+ > Settings**:
   - Golf ring: *Full data*
   - Personal code: `your-github-name/golf-s72-ring`

That's it. Within 30 minutes your ring shows your last round, then updates after each new round.

## Good to know

- Secrets are encrypted by GitHub: nobody can read them, not even you. Only the counts are published in `golf.json` (no course, date or place).
- Your password is used once; afterwards a renewed login token is kept in the private cache of your repository.
- Garmin has no public golf API: this uses the unofficial library [python-garminconnect](https://github.com/cyberjunky/python-garminconnect).
- If your Garmin account asks for a code by email or SMS at login, use the token instead of step 3: in your repository, **Code > Codespaces > Create codespace on main**, type `pip install garminconnect==0.3.20` then `python get_token.py`, and put the line it prints in a secret named `GARMIN_TOKENS`.

## En français

1. Compte GitHub gratuit sur github.com/signup.
2. Sur cette page : **Use this template > Create a new repository**, nom `golf-s72-ring`, **Public**.
3. Dans votre dépôt : **Settings > Secrets and variables > Actions > New repository secret** : `GARMIN_EMAIL` (votre adresse Garmin Connect) et `GARMIN_PASSWORD` (votre mot de passe).
4. Appli Connect IQ, réglages du cadran : Rond golf = *Données complètes*, Code personnel = `votre-nom-github/golf-s72-ring`.

Le rond prend vos vraies couleurs dans les 30 minutes.
