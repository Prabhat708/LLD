# LLD Interview Handbook — Part 4: Object Relationships, Coupling/Cohesion, DI, Refactoring & Puzzles

---

## Q32. [Level 2] Explain High Cohesion and Loose Coupling — why do interviewers always pair these terms, and how do you measure/recognize violations in real code?

**Expected Answer:** **Cohesion** = how closely related and focused the responsibilities *within* a single module/class are (high cohesion = a class does one well-defined thing, and its methods all operate closely on the same data/purpose). **Coupling** = how much one module *depends on* the internals/details of another (low/loose coupling = modules interact only through stable abstractions, minimal knowledge of each other's internals). They're paired because they're the two axes that jointly determine maintainability: high cohesion within a class + loose coupling between classes = changes stay localized. Recognize violations: a class using only 2 of its 10 instance variables in most methods signals low cohesion (probably should be split); a class that must be recompiled/changed whenever an unrelated class changes signals tight coupling.

**Why interviewer asks this:** Foundational vocabulary question that underlies almost every other LLD answer — interviewer wants to hear you use these terms correctly throughout the interview, not just define them once.

**Common Mistakes:**
- Defining only one of the two terms
- Not giving a concrete "smell" for detecting violations

**Follow-ups:** "Can a class be highly cohesive but still tightly coupled to the rest of the system? Give an example."

**Best Follow-up Answer:** Yes — a `PaymentValidator` class can be internally perfectly cohesive (every method genuinely relates to payment validation) while still being tightly coupled if it directly imports and calls a concrete `StripeAPIClient` instead of an abstraction — cohesion is an internal property, coupling is a relational property; they're independent axes.

---

## Q33. [Level 2-3] Dependency Injection — explain the three common forms (constructor, setter, interface injection) and when you'd choose each.

**Expected Answer:**
- **Constructor injection**: dependencies passed via constructor; object is fully valid immediately after construction; dependency is mandatory and immutable for the object's lifetime. *Preferred default* — makes dependencies explicit and required.
- **Setter injection**: dependencies set via a setter method after construction; allows optional dependencies or reconfiguration later, but risks the object being used in a partially-initialized state if the setter isn't called before use.
- **Interface injection**: the dependency itself defines an interface the injector must implement to supply itself (less common in Python/dynamic languages; more seen in older Java DI frameworks).

Choose constructor injection by default (fail-fast, immutable, explicit); use setter injection only for genuinely optional dependencies with sensible defaults.

**Why interviewer asks this:** Tests practical DI knowledge beyond "DI = passing dependencies" — the *form* matters for correctness (fail-fast vs silent nulls).

**Common Mistakes:**
- Not knowing setter injection risks partially-initialized objects
- Treating all three forms as interchangeable with no trade-off discussion

**Follow-ups:** "What's a 'poor man's DI container' and when is a full DI framework overkill?"

**Best Follow-up Answer:** A "poor man's DI container" is simply manually wiring dependencies at the application's composition root (e.g., in `main()`) rather than using a framework/container — appropriate for small-to-medium codebases; a full DI framework (Spring, dependency-injector) becomes worth its complexity when the object graph is large, has many optional/scoped dependencies, or needs runtime configuration-driven wiring.

```python
# Constructor injection (preferred)
class OrderService:
    def __init__(self, payment: PaymentStrategy, repo: OrderRepository):
        self.payment = payment
        self.repo = repo

# Composition root — manual wiring, no framework needed for small apps
service = OrderService(payment=UPIPayment(), repo=SQLOrderRepository())
```

---

## Q34. [Level 3] Aggregation vs Composition — draw the UML distinction, and explain a scenario where choosing the wrong one causes a real bug (not just a "wrong diagram" issue).

**Expected Answer:** UML: aggregation = hollow/open diamond at the "whole" end; composition = filled/solid diamond at the "whole" end, both pointing from whole to part. Real bug scenario: modeling a `Playlist` containing `Song`s as **composition** (playlist owns songs, deletes them when playlist is deleted) — if songs are actually shared across multiple playlists (a real `Song` can belong to many `Playlist`s), composition's implied exclusive-ownership/cascading-delete semantics would incorrectly delete a song still referenced by another playlist when one playlist is removed. It should be **aggregation** — `Song`s exist independently and are just referenced by playlists.

```
Composition (exclusive ownership, cascading lifecycle):
  House ◆──── Room     (destroy House → Rooms destroyed)

Aggregation (shared/independent lifecycle):
  Playlist ◇──── Song   (destroy Playlist → Songs persist, may be in other playlists)
```

**Why interviewer asks this:** Tests whether you understand these aren't just diagramming trivia — picking the wrong one leads to real bugs (premature deletion, dangling references, memory issues in manual-memory languages).

**Common Mistakes:**
- Treating this as purely a diagramming exercise with no real-world consequence
- Getting the diamond direction backwards (diamond is always at the "whole"/container end)

**Follow-ups:** "In a garbage-collected language like Python, does getting aggregation vs composition 'wrong' still matter, since there's no manual memory management?"

**Best Follow-up Answer:** Yes — even with GC, cascading-delete *business logic* (e.g., "when I delete this Order, also delete its OrderLineItems from the DB") is a deliberate design decision independent of memory management; getting the ownership model wrong causes orphaned or incorrectly-deleted *data* (real, user-visible bugs), not just memory leaks.

---

## Q35. [Level 4, SDE-2, Code Review] Review this code and identify every design flaw you can find (SOLID violations, coupling issues, missing abstractions):

```python
class OrderProcessor:
    def process_order(self, order_data):
        # validate
        if order_data['amount'] <= 0:
            raise ValueError("Invalid amount")

        # calculate tax
        if order_data['country'] == 'US':
            tax = order_data['amount'] * 0.08
        elif order_data['country'] == 'IN':
            tax = order_data['amount'] * 0.18
        else:
            tax = 0

        # save to mysql
        import mysql.connector
        conn = mysql.connector.connect(host='localhost')
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO orders VALUES ({order_data['id']}, {order_data['amount']})")
        conn.commit()

        # send email
        import smtplib
        server = smtplib.SMTP('smtp.gmail.com')
        server.sendmail('shop@x.com', order_data['email'], 'Order confirmed')

        return order_data['amount'] + tax
```

**Expected Answer, structured as a real code review:**
1. **SRP violation** — one method does validation, tax calculation, persistence, and notification: four reasons to change.
2. **OCP violation** — tax logic is an `if/elif` on country string; adding a new country requires editing this method (should be a `TaxStrategy` per country/region).
3. **DIP violation** — directly instantiates `mysql.connector` and `smtplib.SMTP` inline; no abstraction for persistence or notification, making this untestable without a real DB and real SMTP server.
4. **SQL injection vulnerability** — raw string interpolation into SQL (`f"INSERT INTO orders VALUES ({order_data['id']}, ...)"`) — critical security bug, must use parameterized queries.
5. **No error handling** around DB/network calls — a DB failure leaves the method half-done with no rollback, and an email failure would crash order processing entirely (order should probably still succeed even if the confirmation email fails — these have different failure tolerances).
6. **Untyped/unstructured input** — `order_data` is a raw dict with string keys; no validation of dict shape, easy to typo a key and get a runtime `KeyError` — should be a typed dataclass/Pydantic model.
7. **Imports inside the method** — unconventional and hides dependencies; should be top-level imports (or better, injected dependencies, tying back to point 3).
8. **Testability** — this method cannot be unit tested without hitting a real database and real SMTP server; it should be decomposed and dependencies injected.

**Why interviewer asks this:** This IS the actual job — reviewing real, messy code for design flaws is a more realistic day-to-day skill than reciting pattern definitions. Very common at SDE-2/Senior bar-raiser rounds.

**Common Mistakes:**
- Only spotting 1-2 issues (usually just SRP) and missing the security bug or testability issue
- Not proposing a fix, only listing complaints

**Follow-ups:** "Refactor this into a testable design."

**Best Follow-up Answer:**

```python
from dataclasses import dataclass
from abc import ABC, abstractmethod

@dataclass
class OrderData:
    id: int
    amount: float
    country: str
    email: str

class TaxStrategy(ABC):
    @abstractmethod
    def calculate(self, amount: float) -> float: ...

class USTax(TaxStrategy):
    def calculate(self, amount): return amount * 0.08
class INTax(TaxStrategy):
    def calculate(self, amount): return amount * 0.18
class NoTax(TaxStrategy):
    def calculate(self, amount): return 0.0

TAX_STRATEGIES = {"US": USTax(), "IN": INTax()}

class OrderRepository(ABC):
    @abstractmethod
    def save(self, order: OrderData): ...

class EmailNotifier(ABC):
    @abstractmethod
    def send_confirmation(self, order: OrderData): ...

class OrderValidator:
    def validate(self, order: OrderData):
        if order.amount <= 0:
            raise ValueError("Invalid amount")

class OrderProcessor:
    def __init__(self, repo: OrderRepository, notifier: EmailNotifier,
                 validator: OrderValidator):
        self.repo, self.notifier, self.validator = repo, notifier, validator

    def process_order(self, order: OrderData) -> float:
        self.validator.validate(order)
        tax_strategy = TAX_STRATEGIES.get(order.country, NoTax())
        tax = tax_strategy.calculate(order.amount)
        self.repo.save(order)                     # parameterized internally
        try:
            self.notifier.send_confirmation(order)  # failure here shouldn't fail the order
        except Exception:
            pass  # log, don't propagate
        return order.amount + tax
```

---

## Q36. [Level 3, Puzzle] Two candidates argue: one says "always program to an interface," the other says "that's overkill for a class with only one implementation." Who's right, and how do you settle this in an actual PR review?

**Expected Answer:** Both have a point depending on context — this is a judgment question, not a binary answer. Rule used by experienced engineers: introduce an interface when (a) there are genuinely 2+ implementations *now*, (b) a second implementation is *near-term certain* (e.g., explicitly on the roadmap, or required for testing with a fake/mock where the real dependency is slow/external like a DB or network call), or (c) the boundary is an architectural seam you want to protect (e.g., between layers, or a third-party integration you may need to swap). If none of these apply — single implementation, no near-term variation, no test-isolation need — a concrete class with no interface is simpler and equally correct; adding one preemptively is speculative YAGNI-violating abstraction.

**Why interviewer asks this:** Senior/staff-level design-judgment question, common as a "there's no single right answer, defend your reasoning" prompt.

**Common Mistakes:**
- Picking a side dogmatically instead of giving the actual decision criteria
- Not mentioning the "external/slow dependency → interface for testability" exception, which is the most common legitimate single-implementation-interface case

**Follow-ups:** "Give a concrete single-implementation case where you WOULD still add the interface."

**Best Follow-up Answer:** A single `SendGridEmailClient` calling a real external API — even with no second provider planned, wrapping it behind an `EmailClient` interface is justified purely for **test isolation** (so tests can inject a `FakeEmailClient` and not hit the network), which is a concrete, present-tense need, not speculation.

---

## Q37. [Level 4, Scenario/Tradeoff] You must choose between Strategy pattern and a simple dictionary-based dispatch (`{"email": send_email, "sms": send_sms}[channel]()`) for selecting behavior. When is the dict approach actually the better engineering choice, despite Strategy being the "textbook" pattern?

**Expected Answer:** Dict dispatch is better when: the "strategies" are simple, stateless functions with no shared setup/config, there's no need for polymorphic objects with their own state or multiple methods, and the team values conciseness over ceremony. Strategy (full class-based) is better when: strategies need to hold their own configuration/state (e.g., a `TaxStrategy` needing a `rate` set at construction), need multiple related methods (not just one callable), need to participate in a broader type hierarchy (e.g., DI, polymorphic collections), or need to be independently unit-testable/mockable as objects. Neither is universally "more correct" — dict dispatch is functionally a lightweight Strategy pattern for the stateless-function case; forcing full class ceremony for a one-liner function selection is over-engineering.

**Why interviewer asks this:** Tests pragmatism vs pattern-dogma — a strong senior signal is knowing when a "lesser" solution is actually the right engineering call.

**Common Mistakes:**
- Insisting Strategy (full OOP) is always superior "because it's the textbook pattern"
- Not identifying the concrete trigger (state/multiple methods) that tips the decision toward full Strategy

**Follow-ups:** "Does using a dict-dispatch still satisfy OCP?"

**Best Follow-up Answer:** Yes, structurally similar to Strategy — adding a new channel means adding a new dict entry and function, not modifying existing dispatch logic (assuming the calling code doesn't branch on channel elsewhere) — the dict *is* the extension point, just as the interface is in class-based Strategy.

```python
def send_email(msg): print(f"Email: {msg}")
def send_sms(msg): print(f"SMS: {msg}")

DISPATCH = {"email": send_email, "sms": send_sms}

def notify(channel: str, msg: str):
    DISPATCH[channel](msg)   # OCP-respecting: new channel = new dict entry
```

---

## Q38. [Level 3, Edge Case] Your Decorator-based logging wrapper (`LoggingDecorator(service)`) wraps a service whose method can raise an exception. Where should the log statement go, and what edge case breaks a naive implementation?

**Expected Answer:** Should wrap in try/except/finally (or try/else) to log *both* success and failure paths — logging only on the success path silently swallows visibility into failures, which is exactly when logs matter most. Naive implementation that logs only after a successful return will never log failed calls, because the exception propagates past the log statement before it executes. Correct: log entry (optionally), call in a try block, log success in the try body immediately after the call, log failure (with exception info) in an except block, then **re-raise** — a decorator must never silently swallow exceptions from the wrapped object, since callers up the chain are relying on LSP-consistent behavior (the decorated object should behave like the undecorated one, just with added logging).

**Why interviewer asks this:** Tests attention to a subtle-but-common real bug in decorator/aspect-style code (also relevant to retry/circuit-breaker decorators).

**Common Mistakes:**
- Logging only in a "happy path" spot after the call, missing exceptions entirely
- Swallowing the exception in the except block instead of re-raising (silently changes behavior — an LSP violation for the decorator)

**Follow-ups:** "How would this change if you were writing a Retry decorator instead of a Logging one?"

**Best Follow-up Answer:** A Retry decorator *should* catch the exception internally (up to a max attempt count, often with backoff) rather than always re-raising immediately — but must still re-raise after exhausting retries, and should distinguish retryable errors (e.g., transient network errors) from non-retryable ones (e.g., validation errors) rather than blindly retrying everything.

```python
class LoggingDecorator:
    def __init__(self, service):
        self._service = service
    def execute(self, *args, **kwargs):
        try:
            result = self._service.execute(*args, **kwargs)
            print(f"SUCCESS: {args}")
            return result
        except Exception as e:
            print(f"FAILURE: {args} -> {e}")
            raise    # never swallow — re-raise so behavior matches undecorated service
```

---

## Q39. [Level 5, Senior, Design Tradeoff] A teammate proposes using inheritance for a `Cache` hierarchy: `Cache → LRUCache → TimedLRUCache → DistributedTimedLRUCache`. You suspect this will become unmaintainable. Walk through your reasoning and propose an alternative structure.

**Expected Answer:** Reasoning: each "feature" (eviction policy = LRU, expiry = timed, distribution = distributed) is an *orthogonal concern*, not a taxonomic specialization — stacking them via linear inheritance forces a fixed order and prevents mixing (e.g., what if you want `TimedDistributedCache` without LRU, using FIFO eviction instead? You'd need a whole new inheritance branch). This is the same combinatorial explosion problem as Q9's flying birds. Alternative: decompose into composed, independently swappable components — `EvictionPolicy` (LRU/FIFO/LFU), `ExpiryPolicy` (timed/none), `StorageBackend` (local/distributed) — and a single `Cache` class composed of these three interchangeable strategies, injected via constructor. This supports all combinations (3 policies × 2 expiry × 2 backends = 12 combinations) with only 7 small classes instead of a combinatorial inheritance tree.

**Why interviewer asks this:** Senior-level architecture question that synthesizes composition-over-inheritance, Strategy, and OCP into a realistic infra-component design scenario (caches are a very common LLD topic at this level).

**Common Mistakes:**
- Agreeing to the inheritance hierarchy without pushing back
- Proposing composition but not identifying the actual orthogonal axes (eviction, expiry, storage) — just saying "use composition" vaguely without concrete decomposition

**Follow-ups:** "How would you migrate an existing production `LRUCache` subclass hierarchy to this design without breaking existing callers?"

**Best Follow-up Answer:** Introduce the new composed `Cache` class alongside the old hierarchy; make old subclasses (e.g., `LRUCache`) thin adapters that internally construct the new composed `Cache` with the equivalent policies, preserving the old public API temporarily; migrate callers to the new composed API incrementally; delete the old hierarchy once all callers migrate (strangler fig again — a recurring senior-level migration pattern).

```python
from abc import ABC, abstractmethod

class EvictionPolicy(ABC):
    @abstractmethod
    def evict(self, store: dict): ...

class LRUEviction(EvictionPolicy):
    def evict(self, store): ...   # remove least-recently-used key

class ExpiryPolicy(ABC):
    @abstractmethod
    def is_expired(self, key, meta) -> bool: ...

class TimedExpiry(ExpiryPolicy):
    def is_expired(self, key, meta): ...

class Cache:
    def __init__(self, eviction: EvictionPolicy, expiry: ExpiryPolicy | None = None):
        self._store = {}
        self._eviction = eviction
        self._expiry = expiry     # composed, swappable, mixable independently
```

---

## Q40. [Level 2, Interview Puzzle] "If Python doesn't enforce private members (no true `private` keyword), does encapsulation even mean anything in Python?"

**Expected Answer:** Yes — encapsulation is a *design discipline*, not purely a language-enforcement mechanism (same point as OCP in Q13). Python's `_single_underscore` (convention: "internal, don't touch") and `__double_underscore` (name-mangling: makes accidental external access harder, though not impossible via `_ClassName__attr`) are conventions backed by tooling (linters) and team norms rather than compiler enforcement. The *intent* of encapsulation — protecting invariants via a controlled interface — is still fully achievable in Python; what's absent is compiler-level prevention of violation, replaced by convention + trust + code review.

**Why interviewer asks this:** Language-philosophy question that tests whether you understand principles as design intentions vs. language features — a recurring theme interviewers use to test depth over memorization.

**Common Mistakes:**
- "Python doesn't have real encapsulation" (overstates it — conflates enforcement mechanism with the principle itself)
- Not knowing name mangling exists/how it works

**Follow-ups:** "Show how name mangling works and how it can still be bypassed."

**Best Follow-up Answer:**

```python
class Account:
    def __init__(self):
        self.__balance = 100   # name-mangled to _Account__balance

a = Account()
# a.__balance          # AttributeError — not directly accessible
print(a._Account__balance)  # 100 — still bypassable, by design; Python trusts consenting adults
```

---

**Continue to Part 5 (LLD Project-Specific Questions: Food Delivery, Document Editor, Notification System) → `05_LLD_Projects_Questions.md`**
