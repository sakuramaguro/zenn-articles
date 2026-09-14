import Mathlib

namespace LeanBook.Ch05

-- BEGIN SOURCE ch05_021

-- 次元定理の完全証明
-- 数学：dim V = dim(ker f) + dim(Im f)
theorem dimension_theorem {K V W : Type*}
    [Field K]
    [AddCommGroup V] [Module K V] [FiniteDimensional K V]
    [AddCommGroup W] [Module K W]
    (f : V →ₗ[K] W) :
    Module.finrank K V = Module.finrank K (LinearMap.ker f) +
                         Module.finrank K (LinearMap.range f) := by
  -- ① ker f は有限次元（V の部分空間なので）
  have h_ker : FiniteDimensional K (LinearMap.ker f) :=
    FiniteDimensional.finiteDimensional_submodule f.ker
  -- ② Im f は有限次元（線形写像の像なので）
  have h_range : FiniteDimensional K (LinearMap.range f) :=
    Module.Finite.range f
  -- ③ 次元加法性定理を取り出す
  have key := LinearMap.finrank_range_add_finrank_ker f
  -- ④ 左右・順番のズレを omega が吸収する
  omega
  -- No goals ✓
-- END SOURCE ch05_021

-- BEGIN SOURCE ch05_022
#print axioms dimension_theorem
-- END SOURCE ch05_022

end LeanBook.Ch05
