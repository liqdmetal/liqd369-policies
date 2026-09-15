# liqd369 privacy policies

Static privacy-policy pages for the liqd369 offline word-game apps:

- [Tile Coach](tile-coach.html)
- [Anagram Wizard](anagram-wizard.html)
- [Daily Word](daily-word.html)

The live site is published at <https://liqdmetal.github.io/liqd369-policies/> using GitHub Pages.

## Ownership and contact

- Developer/publisher: **liqdmetal**
- Privacy contact: <liqdmetal369@pm.me>
- Current policy version: **1.1**
- Current effective date: **September 15, 2026**

## Local validation

The repository has no runtime dependencies. Run:

```bash
python3 validate.py
```

The validation script checks the required pages, required metadata, internal links, and the hosting/privacy disclosures that must remain on each policy page. Run it locally before publishing changes.

## Release checklist

Before publishing an app or changing an app build:

1. Verify the policy matches the actual permissions, network behavior, SDKs, storage, backup rules, and platform transfer behavior in the released builds.
2. Keep Google Play Data Safety, Apple App Privacy details, store metadata, in-app policy links, and these pages synchronized.
3. Reconfirm the general-audience target-audience declaration and update the policy if the apps become child-directed or collect data from children.
4. Update the policy version, effective date, and change history for material changes.
5. Run `python3 validate.py` and test every live URL over HTTPS.
6. Review changes before publishing; the policy pages should not be changed directly without checking the corresponding app release.

## Hosting note

GitHub Pages is a third-party hosting service. GitHub documents that visitor IP addresses are logged and stored for security purposes. The app policies distinguish that website hosting activity from the offline apps' local-only data handling.

## Word-list attribution

Where an app bundles the ENABLE word list, retain the source attribution in the app and its documentation. The ENABLE documentation releases the master list into the public domain and asks game designers to credit its originators.
