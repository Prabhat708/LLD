# LLD Interview Handbook — Part 1: OOP

Format for every question: Question → Expected Answer → Why It's Asked → Common Mistakes → Follow-ups → Best Follow-up Answer → Code (if applicable) → Diagram (if applicable).

---

## Q1. [Level 1] What is the difference between a class and an object?

**Expected Answer:** A class is a blueprint/template that defines attributes (state) and methods (behavior). An object is a runtime instance of that class, occupying memory, with its own copy of instance attributes (unless static/class-level). Say it crisply: "Class is compile-time/definition-time; object is run-time/instance-time."

**Why interviewer asks this:** Filters candidates who've only memorized syntax vs those who understand the mental model. Sets up deeper questions on state vs behavior.

**Common Mistakes:**
- Saying "class and object are the same thing"
- Confusing "class variable" with "instance variable" when giving examples

**Follow-ups:**
- "Can two objects of the same class have different behavior?" 
- "What's a class variable vs instance variable?"

**Best Follow-up Answer:** Yes — via different instance state driving conditional behavior, or by injecting different strategy/dependency objects (this is a natural segue into Strategy pattern and DI). Class variables are shared across all instances (defined at class level); instance variables are per-object.

```python
class Car:
    wheels = 4  # class variable, shared

    def __init__(self, color):
        self.color = color  # instance variable, per-object
```

---

## Q2. [Level 1] Explain Encapsulation with a real-world example. Why is it not just "using private variables"?

**Expected Answer:** Encapsulation = bundling data + the methods that operate on it, while controlling/restricting direct external access to protect invariants. It's not merely "making fields private" — it's about exposing a controlled, intention-revealing interface (getters/setters, validated setters, or better, behavior methods) so the object's internal state can never become invalid. A `BankAccount` doesn't expose `balance` for direct mutation; it exposes `withdraw()`/`deposit()` which enforce invariants (balance ≥ 0).

**Why interviewer asks this:** Many candidates parrot "encapsulation = private fields." Interviewer wants to see if you understand it's about *invariant protection*, not just access modifiers.

**Common Mistakes:**
- Equating encapsulation with "private + getter/setter" (that's often just exposing the field indirectly — an anti-pattern called "anemic encapsulation")
- Not mentioning invariants at all

**Follow-ups:**
- "If you add a getter and setter for every private field, have you actually achieved encapsulation?"
- "How does encapsulation relate to SRP?"

**Best Follow-up Answer:** No — blind getters/setters for every field just reintroduce public mutable state through the back door; it's "encapsulation theater." True encapsulation means exposing behavior, not raw state, so invalid states are structurally impossible.

```python
class BankAccount:
    def __init__(self, balance: float):
        self.__balance = balance  # name-mangled, private

    def withdraw(self, amount: float):
        if amount > self.__balance:
            raise ValueError("Insufficient funds")
        self.__balance -= amount

    def get_balance(self) -> float:
        return self.__balance
```

---

## Q3. [Level 2] Differentiate Abstraction and Encapsulation. Candidates often confuse these — how would you explain the difference precisely?

**Expected Answer:** Abstraction is about *hiding complexity/showing only relevant behavior* (the "what," design-time decision — e.g., `Shape.area()` without exposing the formula). Encapsulation is about *hiding internal state and controlling access* (the "how is data protected," implementation-time mechanism — access modifiers). Abstraction is achieved through abstract classes/interfaces; encapsulation is achieved through access modifiers + method design. They're complementary, not the same axis.

**Why interviewer asks this:** Extremely common trick question — tests precision of understanding, not memorization.

**Common Mistakes:**
- Saying "they're the same thing"
- Giving encapsulation's definition when asked about abstraction

**Follow-ups:**
- "Can you have abstraction without encapsulation, or vice versa?"

**Best Follow-up Answer:** Yes to both. An abstract `PaymentMethod` interface with public mutable fields on implementers has abstraction without encapsulation. A fully encapsulated concrete class with no interface/abstract layer has encapsulation without abstraction.

---

## Q4. [Level 1-2] What is Inheritance? What problems does it solve, and what problems does it create?

**Expected Answer:** Inheritance lets a subclass reuse/extend behavior and state of a superclass ("is-a" relationship). It solves code reuse and enables polymorphism. It creates: tight coupling between parent/child (fragile base class problem), potential LSP violations, deep hierarchies that are hard to reason about, and it exposes the *entire* parent interface even when only some is applicable (a common ISP/LSP trap).

**Why interviewer asks this:** Wants to see if you'll default to inheritance blindly or reason about trade-offs — sets up "favor composition over inheritance."

**Common Mistakes:**
- Listing only benefits, not the drawbacks
- Not mentioning the fragile base class problem

**Follow-ups:**
- "Give an example where inheritance breaks LSP."

**Best Follow-up Answer:** Classic: `Square extends Rectangle`. Setting width and height independently is valid for Rectangle but breaks Square's invariant (width == height), so substituting Square wherever Rectangle is expected can silently break client code.

---

## Q5. [Level 2] Explain Polymorphism — compile-time vs run-time. Does Python/C++ support both? How?

**Expected Answer:** Polymorphism = "many forms" — same interface, different implementations.
- **Compile-time (static) polymorphism**: method overloading, resolved at compile time. C++ supports true overloading; Python does *not* support true overloading (last-defined method wins) — Python fakes it via default args, `*args/**kwargs`, or `functools.singledispatch`.
- **Run-time (dynamic) polymorphism**: method overriding, resolved via vtable/dynamic dispatch at runtime. Both C++ (via `virtual` functions) and Python (all methods are virtual by default) support this.

**Why interviewer asks this:** Language-nuance question — separates candidates who deeply know both languages from those who only know one.

**Common Mistakes:**
- Claiming Python supports overloading like C++ does
- Forgetting that C++ needs the `virtual` keyword for dynamic dispatch; without it, you get static binding (a classic C++ gotcha)

**Follow-ups:**
- "In C++, what happens if you call an overridden method through a base class pointer *without* `virtual`?"

**Best Follow-up Answer:** Static binding occurs — the base class version is called (not the derived override), because the compiler resolves the call at compile time based on the pointer's static type, not the object's dynamic type. This is why base class destructors should also be `virtual` (else derived destructors won't run → resource leaks).

```cpp
class Shape {
public:
    virtual double area() const { return 0; }
    virtual ~Shape() {}  // virtual destructor — critical
};
class Circle : public Shape {
    double r;
public:
    Circle(double r) : r(r) {}
    double area() const override { return 3.14159 * r * r; }
};
```

---

## Q6. [Level 2] Association vs Aggregation vs Composition — explain with lifetime/ownership semantics, not just "has-a."

**Expected Answer:**
- **Association**: A general relationship between two independent classes; neither owns the other; both can exist independently (e.g., `Teacher` and `Student`).
- **Aggregation**: A "has-a" relationship with *no ownership* — a whole-part relation where the part can outlive the whole (e.g., `Department` has `Professor`s; if the department is dissolved, professors still exist).
- **Composition**: A "has-a" relationship *with ownership and lifecycle binding* — the part cannot exist independently of the whole (e.g., `House` has `Room`s; destroy the house, the rooms cease to exist as separate entities).

The key differentiator interviewers want: **lifetime dependency**, not just UML diamond shape.

**Why interviewer asks this:** One of the most common LLD questions; separates rote UML memorizers from people who understand *why* the distinction matters for design (memory management, cascading deletes, design flexibility).

**Common Mistakes:**
- Saying "aggregation is hollow diamond, composition is filled diamond" and stopping there (correct but shallow)
- Not being able to give a code example showing the actual lifetime difference

**Follow-ups:**
- "Show composition vs aggregation in code."

**Best Follow-up Answer:**

```python
# Composition: Engine is created and destroyed with Car
class Engine:
    def __init__(self, hp: int):
        self.hp = hp

class Car:
    def __init__(self, hp: int):
        self.engine = Engine(hp)  # Car owns the Engine's lifecycle

# Aggregation: Professor exists independently of Department
class Professor:
    def __init__(self, name: str):
        self.name = name

class Department:
    def __init__(self, professors: list[Professor]):
        self.professors = professors  # injected, not owned/created
```

---

## Q7. [Level 3, SDE-1] What are Abstract Classes and Interfaces? When would you use one over the other?

**Expected Answer:** An abstract class can have both abstract (unimplemented) and concrete (implemented) methods, plus state (instance variables); it's used when subclasses share common implementation/state ("is-a" with shared code). An interface (in Python, an ABC with only abstract methods, or `Protocol`) declares *only* a contract — no shared implementation or state; used when unrelated classes need to guarantee the same capability ("can-do" relationship). Rule of thumb: abstract class for shared code + is-a hierarchy; interface for a capability contract across unrelated classes (supports multiple interface implementation, unlike multiple class inheritance which is discouraged).

**Why interviewer asks this:** Directly tests DIP/ISP readiness and hierarchy design judgment.

**Common Mistakes:**
- Saying "Python doesn't have interfaces" (it does — ABCs, or structural typing via `Protocol`)
- Not knowing a class can implement multiple interfaces but (in most single-inheritance-preferring designs) extend only one abstract class

**Follow-ups:**
- "Can Python classes have multiple inheritance? Should they?"

**Best Follow-up Answer:** Yes, Python supports multiple inheritance (MRO resolved via C3 linearization), but it's generally discouraged for concrete classes due to the diamond problem and fragile coupling — prefer multiple interface (ABC) implementation over multiple concrete-class inheritance.

```python
from abc import ABC, abstractmethod

class PaymentMethod(ABC):          # interface-like: pure contract
    @abstractmethod
    def pay(self, amount: float) -> bool: ...

class Vehicle(ABC):                # abstract class: shared state + contract
    def __init__(self, brand: str):
        self.brand = brand         # shared state

    def display_brand(self):       # shared concrete method
        print(self.brand)

    @abstractmethod
    def start_engine(self): ...    # must be implemented by subclass
```

---

## Q8. [Level 3, SDE-1, Coding] Design a `Shape` hierarchy (Circle, Rectangle, Triangle) demonstrating abstraction + polymorphism + encapsulation together. Interviewer will ask you to add a new shape live.

**Expected Answer (talk through, then code):** Define an abstract `Shape` with an abstract `area()` and `perimeter()`. Each concrete shape encapsulates its own dimensions as private attributes with validation in the constructor. A client function (e.g., `total_area(shapes: list[Shape])`) works polymorphically over any shape without knowing concrete types — this demonstrates OCP too (adding `Triangle` requires zero changes to client code).

**Why interviewer asks this:** Classic warm-up coding question that touches four pillars simultaneously and smoothly transitions into OCP/SOLID discussion.

**Common Mistakes:**
- Forgetting validation in constructors (negative radius, etc.)
- Making `area()` concrete in the base class with a `pass` or returning 0 instead of `@abstractmethod` (weakens the contract — subclasses could silently forget to override)
- Not writing a polymorphic client function to prove the point

**Follow-ups:**
- "Now add a `Square`. What do you need to change?"
- "How would you support shapes that need `volume()` too (3D shapes)? Same hierarchy or new one?"

**Best Follow-up Answer:** Adding `Square` requires zero changes to `Shape`, `total_area`, or other shapes — only a new class (OCP in action). For 3D shapes, don't force `volume()` onto the same `Shape` interface (that would violate ISP for 2D shapes that don't have volume) — create a separate `Solid` abstraction, or a `ThreeDimensional` mixin/interface that only 3D shapes implement.

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self) -> float: ...
    @abstractmethod
    def perimeter(self) -> float: ...

class Circle(Shape):
    def __init__(self, radius: float):
        if radius <= 0:
            raise ValueError("radius must be positive")
        self.__radius = radius
    def area(self) -> float:
        return 3.14159 * self.__radius ** 2
    def perimeter(self) -> float:
        return 2 * 3.14159 * self.__radius

class Rectangle(Shape):
    def __init__(self, w: float, h: float):
        self.__w, self.__h = w, h
    def area(self) -> float:
        return self.__w * self.__h
    def perimeter(self) -> float:
        return 2 * (self.__w + self.__h)

def total_area(shapes: list[Shape]) -> float:
    return sum(s.area() for s in shapes)   # polymorphic, no type checks
```

---

## Q9. [Level 4, SDE-2] "Favor composition over inheritance" — defend this principle with a concrete design failure caused by deep inheritance, and show the composition-based fix.

**Expected Answer:** Deep inheritance chains cause the **fragile base class problem** and **combinatorial explosion**: e.g., modeling `Bird` → `FlyingBird`, `SwimmingBird`, `FlyingSwimmingBird`... every new combination of capability needs a new class or forces awkward overrides (a `Penguin extends Bird` inheriting `fly()` it must override to throw an exception — an LSP violation). Composition fixes this by injecting behavior as interchangeable strategy objects (`FlyBehavior`, `SwimBehavior`) so capabilities combine freely at runtime without new classes per combination. This is literally the Strategy pattern applied to solve an inheritance-explosion problem — the canonical "Duck" example from Head First Design Patterns.

**Why interviewer asks this:** SDE-2 bar — wants a principled argument backed by a real failure mode, not a slogan.

**Common Mistakes:**
- Saying "composition is always better" without justifying when inheritance IS appropriate (true, stable "is-a" taxonomies with no behavioral variance, e.g., `Exception` hierarchies)
- Not connecting it to LSP

**Follow-ups:**
- "So is inheritance always bad? When would you still use it?"

**Best Follow-up Answer:** No — inheritance is appropriate for stable, narrow "is-a" taxonomies where subclasses genuinely don't need to swap behavior at runtime and truly satisfy LSP (e.g., exception hierarchies, or a `Shape` hierarchy where `area()` legitimately differs by shape and never needs to change per-instance). The rule isn't "never inherit," it's "don't inherit for code reuse of *varying* behavior — inherit for genuine taxonomic is-a with stable contracts."

```python
from abc import ABC, abstractmethod

class FlyBehavior(ABC):
    @abstractmethod
    def fly(self): ...

class CanFly(FlyBehavior):
    def fly(self): print("Flying high")

class CannotFly(FlyBehavior):
    def fly(self): print("I cannot fly")

class Duck:
    def __init__(self, fly_behavior: FlyBehavior):
        self.fly_behavior = fly_behavior   # composition, swappable at runtime
    def perform_fly(self):
        self.fly_behavior.fly()

mallard = Duck(CanFly())
rubber_duck = Duck(CannotFly())
```

---

## Q10. [Level 5, Senior] You inherit a codebase with a 6-level-deep inheritance hierarchy (`Employee → SalariedEmployee → Manager → SeniorManager → RegionalManager → VP`) where each level overrides 2-3 methods from its parent, and adding a new employee type requires touching 3 existing classes. How do you diagnose and refactor this?

**Expected Answer:** Diagnose: this is a **rigidity/fragility smell (OCP + fragile base class violation)** — deep hierarchies where changes ripple upward/downward indicate behavior is being modeled as *type* when it should be modeled as *composed data/strategy*. Refactor approach:
1. Identify the actual varying dimensions (e.g., "how bonus is calculated," "who they report to," "approval authority") — these are likely orthogonal, not truly hierarchical.
2. Flatten to a single `Employee` class composed of interchangeable strategies: `CompensationStrategy`, `ApprovalAuthority`, etc. (Strategy pattern), possibly combined with a `role` value object instead of a subclass per role.
3. Migrate incrementally — don't do a big-bang rewrite; use the **Strangler Fig** approach: introduce composition-based `Employee` alongside old hierarchy, migrate call sites, delete subclasses once unused.
4. Validate via tests before/after each step (characterization tests if none exist).

**Why interviewer asks this:** Senior-level system judgment question — real-world refactoring under constraints (can't rewrite everything at once), not textbook pattern application.

**Common Mistakes:**
- Jumping straight to "just use composition" without a migration plan
- Ignoring that a live production hierarchy can't be replaced atomically
- Not identifying *why* the hierarchy grew that way (usually: someone kept using inheritance for code reuse of loosely-related behavior)

**Follow-ups:**
- "How do you convince a team mid-sprint that this refactor is worth the risk?"

**Best Follow-up Answer:** Frame it in terms of measurable cost: cite the specific pain (3-class ripple per new employee type = velocity tax), propose an incremental, low-risk migration (strangler fig, one role at a time, behind tests), and tie it to an upcoming roadmap need (e.g., "we're about to add 4 new employee types this quarter — this refactor pays for itself by Q2").

---

**Continue to Part 2 (SOLID) → `02_SOLID_Interview_Questions.md`**
