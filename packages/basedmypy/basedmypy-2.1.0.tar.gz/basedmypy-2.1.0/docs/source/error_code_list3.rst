.. _error-codes-based:

Error codes unique to basedmypy
===============================

.. _code-no-any-decorated:

Check that a decorated function isn't dynamic [no-any-decorated]
----------------------------------------------------------------

From :confval:`disallow_any_decorated`

.. _code-no-any-explicit:

Ban use of ``Any`` [no-any-explicit]
------------------------------------

From :confval:`disallow_any_explicit`

.. _code-no-any-expr:

Ban any expression that contains ``Any`` [no-any-expr]
------------------------------------------------------

From :confval:`disallow_any_expr`

.. _code-no-subclass-any:

Don't subclass ``Any`` [no-subclass-any]
----------------------------------------

From :confval:`disallow_subclassing_any`

.. _code-no-untyped-usage:

Don't use anything that contains ``Any`` [no-untyped-usage]
-----------------------------------------------------------

From :confval:`no_untyped_usage`

.. _code-unsafe-variance:

Check that type variables are used in accordance with their variance [unsafe-variance]
--------------------------------------------------------------------------------------

.. code-block:: python

    inT = TypeVar("inT", contravariant=True)
    outT = TypeVar("outT", covariant=True)

    class X(Generic[inT, outT]):
        def foo(self,
            t: outT  # This usage of this covariant type variable is unsafe as a return type.  [unsafe-variance]
        ) -> inT:  # This usage of this contravariant type variable is unsafe as a return type.  [unsafe-variance]
            pass

.. _code-reveal:
