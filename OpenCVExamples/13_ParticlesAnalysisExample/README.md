# Particle analysis example
This example shows we can use the Particle class to compute the different
particle parameters after labeling an image using the Connected Components
algorithm.

In this case, we use an already labeled image, that we load, and we extract
each of the pixels that belongs to each particle. Then, we compute its parameters,
and we filter them based on different criterias. Over the loop that checks
these criterias, we show 4 different ways to filter.

At the end, we show the result of this filtering.
# Application screenshot
# Filtering by area
![app screenshot](/OpenCVExamples/13_ParticlesAnalysisExample/images/AreaFiltering.png)
# Filtering by Elongation
![app screenshot](/OpenCVExamples/13_ParticlesAnalysisExample/images/ElongationFiltering.png)
# Filtering by Area and Elongation
![app screenshot](/OpenCVExamples/13_ParticlesAnalysisExample/images/ElongationAndAreaFiltering.png)
# Filtering by Area, Elongation and orientation
![app screenshot](/OpenCVExamples/13_ParticlesAnalysisExample/images/ElongatioAreaOrientationFiltering.png)