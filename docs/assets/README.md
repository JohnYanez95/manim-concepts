# docs/assets

`welcome.gif` is the one committed render — the front page's animation,
produced by the repo itself. To regenerate after editing
`welcome_scene.py` (or when a new series joins its hand-listed row — the row lists
series, not topics):

```bash
uv run python docs/assets/welcome_scene.py -q draft
ffmpeg -y -i media/videos/welcome_scene/480p15/01_Welcome.mp4 \
  -vf "fps=12,scale=720:-1:flags=lanczos,split[s0][s1];\
[s0]palettegen=max_colors=96[p];[s1][p]paletteuse=dither=bayer" \
  docs/assets/welcome.gif
```

Keep it under the 512 KB large-file hook; the palette pass above lands
around 340 KB.
