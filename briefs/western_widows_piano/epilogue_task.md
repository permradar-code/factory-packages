# Epilogue add-on (after C38, before N10)

1. Narration: `narration/N09b.txt`, voice Bill:
   `python tts_elevenlabs.py --voice <Bill ID> --only N09b`
   (copy N09b.txt into your local narration folder first). Push audio/narration/N09b.mp3 + N09b.alignment.json.
2. Images (ChatGPT, film look — NOT the bright thumbnail look: photorealistic, 1879 Colorado, natural light, muted warm tones, 35mm grain, 16:9, no text). Use the character refs.
   - I70: autumn wedding outside a small white wooden frontier church, golden aspens; Clara (refs) in a simple ivory 1870s dress with a small bouquet of wildflowers, Mercer (refs) in a clean dark suit, hat in hand; townspeople smiling and applauding; Agatha in the crowd, for once smiling.
   - I71: Lily (refs) in a pale yellow dress walking ahead on a dirt path, scattering wildflower petals from a small basket, smiling, church and aspens behind.
   - I72: night, the Whitmore parlor by lamplight: Clara at the piano laughing softly, Mercer standing beside her singing with his eyes closed, Lily asleep on a chair with her rag doll.
   Max 2 regenerations each. Save visuals/images/I70.png, I71.png, I72.png (full resolution), push.
3. Historical fix (Colorado became a state in 1876, so "Colorado Territory, 1879" is wrong):
   `python tts_elevenlabs.py --voice <Bill ID> --only N01_fix` — text in `narration/N01_fix.txt`
   ("Cedar Bluff, Colorado. October, 1879."), same voice settings as N01. Push audio/narration/N01_fix.mp3 + N01_fix.alignment.json.
   Do NOT regenerate the full N01. I will splice it in during montage.
