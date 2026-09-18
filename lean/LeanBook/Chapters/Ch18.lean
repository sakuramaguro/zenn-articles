import Mathlib

namespace LeanBook.Ch18

-- BEGIN SOURCE ch18_001
open MeasureTheory
open scoped ENNReal

-- 型の全体は実際の #check 出力で確認する。コメントは要約。
#check @MeasureTheory.Lp
#check @MeasureTheory.MemLp
-- MemLp f p μ = AEStronglyMeasurable f μ ∧ eLpNorm f p μ < ∞
#check @IsProbabilityMeasure

-- この定義自体は可積分性や確率測度の仮定を受け取らない。
noncomputable def expectation {Ω : Type*} [MeasurableSpace Ω]
    (P : Measure Ω) (X : Ω → ℝ) : ℝ :=
  ∫ ω, X ω ∂P
#check @expectation

theorem expectation_const {Ω : Type*} [MeasurableSpace Ω]
    (P : Measure Ω) [IsProbabilityMeasure P] (c : ℝ) :
    expectation P (fun _ => c) = c := by
  rw [expectation, integral_const]
  simp

#check @MeasureTheory.Filtration
#check @MeasureTheory.Martingale
-- END SOURCE ch18_001

-- BEGIN SOURCE ch18_002
open MeasureTheory
open scoped ENNReal

#check @MeasureTheory.Lp

-- 定義域と測度を明示する。
#check (inferInstance : NormedAddCommGroup (Lp ℝ 2 (volume : Measure ℝ)))
#check (inferInstance : NormedSpace ℝ (Lp ℝ 2 (volume : Measure ℝ)))
#check (inferInstance : InnerProductSpace ℝ (Lp ℝ 2 (volume : Measure ℝ)))
#check (inferInstance : CompleteSpace (Lp ℝ 2 (volume : Measure ℝ)))
-- END SOURCE ch18_002

-- BEGIN SOURCE ch18_003
open MeasureTheory
open scoped ENNReal

#check @MeasureTheory.MemLp
#print MeasureTheory.MemLp
#check @MeasureTheory.memLp_const
#check @MeasureTheory.memLp_one_iff_integrable
#check @MeasureTheory.eLpNorm_eq_lintegral_rpow_enorm_toReal

theorem memLp_definition (f : ℝ → ℝ) (p : ℝ≥0∞) (μ : Measure ℝ) :
    MemLp f p μ ↔ AEStronglyMeasurable f μ ∧ eLpNorm f p μ < ∞ :=
  Iff.rfl

theorem constant_memLp (c : ℝ) (p : ℝ≥0∞) (μ : Measure ℝ)
    [IsFiniteMeasure μ] : MemLp (fun _ => c) p μ :=
  memLp_const c

theorem memLp_one_on (f : ℝ → ℝ) (s : Set ℝ) :
    MemLp f 1 (volume.restrict s) ↔ IntegrableOn f s volume :=
  memLp_one_iff_integrable

-- 0・有限の正の指数・∞を分ける。
theorem eLpNorm_at_zero (f : ℝ → ℝ) (μ : Measure ℝ) :
    eLpNorm f 0 μ = 0 := by
  simp

theorem eLpNorm_at_finite (f : ℝ → ℝ) (p : ℝ≥0∞) (μ : Measure ℝ)
    (hp0 : p ≠ 0) (hptop : p ≠ ∞) :
    eLpNorm f p μ = (∫⁻ x, ‖f x‖ₑ ^ p.toReal ∂μ) ^ (1 / p.toReal) :=
  eLpNorm_eq_lintegral_rpow_enorm_toReal hp0 hptop

theorem eLpNorm_at_top (f : ℝ → ℝ) (μ : Measure ℝ) :
    eLpNorm f ∞ μ = eLpNormEssSup f μ :=
  eLpNorm_exponent_top
-- END SOURCE ch18_003

-- BEGIN SOURCE ch18_004
open MeasureTheory

#print IsProbabilityMeasure

theorem probability_univ {Ω : Type*} [MeasurableSpace Ω]
    (P : Measure Ω) [IsProbabilityMeasure P] : P Set.univ = 1 :=
  IsProbabilityMeasure.measure_univ

-- Leanの測度は任意の部分集合で評価できる。この不等式には可測性は不要。
theorem probability_le_one {Ω : Type*} [MeasurableSpace Ω]
    (P : Measure Ω) [IsProbabilityMeasure P] (A : Set Ω) : P A ≤ 1 :=
  prob_le_one

theorem probability_of_univ_eq_one {Ω : Type*} [MeasurableSpace Ω]
    (P : Measure Ω) (hP : P Set.univ = 1) : IsProbabilityMeasure P :=
  ⟨hP⟩
-- END SOURCE ch18_004

-- BEGIN SOURCE ch18_005
open MeasureTheory

-- 可測性の証明そのものには、確率測度は必要ない。
theorem random_variable_preimage {Ω : Type*} [MeasurableSpace Ω]
    (X : Ω → ℝ) (hX : Measurable X) (B : Set ℝ) (hB : MeasurableSet B) :
    MeasurableSet (X ⁻¹' B) :=
  hX hB
-- END SOURCE ch18_005

-- BEGIN SOURCE ch18_006
open MeasureTheory

noncomputable def myExpectation {Ω : Type*} [MeasurableSpace Ω]
    (P : Measure Ω) (X : Ω → ℝ) : ℝ :=
  ∫ ω, X ω ∂P

-- 加法性を使う段階では両方の可積分性が必要。
theorem expectation_add {Ω : Type*} [MeasurableSpace Ω] (P : Measure Ω)
    (X Y : Ω → ℝ) (hX : Integrable X P) (hY : Integrable Y P) :
    myExpectation P (fun ω => X ω + Y ω) =
      myExpectation P X + myExpectation P Y :=
  integral_add hX hY
-- END SOURCE ch18_006

-- BEGIN SOURCE ch18_007
open MeasureTheory

theorem integral_const_probability {Ω : Type*} [MeasurableSpace Ω]
    (P : Measure Ω) [IsProbabilityMeasure P] (c : ℝ) :
    (∫ _ω : Ω, c ∂P) = c := by
  rw [integral_const]
  simp
-- END SOURCE ch18_007

-- BEGIN SOURCE ch18_008
open MeasureTheory

#check @MeasureTheory.Filtration
#check @MeasureTheory.Martingale
#check @MeasureTheory.condExp
#check @MeasureTheory.Martingale.condExp_ae_eq

-- 確率測度は有限なので、部分σ代数上の定数の条件付き期待値も元の定数。
theorem condExp_const_probability {Ω : Type*} [m₀ : MeasurableSpace Ω]
    (P : Measure Ω) [IsProbabilityMeasure P]
    (m : MeasurableSpace Ω) (hm : m ≤ m₀) (c : ℝ) :
    condExp m P (fun _ => c) = fun _ => c :=
  condExp_const hm c

-- 既にマルチンゲールであると仮定した過程の性質を取り出す。
-- この結論には IsProbabilityMeasure P を別途仮定する必要はない。
theorem martingale_condExp_property {Ω : Type*} [m₀ : MeasurableSpace Ω]
    (P : Measure Ω) {ι : Type*} [Preorder ι]
    (f : ι → Ω → ℝ) (ℱ : Filtration ι m₀) (hf : Martingale f ℱ P)
    (s t : ι) (hst : s ≤ t) :
    (condExp (ℱ s) P (f t)) =ᵐ[P] f s :=
  hf.condExp_ae_eq hst

theorem martingale_term_integrable {Ω : Type*} [m₀ : MeasurableSpace Ω]
    (P : Measure Ω) {ι : Type*} [Preorder ι]
    (f : ι → Ω → ℝ) (ℱ : Filtration ι m₀) (hf : Martingale f ℱ P) (t : ι) :
    Integrable (f t) P :=
  hf.integrable t
-- END SOURCE ch18_008

-- BEGIN SOURCE ch18_009
open MeasureTheory

#print IsProbabilityMeasure
#check @IsProbabilityMeasure.measure_univ
-- 単一フィールド measure_univ : μ Set.univ = 1 を持つPropの型クラス。
-- #print と #check は構造・型の確認であり、証明のゴールを閉じる操作ではない。
-- END SOURCE ch18_009

-- BEGIN SOURCE ch18_010
open MeasureTheory

theorem probability_univ_from_instance {Ω : Type*} [MeasurableSpace Ω]
    (P : Measure Ω) [IsProbabilityMeasure P] : P Set.univ = 1 :=
  IsProbabilityMeasure.measure_univ
-- END SOURCE ch18_010

-- BEGIN SOURCE ch18_011
open MeasureTheory

theorem expectation_one {Ω : Type*} [MeasurableSpace Ω]
    (P : Measure Ω) [IsProbabilityMeasure P] :
    (∫ _ω : Ω, (1 : ℝ) ∂P) = 1 := by
  simp
-- END SOURCE ch18_011

-- BEGIN SOURCE ch18_012
open MeasureTheory

theorem expectation_one_by_expansion {Ω : Type*} [MeasurableSpace Ω]
    (P : Measure Ω) [IsProbabilityMeasure P] :
    (∫ _ω : Ω, (1 : ℝ) ∂P) = 1 := by
  rw [integral_const, Measure.real, measure_univ, ENNReal.toReal_one, one_smul]
-- END SOURCE ch18_012

-- BEGIN SOURCE ch18_013
open MeasureTheory
open scoped ENNReal

-- 実数直線のLebesgue測度を使うL²空間。
#check (inferInstance : InnerProductSpace ℝ (Lp ℝ 2 (volume : Measure ℝ)))
#check (inferInstance : NormedAddCommGroup (Lp ℝ 2 (volume : Measure ℝ)))
#check (inferInstance : CompleteSpace (Lp ℝ 2 (volume : Measure ℝ)))
-- 内積と完備性を合わせて、Hilbert空間であることを確認する。
-- END SOURCE ch18_013

-- BEGIN SOURCE ch18_014
open MeasureTheory
open scoped ENNReal

#check @MeasureTheory.L2.inner_def
#check @MeasureTheory.Lp.norm_def

theorem real_l2_inner {α : Type*} [MeasurableSpace α] (μ : Measure α)
    (f g : Lp ℝ 2 μ) : inner ℝ f g = ∫ x, f x * g x ∂μ := by
  rw [L2.inner_def]
  congr 1
  funext x
  exact mul_comm (g x) (f x)

theorem real_l2_norm_sq {α : Type*} [MeasurableSpace α] (μ : Measure α)
    (f : Lp ℝ 2 μ) : ‖f‖ ^ 2 = ∫ x, (f x) ^ 2 ∂μ := by
  rw [← real_inner_self_eq_norm_sq, real_l2_inner]
  simp only [pow_two]

theorem complex_l2_inner {α : Type*} [MeasurableSpace α] (μ : Measure α)
    (f g : Lp ℂ 2 μ) :
    inner ℂ f g = ∫ x, star (f x) * g x ∂μ := by
  simpa only [RCLike.inner_apply, RCLike.star_def, mul_comm] using
    (L2.inner_def (𝕜 := ℂ) f g)
-- END SOURCE ch18_014

-- BEGIN SOURCE ch18_015
open MeasureTheory

-- 離散時間（ι = ℕ）の場合を、点ごとのa.e.等式の形で再掲する。
theorem nat_martingale_condExp {Ω : Type*} [m₀ : MeasurableSpace Ω]
    (P : Measure Ω) [IsProbabilityMeasure P]
    (ℱ : Filtration ℕ m₀) (f : ℕ → Ω → ℝ)
    (hf : Martingale f ℱ P) (s t : ℕ) (hst : s ≤ t) :
    ∀ᵐ ω ∂P, (condExp (ℱ s) P (f t)) ω = f s ω :=
  hf.condExp_ae_eq hst
-- END SOURCE ch18_015

end LeanBook.Ch18
