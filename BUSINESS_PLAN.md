# ViralPulse — AI YouTube Shorts Engine

## Overview
- **Type:** SaaS — AI video generation
- **Status:** MVP built, ready for Railway deployment
- **GitHub:** https://github.com/nova-hermes/viralpulse
- **Based on:** Verticals v3 (MIT license) by Rushindra Sinha

## What It Does
One command: topic in → published YouTube Short out. ~3 min, ~$0.11/video.
Pipeline: Research → Script → Visuals → Voice → Captions → Assemble → Upload

## Pricing Tiers
| Plan | Price | Videos/Month |
|------|-------|-------------|
| Free | $0 | 5 (watermarked) |
| Starter | $29/mo | 30 |
| Pro | $79/mo | 100 |
| Agency | $199/mo | Unlimited |
| Lifetime (owner) | $0 | Unlimited |

## Tech Stack
- **Backend:** FastAPI + SQLite
- **Frontend:** Jinja2 templates + vanilla CSS
- **Pipeline:** Python (Claude/Gemini/GPT + Edge TTS + Whisper + ffmpeg)
- **Deploy:** Railway (Dockerfile ready)

## Owner Account
- Email: doug@viralpulse.com
- Password: viralpulse2026
- Plan: Lifetime (unlimited)

## Revenue Model
1. **SaaS subscriptions** — primary revenue
2. **Faceless YouTube channels** — owner uses the tool to run channels
3. **Done-for-you service** — agency model for high-ticket clients

## Next Steps
- [ ] Deploy to Railway
- [ ] Set up Stripe + NOWPayments billing
- [ ] Create first faceless YouTube channel (proof of concept)
- [ ] Add custom domain (viralpulse.com)
- [ ] Marketing via Twitter watchlist

## Cost Structure
- Video generation: $0.04-0.11 per video (depending on config)
- Free tier: Ollama + Edge TTS + Pexels = $0.00
- Hosting: ~$5/mo on Railway
