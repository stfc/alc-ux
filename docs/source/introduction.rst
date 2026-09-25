Introduction to AiiDA
=====================

What is AiiDA?
--------------

`AiiDA <https://www.aiida.net>`_ (Automated Interactive Infrastructure and
Database for Computational Science) is an open-source workflow management engine
for computational science. It runs, tracks, and stores calculations while
automatically preserving their full **provenance** — a complete, queryable
record of every input, output, calculation, and the connections between them.

At its core, AiiDA lets researchers describe complex, multi-step computations
once and then run them reliably and reproducibly, whether that means a single
calculation on a local machine or thousands of jobs dispatched to remote
high-performance computing (HPC) clusters. Every piece of data that enters or
leaves a calculation is captured as a node in a directed graph, so results can
always be traced back to exactly how they were produced.

Aims of AiiDA
-------------

AiiDA is built around four guiding principles, often summarised as **ADES** —
Automation, Data, Environment, and Sharing:

Automation
   Complex workflows spanning many calculations and codes can be encoded once
   and executed with minimal manual intervention. The engine handles job
   submission, data transfer, scheduling, and error recovery, making
   high-throughput studies of thousands of calculations practical.

Data
   All inputs, outputs, and the calculations connecting them are stored in a
   provenance graph. This makes the full history of a result explicit and allows
   the entire database to be searched and queried efficiently.

Environment
   By recording the complete provenance of every calculation, AiiDA makes
   results **reproducible** — the exact steps and data behind any output can be
   inspected and re-run, supporting the FAIR (Findable, Accessible,
   Interoperable, Reusable) principles for research data.

Sharing
   Provenance graphs, workflows, and results can be exported and shared with
   collaborators or the wider community, enabling others to reuse and build upon
   existing work.

How AiiDA is Used
-----------------

A typical AiiDA workflow involves a few key concepts:

- **Computers and codes** — AiiDA is told about the machines available to it
  (from ``localhost`` to remote HPC clusters reached over SSH) and the
  executables installed on them.
- **Plugins** — code-specific plugins know how to prepare the input files for a
  given program and parse its outputs back into structured AiiDA data nodes.
- **The daemon** — a long-running background process picks up submitted
  calculations and workflows, drives them through their steps, submits jobs to
  the appropriate computers, and records everything as it goes.
- **Querying results** — because every calculation and data node is stored in
  the provenance graph, results can be retrieved, compared, and analysed long
  after the original run.

Traditionally these features are accessed through AiiDA's Python API or
command-line interface, which offers great power and flexibility but assumes
familiarity with programming and with AiiDA's concepts.

`AiiDAlab <https://www.aiidalab.net>`_ builds on top of AiiDA to make these
capabilities available through a browser-based graphical interface, so that
users can configure resources, submit workflows, and inspect results without
writing code. The next page, :doc:`overview`, looks at how AiiDAlab and the
underlying AiiDA components fit together.
