# LLD Interview Handbook — Part 2: SOLID Principles

---

## Q11. [Level 1] State the Single Responsibility Principle in your own words — not the textbook definition.

**Expected Answer:** "A class should have only one reason to change." In practice: a class should own exactly one *axis of change* / one actor's concern. Not "one method" (a common misconception) — a class can have many methods as long as they all serve the same responsibility/actor.

**Why interviewer asks this:** Tests if you understand "responsibility" ≠ "single method." This is the single most misunderstood SOLID principle.

**Common Mistakes:**
- "A class should do only one thing" interpreted literally as one method
- Not being able to name the "actor" whose change would trigger the class's change

**Follow-ups:**
- "Give an example of a class that looks like it does 'one thing' but actually violates SRP."

**Best Follow-up Answer:** A `Report` class with `generate_report()` and `save_to_file()` looks cohesive but has two reasons to change: business logic for report content (changes when report requirements change) and persistence format (changes when storage strategy changes) — two different actors (business analyst vs infra team) can independently demand changes. Split into `ReportGenerator` and `ReportSaver`.

```python
# Violation
class Report:
    def generate(self): ...
    def save_to_file(self, path): ...   # different reason to change

# Fixed
class ReportGenerator:
    def generate(self) -> str: ...

class ReportSaver:
    def save(self, content: str, path: str): ...
```

---

## Q12. [Level 2, Coding] Refactor this SRP-violating `Order` class.

```python
class Order:
    def calculate_total(self): ...
    def save_to_db(self): ...
    def send_confirmation_email(self): ...
    def print_invoice(self): ...
```

**Expected Answer:** Four responsibilities → four actors (business logic, persistence, notifications, presentation/printing). Extract `OrderRepository` (persistence), `EmailNotifier` (notification), `InvoicePrinter` (presentation); `Order` keeps only `calculate_total()` plus its own state.

**Why interviewer asks this:** Standard hands-on SRP refactor — every SDE-1/2 candidate should ace this instantly.

**Common Mistakes:**
- Extracting classes but still calling them *from inside* `Order` (keeps `Order` coupled to infra — should be orchestrated by a service/use-case layer instead, injected via DI)
- Over-extracting single-line methods into their own classes (over-engineering)

**Follow-ups:**
- "Who calls `OrderRepository.save()`, `EmailNotifier.send()`, etc., after this refactor?"

**Best Follow-up Answer:** A higher-level orchestrator/use-case class (e.g., `PlaceOrderService`) coordinates them via dependency injection — `Order` itself stays a pure domain model with no infra dependencies (this is also the Dependency Inversion Principle in action).

```python
class Order:
    def calculate_total(self) -> float: ...

class OrderRepository:
    def save(self, order: Order): ...

class EmailNotifier:
    def send_confirmation(self, order: Order): ...

class PlaceOrderService:
    def __init__(self, repo: OrderRepository, notifier: EmailNotifier):
        self.repo, self.notifier = repo, notifier
    def place(self, order: Order):
        self.repo.save(order)
        self.notifier.send_confirmation(order)
```

---

## Q13. [Level 2] Explain Open/Closed Principle. How do you achieve "closed for modification" in a dynamically typed language like Python where you can monkey-patch anything?

**Expected Answer:** OCP = classes should be open for extension, closed for modification — new behavior added via new code (new classes implementing an interface), not by editing existing tested code. In Python, "closed" isn't enforced by the compiler (unlike `final` in Java) — it's a *design discipline*, enforced via abstraction (ABCs/protocols) + polymorphism + code review norms, not language mechanics. You rely on team convention and interfaces rather than compiler guarantees.

**Why interviewer asks this:** Tests whether you understand OCP is a design principle, not a language feature — important because interviewers probe whether Python/JS candidates conflate "possible" with "correct design."

**Common Mistakes:**
- Saying Python enforces this the same way as statically typed languages
- Confusing OCP with "never touch existing code ever" — OCP is about *extension points* for anticipated variability, not a blanket ban on all edits (bug fixes still require modification)

**Follow-ups:**
- "Give an example violating OCP with `if/elif` chains on type, and the polymorphic fix."

**Best Follow-up Answer:**

```python
# Violation — every new discount type requires editing this function
def calculate_discount(customer_type, amount):
    if customer_type == "regular":
        return amount * 0.05
    elif customer_type == "premium":
        return amount * 0.10
    elif customer_type == "vip":
        return amount * 0.20
    # adding "student" means editing this function again

# OCP-compliant — new types added without touching existing code
from abc import ABC, abstractmethod

class DiscountStrategy(ABC):
    @abstractmethod
    def calculate(self, amount: float) -> float: ...

class RegularDiscount(DiscountStrategy):
    def calculate(self, amount): return amount * 0.05

class PremiumDiscount(DiscountStrategy):
    def calculate(self, amount): return amount * 0.10

class StudentDiscount(DiscountStrategy):   # new — zero changes elsewhere
    def calculate(self, amount): return amount * 0.15
```

---

## Q14. [Level 3, SDE-1] Explain Liskov Substitution Principle with the sub-rules: return type, method argument (contravariance), exceptions, invariants, and pre/postconditions. Give one violating example per sub-rule if possible.

**Expected Answer:**
- **Return type rule (covariance allowed)**: An overriding method's return type must be the same or a *subtype* of the base method's declared return type — callers expecting `Animal` must still get something usable as `Animal`.
- **Method argument rule (contravariance)**: Overriding method's parameter types must be the same or a *supertype* — it must accept at least everything the base method accepted, or callers passing base-expected args will break.
- **Exception rule**: Overriding method must not throw new checked exception types the base method didn't declare — callers only catch what the base contract promised.
- **Class invariants**: Conditions that must hold true for every instance (e.g., `balance >= 0`) must be preserved by subclasses — a subclass must not violate invariants the base class guarantees.
- **History constraint**: Subclasses shouldn't allow state changes the base class disallows (e.g., an immutable `Point` base shouldn't have a mutable subclass allowing coordinate changes after construction).
- **Precondition rule**: Subclass cannot *strengthen* preconditions (can't demand more than the base required — the caller was told less was needed).
- **Postcondition rule**: Subclass cannot *weaken* postconditions (must still guarantee at least what the base promised after execution).

**Why interviewer asks this:** LSP is the most nuanced SOLID principle and the sub-rules are explicitly in your prep list — this is a guaranteed SDE-1+ interview question at rigor-focused companies (Amazon, Google).

**Common Mistakes:**
- Only citing the Square/Rectangle example and stopping there
- Confusing precondition/postcondition direction (mixing up "strengthen" vs "weaken")

**Follow-ups:**
- "Give a real API example of a precondition-strengthening LSP violation."

**Best Follow-up Answer:** Base `FileReader.read(path)` accepts any path. Override `SecureFileReader.read(path)` throws if the path isn't in an allow-list — this *strengthens* the precondition (base accepted more inputs than the override now does), breaking any client that substitutes `SecureFileReader` where `FileReader` was expected and passes a previously-valid path.

```python
# Precondition strengthening — LSP violation
class FileReader:
    def read(self, path: str) -> str:
        return open(path).read()   # accepts any path

class SecureFileReader(FileReader):
    ALLOWED = {"/safe/a.txt"}
    def read(self, path: str) -> str:
        if path not in self.ALLOWED:
            raise PermissionError("not allowed")  # stronger precondition — breaks substitutability
        return super().read(path)
```

---

## Q15. [Level 3, Coding] Classic: `Bird` base class has `fly()`. `Penguin extends Bird`. Identify the LSP violation and fix it with two different approaches — discuss trade-offs of each.

**Expected Answer:** Violation: `Penguin` can't fly, so overriding `fly()` to `raise NotImplementedError` breaks substitutability — any code doing `for bird in birds: bird.fly()` crashes on a `Penguin`. Two fixes:
1. **Segregate by capability (interface split)**: `FlyingBird(Bird)` with `fly()`, non-flying birds don't implement it. Simple, but if many capabilities exist (fly, swim, run) risks interface explosion.
2. **Composition with behavior objects**: `Bird` holds a `MovementBehavior` (e.g., `FlyingMovement`, `WalkingMovement`) injected per instance — most flexible, supports runtime behavior changes (e.g., injured bird switches from flying to walking) but is more code for simple cases.

Trade-off: option 1 is simpler and sufficient when capabilities are static and few; option 2 is better when behaviors vary independently, combine in multiple ways, or must change at runtime.

**Why interviewer asks this:** THE canonical LSP question — tests whether you can produce a fix, not just identify the smell, and reason about which fix fits which context (SDE-2 signal).

**Common Mistakes:**
- Fixing it by just making `fly()` do nothing silently (hides the bug — worse than an exception, since callers get no signal)
- Only giving one fix without discussing trade-offs

**Follow-ups:**
- "Which approach would you use for a video game with 50 different creature types with overlapping abilities?"

**Best Follow-up Answer:** Composition (behavior objects / capability components), because with 50 types and overlapping abilities, interface-per-capability subclassing explodes combinatorially, while composed behavior components mix and match freely and can change at runtime (an Entity-Component-System-style design).

```python
from abc import ABC, abstractmethod

class Bird(ABC):
    @abstractmethod
    def move(self): ...

class FlyingBird(Bird):
    def move(self): print("Flying")

class WalkingBird(Bird):
    def move(self): print("Waddling")

class Sparrow(FlyingBird): pass
class Penguin(WalkingBird): pass   # no longer forced to implement fly()
```

---

## Q16. [Level 3] Explain Interface Segregation Principle. How does a "fat interface" cause problems downstream, concretely?

**Expected Answer:** ISP: clients should not be forced to depend on methods they don't use — many small, role-specific interfaces beat one large general-purpose interface. A fat interface (e.g., `Worker` with `work()`, `eat()`, `sleep()`) forces a `RobotWorker` to implement `eat()`/`sleep()` with dummy/throwing bodies — this (a) violates LSP (dummy implementations misrepresent the contract), (b) creates false coupling (any change to `eat()`'s signature forces `RobotWorker` to recompile/change even though it never used it), and (c) signals the interface is really multiple responsibilities bundled together (ISP is SRP applied to interfaces).

**Why interviewer asks this:** Tests understanding of ISP as a *consequence-driven* principle, not just a rule to recite.

**Common Mistakes:**
- Not connecting ISP to SRP ("ISP is basically SRP for interfaces")
- Not explaining the *downstream* cost (recompilation/coupling), only the immediate awkwardness

**Follow-ups:**
- "Refactor the fat `Worker` interface."

**Best Follow-up Answer:**

```python
from abc import ABC, abstractmethod

class Workable(ABC):
    @abstractmethod
    def work(self): ...

class Eatable(ABC):
    @abstractmethod
    def eat(self): ...

class Sleepable(ABC):
    @abstractmethod
    def sleep(self): ...

class HumanWorker(Workable, Eatable, Sleepable):
    def work(self): ...
    def eat(self): ...
    def sleep(self): ...

class RobotWorker(Workable):   # only implements what applies
    def work(self): ...
```

---

## Q17. [Level 3-4] Explain Dependency Inversion Principle precisely — many candidates confuse it with Dependency Injection. What's the actual distinction?

**Expected Answer:** DIP is a *design principle*: high-level modules should not depend on low-level modules; both should depend on abstractions. Abstractions should not depend on details; details should depend on abstractions. It's about the *direction of the dependency arrow* — business logic should own the interface, and infrastructure implements it (inverted from the "natural" flow where business logic directly imports infra). **Dependency Injection** is one *technique* (a mechanism) commonly used to achieve DIP — passing dependencies in via constructor/setter rather than instantiating them internally. You can have DI without DIP (injecting a concrete low-level class directly, still coupled to it) and DIP without DI (e.g., service locator pattern, less common/desirable). They're related but distinct: DIP is the *what/why* (architecture principle), DI is the *how* (implementation technique).

**Why interviewer asks this:** Extremely common point of confusion; separates candidates who deeply understand architecture from those who memorized "DIP = inject dependencies."

**Common Mistakes:**
- Treating DIP and DI as synonyms
- Not explaining the "abstractions owned by high-level module" nuance

**Follow-ups:**
- "Show DI without achieving DIP."

**Best Follow-up Answer:**

```python
# DI without DIP — still coupled to a concrete low-level class
class MySQLDatabase:
    def save(self, data): ...

class OrderService:
    def __init__(self, db: MySQLDatabase):   # injected, but concrete type — high-level module still depends on low-level detail
        self.db = db

# DIP achieved — both depend on abstraction
from abc import ABC, abstractmethod

class Database(ABC):
    @abstractmethod
    def save(self, data): ...

class MySQLDatabase(Database):
    def save(self, data): ...

class OrderService:
    def __init__(self, db: Database):   # depends on abstraction, not concrete detail
        self.db = db
```

---

## Q18. [Level 4, SDE-2, Scenario] You're designing a `NotificationService` that currently sends only Email. Product says "we'll likely add SMS and Push in the next two quarters, but we're not sure of the exact channels yet." Walk through how you'd apply OCP + DIP here, and where you'd draw the line to avoid over-engineering.

**Expected Answer:** Define a `NotificationChannel` interface with `send(message)`. `NotificationService` depends on a list/collection of `NotificationChannel` (DIP — depends on abstraction). Adding SMS/Push later = new classes implementing the interface, zero changes to `NotificationService` (OCP). Where to draw the line: don't pre-build config-driven plugin registries, dynamic channel discovery, or a full rules engine *before* the second channel actually exists — YAGNI. Build the interface abstraction now (cheap, low-risk, clearly needed since 2+ channels are *confirmed* future work), but defer speculative extensibility (e.g., third-party plugin SDK) until there's real evidence of need beyond the stated two.

**Why interviewer asks this:** SDE-2/Senior bar — must show judgment about *how much* abstraction is warranted, not just "add interfaces everywhere." Real interviews at this level probe over-engineering awareness.

**Common Mistakes:**
- Building a fully generic, config-driven, reflection-based channel loader "just in case" — this is the #1 red flag interviewers watch for at senior level (over-engineering)
- Under-engineering: hardcoding `if channel == "email"` when 2 more channels are explicitly confirmed as coming

**Follow-ups:**
- "How would you decide if a Factory is warranted here yet?"

**Best Follow-up Answer:** Factory becomes warranted once channel *creation* itself has non-trivial logic or configuration (e.g., choosing SMS provider based on region) — with only 2-3 known channels and simple construction, direct instantiation + DI is enough; introduce `NotificationChannelFactory` only when creation logic grows complex enough to be worth isolating (a concrete trigger, not speculation).

```python
from abc import ABC, abstractmethod

class NotificationChannel(ABC):
    @abstractmethod
    def send(self, message: str): ...

class EmailChannel(NotificationChannel):
    def send(self, message): print(f"Email: {message}")

class SMSChannel(NotificationChannel):   # added later, zero change elsewhere
    def send(self, message): print(f"SMS: {message}")

class NotificationService:
    def __init__(self, channels: list[NotificationChannel]):
        self.channels = channels
    def notify(self, message: str):
        for ch in self.channels:
            ch.send(message)
```

---

## Q19. [Level 4] Can following SOLID principles too rigidly hurt a codebase? Give a real trade-off scenario.

**Expected Answer:** Yes — SOLID applied dogmatically produces "abstraction soup": excessive interfaces with single implementations, indirection for indirection's sake, and classes so small the cognitive cost of navigating between them exceeds the benefit. Example: applying SRP so aggressively that a simple `UserValidator` becomes five one-method classes wired through DI containers for a feature that will never realistically vary. Trade-off: abstraction has a cost (navigation complexity, more files, harder onboarding) that must be justified by *actual* expected variability — not hypothetical future flexibility. Rule of thumb used by senior engineers: introduce the abstraction when the second real variant appears (or is contractually certain), not preemptively for a single implementation "in case."

**Why interviewer asks this:** Senior/staff-level judgment question — anyone can recite SOLID; fewer can articulate its costs and know when to stop applying it.

**Common Mistakes:**
- Saying "SOLID should always be followed strictly" (red flag for senior roles — shows lack of real-world engineering judgment)
- Not giving a concrete example of over-application

**Follow-ups:**
- "How do you push back on a teammate who insists every class needs an interface 'for testability'?"

**Best Follow-up Answer:** Point out that mocking concrete classes is possible in most modern test frameworks (e.g., Python's `unittest.mock` patches concrete classes directly), so "testability" alone doesn't require an interface — interfaces are justified when there are genuinely multiple implementations (real or contractually near-term), not solely for mocking convenience.

---

**Continue to Part 3 (Design Patterns) → `03_Design_Patterns_Interview_Questions.md`**
