# LLD Interview Handbook — Part 3: Design Patterns (Singleton, Factory Method, Decorator, Strategy, Observer)

---

## Q20. [Level 1] What problem does Singleton solve, and what are its two core requirements?

**Expected Answer:** Ensures a class has exactly one instance and provides a global access point to it. Two requirements: (1) private/controlled constructor so external code can't create new instances directly, (2) a static method (`get_instance()`) that creates the instance on first call and returns the same one thereafter.

**Why interviewer asks this:** Warm-up — but sets up deep thread-safety and anti-pattern discussion that follows.

**Common Mistakes:**
- Just saying "only one object exists" without mentioning the controlled-construction mechanism
- Confusing Singleton with a global variable (related failure mode, discussed in Q23)

**Follow-ups:**
- "Why not just use a module-level global variable in Python instead?"

**Best Follow-up Answer:** Python modules ARE naturally singletons (imported once, cached in `sys.modules`), so for simple cases a module-level instance is often the more idiomatic, simpler choice — the classic OOP Singleton pattern is more relevant in languages without that module caching guarantee (Java/C++), or when you need lazy initialization, subclassing, or controlled teardown that a bare module-level object doesn't give you cleanly.

```python
class DatabaseConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```

---

## Q21. [Level 3, SDE-1] Implement a thread-safe Singleton in Python and in C++. Explain the double-checked locking pattern and why the first `if` check outside the lock matters.

**Expected Answer:** Naive Singleton is not thread-safe — two threads can both pass the "is None" check before either sets the instance, creating two instances. Fix: lock around instance creation. **Double-checked locking**: check `if instance is None` (fast path, no lock) → only acquire the lock if it might be None → check again *inside* the lock (in case another thread created it while waiting for the lock) → create. The outer check avoids the *cost* of acquiring a lock on every single call after the instance already exists (locks are expensive); the inner check avoids the race.

**Why interviewer asks this:** Concurrency + Singleton is a very common SDE-1/2 pairing at product companies — tests real threading understanding, not just pattern syntax.

**Common Mistakes:**
- Forgetting the second check inside the lock (creates instance twice under race conditions)
- Not knowing that in C++11+, function-local `static` variables are already thread-safe by language guarantee (Meyer's Singleton) — simpler than manual double-checked locking

**Follow-ups:**
- "In C++11, what's the simplest thread-safe Singleton, and why don't you need manual locking?"

**Best Follow-up Answer:** Meyer's Singleton — a function-local `static` object. The C++11 standard guarantees that static local variable initialization is thread-safe (the compiler inserts synchronization automatically), so no manual double-checked locking is needed.

```cpp
class Singleton {
public:
    static Singleton& getInstance() {
        static Singleton instance;  // thread-safe init guaranteed by C++11 standard
        return instance;
    }
    Singleton(const Singleton&) = delete;
    Singleton& operator=(const Singleton&) = delete;
private:
    Singleton() {}
};
```

```python
import threading

class Singleton:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:                 # first check, no lock (fast path)
            with cls._lock:
                if cls._instance is None:          # second check, inside lock (race-safe)
                    cls._instance = super().__new__(cls)
        return cls._instance
```

---

## Q22. [Level 4, SDE-2] Why is Singleton often called an anti-pattern? List at least 3 concrete downsides and how you'd mitigate each.

**Expected Answer:**
1. **Global mutable state** → hidden coupling; any code anywhere can mutate shared state, making reasoning about the system harder. *Mitigate*: minimize mutable state in the singleton; prefer immutable configuration singletons.
2. **Testing difficulty** → singletons persist state across tests, causing test pollution/order-dependence; hard to mock since code calls `getInstance()` directly rather than receiving a dependency. *Mitigate*: inject the singleton instance as a dependency (constructor injection) rather than calling `getInstance()` inline everywhere; provide a `reset()` for tests, or better, avoid the pattern and use a DI container to manage single-instance lifetime instead.
3. **Hidden dependencies** → a class silently depending on `Logger.getInstance()` doesn't declare that dependency in its constructor, violating the Explicit Dependencies Principle and making the dependency graph invisible from the class signature.
4. **Violates SRP** → the class both manages its core responsibility AND manages its own lifecycle/instantiation control.

**Why interviewer asks this:** Senior-level pattern-critique question — wants to see you can argue *against* a pattern you just implemented, showing balanced judgment rather than pattern-worship.

**Common Mistakes:**
- Defending Singleton unconditionally ("it's fine, I use it all the time")
- Not offering mitigations, only criticisms

**Follow-ups:**
- "If Singleton has all these problems, what would you use instead for something like a logger or config manager?"

**Best Follow-up Answer:** Use a DI container/framework to manage the object's lifetime as a "single instance per application" scope, and inject it explicitly into constructors that need it — this gets the "only one instance" benefit while keeping dependencies visible and testable, without the global-access-point anti-pattern.

---

## Q23. [Level 2] Difference between Singleton and a plain global variable?

**Expected Answer:** A global variable can be reassigned/overwritten by any code and offers no construction control, no lazy initialization, no encapsulation of creation logic, and (in OOP languages) no polymorphism/subclassing support. Singleton controls *when* and *how* the instance is created (lazy init, thread-safety, validation), can be subclassed/mocked via interfaces, and encapsulates state behind methods rather than exposing a raw mutable variable.

**Why interviewer asks this:** Tests precision — many candidates think Singleton = "fancy global variable" without grasping the construction-control distinction.

**Common Mistakes:**
- "They're basically the same" (loses points for missing the encapsulation/lazy-init/polymorphism angle)

**Follow-ups:** "Is a Singleton just OOP-flavored global state, so does it have the same downsides?" 

**Best Follow-up Answer:** Yes, largely — the encapsulation is real but doesn't eliminate the *global mutable state* problem; that's exactly why Singleton is criticized alongside globals (see Q22).

---

## Q24. [Level 2] What is the Factory Method pattern? How is it different from just calling `ClassName()` directly?

**Expected Answer:** Factory Method defines an interface/method for creating an object, letting subclasses (or a parameter-driven branch) decide which concrete class to instantiate — the client code depends on an abstract product type, not concrete constructors. Difference from direct instantiation: direct `ClassName()` hardcodes the concrete type at the call site (tight coupling, violates DIP/OCP if the type needs to vary); Factory Method centralizes and abstracts creation logic so client code stays decoupled from concrete classes and new types can be added without touching client code.

**Why interviewer asks this:** Establishes the baseline before probing Factory vs Abstract Factory and Factory vs Strategy differences.

**Common Mistakes:**
- Confusing Factory Method with Abstract Factory (different scope — see Q28)
- Not explaining *why* it helps (DIP/OCP), only *what* it does

**Follow-ups:** "When would a simple `if/elif` factory function be fine vs when do you need the full Factory Method pattern with subclassing?"

**Best Follow-up Answer:** A simple conditional/parametrized factory *function* is fine and often preferred when there's no need for factory subclassing (i.e., a single creation policy suffices) — it's simpler and equally satisfies OCP for the *client* (client still depends on the abstraction, not concrete types). Full Factory Method (with factory subclasses) is warranted when *different creators* need to produce different families/defaults of the product polymorphically (e.g., `WindowsButtonFactory` vs `MacButtonFactory`).

```python
from abc import ABC, abstractmethod

class Notification(ABC):
    @abstractmethod
    def notify(self, msg: str): ...

class EmailNotification(Notification):
    def notify(self, msg): print(f"Email: {msg}")

class SMSNotification(Notification):
    def notify(self, msg): print(f"SMS: {msg}")

class NotificationFactory:
    @staticmethod
    def create(channel: str) -> Notification:
        if channel == "email":
            return EmailNotification()
        elif channel == "sms":
            return SMSNotification()
        raise ValueError(f"Unknown channel: {channel}")

# Client depends only on the abstraction + factory, never on concrete classes
notif = NotificationFactory.create("email")
notif.notify("Order shipped")
```

---

## Q25. [Level 4, SDE-2] Factory Method vs Abstract Factory — explain the distinction precisely, with an example where Abstract Factory is clearly necessary.

**Expected Answer:** Factory Method creates *one* product via *one* creation method (often overridden per subclass). Abstract Factory creates *families of related products* that must be used together, via multiple creation methods on one factory interface. Necessity example: a cross-platform UI toolkit needing `Button` + `Checkbox` + `Scrollbar` that must all match the same OS look-and-feel — `WindowsUIFactory` produces a matched `WindowsButton`+`WindowsCheckbox`+`WindowsScrollbar` set; `MacUIFactory` produces the Mac-matched set. A single Factory Method can't guarantee the *family consistency* (that all created widgets belong to the same theme) — Abstract Factory's whole purpose is enforcing that related-object consistency.

**Why interviewer asks this:** A very common "differentiate the patterns" question at SDE-2 level — Abstract Factory is frequently confused with Factory Method.

**Common Mistakes:**
- Saying "Abstract Factory is just Factory Method with more methods" without explaining the *family consistency* guarantee that's the actual point
- Giving an example that doesn't actually need multiple related products

**Follow-ups:** "Could you build the cross-platform UI example using only Factory Method? What would you lose?"

**Best Follow-up Answer:** You could use separate Factory Methods per widget type, but then nothing structurally *prevents* mixing a `WindowsButton` with a `MacCheckbox` at a call site — you'd lose the compile-time/structural guarantee that a consistent family is always produced together, which is Abstract Factory's core value.

```python
from abc import ABC, abstractmethod

class Button(ABC):
    @abstractmethod
    def render(self): ...
class Checkbox(ABC):
    @abstractmethod
    def render(self): ...

class WindowsButton(Button):
    def render(self): print("Windows-style button")
class WindowsCheckbox(Checkbox):
    def render(self): print("Windows-style checkbox")

class MacButton(Button):
    def render(self): print("Mac-style button")
class MacCheckbox(Checkbox):
    def render(self): print("Mac-style checkbox")

class UIFactory(ABC):                     # Abstract Factory
    @abstractmethod
    def create_button(self) -> Button: ...
    @abstractmethod
    def create_checkbox(self) -> Checkbox: ...

class WindowsUIFactory(UIFactory):
    def create_button(self): return WindowsButton()
    def create_checkbox(self): return WindowsCheckbox()

class MacUIFactory(UIFactory):
    def create_button(self): return MacButton()
    def create_checkbox(self): return MacCheckbox()
```

---

## Q26. [Level 2-3] Explain the Decorator pattern. How does it differ from just subclassing to add behavior?

**Expected Answer:** Decorator wraps an object to add responsibilities dynamically at runtime, without altering the original class and without the combinatorial subclass explosion inheritance causes. Both decorator and the wrapped object implement the same interface, so decorators are composable and transparent to clients. Difference from subclassing: subclassing adds behavior *statically* (fixed at compile-time, one combination per subclass — e.g., `MilkCoffee`, `SugarCoffee`, `MilkSugarCoffee`... explodes with N add-ons into 2^N subclasses); Decorator adds behavior *dynamically* by wrapping, letting you stack any combination at runtime (`SugarDecorator(MilkDecorator(Coffee()))`) with only N decorator classes total, not 2^N.

**Why interviewer asks this:** Classic pattern-differentiation question that directly tests "why not just use inheritance" reasoning (ties back to composition-over-inheritance).

**Common Mistakes:**
- Not mentioning the exponential subclass explosion inheritance would cause
- Forgetting that Decorator requires the decorator to implement the *same interface* as the wrapped object (so it's transparent/substitutable — an LSP-respecting design)

**Follow-ups:** "Order matters when stacking decorators — give an example where wrapping order changes behavior/output."

**Best Follow-up Answer:** `EncryptDecorator(CompressDecorator(FileWriter()))` vs `CompressDecorator(EncryptDecorator(FileWriter()))` — compress-then-encrypt vs encrypt-then-compress produce different (and the latter typically worse, since encrypted data doesn't compress well) results, even though both are "valid" stackings — decorator order is a real design decision, not incidental.

```python
from abc import ABC, abstractmethod

class Coffee(ABC):
    @abstractmethod
    def cost(self) -> float: ...
    @abstractmethod
    def description(self) -> str: ...

class SimpleCoffee(Coffee):
    def cost(self): return 2.0
    def description(self): return "Coffee"

class CoffeeDecorator(Coffee):             # decorators share the base interface
    def __init__(self, coffee: Coffee):
        self._coffee = coffee
    def cost(self): return self._coffee.cost()
    def description(self): return self._coffee.description()

class MilkDecorator(CoffeeDecorator):
    def cost(self): return self._coffee.cost() + 0.5
    def description(self): return self._coffee.description() + " + Milk"

class SugarDecorator(CoffeeDecorator):
    def cost(self): return self._coffee.cost() + 0.2
    def description(self): return self._coffee.description() + " + Sugar"

order = SugarDecorator(MilkDecorator(SimpleCoffee()))
print(order.description(), order.cost())   # Coffee + Milk + Sugar 2.7
```

---

## Q27. [Level 3] What is the Strategy pattern? How is it different from Decorator — both "wrap" behavior via composition, so what's the actual distinction?

**Expected Answer:** Strategy encapsulates *interchangeable algorithms* for a single task and lets the client swap which algorithm is used (e.g., different sorting/payment/routing algorithms) — the strategies are *mutually exclusive alternatives* for doing the same job. Decorator *adds/stacks* additional responsibilities *on top of* existing behavior — decorators are *additive and composable*, not alternatives (you can stack many decorators; you pick exactly one strategy at a time). Structurally similar (composition + shared interface + delegation) but their *intent* differs: Strategy = "choose one algorithm," Decorator = "layer on extra behavior."

**Why interviewer asks this:** Very common "these look the same in code, what's actually different" trap question — tests intent-level pattern understanding vs surface structure memorization.

**Common Mistakes:**
- Saying "they're basically the same pattern" (loses points — intent matters, not just UML shape)
- Not being able to articulate "mutually exclusive" vs "additive/stackable" distinction

**Follow-ups:** "Can you combine Strategy and Decorator in the same design? Give an example."

**Best Follow-up Answer:** Yes — e.g., a `PaymentProcessor` uses Strategy to select *how* to charge (CreditCard, PayPal, UPI — mutually exclusive), while Decorator wraps the chosen strategy to *add* cross-cutting behavior like logging, retry, or fraud-check on top, regardless of which strategy was chosen.

```python
from abc import ABC, abstractmethod

class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount: float): ...

class CreditCardPayment(PaymentStrategy):
    def pay(self, amount): print(f"Paid {amount} via Credit Card")

class UPIPayment(PaymentStrategy):
    def pay(self, amount): print(f"Paid {amount} via UPI")

class PaymentContext:
    def __init__(self, strategy: PaymentStrategy):
        self.strategy = strategy               # swappable at runtime
    def execute_payment(self, amount: float):
        self.strategy.pay(amount)

context = PaymentContext(UPIPayment())
context.execute_payment(500)
context.strategy = CreditCardPayment()          # swap strategy
context.execute_payment(1000)
```

---

## Q28. [Level 3] Explain the Observer pattern. What's the difference between "push" and "pull" models, and which would you choose for a stock price ticker with 10,000 subscribers?

**Expected Answer:** Observer defines a one-to-many dependency: when the Subject's state changes, all registered Observers are notified automatically, without the Subject knowing concrete Observer types (loose coupling). **Push model**: Subject sends the full changed data to observers in the notification call (`update(new_price)`). **Pull model**: Subject just signals "something changed"; observers query the Subject for the specific data they need (`update(subject); subject.get_price()`). For 10,000 stock ticker subscribers: prefer **push with minimal payload** (just the changed price) for efficiency at scale — pull would mean every one of 10,000 observers makes a call back into the subject, increasing coupling and potentially causing contention; but push must avoid over-sending large objects — send only what changed, not the entire subject state, to keep notification cheap at scale.

**Why interviewer asks this:** Real-world Observer implementation reasoning at scale — tests whether you can reason about performance implications of a pattern, not just recite its structure.

**Common Mistakes:**
- Not knowing push vs pull terminology at all
- Not connecting the choice to the *scale* constraint given in the question (10,000 subscribers)

**Follow-ups:** "What happens if an Observer's `update()` throws an exception — should it break notification for the remaining 9,999 observers?"

**Best Follow-up Answer:** No — the Subject's notify loop should catch and isolate exceptions per-observer (log and continue) so one misbehaving observer doesn't prevent the rest from being notified; this is a common production robustness detail interviewers listen for.

```python
from abc import ABC, abstractmethod

class Observer(ABC):
    @abstractmethod
    def update(self, price: float): ...

class Subject:
    def __init__(self):
        self._observers: list[Observer] = []
    def subscribe(self, obs: Observer):
        self._observers.append(obs)
    def unsubscribe(self, obs: Observer):
        self._observers.remove(obs)
    def notify(self, price: float):
        for obs in self._observers:
            try:
                obs.update(price)              # push model — minimal payload
            except Exception as e:
                print(f"Observer failed: {e}")  # isolate failures

class StockTicker(Subject):
    def set_price(self, price: float):
        self.notify(price)

class MobileAppObserver(Observer):
    def update(self, price: float):
        print(f"Mobile app shows price: {price}")
```

---

## Q29. [Level 4, SDE-2] Observer pattern + threading: if multiple threads call `subscribe()`/`unsubscribe()` while another thread is mid-`notify()`, what breaks, and how do you fix it?

**Expected Answer:** Iterating over a list while another thread mutates it concurrently causes a `RuntimeError: list changed size during iteration` in Python (or undefined behavior/crashes in C++ with unsynchronized vectors) — a classic concurrent-modification bug. Fixes: (1) copy the observer list before iterating (`for obs in list(self._observers):`) so notify() iterates a snapshot while subscribe/unsubscribe mutate the live list safely, or (2) use a lock around both mutation and notification (simpler but serializes and can deadlock if an observer's `update()` tries to subscribe/unsubscribe itself), or (3) use a thread-safe/copy-on-write collection.

**Why interviewer asks this:** SDE-2 signal — pattern + concurrency correctness combined, a favorite at product companies with high-concurrency systems (Uber, Amazon).

**Common Mistakes:**
- Not identifying this as a concurrent-modification-during-iteration bug at all
- Proposing a lock that wraps `notify()` entirely, without noticing this can deadlock if an observer callback tries to re-enter subscribe/unsubscribe on the same lock (reentrancy issue)

**Follow-ups:** "How would you avoid the deadlock risk in your lock-based fix?"

**Best Follow-up Answer:** Use a reentrant lock (`threading.RLock` in Python) so the same thread can re-acquire it without deadlocking if a callback re-enters, or better, avoid holding the lock during the actual `update()` calls — snapshot the list under the lock, release it, then notify outside the lock.

```python
import threading

class Subject:
    def __init__(self):
        self._observers: list[Observer] = []
        self._lock = threading.Lock()
    def subscribe(self, obs):
        with self._lock:
            self._observers.append(obs)
    def unsubscribe(self, obs):
        with self._lock:
            self._observers.remove(obs)
    def notify(self, price):
        with self._lock:
            snapshot = list(self._observers)   # copy under lock
        for obs in snapshot:                   # notify outside lock — no deadlock risk
            obs.update(price)
```

---

## Q30. [Level 4] "Why not use Observer instead of Strategy here?" — a common interviewer trap. Given a `PaymentProcessor` that must select exactly one payment method to execute a charge, explain why Observer is the wrong pattern and Strategy is right.

**Expected Answer:** Observer is for one-to-*many* broadcast notification where *all* observers react (a "someone needs to know this happened" relationship) — it's not for *selecting a single algorithm to execute*. Using Observer here would mean "notifying" multiple payment methods and somehow picking one to actually act, which misuses the pattern's intent (multiple reactions) for a single-selection problem. Strategy directly models "pick one algorithm, execute it" — the correct intent match. Rule for interviews: always match pattern to *intent* (what problem is being solved — selection vs broadcast vs staged construction vs structural wrapping), not to surface structural similarity.

**Why interviewer asks this:** Classic "why not pattern X" question that tests whether you choose patterns by intent or by memorized structure — a strong signal of real design maturity.

**Common Mistakes:**
- Trying to force-fit Observer with a "first responder wins" hack instead of just saying it's the wrong pattern
- Not being able to name the actual *intent* difference (broadcast vs selection)

**Follow-ups:** "Where WOULD Observer correctly appear in a payment system?"

**Best Follow-up Answer:** After a payment completes, multiple independent systems need to *react* to that event — send a receipt email, update analytics, trigger a loyalty-points service, alert fraud detection — that's a genuine one-to-many broadcast, correctly modeled with Observer (or an event bus/pub-sub, which is Observer at a system/service scale).

---

## Q31. [Level 5, Senior, Pattern Identification] You review this code in a PR. Identify every pattern being used (correctly or incorrectly) and flag any misuse:

```python
class Logger:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

class ShapeFactory:
    def create(self, kind): ...

class Shape(ABC):
    @abstractmethod
    def draw(self): ...

class BorderedShape(Shape):
    def __init__(self, shape: Shape):
        self.shape = shape
    def draw(self):
        self.shape.draw()
        print("with border")

class ShapeChangeListener(ABC):
    @abstractmethod
    def on_change(self, shape): ...

class ShapeEditor(Shape):
    def __init__(self):
        self.listeners = []
    def add_listener(self, l): self.listeners.append(l)
    def draw(self):
        for l in self.listeners:
            l.on_change(self)
```

**Expected Answer:** `Logger` = Singleton (correctly implemented, though see Q22 for whether it *should* be used at all). `ShapeFactory` = Factory Method. `BorderedShape` = Decorator (correctly wraps `Shape`, same interface, adds behavior). `ShapeChangeListener` + `ShapeEditor.listeners` = Observer — but **misuse flag**: `ShapeEditor` extends `Shape` *and* implements Observer's subject role *and* the `draw()` method is firing `on_change` notifications instead of actually drawing — this conflates "draw" (rendering responsibility) with "notify of change" (event responsibility), an SRP violation baked into a pattern misuse: `draw()` should render; a separate method like `notify_change()` should fire listener updates when the shape's state actually changes (not every draw call).

**Why interviewer asks this:** Senior-level code review / pattern-identification-in-the-wild question — tests real ability to spot patterns AND their subtle misapplications in unfamiliar code, the actual on-the-job skill.

**Common Mistakes:**
- Correctly naming the patterns but missing the SRP violation buried in `ShapeEditor.draw()`
- Not noticing `ShapeEditor` inheriting `Shape` while also being an Observer Subject bloats its responsibility (is it a shape, or a shape-change publisher, or both — should probably be composition, not inheritance, of the "shape" role)

**Follow-ups:** "How would you restructure `ShapeEditor`?"

**Best Follow-up Answer:** Separate concerns: `ShapeEditor` composes a `Shape` (not inherits it) and owns the listener list; `draw()` delegates to the composed shape; a distinct `set_shape()`/`edit()` method mutates state and calls `notify_change()` to fire listeners — decoupling "is a drawable thing" from "manages change notifications."

---

**Continue to Part 4 (Object Relationships & Core Design Concepts) → `04_Object_Relationships_and_Design_Concepts.md`**
