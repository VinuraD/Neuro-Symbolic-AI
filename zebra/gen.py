from __future__ import annotations
import itertools
import numpy as np
from ortools.sat.python import cp_model
import random
import typing
from .utils import Constraint


DEFAULT_CATEGORIES = {
    "color":["red", "green", "white", "yellow", "blue"],
    "nation":["brit", "swede", "dane", "norwegian", "german"],
    "pet":["dog", "bird", "cat", "horse", "fish"],
    "drink":["tea", "coffee", "milk", "beer", "water"],
    "hobby":["painting", "reading", "swimming", "guitar", "cooking"]
}



def _n_categories(categories=DEFAULT_CATEGORIES):
    return len(categories)


n=_n_categories(DEFAULT_CATEGORIES)

#maps categories and variable names to the variable objects
def build_model(categories=DEFAULT_CATEGORIES, n=5,clues=[]):
    model = cp_model.CpModel()
    variables = {}
    for cat,val in categories.items():
        for v in val:
            variables[(cat,v)] = model.NewIntVar(1,n,f"{cat}_{v}")
        model.AllDifferent([variables[(cat,v)] for v in val]) #each value in a categoruy can only be assigned to one house


    for clue in clues:
        if isinstance(clue, Constraint):
            clue_type = clue.type
            args = clue.args
        else:
            clue_type = clue[0]
            args = clue[1:]

        if clue_type == "eq":
            _, (cat1, val1), (cat2, val2) = args
            model.Add(variables[(cat1, val1)] == variables[(cat2, val2)])
        elif clue_type == "pos":
            _, (cat1, val1), pos = args
            model.Add(variables[(cat1,val1)]==pos)
        elif clue_type=="left_of":
            _,(cat1,val1), (cat2,val2)=clue
            model.Add(variables[(cat1,val1)]==variables[(cat2,val2)]-1)
        elif clue_type=="next_to":
            _,(cat1,val1), (cat2,val2)=clue
            diff=model.NewIntVar(-n,n,"")
            dist=model.NewIntVar(0,n,"")
            model.Add(diff==variables[(cat1,val1)]-variables[(cat2,val2)])
            model.AddAbsEquality(dist,diff)
            model.Add(dist==1) #either on left or right
        elif clue_type=="neq":
            _, (cat1,val1), (cat2,val2)=clue
            model.Add(variables[(cat1,val1)]!=variables[(cat2,val2)])
    return model, variables

class _SolutionCounter(cp_model.CpSolverSolutionCallback):
    def __init__(self,limit=2):
        self.count=0
        self._limit=limit

    def on_solution_callback(self):
        self.count+=1
        if self.count>=self._limit:
            self.StopSearch()


def count_solutions(categories,clues,limit=2):
    model,_=build_model(categories,clues)
    solver=cp_model.CpSolver()
    solver.parameters.enumerate_all_solutions=True
    solver.parameters.num_search_workers=1
    counter=_SolutionCounter(limit)
    solver.Solve(model,counter)
    return counter.count   

def solve(categories, clues):
    model, pos = build_model(categories, clues)
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return None
    grid={h : {} for h in range(1,n+1)}
    for (cat,val), var in pos.items():
        grid[solver.Value(var)][cat]=val
    return grid

def random_solution(categories,rng):
    grid={h : {} for h in range(1,n+1)}
    for cat,vals in categories.items():
        houses=list(range(1,n+1))
        rng.shuffle(houses)
        for val,h in zip(vals,houses):
            grid[h][cat]=val
    return grid

def derive_true_clues(categories, solution, rng):
    """Generate a pool of clues that are all TRUE for `solution`.

    Includes every 'pos' clue (so the pool alone pins the unique solution),
    plus same-house, adjacency, and a sample of difference clues.
    """
    cats = list(categories.keys())
    # position of each attribute in the solution
    where = {}
    for h in range(1, n + 1):
        for cat, val in solution[h].items():
            where[(cat, val)] = h

    clues = []
    # fixed positions (guarantee the starting set is uniquely solvable)
    for attr, h in where.items():
        clues.append(("pos", attr, h))
    # same-house pairs (one per distinct category pair per house)
    for h in range(1, n + 1):
        attrs = [(c, solution[h][c]) for c in cats]
        for a, b in itertools.combinations(attrs, 2):
            clues.append(("eq", a, b))
    # adjacency clues (immediate-left and next-to) across adjacent houses
    for h in range(1, n):
        left = [(c, solution[h][c]) for c in cats]
        right = [(c, solution[h + 1][c]) for c in cats]
        for a in left:
            for b in right:
                clues.append(("imm_left", a, b))
                clues.append(("next", a, b))
    # a sample of difference clues (there are many; keep a handful)
    diff_pool = []
    attrs_all = list(where.keys())
    for a, b in itertools.combinations(attrs_all, 2):
        if where[a] != where[b]:
            diff_pool.append(("neq", a, b))
    rng.shuffle(diff_pool)
    clues.extend(diff_pool[: 2 * n])

    rng.shuffle(clues)
    return clues


def generate_unique_puzzle(categories=None, seed=None, prefer_relational=True):
    """Generate (clues, solution) where `clues` uniquely determine `solution`.

    Strategy: derive all true clues (over-determined => unique), then greedily
    remove clues that are not needed for uniqueness. If `prefer_relational`,
    try to drop 'pos' clues first so the final puzzle leans on relations.
    """
    if categories is None:
        categories = DEFAULT_CATEGORIES
    rng = random.Random(seed)

    solution = random_solution(categories, rng)
    pool = derive_true_clues(categories, solution, rng)

    # sanity: the full pool must be uniquely solvable
    assert is_unique(categories, pool), "true-clue pool was not unique (bug)"

    # order trimming: drop 'pos' clues first for more interesting puzzles
    order = sorted(range(len(pool)),
                   key=lambda i: (0 if (prefer_relational and pool[i][0] == "pos") else 1))
    order = sorted(order, key=lambda i: rng.random())  # light shuffle within
    if prefer_relational:
        order.sort(key=lambda i: 0 if pool[i][0] == "pos" else 1)

    kept = list(pool)
    for i in order:
        clue = pool[i]
        if clue not in kept:
            continue
        trial = [c for c in kept if c is not clue]
        if is_unique(categories, trial):
            kept = trial
    return kept, solution


# --------------------------------------------------------------------------
# rendering (template-based; the neural renderer replaces this later)
# --------------------------------------------------------------------------
def render_clue(clue):
    kind = clue[0]
    if kind == "pos":
        _, (c, v), p = clue
        return f"The {v} ({c}) is in house {p}."
    if kind == "eq":
        _, (c1, v1), (c2, v2) = clue
        return f"The {v1} ({c1}) shares a house with the {v2} ({c2})."
    if kind == "neq":
        _, (c1, v1), (c2, v2) = clue
        return f"The {v1} ({c1}) is not in the same house as the {v2} ({c2})."
    if kind == "imm_left":
        _, (c1, v1), (c2, v2) = clue
        return f"The {v1} ({c1}) is immediately left of the {v2} ({c2})."
    if kind == "next":
        _, (c1, v1), (c2, v2) = clue
        return f"The {v1} ({c1}) is next to the {v2} ({c2})."
    return str(clue)


def render_solution(categories, solution):
    # n = _n_houses(categories)
    cats = list(categories.keys())
    width = max(len(c) for c in cats) + 1
    lines = ["house: " + "  ".join(f"{h:>8}" for h in range(1, n + 1))]
    for c in cats:
        row = "  ".join(f"{solution[h][c]:>8}" for h in range(1, n + 1))
        lines.append(f"{c:<{width}}: {row}")
    return "\n".join(lines)

def constraint_to_str(constraint):
    if isinstance(constraint, Constraint):
        return render_clue((constraint.type, *constraint.args))
    return str(constraint)

# # --------------------------------------------------------------------------
# # demo / self-test
# # --------------------------------------------------------------------------
# if __name__ == "__main__":
#     cats = DEFAULT_CATEGORIES
#     clues, solution = generate_unique_puzzle(cats, seed=7)

#     print(f"Generated a puzzle with {len(clues)} clues.\n")
#     for clue in clues:
#         print("  - " + render_clue(clue))

#     print("\nIntended solution:")
#     print(render_solution(cats, solution))

#     # verify: unique, and the solver recovers exactly the intended solution
#     n_sols = count_solutions(cats, clues, limit=2)
#     recovered = solve(cats, clues)
#     print(f"\nself-test: solution count (capped at 2) = {n_sols}")
#     print(f"self-test: unique = {is_unique(cats, clues)}")
#     print(f"self-test: solver matches intended solution = {recovered == solution}")