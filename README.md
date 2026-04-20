# ViralPulse

**AI-powered YouTube Shorts engine. Topic in. Published Short out. Any niche. ~$0.11 per video.**

## What It Does

ViralPulse is an open-source AI content engine that transforms any topic into a published YouTube Short in under 3 minutes. One command researches the topic, writes a hook-driven script, generates cinematic b-roll, records a natural voiceover, burns in animated captions, adds background music, generates a thumbnail, and uploads to YouTube.

## Features

- **Niche Intelligence** — 15+ built-in niches (tech, fitness, finance, cooking, true crime, etc.) that shape script tone, visual style, captions, and music
- **Multi-Provider Support** — Claude, Gemini, GPT, Ollama (LLM) + Edge TTS, ElevenLabs, Kokoro (voice) + Gemini Imagen, Replicate, Pexels (visuals)
- **$0.00 Mode** — Run completely free with Ollama + Edge TTS + Pexels
- **Multi-Platform Export** — YouTube, TikTok, Instagram Reels, X
- **Web UI** — Gradio-based interface for non-developers
- **Google Colab** — Zero-install usage

## Quick Start

```bash
pip install viralpulse

# Set up API keys (or use $0.00 mode)
viralpulse setup

# Generate a Short
viralpulse run --topic "Sam Altman just fired 200 safety researchers" --niche tech
```

## Cost Per Video

| Configuration | Cost |
|---------------|------|
| Premium (Claude + Gemini + ElevenLabs) | ~$0.11 |
| Budget (Gemini + Edge TTS) | ~$0.04 |
| Free (Ollama + Pexels + Edge TTS) | $0.00 |

## Pipeline

```
RESEARCH → SCRIPT → VISUALS → VOICE → CAPTIONS → ASSEMBLE → UPLOAD
```

1. **Research** — DuckDuckGo search + web scraping for real facts
2. **Script** — LLM writes 60-90 second hook-driven script
3. **Visuals** — 3-5 AI-generated b-roll frames (9:16 portrait)
4. **Voice** — Text-to-speech voiceover
5. **Captions** — Whisper word-level timestamps, animated highlights
6. **Assemble** — ffmpeg combines everything + music with voice ducking
7. **Upload** — Publishes to YouTube with title, description, tags, thumbnail

## License

MIT

---

*Based on [Verticals](https://github.com/rushindrasinha/youtube-shorts-pipeline) by Rushindra Sinha.*
