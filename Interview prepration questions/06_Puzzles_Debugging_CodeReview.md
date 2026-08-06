# LLD Interview Handbook — Part 6: Interview Puzzles, Debugging Bad Designs, Refactoring Drills

---

## Q51. [Level 3, Debugging] Find the bug: this Singleton is supposed to survive across a multi-process deployment (e.g., 4 Gunicorn workers), but engineers report seeing "different" singleton states per request.

```python
class ConfigManager:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```

**Expected Answer:** This isn't a code bug — it's a **conceptual misunderstanding of Singleton's scope**. Singleton guarantees one instance *per process* (per Python interpreter). With 4 Gunicorn workers, you have 4 separate OS processes, each with its own Python interpreter and its own "singleton" instance — there is no shared memory between them by default. The fix isn't a code change to the Singleton class; it's recognizing that in-process Singleton cannot provide cross-process global state — you need an external shared store (Redis, a database, shared memory segment) for true cross-process singleton-like state.

**Why interviewer asks this:** Classic "candidate assumes Singleton means globally-one-instance-everywhere" trap — a very common real production misunderstanding, especially relevant at companies running horizontally-scaled services (Uber, Amazon, Flipkart).

**Common Mistakes:**
- Trying to "fix" this with more locking/threading code (misses that it's a process-boundary issue, not a threading issue)
- Not knowing that separate processes don't share Python object memory

**Follow-ups:** "How would you actually share config across all 4 workers?"

**Best Follow-up Answer:** Use an external, out-of-process store as the source of truth (Redis, a config service, or environment variables/files reloaded per worker) — each worker's in-process object becomes a *cache* of that shared external state, not the sole source of truth; the "singleton" pattern still applies *within* each process for local access convenience, layered on top of the shared external store.

---

## Q52. [Level 3, Debugging] Find the bug in this Observer implementation — subscribers stop receiving updates after a while in production, but work fine in local testing.

```python
class Subject:
    def __init__(self):
        self._observers = []
    def subscribe(self, observer):
        self._observers.append(observer)
    def notify(self, event):
        for obs in self._observers:
            obs.update(event)

class UIWidget(Observer):
    def update(self, event):
        self.refresh_display(event)
```

Client code:
```python
def register_widget(subject):
    widget = UIWidget()
    subject.subscribe(widget)
```

**Expected Answer:** `widget` is a local variable inside `register_widget()` with no reference kept outside the function except the one held by `subject._observers` (a *strong* reference in this case, so this particular snippet wouldn't actually be garbage-collected — but the intended "gotcha" pattern here, extremely common in real systems using *weak* references for observers to avoid memory leaks, is the inverse bug). The realistic production version of this bug: if `Subject` holds observers via `weakref.WeakSet`/`weakref.ref` (a legitimate technique to avoid Subject keeping Observers alive forever/causing memory leaks), and the client doesn't keep its own strong reference to `widget`, the widget gets garbage collected and silently stops receiving updates — "works in local testing" because in a quick test script, references often coincidentally stay alive slightly longer or the GC hasn't run yet, while in a longer-running production process, GC eventually collects the widget.

**Why interviewer asks this:** Tests advanced understanding of the *lifetime* interaction between Observer pattern and garbage collection — a nuanced, easy-to-miss production bug class ("observers silently stop working") that's genuinely happened in real codebases using weak references.

**Common Mistakes:**
- Assuming this specific code as written has this bug (it technically doesn't, since it's a strong reference) — the value is in recognizing *when* this class of bug occurs (weak references) and being able to discuss it
- Not knowing weak references exist as a legitimate Observer memory-leak mitigation technique

**Follow-ups:** "Why would you use weak references for observers in the first place?"

**Best Follow-up Answer:** To avoid the Subject inadvertently keeping every subscribed Observer alive forever (a memory leak) when observers should be allowed to be garbage collected once nothing else references them (e.g., a UI widget that's been closed/destroyed shouldn't be kept alive just because it forgot to unsubscribe) — but this trades one bug class (leaks) for another (silent early collection), which is why explicit `unsubscribe()` lifecycle management is often the safer, more predictable choice over relying on weak references and GC timing.

---

## Q53. [Level 4, Debugging] Find the design flaw: this Strategy-based discount system silently applies the WRONG discount under a specific ordering of operations.

```python
class DiscountContext:
    def __init__(self):
        self.strategy = None

    def set_strategy(self, strategy):
        self.strategy = strategy

    def apply_discount(self, amount):
        return self.strategy.calculate(amount)

context = DiscountContext()
context.apply_discount(100)   # called before set_strategy()
```

**Expected Answer:** `self.strategy` defaults to `None` and is only set via a separate `set_strategy()` call (classic setter-injection pitfall from Q33) — nothing prevents `apply_discount()` from being called before a strategy is ever set, causing an `AttributeError: 'NoneType' object has no attribute 'calculate'` (or worse, in a looser language, silently returning something nonsensical instead of failing clearly). Fix: require the strategy at construction time (constructor injection) so the object can never exist in an invalid, strategy-less state — "make illegal states unrepresentable."

**Why interviewer asks this:** Direct, hands-on test of the constructor-vs-setter-injection trade-off discussed in Q33 — shows the abstract principle causing a concrete, reproducible bug.

**Common Mistakes:**
- Fixing it with a `None` check + default fallback strategy inside `apply_discount()` (band-aid — still allows constructing an invalid object silently, just delays the failure/masks the bug instead of preventing it)
- Not connecting this back to "fail fast" design principle

**Follow-ups:** "Is a `None` check with a sensible default (e.g., `NoDiscountStrategy`) ever the right fix instead of forcing constructor injection?"

**Best Follow-up Answer:** Sometimes — a **Null Object pattern** (default `NoDiscountStrategy` returning `amount` unchanged) can be a legitimate design choice if "no discount" is a genuinely valid, common state (not an error condition) — the key difference from the band-aid: it's an explicit, intentional default set on construction (`DiscountContext(strategy=NoDiscountStrategy())`), not a runtime `None`-check patch covering up a forgotten `set_strategy()` call. Intent matters: is "no strategy" a valid business state, or a bug?

```python
class DiscountContext:
    def __init__(self, strategy: DiscountStrategy):   # required at construction — fail fast
        self.strategy = strategy
    def apply_discount(self, amount):
        return self.strategy.calculate(amount)
```

---

## Q54. [Level 4, Debugging/Refactor] This Factory Method is a maintenance nightmare — every new vehicle type requires editing this function AND touching 2 other files. Find all the coupling problems and fix them.

```python
def create_vehicle(vehicle_type, **kwargs):
    if vehicle_type == "car":
        from vehicles.car import Car
        return Car(**kwargs)
    elif vehicle_type == "truck":
        from vehicles.truck import Truck
        return Truck(**kwargs)
    elif vehicle_type == "motorcycle":
        from vehicles.motorcycle import Motorcycle
        return Motorcycle(**kwargs)
    else:
        raise ValueError(f"Unknown type: {vehicle_type}")
```

**Expected Answer:** Problems: (1) **OCP violation** — every new vehicle type requires editing this function directly. (2) The factory function *itself* has knowledge of every concrete class's import path — tight coupling to implementation details, and this coupling grows unboundedly as types are added. (3) `**kwargs` gives no compile-time/IDE signal of what each vehicle type actually needs — error-prone, hard to discover valid arguments. Fix: use a **registry pattern** — a dict mapping type strings to constructor callables, populated via a `@register_vehicle("car")` decorator on each vehicle class itself, so adding a new vehicle type means writing a new file with a decorator and touching *zero* existing files (true OCP compliance, not just moving the if/elif elsewhere).

**Why interviewer asks this:** Realistic, common production anti-pattern (the "growing if/elif factory") — tests if you know the registry-pattern fix, a very practical technique beyond textbook Factory Method that real engineers use to achieve genuine OCP compliance for creation logic.

**Common Mistakes:**
- Just moving the if/elif into a dict of classes without addressing *where new types get registered* (doesn't solve OCP if you still have to edit a central dict manually every time — though this is a smaller improvement, it's not the full fix)
- Not noticing the inline imports scattered across branches signal a deeper coupling smell

**Follow-ups:** "What if two different plugins each try to register a vehicle type called 'car'?"

**Best Follow-up Answer:** The registry should raise/warn on duplicate key registration rather than silently overwriting (`if type_name in _registry: raise ValueError("already registered")`) — silent overwrites in plugin-style registries are a classic source of very confusing bugs where "the wrong implementation" mysteriously runs depending on import order.

```python
_registry: dict[str, type] = {}

def register_vehicle(type_name: str):
    def decorator(cls):
        if type_name in _registry:
            raise ValueError(f"'{type_name}' already registered")
        _registry[type_name] = cls
        return cls
    return decorator

def create_vehicle(vehicle_type: str, **kwargs):
    if vehicle_type not in _registry:
        raise ValueError(f"Unknown type: {vehicle_type}")
    return _registry[vehicle_type](**kwargs)

# vehicles/car.py
@register_vehicle("car")
class Car:
    def __init__(self, **kwargs): ...
# Adding "car" required ZERO edits to create_vehicle() or any other file
```

---

## Q55. [Level 5, Senior Puzzle] A staff engineer claims: "Every design pattern is just a workaround for a missing language feature." Do you agree or disagree? Defend your position with at least two pattern examples.

**Expected Answer:** Partially true, and a nuanced answer is expected — this is a known, real critique (notably associated with discussions around Peter Norvig's "Design Patterns in Dynamic Languages" analysis, where several GoF patterns become trivial or unnecessary in languages with first-class functions/dynamic typing). Examples supporting the claim: **Strategy** in a language with first-class functions (Python, JavaScript) often doesn't need a full class hierarchy — a plain function or lambda passed as a parameter achieves the same effect (see Q37's dict-dispatch discussion) — the "pattern" partly compensates for older languages (Java pre-lambdas, C++ pre-`std::function`) lacking first-class functions. **Iterator** pattern is largely unnecessary in Python because the language has built-in iterator protocol/generators as first-class features. Counter-examples where the claim is weaker: **Observer** and **Composite** encode genuine *structural/relationship* ideas (one-to-many notification, recursive tree uniformity) that aren't reducible to "missing a language feature" — they're conceptual solutions to relationship-modeling problems that persist regardless of language features. Conclusion: some patterns (Strategy, Command, Iterator) are partly language-gap workarounds that shrink in languages with better feature support; others (Observer, Composite, Decorator, Singleton's *intent* if not its ceremony) encode structural design ideas that remain valuable regardless of language.

**Why interviewer asks this:** Staff/Senior-level intellectual depth question — tests whether you have genuine, independently-formed opinions about design patterns' actual value versus reciting GoF dogma uncritically; a sign of engineering maturity that goes beyond interview-prep memorization.

**Common Mistakes:**
- Fully agreeing or fully disagreeing without concrete examples on both sides
- Not knowing the real intellectual history here (Norvig's observation is a well-known, legitimate critique worth being aware of, though you don't need to name-drop it)

**Follow-ups:** "So should engineers stop learning GoF patterns since some are 'language workarounds'?"

**Best Follow-up Answer:** No — even where a pattern's *ceremony* (full class hierarchies) is unnecessary in a modern language, the underlying *design vocabulary and intent* (e.g., "this is a Strategy-shaped problem," "this is a Composite-shaped tree") remains valuable as shared vocabulary for communicating design intent with a team, and understanding the classic patterns makes you faster at both recognizing the shape of a problem and recognizing when a lighter-weight, language-native solution (a plain function, a dict) suffices instead of forcing full ceremony.

---

## Q56. [Level 5, Design Interview Simulation] Interviewer says: "Design a Parking Lot system." You have 45 minutes. Walk through your exact approach step by step — what do you clarify first, what classes do you sketch, what patterns naturally emerge?

**Expected Answer (process, not just final code):**
1. **Clarify requirements first** (2-3 min): multiple floors? multiple vehicle types (car/bike/truck) with different spot sizes? payment required? how is spot availability tracked — real-time? Entry/exit gates? This shows interview process maturity — jumping straight to code without clarifying is a common junior mistake.
2. **Identify core entities**: `ParkingLot`, `Floor`, `ParkingSpot` (with a `SpotType`/size), `Vehicle` (with a `VehicleType`), `Ticket`, `PaymentStrategy`.
3. **Identify relationships**: `ParkingLot` *composed of* `Floor`s (composition — floors don't exist without the lot); `Floor` *composed of* `ParkingSpot`s; a `Ticket` *associates* a `Vehicle` with a `ParkingSpot` (association, not ownership — vehicle exists independently).
4. **Identify natural pattern fits**: **Strategy** for spot-assignment policy (nearest-available vs specific-floor-preference) and for payment methods; **Singleton** for `ParkingLot` itself if there's genuinely one lot instance system-wide (justify per Q41's reasoning, don't just default to it); **Factory Method** for creating the right `ParkingSpot` subtype; **Observer** if floors need to broadcast "lot full" events to a display board.
5. **Sketch the core class skeleton and key methods** (`park_vehicle()`, `unpark_vehicle()`, `find_available_spot()`), then **narrate trade-offs out loud** as you go (e.g., "I'll use a Strategy for spot assignment since the interviewer may want to change the allocation policy").
6. **State assumptions explicitly** and invite the interviewer to redirect ("I'm assuming single-lot for now — should I generalize to multiple lots?").

**Why interviewer asks this:** This is the actual format of most real 45-60 minute LLD interviews (Parking Lot, Elevator System, Library Management, Vending Machine are canonical prompts) — tests whether your pattern knowledge translates into a coherent, communicative, well-paced live design process, not just isolated pattern trivia.

**Common Mistakes:**
- Diving into code in the first 5 minutes without clarifying requirements (biggest, most common failure mode interviewers report)
- Cramming in every pattern you know "to show off" rather than justifying each by the actual requirement that calls for it (over-engineering under interview pressure)
- Going silent while thinking instead of narrating reasoning out loud (interviewers grade your thought process, not just the final artifact)

**Follow-ups:** "If I told you halfway through that there are now 5 parking lots across the city sharing a central booking system, how would your design change?"

**Best Follow-up Answer:** This reframes `ParkingLot` from a Singleton to one of *many* instances managed by a higher-level `ParkingLotRegistry`/`BookingService` — exactly the kind of requirement change that punishes over-committing to Singleton early (reinforcing Q41/Q47's caution about justifying Singleton only when the single-instance requirement is actually confirmed, not assumed) — showing you can adapt your design live, rather than being locked into an earlier assumption, is itself a strong signal.

```python
from abc import ABC, abstractmethod
from enum import Enum

class VehicleType(Enum):
    CAR = "car"; BIKE = "bike"; TRUCK = "truck"

class SpotAssignmentStrategy(ABC):
    @abstractmethod
    def find_spot(self, floors: list, vehicle_type: VehicleType): ...

class NearestSpotStrategy(SpotAssignmentStrategy):
    def find_spot(self, floors, vehicle_type):
        for floor in floors:
            spot = floor.get_available_spot(vehicle_type)
            if spot:
                return spot
        return None

class ParkingLot:
    def __init__(self, floors: list, strategy: SpotAssignmentStrategy):
        self.floors = floors                 # composition
        self.strategy = strategy             # strategy, swappable

    def park_vehicle(self, vehicle):
        spot = self.strategy.find_spot(self.floors, vehicle.type)
        if not spot:
            raise Exception("Lot full")
        spot.assign(vehicle)
        return Ticket(vehicle, spot)          # association
```

---

## Q57. [Level 2, Rapid Fire — common in phone screens] Quick-fire round. Answer each in 1-2 sentences.

- **"Is `super().__init__()` mandatory in Python subclasses?"** No — only needed if you want the parent's `__init__` logic to run; if omitted, the parent's `__init__` simply doesn't execute (unlike Java/C++ where a no-arg parent constructor is called implicitly).
- **"Can an abstract class have a constructor?"** Yes — abstract classes can have `__init__` with real logic; it runs when a concrete subclass is instantiated (you just can't instantiate the abstract class directly).
- **"Can you instantiate a class with an abstract method that isn't overridden?"** No — Python's `ABC`/`abstractmethod` raises `TypeError` at instantiation time if any abstract method is unimplemented.
- **"Is method overloading possible in Python?"** Not natively (last definition wins) — simulated via default args, `*args`, or `functools.singledispatch`.
- **"What's the difference between `@staticmethod` and `@classmethod`?"** `@staticmethod` takes no implicit first arg (no access to class or instance); `@classmethod` takes `cls` as first arg (can access/modify class-level state, useful for alternate constructors).
- **"Does composition allow runtime flexibility that inheritance doesn't?"** Yes — a composed object reference can be swapped at runtime; a class's inheritance hierarchy is fixed at definition/compile time.
- **"What's a 'God object' anti-pattern?"** A class that knows/does too much (severe SRP violation), becoming a central dependency hub that's hard to test, change, or reason about.
- **"Why is multiple inheritance risky?"** Diamond problem ambiguity (which parent's method wins) and tight coupling to two class hierarchies at once; Python resolves via MRO/C3 linearization but it's still often hard to reason about.

**Why interviewer asks this:** Rapid-fire rounds test breadth and speed of recall, common in initial phone screens before the deeper design round — shows you're not just capable of deep answers but also fluent enough to answer fast under light pressure.

---

## Q58. [Level 4, Advantages/Disadvantages Drill] For each pattern, give ONE genuine disadvantage an interviewer would respect (not a throwaway "it adds complexity").

- **Singleton**: Introduces global mutable state and hidden dependencies, making unit tests order-dependent unless explicitly reset between tests — a real, specific testing cost, not just "complexity."
- **Factory Method**: Requires a new subclass (or registry entry) per product type, which for a very small, stable set of types (e.g., exactly 2 types, never expanding) is genuinely more indirection than a plain constructor call would need.
- **Decorator**: Debugging a deeply stacked decorator chain (5+ layers) means stepping through many thin wrapper calls to find where behavior actually happens — stack traces become noisy and harder to read.
- **Strategy**: For a very small number of rarely-changing algorithms, introduces a full interface + multiple classes where a simple `if/else` would have been equally maintainable and more discoverable (less indirection to trace).
- **Observer**: Notification order among multiple observers is often unspecified/implementation-dependent, and debugging "why didn't observer X react" requires tracing the entire subscription graph, which can be non-obvious in a large system.

**Why interviewer asks this:** Tests whether you can critique the patterns you just praised — one-sided "patterns are always good" answers are a red flag for balanced engineering judgment at any level above entry.

**Common Mistakes:**
- Giving generic disadvantages that apply to all patterns equally ("it's more code") instead of a disadvantage *specific* to that pattern's actual mechanism
- Refusing to admit any real disadvantage, treating the question defensively

**Follow-ups:** "Which of these five patterns, in your experience/study, gets over-used the most in real interviews and codebases?"

**Best Follow-up Answer:** Singleton, by a wide margin — it's the easiest pattern to reach for reflexively ("there should only be one of these") without interrogating whether global access is actually needed versus simply constructing once and injecting, which is why interviewers probe it the hardest (see Q22, Q41, Q47) — knowing this ahead of time means you should be ready to defend or self-critique any Singleton usage in your own project walkthrough.

---

## Handbook Complete — Quick Study-Order Recommendation

1. Part 1 (OOP) → Part 2 (SOLID) → Part 3 (Patterns): build the vocabulary and defend-the-basics muscle first.
2. Part 4 (Relationships/DI/Coupling): the connective tissue interviewers use to link everything together.
3. Part 5 (Your Projects): rehearse these OUT LOUD — interviewers will ask project-specific follow-ups more than generic ones once you mention a project on your resume.
4. Part 6 (Puzzles/Debugging): do these last, under a timer, to simulate real interview pressure — this is where SDE-2/Senior bar-raiser rounds actually live.

**Total: 58 in-depth questions across Levels 1-5, covering every category requested:** OOP theory/coding, SOLID theory/coding, pattern theory/coding, pattern identification, refactoring, scenario-based, real-world examples, pattern differences, advantages/disadvantages, "why not X instead," edge cases, design trade-offs, puzzles, debugging bad designs, code review, object relationships, composition vs inheritance, aggregation vs composition, DI, loose coupling/high cohesion, and dedicated deep-dives into your Food Delivery App, Notification System, and Document Editor.
