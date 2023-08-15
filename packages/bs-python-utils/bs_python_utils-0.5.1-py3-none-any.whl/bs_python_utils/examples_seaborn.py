"""examples using my Seaborn functions"""

import seaborn as sns

from bs_python_utils.bs_seaborn import (
    bs_sns_bar_x_byf,
    bs_sns_bar_x_byfg,
    bs_sns_get_legend,
)

cars = sns.load_dataset("mpg")

g1 = bs_sns_bar_x_byf(
    cars,
    "horsepower",
    "cylinders",
    label_x="Horsepower",
    label_f="Number of cylinders",
    title="Mean HP by number of cylinders",
)

g2 = bs_sns_bar_x_byfg(
    cars,
    "horsepower",
    "cylinders",
    "origin",
    label_x="Horsepower",
    label_f="Number of cylinders",
    label_g="Origin",
    title="Mean HP by number of cylinders and origin",
)

# change labels in legend
l2 = bs_sns_get_legend(g2)
labels2 = ["USA", "Japan", "Europe"]
for t, lab in zip(l2.texts, labels2, strict=True):
    t.set_text(lab)
