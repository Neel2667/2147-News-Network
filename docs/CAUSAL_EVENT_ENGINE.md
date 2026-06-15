# Causal Event Engine — 2147 News Network

Last updated: 2026-06-15

## Purpose

The 2147 News Network should not feel like disconnected random fictional headlines. It should feel like a living world where every story has causes, consequences, reactions, secondary effects, and long-term continuity.

Instead of simply inventing a headline, the system should analyze the current state of the fictional world and ask:

1. What happened before this?
2. Who is affected?
3. Who benefits?
4. Who loses?
5. Who responds publicly?
6. What policy, market, social, legal, or environmental ripple follows?
7. Which new event should happen next?

This creates a chain of believable future news.

## Core Idea

News should be generated from **event causality**, not isolated imagination.

Example chain:

```text
Oxygen prices rise on Luna
  ↓
Lunar miners begin strike
  ↓
Helium-3 shipments are delayed
  ↓
Earth fusion-grid companies warn of price instability
  ↓
Earth Union Senate opens emergency energy hearing
  ↓
Mars uses crisis to argue for independent energy treaties
  ↓
Earth-Mars political tensions increase
```

Now every new episode can be based on the ripple of earlier episodes.

## Event Object Schema

Each event should be stored as structured data.

```json
{
  "id": "event_2147_001_mars_referendum_final_cycle",
  "date": "2147-10-18",
  "time": "19:42 UTC-Orbital",
  "title": "Mars enters final voting cycle in independence referendum",
  "category": "space_politics",
  "location_id": "loc_valles_marineris_capital_zone",
  "actors": [
    "org_mars_civic_council",
    "org_earth_union_senate",
    "person_leila_moreau"
  ],
  "summary": "Mars begins the final voting cycle on whether to become the first independent off-world republic.",
  "causes": [
    "event_2136_oxygen_credit_protests",
    "event_2142_mars_trade_autonomy_dispute"
  ],
  "direct_effects": [
    "Earth Union legal review begins",
    "Mars settlement markets suspend long-term infrastructure contracts",
    "Outer Belt Cooperative offers to observe talks"
  ],
  "ripple_seeds": [
    {
      "type": "political_response",
      "probability": 0.9,
      "delay_days": 2,
      "description": "Earth Union Senate schedules emergency hearing on Mars sovereignty."
    },
    {
      "type": "market_reaction",
      "probability": 0.7,
      "delay_days": 1,
      "description": "Energy and cargo markets react to Earth-Mars legal uncertainty."
    },
    {
      "type": "labor_action",
      "probability": 0.4,
      "delay_days": 7,
      "description": "Lunar labor unions link oxygen-credit demands to Mars autonomy debate."
    }
  ],
  "status": "active",
  "importance": 10,
  "episode_refs": ["2147-001"]
}
```

## Event Types

Use these event types to keep stories varied:

- political_decision
- election_result
- legal_challenge
- court_ruling
- corporate_statement
- market_reaction
- labor_action
- disaster
- scientific_discovery
- infrastructure_failure
- diplomatic_response
- public_protest
- policy_change
- security_incident
- cultural_reaction
- technology_release
- environmental_shift

## Ripple Categories

Every event should create ripples in several dimensions.

### Political Ripple

Examples:
- emergency senate session
- diplomatic protest
- new treaty proposal
- regional autonomy demand
- opposition leader statement

### Economic Ripple

Examples:
- commodity price changes
- trading pause
- supply-chain delay
- corporate warning
- insurance rate increase

### Social Ripple

Examples:
- protests
- migration applications increase
- worker strikes
- public opinion shift
- cultural backlash

### Legal Ripple

Examples:
- court filing
- tribunal ruling
- regulatory investigation
- consent law debate
- rights petition

### Infrastructure Ripple

Examples:
- transit shutdown
- grid instability
- communication delay
- habitat maintenance emergency
- port congestion

### Scientific Ripple

Examples:
- probe confirmation
- peer review dispute
- research funding shift
- unknown signal analysis
- safety protocol update

## Event Lifecycle

Each event moves through stages:

```text
seed → developing → breaking → confirmed → reaction → consequence → resolved/archive
```

### Seed

A possible future development.

### Developing

Early reports, not fully confirmed.

### Breaking

Major event happening now.

### Confirmed

Officials, records, or data confirm the event.

### Reaction

Politicians, companies, agencies, and citizens respond.

### Consequence

The event creates a new policy, strike, market movement, conflict, or discovery.

### Resolved / Archive

The story becomes background context for future events.

## Episode Generation Method

For each new episode, the app should:

1. Load the current world state.
2. Find active unresolved events.
3. Score events by importance, freshness, and visual potential.
4. Select one main story.
5. Generate 3–5 ripple events as secondary headlines.
6. Add at least one background event from the archive for context.
7. Create quotes from affected actors.
8. Create visual scene plans based on event category.
9. Update the world state with new consequences.

## Event Scoring Formula

Suggested scoring:

```text
score = importance + urgency + number_of_affected_actors + visual_potential + continuity_value - repetition_penalty
```

Factors:
- importance: 1–10
- urgency: 1–10
- affected actors: 1–5
- visual potential: 1–10
- continuity value: 1–10
- repetition penalty: 0–5

## Example: Mars Referendum Ripple Tree

```text
EVENT: Mars referendum final voting cycle
CAUSES:
- 2136 oxygen-credit protests
- 2142 trade autonomy dispute
- 2145 Earth-Mars tax arbitration collapse

DIRECT RIPPLES:
- Earth Union Senate schedules sovereignty hearing
- Mars infrastructure bonds fluctuate
- Lunar unions demand oxygen-credit protections
- Outer Belt Cooperative offers observer mission

SECONDARY RIPPLES:
- Helion Grid Systems warns of energy price instability
- Orbital Transit Authority prepares cargo rerouting plan
- Synthetic Rights Tribunal asks if AI residents of Mars can vote

LONG-TERM RIPPLES:
- Mars-Earth water rights negotiation
- independence treaty challenge
- Outer Belt recognition debate
```

## Why This Feels Real

Real news is rarely random. It is usually a visible moment in a longer chain.

A real-feeling story includes:
- before-event context
- named decision makers
- institutional reaction
- economic impact
- public response
- unresolved next step

This system ensures that every 2147 News Network episode feels like one chapter in a living timeline.

## Editorial Rule

When writing a story, always include this line internally:

```text
This event exists because: [cause event IDs]
This event will likely cause: [ripple event IDs or ripple seeds]
```

If a story has no cause and no consequence, it should not be a main story.
