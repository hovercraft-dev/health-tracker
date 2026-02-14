# Hovercraft Reset - Knowledge Extract - 2026-02-12

## Overview
Distilled actionable knowledge from the Hovercraft Reset Project conversations (November 2025 - February 2026). Focus: body recomposition, kettlebell programming, systematic tracking, and sustainable execution.

---

## Training Frameworks

### The A-B-C Weekly Structure (Validated & Optimised)

**Core Principle:** Separation of stressors prevents interference and enables progress during calorie deficit.

**Day A - Heavy Strength Grind (45-60 min)**
- **Primary:** Double Military Press - Ladder progression
  - Current: 28kg ladders (1,2,3,4) × 6-13 sets
  - Progression: Add ladders → Add rungs → Increase weight
- **Secondary:** Double Front Squat - Wave loading
  - Week 1: 32kg 5×5 (volume)
  - Week 2: 40kg 5×3 (intensity)
  - Prevents CNS burnout in deficit
- **Tertiary:** Heavy rows for structural balance

**Day B - Power & Conditioning (45-60 min)**
- **Primary:** Two-Hand Swings - A+A Protocol
  - 40kg, 5 reps × 30-40 sets
  - Full recovery between sets (talk test)
  - Power > exhaustion
- **Secondary:** Turkish Get-Ups
  - 32kg/40kg, 5×2
  - Quality over quantity
- Key insight: Short bursts + long rest = power endurance without lactic interference

**Day C - Metabolic Density (20-25 min)**
- **The Giant Killer Complex:**
  - 1 Clean (both arms)
  - 2 Front Squats
  - 3 Presses (each arm = 6 total)
  - = 1 round
- Current: 24kg, 19-22 rounds in 20 minutes
- Progression: Volume first (22+ rounds), then increase weight to 28kg
- Accept drop in rounds (12-15) when weight increases

**Weekly Frequency:**
- Sustainable baseline: **3 sessions/week**
- Optional 4th session: Rotate Day A or C
- Optional: Weighted vest walks time permitting
- Lesson: 3×/week prevents "it worked so well that I stopped doing it" trap

### Progression Protocols

**Ladder Progression (for presses):**
```
Set 1: 1 press/arm
Set 2: 2 presses/arm
Set 3: 3 presses/arm
Set 4: 4 presses/arm
= 1 ladder (10 presses/arm total)

Progress: Add ladders → Add rungs → Increase weight
Example: 6 ladders → 7 ladders → add 5th rung → move to 32kg
```

**Wave Loading (for squats):**
```
Week 1 (Volume): 32kg 5×5
Week 2 (Intensity): 40kg 5×3
Week 3 (Volume): 32kg 6×5
Week 4 (Intensity): 40kg 6×3
```
- Natural deload built in
- Both heavy and volume stimulus
- Ideal for deficit work

**Equipment Progression Path:**
- Current working weights: Double 28kg
- Testing phase: Double 32kg (occasional low reps)
- Future (requires surplus): Double 40kg
- Rule: Master current weight 8-12 weeks before advancing
- Jump size matters: 28kg → 32kg = reasonable (4kg/bell), 32kg → 40kg = too large (8kg/bell)

**Psychological Reward System:**
- 36kg pair purchase at 100kg milestone
- 48kg Beast at 95kg maintenance goal
- Equipment as progress markers, not prerequisites

### Autoregulation Rules

**Stop Criteria:**
- Stop set when bar speed slows (grind = last rep)
- Stop session if form degrades
- Stop progression if strength drops >10%

**RPE Guidelines:**
- Day A: Sets at RPE 7-8 (2-3 reps in reserve)
- Day B: Swings at RPE 6-7 (powerful, not fatiguing)
- Day C: Overall RPE 8-9 (hard but sustainable)

**Critical Insight:** In deficit, maintain > progress = winning strategy. Don't chase PRs.

**Practical Example of Autoregulation:**
- Issue: Back discomfort after poorly-timed weighted vest walk
- Response: Switched from planned presses to A+A swings
- Outcome: Maintained training stimulus without aggravating injury
- Lesson: Flexibility within structure prevents derailment

---

## Nutrition Optimisation

### Macro Framework (Deficit Phase)

**Daily Targets:**
- Calories: 2,300-2,500 kcal
- Protein: 180-200g minimum (current average: 200g)
- Carbs: ~205g
- Fat: ~84g

**Deficit Sweet Spot:**
- Below 2,200 kcal = strength drops, adherence suffers
- 2,300-2,500 kcal = sustainable 0.5-0.8kg/week loss
- Above 2,800 kcal untracked = historical drift pattern

### Repeatable Meal Strategy

**Core Principle:** Minimise decision fatigue through consistent food choices.

**Protein Sources:**
- Tesco meatballs (precise portion control)
- Chicken breast
- Steak
- Organ meats (liver/kidneys) via ice cube system
- Sardines
- Eggs
- Fage 0% Greek yoghurt
- Homemade kefir

**Carbohydrate Base:**
- Boiled potatoes (high satiety during deficit)
- Oats (workout days)
- White rice (temporarily avoided due to satiety concerns)

**Vegetables:**
- Kale, spinach, bell peppers, mushrooms
- Consumed for micronutrient density

### The Liver Ice Cube System

**Innovation:** Real-food supplementation approach

**Process:**
1. Batch-cook organ meats (liver/kidneys)
2. Portion into ice cube trays
3. Freeze for portion-controlled "supplements"
4. Add to meals as micronutrient boost

**Benefit:** Masterjohn-inspired micronutrient density without pill fatigue

### Transition to Maintenance (Future)

**Phase 2 Adjustments (April 2026, ~100kg):**
- Increase to 2,500-2,700 kcal
- Maintain 180-200g protein
- Slower loss rate
- More strength emphasis in training

**Phase 3 - Maintenance (July 2026+, 92-95kg):**
- Small surplus: 2,800-3,000 kcal
- Continue protein targets
- Progressive overload focus
- Equipment goal: Double 40kg proficiency

---

## Data Tracking Systems

### Core Metrics

**Primary Indicators:**
- **Weight:** Daily (after bathroom, before eating)
- **Waist:** Weekly minimum (more reliable than scale for body composition)
- **Weight-to-Waist Ratio:** Body composition proxy

**Validation Example:**
- 2012: 103kg @ 108.6cm waist = Higher body fat
- 2026: 106kg @ 102cm waist = More muscle, less fat
- **8.5% better ratio** = successful recomposition

**Secondary Metrics:**
- Hips measurement
- Training performance (weights, reps, rounds)
- Sleep quality (1-10 scale)
- Blood pressure (added after specialist insight)

### Progressive Web Apps for Mobile Data Entry

**Problem:** Manual Google Sheets entry on mobile is tedious

**Solution:** Two PWAs hosted on GitHub Pages

**Architecture:**
```
PWA (client) → Apps Script endpoint → Google Sheets (backend)
```

**Implementation:**
- Body Tracker: hovercraft-dev.github.io/body-tracker
- Wife's Tracker: hovercraft-dev.github.io/maz-tracker
- Separate URLs instead of authentication (reduces friction)
- Direct integration with existing Google Sheets tracking

**Design Decisions:**
- Clean, athletic theme for personal tracker
- Warm wellness aesthetic for wife's tracker
- Medication tracking via checkboxes
- Optional collapsible notes for symptom tracking

**Technical Lessons:**
- CORS issues resolved using 'no-cors' mode
- Apps Script deployment requires recreation for URL changes
- Basic Git workflow: commit, push to main branch, auto-deploy
- iPhone PWA: Safari → Share → Add to Home Screen

### Google Sheets Visualisation

**Setup:**
- Automated charts with trendline projections
- 30-day and 60-day forecast windows
- Extends through May 2026
- Auto-updates as new data logged

**Psychological Benefit:**
- Removes daily scale obsession
- Provides trajectory confidence
- Visual accountability without micromanagement

### Token Efficiency Strategy

**Problem:** Large PDF analysis consumed excessive tokens

**Solutions:**
1. CSV exports from individual sheet tabs (not full workbook)
2. Separate conversations for different topics
3. Markdown documentation as primary reference
4. Only reference PDFs when absolutely necessary

**File Structure:**
- `01_Core_Reference.md` - Full analysis and history
- `02_Program_Library.md` - Detailed programme explanations
- `03_Quick_Start_Guide.md` - Daily reference
- `HOVERCRAFT_RESET_MANIFESTO.md` - Philosophy and principles

---

## Health Management

### Eye Condition Monitoring (Moorfields Clinic)

**Background:** Condition monitored since 2007, requiring daily drops and 2016 surgical intervention

**Recent Development (February 2026):**
- New medication working effectively
- Surgery avoided
- Specialist noted correlation between blood pressure and condition

**Action Taken:**
- Added blood pressure monitoring to tracking protocol
- Purchased clinically validated Omron upper arm monitor
- Relevant for both health optimisation and aviation medical renewal (May/June)

**Training Considerations:**
- Heavy bilateral lifts with breath-holding under load may impact pressure
- Modification: Reduce prolonged Valsalva during deficit phase
- Maintain strength work without extreme loading

### Body Composition and Health Correlation

**Evidence-Based Insight:**
- Every 10% body weight loss correlates with measurable pressure improvements
- Current progress: 7.7% reduction (114.8kg → 106kg)
- Represents meaningful therapeutic benefit beyond aesthetics

### Sleep Optimisation During Deficit

**Problem:** Sleep disruption 6 weeks into deficit (earlier wake times, difficulty returning to sleep)

**Troubleshooting Process (systematic, one variable at a time):**
1. Initially tried magnesium glycinate (400mg elemental)
   - Result: Deep initial sleep, middle-of-night waking
2. Reduced to 100mg elemental magnesium
   - Result: Still causing 6-hour wake (vs 8-hour goal)
3. Eliminated magnesium entirely
4. Tried English Tea Shop organic chamomile blend (chamomile, lavender, hop leaves, valerian, lemon balm)
   - Result: 7 hours quality sleep

**Solution:**
- Herbal tea blend more effective than high-dose magnesium
- Ordered loose leaf holy basil tea for continued experimentation
- Aircraft troubleshooting methodology: change one variable, track results

**Physiological Context:**
- Some sleep disruption 6 weeks into sustained deficit is normal
- Hormonal adaptations to energy restriction
- Not a fundamental problem, just requires right approach

### Aviation Medical Requirements

**Class 1 Medical Renewal:** May/June 2026

**Relevant Factors:**
- Previous blood pressure: 140 systolic (approaching concerning levels)
- Current weight loss likely improving cardiovascular markers
- Eye condition monitoring aligned with medical requirements
- Strength training validation: Specialist initially hesitant ("too old" at 45), became supportive when understanding kettlebell methodology vs heavy barbell work

---

## Psychological & Behavioural Frameworks

### The Paper Towel Roll Effect

**Analogy:** Fat loss from larger frame produces less visible change initially, becomes dramatically apparent as body leans out.

**Practical Milestones:**
- **105kg → 100kg:** People start noticing (facial leanout, clothing fit)
- **100kg → 95kg:** Dramatic transformation becomes undeniable
- **Current (106kg):** Changes not yet at "wow level" despite 9kg loss
- Muscle preservation during deficit will result in more athletic appearance than previous weight loss experiences

### Water Retention vs Fat Loss Plateaus

**Critical Insight:** Temporary scale fluctuations after social events ≠ actual fat loss plateau

**Decision Framework:**
- Scale up 1-2kg after social event → Water retention, maintain course
- Waist measurement unchanged → Confirmation of water retention
- Don't abandon plan based on temporary fluctuations

**Validation:**
- User broke through 105kg shortly after understanding this pattern
- Achieved 101cm waist (out of high cardiovascular risk category)

### The "It Worked So Well That I Stopped Doing It" Trap

**Historical Pattern:**
- 2013: Reached 80kg with visible muscle
- Subsequent drift to 115kg during "maintenance mode without structure"
- 91kg (2016) → 99kg (2017) → 115kg (2023) during "freestyle" periods

**Solution:**
- Active structure required forever, not passive drift
- 3 sessions/week sustainable baseline (vs ambitious 4+ that leads to burnout)
- Maintenance phase requires **different** structure, not absence of structure

**Future Maintenance Programming (August 2026+):**
- A-A-B structure (two strength days, one power day)
- Drops metabolic density work once at goal weight
- Systematic progression towards double 40kg work over 18-24 months

### Red Flags (Immediate Action Required)

🚨 **Strength drops >10% on key lifts** → Increase calories 200-300, add rest day  
🚨 **Missing multiple workouts** → Schedule or recovery problem  
🚨 **Sleep problems persist >2 weeks** → Address immediately  
🚨 **Chronic fatigue/irritability** → Deficit too aggressive  
🚨 **Tracking gaps >3 days** → Drift begins here

---

## Project Setup & Documentation

### Markdown Documentation Strategy

**Purpose:** Create living reference system that evolves with programme

**File Structure:**
1. **Core Reference** - Historical analysis, lessons learned, risk management
2. **Programme Library** - Detailed training explanations, progressions
3. **Quick Start Guide** - Daily checklist, workout reference
4. **Manifesto** - Philosophy, principles, non-negotiables (bedroom reference)

**Benefit:**
- Token-efficient (vs repeatedly analysing PDFs)
- Version-controlled via Project files
- Easily updated as milestones reached
- Printable for offline reference

### UK Spelling Preference

**Rationale:** Consistency with personal writing style

**Applied Throughout:**
- Programme (not program)
- Optimisation (not optimization)
- Realise (not realize)
- Behaviour (not behavior)

### Conversation Management

**Strategy:** Separate conversations for different topics

**Categories:**
- Training programming
- Nutrition optimisation
- Health management
- Technical projects (PWAs)
- Data analysis

**Benefit:** Maintains context focus, prevents token bloat, easier to reference specific topics later

---

## Key Decisions Made

### Training
- ✅ 3 sessions/week baseline (not 4)
- ✅ A-B-C structure maintained through deficit
- ✅ No PR chasing during deficit phase
- ✅ Double kettlebells as primary modality
- ✅ Equipment purchases as milestone rewards
- ✅ Master 28kg before progressing to 32kg

### Nutrition
- ✅ 2,300-2,500 kcal deficit range
- ✅ 180-200g protein minimum
- ✅ Repeatable meals to minimise decision fatigue
- ✅ Liver ice cube system for micronutrient density
- ✅ Boiled potatoes as carb staple during deficit

### Tracking
- ✅ Waist measurement more reliable than scale
- ✅ Weight-to-waist ratio as body composition proxy
- ✅ PWAs for mobile data entry
- ✅ Google Sheets with automated visualisations
- ✅ Blood pressure monitoring added

### Health
- ✅ Eye condition improved with new medication
- ✅ Herbal tea more effective than high-dose magnesium for sleep
- ✅ 10% body weight loss as therapeutic target
- ✅ Training modifications to reduce Valsalva during deficit

---

## Lessons Learned

### What Works
1. **Structure > Flexibility** - Every successful phase had a programme
2. **Double Bells = Transformation** - Best results with bilateral loading
3. **Protein Non-Negotiable** - 180-200g/day maintains muscle in deficit
4. **Deficit Sweet Spot** - 2,300-2,500 kcal sustainable, below 2,200 counterproductive
5. **Data Tracking = Accountability** - Every period with logs = progress
6. **Systematic Troubleshooting** - Change one variable at a time

### What Doesn't Work
1. **"Maintenance Mode" Without Structure** - Weight creep inevitable
2. **Chasing PRs in Deficit** - Ego interferes with sustainable progress
3. **Programme Hopping** - Consistency beats creativity
4. **All-or-Nothing Thinking** - Perfect week → blow-up weekend pattern
5. **Jumping Weight Too Fast** - 28kg → 40kg = too large (8kg/bell)

### Critical Insights
- **Body Recomposition is Real:** More muscle at 106kg (2026) than 103kg (2012)
- **Waist > Scale:** More reliable indicator of actual body composition change
- **Strength + Fat Loss Can Coexist:** Maintain current weights = winning in deficit
- **Sleep Disruption at 6 Weeks:** Physiologically normal hormonal adaptation
- **Water Retention ≠ Plateau:** Don't abandon plan based on temporary fluctuations
- **Sustainable Baseline:** 3×/week prevents burnout, 4×/week optional

---

## Templates & Systems Created

### Weekly Training Template (Current - Deficit Phase)
```
Monday: Day C - Giant Killer (24kg, 20 min)
Tuesday: Day A - Strength (28kg ladders, 32kg/40kg squats)
Thursday: Day B - Power (40kg swings A+A, TGUs)
Saturday: Rotate Day A or C
```

### Future Maintenance Template (Post-95kg)
```
Monday: Day A - Strength
Wednesday: Day A - Strength (different focus)
Friday: Day B - Power
Optional: Weighted vest walks
```

### Nutrition Quick Reference
**Protein Priority Foods:**
- Chicken breast, lean beef, fish
- Eggs, Greek yoghurt
- Organ meats (liver ice cubes)
- Sardines
- Protein powder (when needed)

**Calorie Budget:** 2,300-2,500 kcal/day (flexible ±100)

### Weekly Review Checklist (Sunday)
- [ ] Average weight this week vs last week
- [ ] Strength performance (any drops?)
- [ ] Adherence (hit targets how many days?)
- [ ] Sleep quality average
- [ ] Energy levels
- [ ] Adjust if needed: calories ±100-200, extra rest day, deload

### Daily Tracking Checklist
**Morning:**
- [ ] Weight (after bathroom, before eating)
- [ ] Waist (weekly minimum)
- [ ] Sleep quality (1-10)

**Nutrition:**
- [ ] Hit 180-200g protein
- [ ] Stay within 2,300-2,500 kcal
- [ ] Log all food

**Training:**
- [ ] Complete scheduled workout
- [ ] Log exercises, weights, reps/sets
- [ ] Note RPE, energy level

---

## Equipment Reference

### Current Arsenal
- 20kg (pair) - warm-up/technique
- 24kg (pair) - Giant Killer, volume work
- 28kg (pair) - **current working weights** (presses/squats)
- 32kg (pair) - testing phase (occasional low reps)
- 40kg (single) - swings, future squat goal
- 48kg (single) - future power benchmark

### Future Purchases
- **36kg pair** at 100kg milestone (psychological reward)
- **48kg Beast** at 95kg maintenance goal

---

## Success Reminders

1. **You've done this before** (2013: 80kg with visible muscle)
2. **Current body composition > 2012** (more muscle, less fat at same weight)
3. **Deficit = maintain strength, don't chase PRs**
4. **0.5-0.8kg/week loss = perfect pace**
5. **Waist measurement matters more than scale**
6. **14 years of data = clarity** (patterns emerge over months, not days)
7. **Consistency > Perfection** (90% adherence for 6 months > 100% for 2 weeks)

---

## Next Actions

### Immediate (February 2026)
- [ ] Continue current programme through Brazil holiday (late February)
- [ ] Maintain 2,300-2,500 kcal deficit
- [ ] Track blood pressure alongside weight/waist
- [ ] Test herbal tea sleep protocol consistently

### Milestone: 100kg (Target April 2026)
- [ ] Purchase 36kg kettlebell pair (psychological reward)
- [ ] Transition to Phase 2 nutrition (2,500-2,700 kcal)
- [ ] Begin testing double 32kg work more frequently
- [ ] Update markdown documentation

### Milestone: 95kg (Target July 2026)
- [ ] Purchase 48kg Beast
- [ ] Transition to maintenance programming (A-A-B structure)
- [ ] Drop metabolic density work
- [ ] Focus progressive overload towards double 40kg work

---

## References & Tools

**Tracking Systems:**
- Google Sheets: Comprehensive tracking with automated charts
- PWAs: Mobile-friendly data entry (hovercraft-dev.github.io)
- Blood Pressure: Omron upper arm monitor (clinically validated)

**Training Methodologies:**
- RKC/StrongFirst principles
- Pavel Tsatsouline progressions
- A+A Protocol (Al Ciampa)

**Nutrition Approach:**
- Macro-based foundation
- Masterjohn micronutrient principles (organ meats, sardines)
- Repeatable meals for adherence

**Health Monitoring:**
- Moorfields specialist clinic (eye condition)
- Class 1 aviation medical (May/June renewal)

---

**Last Updated:** 2026-02-12  
**Next Review:** After reaching 100kg milestone or significant approach change
