---
name: viralpulse
description: "AI-native vertical video engine with niche intelligence. Takes a one-line topic and a niche profile, and outputs a finished YouTube Short/Reel/TikTok with AI-generated b-roll, voiceover, burned-in captions, background music, and thumbnail. Supports multiple LLM providers (Claude, Gemini, GPT, Ollama), TTS providers (Edge TTS, ElevenLabs), and 15+ content niches."
---

# ViralPulse v3

AI-native vertical video engine: topic + niche -> research -> script -> visuals -> voice -> captions -> music -> thumbnail -> upload.

## Commands

```bash
python -m viralpulse run --news "headline" --niche tech
python -m viralpulse run --discover --auto-pick --niche gaming
python -m viralpulse draft --news "headline" --niche finance --provider gemini
python -m viralpulse produce --draft <path> --voice edge
python -m viralpulse topics --niche tech --limit 20
python -m viralpulse niches
```

## Key flags

--niche NAME: Content niche (tech, gaming, finance, fitness, cooking, travel, etc.)
--provider NAME: LLM provider (claude, gemini, openai, ollama)
--voice NAME: TTS provider (edge, elevenlabs, say)
--platform NAME: Target platform (shorts, reels, tiktok, all)
--lang CODE: Language (en, hi, es, pt, de, fr, ja, ko)

## $0.00 mode

python -m viralpulse run --topic "X" --niche tech --provider ollama --voice edge

Docs: https://github.com/nova-hermes/viralpulse
Product: https://viralpulse.com
