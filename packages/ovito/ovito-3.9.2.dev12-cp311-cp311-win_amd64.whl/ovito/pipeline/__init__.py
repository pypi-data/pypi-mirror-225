"""
This module contains classes that are part of OVITO's data pipeline system.

**Pipelines:**

  * :py:class:`Pipeline`
  * :py:class:`Modifier` (base class of all built-in modifiers)
  * :py:class:`ModifierInterface` (abstract base class for :ref:`user-defined modifiers <writing_custom_modifiers>`)

**Data sources:**

  * :py:class:`StaticSource`
  * :py:class:`FileSource`
  * :py:class:`PipelineSourceInterface` (abstract base class for user-defined pipeline sources)
  * :py:class:`PythonScriptSource` (encapsulates a :py:class:`PipelineSourceInterface` or :ref:`user-defined pipeline source function <manual:data_source.python_script>`)

"""

__all__ = ['Pipeline', 'Modifier', 'StaticSource', 'FileSource', 'PythonScriptSource', 'ModifierInterface', 'PipelineSourceInterface']