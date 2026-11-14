import numpy as np
import pytest
from matro import minimize
from matro._newuoa import PythonNewuoa
from matro._newuoa.x87_math import backend
from matro._newuoa.x87_math import _reference_platform

def quad(x):
    return float((x[0]-1)**2 + 100*(x[1]+2)**2)

@pytest.mark.parametrize('mode', ['adaptive', 'sphere'])
@pytest.mark.parametrize('arithmetic', ['reference', 'portable'])
def test_quadratic_budget_journal(mode, arithmetic):
    if arithmetic == 'reference' and not _reference_platform():
        pytest.skip('Pinned reference backend is Windows x86-64 only')
    observed=[]
    result=minimize(quad, [3., 1.], mode=mode, math_backend=arithmetic,
                    callback=observed.append, maxfev=150)
    assert result.fun < 1e-12
    assert result.nfev == len(result.history) == len(observed) <= 150
    assert result.fun == min(r['f'] for r in result.history)
    assert np.isclose(np.linalg.det(result.metric), 1.)

@pytest.mark.skipif(not _reference_platform(), reason='Reference platform only')
def test_sphere_native_query_equivalence():
    result=minimize(quad, [3.,1.], mode='sphere', math_backend='reference', maxfev=120)
    with backend('reference'):
        native=PythonNewuoa().run(quad, [3.,1.], npt=6, maxfun=120)
    assert np.array_equal(np.array([r['x'] for r in result.history]), native['queries'])
    assert np.array_equal(np.array([r['f'] for r in result.history]), native['values'])

@pytest.mark.parametrize('budget', [1, 3, 6, 10])
def test_initialization_charged(budget):
    result=minimize(quad, [3.,1.], maxfev=budget)
    assert result.nfev <= budget
    assert result.nfev == len(result.history)
    assert result.status == 3 and not result.success

def test_callback_cannot_mutate_core():
    def mutate(record): record['x'][:] = 1e20
    a=minimize(quad, [3.,1.], callback=mutate)
    b=minimize(quad, [3.,1.])
    assert np.array_equal(a.x, b.x) and a.nfev == b.nfev

@pytest.mark.parametrize('options', [dict(maxfev=1.5), dict(maxfev=True),
    dict(initial_radius=0), dict(final_radius=2), dict(mode='invalid'),
    dict(math_backend='invalid')])
def test_invalid_options_do_not_query(options):
    def objective(x): raise AssertionError('should validate before querying')
    with pytest.raises(ValueError): minimize(objective, [1.,2.], **options)

def test_user_error_preserved():
    def objective(x): raise LookupError('objective failed')
    with pytest.raises(RuntimeError) as error: minimize(objective, [1.,2.])
    assert isinstance(error.value.__cause__, LookupError)
