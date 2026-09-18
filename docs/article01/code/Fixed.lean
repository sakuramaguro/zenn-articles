def add_five (n : Nat) : Nat := n + 5

#check add_five
#eval add_five 7
#eval add_five 0
#eval add_five 100

example (n : Nat) : add_five n = n + 5 := by
  rfl
