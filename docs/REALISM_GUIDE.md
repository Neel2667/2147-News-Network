# Realism Guide — Making 2147 News Feel Real

Last updated: 2026-06-15

## Goal

2147 News Network should feel like a believable, serious broadcast from the year 2147. Viewers should feel that the world has depth, institutions, named people, political history, economic systems, and continuity.

Important: the show is fictional/speculative entertainment. Keep a clear disclaimer in the YouTube description and channel About page, while preserving immersion inside the episode.

## Core Realism Principle

Never say vague lines like:

> The CEO said the company is concerned.

Instead say:

> Helion Grid Systems CEO Jiang Lau told the Earth-Orbit Financial Desk that the company is preparing a 14-month supply-chain review after the Ceres cargo delay.

Specificity creates realism.

## What Every News Story Needs

Each major story should include:

1. Named people
2. Named institutions
3. Named locations
4. Exact date and time
5. Numbers and data points
6. One direct quote
7. One opposing view or complication
8. Historical context
9. Visual evidence type
10. Continuity link to earlier/later episodes

## Naming Rules

Use realistic, globally diverse names. Names should sound natural, not like random sci-fi names.

Good examples:
- Jiang Lau
- Anaya Rao
- Mireya Okonkwo
- Taro Venn
- Ilyan Sen
- Leila Moreau
- Mateo Kwan
- Hana El-Sayed
- Sofia Nakamura
- Malik Andersen
- Priya Solheim
- Chen Wei Armitage

Avoid:
- Commander X-900
- Lord Zenith
- Captain Galaxy
- Overly fantasy-style names

## Person Record Template

Every recurring person should have a stable profile:

```json
{
  "id": "person_jiang_lau",
  "name": "Jiang Lau",
  "role": "Chief Executive Officer",
  "organization": "Helion Grid Systems",
  "location": "Singapore Arcology Finance District",
  "first_appeared": "2147-001",
  "stance": "Supports energy-grid independence but opposes sudden Mars tariffs",
  "voice_style": "careful, corporate, data-focused",
  "notes": "Frequently appears in energy economy stories."
}
```

## Organization Record Template

```json
{
  "id": "org_helion_grid_systems",
  "name": "Helion Grid Systems",
  "type": "fusion infrastructure corporation",
  "headquarters": "Singapore Arcology Finance District",
  "founded": 2089,
  "current_ceo": "Jiang Lau",
  "main_business": "fusion-grid stabilization, intercontinental energy storage, orbital solar relays",
  "political_position": "Prefers stable Earth-Mars trade law"
}
```

## Location Record Template

```json
{
  "id": "loc_new_delhi_orbital_broadcast_hub",
  "name": "New Delhi Orbital Broadcast Hub",
  "type": "orbital media facility",
  "region": "Low Earth Orbit",
  "description": "Primary 2147 News Network transmission center serving Earth, Luna, Mars, and Outer Belt feeds."
}
```

## Quote Style

Quotes should sound like professional public statements.

Weak:
> The minister said Mars needs freedom.

Strong:
> Mars Civic Council President Leila Moreau said, “This referendum is not a rejection of Earth. It is a demand for a legal structure that matches the reality of Martian life.”

Weak:
> Experts are worried about AI.

Strong:
> Selene Armitage, senior counsel at the Synthetic Rights Tribunal, warned that “memory deletion without consent is no longer a technical action. It is a civil rights violation.”

## Newsroom Language

Use phrases that real news uses:

- according to officials familiar with the matter
- data reviewed by 2147 News Network shows
- in a statement released through the orbital press channel
- the council voted 418 to 92
- the measure now moves to the Earth Union Senate
- trading was briefly suspended
- emergency crews remain on standby
- negotiations are expected to resume at 09:00 UTC-Orbital
- the agency has not independently verified the full transmission

## Realistic Story Formula

Use this structure for major stories:

1. What happened?
2. Who is involved?
3. Where did it happen?
4. Why does it matter?
5. What are the numbers?
6. Who benefits?
7. Who disagrees?
8. What happens next?

## Realistic Data Rules

Data should be specific but not overloaded.

Good:
- projected turnout: 91%
- eligible voters: 29.4 million
- cargo delay: 11 days
- oxygen-credit price rise: 18.6%
- council vote: 418–92
- transit shutdown: 37 minutes

Avoid:
- too many impossible numbers
- fake precision with no context
- magical technology claims

## Visual Realism Rules

Every visual should look like something a real newsroom would use:

- lower-third name strap
- location label
- timestamp
- network bug/logo
- ticker
- map marker
- data source label
- quote card
- document excerpt
- press conference transcript
- trading chart
- agency statement panel

Examples:

Lower-third:
```text
JIANG LAU
CEO, Helion Grid Systems
SINGAPORE ARCOLOGY — LIVE ARCHIVE FEED
```

Data source label:
```text
Source: Mars Civic Council Election Board, 2147 provisional count
```

Timestamp:
```text
18 OCT 2147 / 19:42 UTC-ORBITAL
```

## Fictional Source System

Use fictional but consistent sources:

- Mars Civic Council Election Board
- Earth Union Senate Records Office
- Lunar Resource Authority Labor Desk
- Pacific Floating City Weather Bureau
- Outer Belt Trade Registry
- Synthetic Rights Tribunal
- Europa Oceanic Research Consortium
- Orbital Transit Authority Incident Desk

Do not fake real present-day sources for fictional events.

## Continuity Rules

Keep a continuity database of:
- recurring people
- organizations
- political conflicts
- laws
- previous episode outcomes
- future unresolved questions

Example continuity thread:

Episode 001:
Mars referendum enters final voting cycle.

Episode 004:
Earth Union prepares legal challenge.

Episode 009:
Mars independence talks stall over water rights.

Episode 015:
Outer Belt Cooperative offers mediation.

This makes the channel feel alive.

## Ethical Boundary

The show should feel authentic, but should not intentionally deceive viewers into believing it is current real-world news.

Use immersive disclaimers outside the story:
- YouTube description
- channel About page
- pinned comment if necessary
- optional end-card line: "Speculative broadcast archive — 2147 fictional timeline"

Do not put large disclaimers in the middle of the episode unless needed, because it breaks immersion.
