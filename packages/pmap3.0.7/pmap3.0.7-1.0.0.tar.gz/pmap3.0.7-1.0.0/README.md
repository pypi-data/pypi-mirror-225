# ![RAPID Overview](../../RAPIDOverview.png)

`RAPID` is an all-in-one multiplex biomedical image analysis software package. It provides both object-based and
pixel-based deep-learning-based image analysis algorithms, as well as numerous downstream functionalities.

Through the object-based approach, `RAPID` provides instance segmentation models that allow users to identify each
individual cell in the image. It also includes several existing cell-phenotyping algorithms, including a novel algorithm
provided exclusively within `RAPID`.

`RAPID` also provides a pixel-based, object-independent approach for single-cell analysis. While the conventional
workflow requires instance segmentation prior to clustering the identified cells into distinct phenotypes, the `RAPID`
pixel-based method features a semantic segmentation algorithm that assigns each pixel to a phenotypic cluster, thus
eliminating the instance segmentation requirement. This is particularly advantageous for cell types and images that
are not easily segmentable. For instance, while existing segmentation algorithms are able to identify round, regularly-
shaped cells, they fail to identify irregularly-shaped cells. Additionally, while object-dependent analyses may perform
well on images acquired at high resolution, they experience a precipitous decline in performance with images of lower
resolution. However, these shortcomings are addressed by the `RAPID` pixel-based approach, which allows for
classification of highly irregularly shaped cells and performs robustly on images acquired at low resolution.

# ![Why RAPID](../../WhyRAPID.png)

`RAPID` includes downstream analysis algorithms that help users interpret both pixel-based and object-based results,
as well as conventional algorithms that are specific for object-based analysis.

Each of the capabilities provided by `RAPID` is available through both a command-line interface as well as an
interactive graphical user interface. You can learn more about `RAPID` and how to use it by reading the
[documentation](../html/index.html).
