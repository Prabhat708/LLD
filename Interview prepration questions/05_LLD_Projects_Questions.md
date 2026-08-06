# LLD Interview Handbook — Part 5: Your LLD Projects (Food Delivery App, Document Editor, Notification System)

These are the questions an interviewer would ask *specifically* after you say "I built a Food Delivery App / Notification System / Document Editor using X, Y, Z patterns" on your resume or in a project walkthrough. Interviewers probe your *own* project harder than generic questions, because they're checking if you actually understand what you built or just copied a tutorial.

---

# SECTION A: Food Delivery App (Singleton, Strategy, Factory Method, Composition, Polymorphism)

## Q41. [Level 3] Walk me through your Food Delivery App's architecture. Where exactly did you use Singleton, and could the app function correctly if that class were NOT a singleton?

**Expected Answer (talk-through structure):** Identify the singleton candidate honestly — typically something like an `OrderManager`, `CartService`, or `DeliveryFleetManager` that must have single global coordination state (e.g., tracking all active orders/delivery agents system-wide). Then directly answer the "could it work without Singleton" question: usually yes, *functionally*, if you instead created one instance at application startup and passed it via dependency injection everywhere it's needed — Singleton just makes that single-instance guarantee structural rather than relying on discipline at the composition root. This is an important admission: Singleton is a *convenience for global access*, not the only way to get "effectively one instance."

**Why interviewer asks this:** Tests whether you can defend your OWN design decisions with reasoning, not just cite "I used Singleton" as a checkbox. The "could it work without it" follow-up specifically hunts for candidates who added patterns because the pattern list told them to, not because the problem needed it.

**Common Mistakes:**
- Being unable to justify why the specific class needed global access vs simply being instantiated once and injected
- Not acknowledging that most "Singleton necessity" claims are actually "convenience" claims, not hard requirements

**Follow-ups:** "What breaks if two `DeliveryFleetManager` instances exist accidentally (bug, not intentional)?"

**Best Follow-up Answer:** Two instances would each maintain their own view of "which delivery agents are currently assigned" — a race where Instance A assigns Agent 7 to Order X while Instance B (unaware) assigns the same Agent 7 to Order Y, causing a double-booking bug. This concretely justifies why *this specific* class benefits from a single source of truth, rather than reciting "singleton = good practice" abstractly.

---

## Q42. [Level 4, SDE-2] You used Strategy for payment methods. Now product wants "apply multiple payment methods to one order" (e.g., partial wallet + partial card). Does your current Strategy design support this? If not, how do you extend it?

**Expected Answer:** Honest answer: a naive Strategy design (`PaymentContext` holding one `PaymentStrategy`) does NOT support split payments — it assumes exactly one strategy per transaction. Extension approaches: (1) **Composite payment strategy** — introduce a `SplitPaymentStrategy` that itself holds a list of `(PaymentStrategy, amount)` pairs and internally iterates, applying each sub-strategy for its portion (this is literally the **Composite pattern** layered on top of Strategy — a strategy that is itself composed of strategies). (2) Ensure each sub-payment can independently fail/rollback — split payments introduce a distributed-transaction-like problem (what if wallet succeeds but card fails? need compensation/rollback logic), which is a real system design consideration beyond pure OOP pattern application.

**Why interviewer asks this:** Classic "requirements changed, does your design survive contact with reality" question — SDE-2 bar tests whether your original design was genuinely extensible (OCP in practice) or just happened to work for the one scenario you built.

**Common Mistakes:**
- Claiming the original design "already supports this" without acknowledging the real change needed
- Not mentioning the partial-failure/rollback problem introduced by splitting payments (a significant real-world complexity, not just a code structure change)

**Follow-ups:** "How do you handle the case where the wallet debit succeeds but the card charge fails?"

**Best Follow-up Answer:** Treat it as a saga/compensating-transaction problem: if a later sub-payment fails, issue compensating actions to reverse the already-successful sub-payments (e.g., refund the wallet debit) before propagating the overall failure — don't leave the order in a partially-charged inconsistent state. This ties LLD to distributed systems thinking, which senior interviewers specifically probe for.

```python
from abc import ABC, abstractmethod

class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount: float) -> bool: ...
    @abstractmethod
    def refund(self, amount: float): ...

class SplitPaymentStrategy(PaymentStrategy):
    def __init__(self, parts: list[tuple[PaymentStrategy, float]]):
        self.parts = parts
        self._completed: list[tuple[PaymentStrategy, float]] = []

    def pay(self, amount: float) -> bool:
        for strategy, part_amount in self.parts:
            if strategy.pay(part_amount):
                self._completed.append((strategy, part_amount))
            else:
                self._rollback()   # compensate already-successful parts
                return False
        return True

    def _rollback(self):
        for strategy, part_amount in self._completed:
            strategy.refund(part_amount)
```

---

## Q43. [Level 4] Your Factory Method creates `Restaurant` objects for different cuisine types. An interviewer asks: "why Factory Method here and not Abstract Factory, given a restaurant has a Menu, a DeliveryPolicy, and a Rating system that might all vary by cuisine/region together?"

**Expected Answer:** This is a genuine design-judgment question, not a trick — if `Menu`, `DeliveryPolicy`, and `Rating` truly need to vary *together as a consistent family* per cuisine/region (e.g., "Indian restaurants" always pair with a specific delivery SLA and menu structure), Abstract Factory is arguably the more correct pattern, matching the Q25 discussion. The honest answer: "My original design used Factory Method because at the time I only needed to vary the `Restaurant` object's creation; if the requirement is genuinely 'these three things always vary together as a consistent bundle,' I'd refactor to Abstract Factory — but I'd first confirm they *actually* need to co-vary, rather than assume it, since forcing an Abstract Factory when the three items vary independently would be over-engineering (see Q19)."

**Why interviewer asks this:** Tests self-critique ability — can you honestly evaluate whether your own past design choice was actually correct under new information, without defensive rationalization? This is one of the highest-signal traits interviewers look for.

**Common Mistakes:**
- Defensively insisting Factory Method was definitely correct without engaging with the hypothetical
- Immediately agreeing Abstract Factory is needed without first questioning whether the three items truly co-vary (jumping to more complexity without justification is itself a red flag)

**Follow-ups:** "What's the actual cost of switching from Factory Method to Abstract Factory later, once you're 6 months into production with existing `Restaurant` instances?"

**Best Follow-up Answer:** The cost is primarily at the *creation call sites* — anywhere `RestaurantFactory.create(cuisine)` is called needs to migrate to the new Abstract Factory's method(s); existing `Restaurant` instances themselves are unaffected since the pattern change is about *how objects are created*, not their runtime structure — so the migration is bounded and mechanical, not a full rewrite (a reassuring, concrete answer that shows migration-cost awareness).

---

## Q44. [Level 3-4, Scenario] Peak lunch hour: 50,000 concurrent orders. Your `OrderManager` (built with Composition — `Order` composed of `List[OrderItem]`) needs to calculate total price for every order in real time. Where would you look first for a bottleneck, and how does your OOP design help or hurt here?

**Expected Answer:** First look at: is `calculate_total()` re-computing from scratch on every read (O(n) over items each call) when it could be cached/incrementally updated on item add/remove? OOP design consideration: if `Order` encapsulates its items and *only* exposes `add_item()`/`remove_item()` (never raw list mutation), you can safely maintain a running total incrementally inside those methods — encapsulation isn't just "good practice," it's what *makes* this optimization safe (if the list were publicly mutable, you couldn't trust an incrementally-cached total to stay correct, since external code could mutate the list directly without going through your update logic). This ties encapsulation directly to a concrete performance/correctness benefit, not an abstract virtue.

**Why interviewer asks this:** Bridges LLD with scale/performance thinking — tests whether you see OOP principles as having *practical* consequences under load, a strong SDE-2 signal, especially at a company like Uber/Flipkart with real peak-traffic scenarios.

**Common Mistakes:**
- Treating this as a pure infra/scaling question disconnected from the OOP design (missing the connection between encapsulation and cache correctness)
- Not mentioning that a publicly mutable list would break the optimization's safety

**Follow-ups:** "What if two threads call `add_item()` on the same `Order` concurrently?"

**Best Follow-up Answer:** Need a lock (or an atomic/thread-safe data structure) around the mutation + running-total update inside `Order`, since a race between two concurrent `add_item()` calls could corrupt the running total (lost update problem) — again, this is only fixable *because* the mutation is encapsulated behind a method where you can add synchronization; if the list were exposed publicly, you couldn't enforce this from within `Order` at all.

---

# SECTION B: Notification System (Singleton, Observer, Strategy, Decorator)

## Q45. [Level 3] Your Notification System uses Observer for subscribers. Product now wants "user preference filtering" — a user should only be notified via channels they've opted into. Does Observer alone solve this, or do you need another pattern?

**Expected Answer:** Observer alone only solves *broadcast* (notifying all subscribers of an event) — it doesn't natively encode *per-subscriber filtering logic*. Two clean approaches: (1) Filter at the Subject side before notifying (Subject checks each observer's preferences before calling `update()`) — simple but couples the Subject to preference logic. (2) **Better**: each Observer implementation itself decides whether to act, inspecting the event and its own stored preference (e.g., `EmailObserver.update(event)` checks `if not self.user_prefs.email_enabled: return`) — keeps the Subject dumb/generic (better separation of concerns) at the cost of every observer duplicating a preference-check pattern (could be pulled into a shared base/decorator). Best of both: wrap observers in a **Decorator** (`PreferenceFilterDecorator(observer, prefs)`) that only forwards to the real observer if the preference allows it — combines Observer + Decorator cleanly, keeping both Subject and concrete Observer simple.

**Why interviewer asks this:** Requirements-evolution question testing whether you understand Observer's actual scope/limits and can combine patterns rather than distorting one pattern to do a job it wasn't meant for.

**Common Mistakes:**
- Cramming filtering logic into the Subject's `notify()` method (couples Subject to business rules it shouldn't know about)
- Not recognizing this as an opportunity to combine Decorator + Observer

**Follow-ups:** "Where would you store user preferences — on the Observer object, or fetched fresh each notification?"

**Best Follow-up Answer:** Fetch fresh (or from a short-lived cache) at notification time rather than storing stale preferences on the Observer object — preferences can change between subscription and notification, and a long-lived Observer object holding stale state is a correctness bug waiting to happen; this connects back to the "history constraint"/staleness discussions from LSP and cache design.

```python
class NotifierWithPreference(Observer):
    def __init__(self, real_observer: Observer, pref_service):
        self._real = real_observer
        self._prefs = pref_service   # fetched, not cached at construction

    def update(self, event):
        if self._prefs.is_channel_enabled(event.user_id, event.channel):
            self._real.update(event)
```

---

## Q46. [Level 4, SDE-2] Your Notification System uses Decorator for retry logic. Interviewer asks: "what happens if a `RetryDecorator` wraps a `RetryDecorator` by accident (double-wrapped)?" Is this a real risk, and how do you defend against it?

**Expected Answer:** Yes, real risk — Decorator's whole point is composability, so nothing structurally prevents double-wrapping the same behavior twice by mistake (e.g., a shared factory function applies a default retry wrapper, and a caller *also* wraps the result in another retry decorator, not realizing it's already wrapped). Effect: retries would compound multiplicatively (3 retries × 3 retries = up to 9 actual attempts), potentially causing much longer worst-case latency or hammering a failing downstream service harder than intended — this could actively worsen an incident (retry storms) rather than help. Defenses: (1) make wrapping explicit and centralized at one composition point (don't let arbitrary call sites apply decorators — apply them once, at construction, in a single documented place), (2) add a marker/idempotency check (e.g., `RetryDecorator` checks if the wrapped object is already a `RetryDecorator` and warns/raises), (3) prefer configuring retry behavior via a single, parameterized `RetryPolicy` object rather than stackable decorators for this specific concern, since retry semantics are usually not meant to compose the way logging/caching decorators are.

**Why interviewer asks this:** Senior-level edge-case/production-safety question — probes whether you think about the failure modes of your own pattern choices, especially around resilience patterns where mistakes have amplified real-world consequences (retry storms are a well-known cause of cascading outages).

**Common Mistakes:**
- Dismissing this as unlikely without a concrete defense mechanism
- Not connecting it to the retry-storm/cascading-failure real-world consequence

**Follow-ups:** "How does this connect to the Circuit Breaker pattern?"

**Best Follow-up Answer:** Circuit Breaker complements Retry by tracking failure rates and "opening" (short-circuiting further attempts) once a downstream service is clearly failing, which prevents exactly the retry-storm amplification risk described above — in production notification systems, Retry and Circuit Breaker are almost always used together, with Circuit Breaker acting as the safety net for when retries alone would make things worse.

---

## Q47. [Level 3] Why did you choose Singleton for a central `NotificationDispatcher` instead of just instantiating it once in `main()` and passing it around?

**Expected Answer (honest, self-critiquing):** The honest answer for most student/portfolio projects: "Singleton was a convenient way to get global access without threading the dependency through every layer manually — but in a production codebase with proper DI at the composition root, `main()`-level instantiation + injection would be equally correct and arguably better for testability, since I could substitute a fake `NotificationDispatcher` in tests without relying on the singleton's global state or needing a reset-between-tests mechanism." This kind of honest trade-off answer (rather than over-defending the choice) is exactly what separates strong candidates.

**Why interviewer asks this:** This is asked on *literally every* project that includes Singleton — interviewers specifically check if you'll defensively justify a choice or honestly discuss its trade-offs, which reveals engineering maturity.

**Common Mistakes:**
- Over-defending Singleton as objectively necessary
- Not being able to articulate the testability cost concretely (see Q22)

**Follow-ups:** "If you rebuilt this system today for a real company, what would you change?"

**Best Follow-up Answer:** Use a DI framework/manual composition root to construct one `NotificationDispatcher` instance and inject it into whatever needs it, keeping the "single instance" property as a *deployment/wiring* decision rather than baking it into the class itself — this keeps the class free of lifecycle-management responsibility (SRP) and fully testable.

---

# SECTION C: Document Editor (Strategy, Composition, Bridge-like Design)

## Q48. [Level 4] You describe your Document Editor as using "Bridge-like design." Explain precisely what Bridge pattern is, and why your design is Bridge-*like* rather than textbook Bridge — what's the actual difference?

**Expected Answer:** Bridge pattern decouples an abstraction from its implementation so both can vary independently — typically: a `Shape` abstraction holds a reference to a `DrawingAPI` implementor (e.g., `Circle` can be drawn via `OpenGLAPI` or `DirectXAPI`, and new shapes or new rendering APIs can be added independently without a combinatorial class explosion, similar in spirit to Strategy but specifically framed around separating *abstraction hierarchy* from *implementation hierarchy*, both allowed to have their own subclass trees). "Bridge-like" in a Document Editor context likely means: a `DocumentElement` abstraction (Paragraph, Image, Table) holds a reference to a `RenderStrategy`/`ExportFormatter` implementor (PDF renderer, HTML renderer, plain-text renderer) — the *document structure* hierarchy and the *rendering/export* hierarchy vary independently, but candidates should be honest that unless there are genuinely two independently-varying *hierarchies* (not just one interface with swappable implementations, which is closer to plain Strategy), it may be more accurately described as Strategy applied per-element rather than true textbook Bridge. The key technical distinction interviewers listen for: **Bridge is about decoupling two hierarchies that both have their own subclasses; Strategy is about swapping a single algorithm/behavior.**

**Why interviewer asks this:** "Bridge-like" is a term candidates sometimes use loosely on resumes — interviewer directly tests if you can articulate the precise boundary rather than hand-waving, and whether you can honestly say "it's actually closer to Strategy" if that's true.

**Common Mistakes:**
- Not being able to distinguish Bridge from Strategy at all when pressed (a real risk if "Bridge-like" was written without fully understanding true Bridge)
- Overclaiming textbook Bridge status without a genuine second varying hierarchy

**Follow-ups:** "Give a case where your Document Editor design would need TRUE Bridge, not just Strategy."

**Best Follow-up Answer:** If `DocumentElement` itself had its own growing subclass hierarchy (Paragraph → NumberedParagraph → NumberedParagraphWithComments...) AND the renderer side also had its own hierarchy (Renderer → StyledRenderer → StyledRenderer WithWatermark...), and *both* hierarchies needed to vary independently while remaining fully combinable, that's when true Bridge's structure (abstraction hierarchy + separate implementor hierarchy, bridged by composition) earns its keep over plain Strategy — Strategy usually assumes a flat set of interchangeable algorithms, not two independently growing hierarchies.

```python
from abc import ABC, abstractmethod

# Implementor hierarchy
class RenderEngine(ABC):
    @abstractmethod
    def render_text(self, text: str) -> str: ...

class PDFRenderEngine(RenderEngine):
    def render_text(self, text): return f"[PDF]{text}"

class HTMLRenderEngine(RenderEngine):
    def render_text(self, text): return f"<p>{text}</p>"

# Abstraction hierarchy, bridged to implementor via composition
class DocumentElement(ABC):
    def __init__(self, engine: RenderEngine):
        self.engine = engine       # the "bridge"
    @abstractmethod
    def render(self) -> str: ...

class Paragraph(DocumentElement):
    def __init__(self, engine: RenderEngine, text: str):
        super().__init__(engine)
        self.text = text
    def render(self):
        return self.engine.render_text(self.text)
```

---

## Q49. [Level 4, SDE-2] Document Editor: you need to support Undo/Redo. Which pattern is the textbook fit, and how would you integrate it with your existing Strategy-based formatting?

**Expected Answer:** **Command pattern** is the textbook fit for Undo/Redo — encapsulate each editing action (insert text, delete text, apply formatting) as a `Command` object with `execute()` and `undo()`, maintained in a history stack. Integration with existing Strategy-based formatting: a `FormatCommand` wraps *which* `FormatStrategy` was applied and stores enough state to reverse it (e.g., the previous formatting state) — `execute()` applies the new `FormatStrategy` to the element, `undo()` restores the prior formatting state. The two patterns compose cleanly: Strategy handles *how* formatting is applied; Command handles *making that application reversible and history-tracked*.

**Why interviewer asks this:** Common natural extension question for any editor-like LLD project — tests whether you know Command pattern (which is notably absent from your studied list, so this checks if you can reason about an unfamiliar-but-adjacent pattern on the spot) and can integrate it with what you already built.

**Common Mistakes:**
- Not knowing Command pattern at all and trying to force Strategy or Observer to do Undo/Redo (neither naturally models reversible, stackable history)
- Forgetting that `undo()` needs enough saved state to actually reverse the action (not just "call the opposite operation," which doesn't always exist symmetrically, e.g., undoing "delete text" needs the deleted text stored, not just an abstract "un-delete")

**Follow-ups:** "How would you implement Redo, and what happens to the redo stack when a new command is executed after an undo?"

**Best Follow-up Answer:** Maintain two stacks: `undo_stack` and `redo_stack`. `execute()` pushes the command onto `undo_stack` and **clears** `redo_stack` (a new action after undoing invalidates the previously-undone future — standard editor behavior, e.g., Word/Google Docs). `undo()` pops from `undo_stack`, calls `.undo()`, pushes onto `redo_stack`. `redo()` pops from `redo_stack`, calls `.execute()`, pushes back onto `undo_stack`.

```python
from abc import ABC, abstractmethod

class Command(ABC):
    @abstractmethod
    def execute(self): ...
    @abstractmethod
    def undo(self): ...

class FormatCommand(Command):
    def __init__(self, element, new_strategy, old_strategy):
        self.element = element
        self.new_strategy = new_strategy
        self.old_strategy = old_strategy   # saved for undo
    def execute(self):
        self.element.format_strategy = self.new_strategy
    def undo(self):
        self.element.format_strategy = self.old_strategy

class CommandHistory:
    def __init__(self):
        self.undo_stack: list[Command] = []
        self.redo_stack: list[Command] = []
    def execute(self, cmd: Command):
        cmd.execute()
        self.undo_stack.append(cmd)
        self.redo_stack.clear()            # invalidate redo on new action
    def undo(self):
        if self.undo_stack:
            cmd = self.undo_stack.pop()
            cmd.undo()
            self.redo_stack.append(cmd)
    def redo(self):
        if self.redo_stack:
            cmd = self.redo_stack.pop()
            cmd.execute()
            self.undo_stack.append(cmd)
```

---

## Q50. [Level 3, Composition] Your Document Editor models a document as `Document` composed of `List[DocumentElement]` where elements can be Paragraphs, Images, Tables — and a Table can itself contain Paragraphs inside cells. What structural pattern does this recursive "container holding similar things, including other containers" shape resemble, even if you didn't explicitly name it?

**Expected Answer:** This is the **Composite pattern** — even without explicitly naming it, treating `Table` (a container of elements) uniformly with `Paragraph`/`Image` (leaf elements) under a common `DocumentElement` interface, where operations like `render()` work identically whether called on a leaf or a container that recursively delegates to its children, is textbook Composite. Recognizing this in your own project (even if unnamed while building it) is a strong signal — Composite is extremely common in document/UI/file-system trees and interviewers want to see you recognize it in the wild, not just when explicitly labeled.

**Why interviewer asks this:** Tests pattern recognition in your OWN code — a great signal is realizing "oh, I used Composite without naming it," which shows structural understanding transfers beyond rote memorization of the 5 patterns you explicitly studied.

**Common Mistakes:**
- Not recognizing the pattern at all and describing it only as "a tree structure" without naming Composite
- Confusing this with simple Composition (the OOP relationship) — Composite (the *pattern*) is a specific application of composition where leaf and container share a uniform interface for recursive operations

**Follow-ups:** "How does `render()` work recursively for a Table containing Paragraphs?"

**Best Follow-up Answer:** `Table.render()` iterates its contained cells/elements (which may themselves be `Paragraph`s or nested `Table`s) and calls `.render()` on each uniformly — the client calling `document.render()` never needs to know whether it's dealing with a leaf or container, since both satisfy the same `DocumentElement.render()` contract; the recursion terminates naturally at leaf elements (Paragraphs, Images) that don't contain further children.

```python
from abc import ABC, abstractmethod

class DocumentElement(ABC):
    @abstractmethod
    def render(self) -> str: ...

class Paragraph(DocumentElement):          # leaf
    def __init__(self, text): self.text = text
    def render(self): return self.text

class Table(DocumentElement):              # composite/container
    def __init__(self):
        self.children: list[DocumentElement] = []
    def add(self, element: DocumentElement):
        self.children.append(element)
    def render(self) -> str:
        return "\n".join(child.render() for child in self.children)  # uniform, recursive

table = Table()
table.add(Paragraph("Cell 1"))
inner_table = Table()
inner_table.add(Paragraph("Nested cell"))
table.add(inner_table)                     # container inside container — works uniformly
print(table.render())
```

---

**Continue to Part 6 (Interview Puzzles, Debugging Bad Designs, Code Review, Refactoring Drills) → `06_Puzzles_Debugging_CodeReview.md`**
