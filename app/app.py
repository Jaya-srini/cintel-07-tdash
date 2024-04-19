import seaborn as sns  # Importing Seaborn for data visualization
from faicons import icon_svg  # Importing icons for graphical representation

from shiny import reactive  # Importing reactive module from shiny
from shiny.express import input, render, ui  # Importing necessary modules from shiny
import palmerpenguins  # Importing dataset palmerpenguins

# Loading the penguins dataset
df = palmerpenguins.load_penguins()

# Setting page options for the dashboard
ui.page_opts(title="Penguins Dashboard", fillable=True)

# Creating sidebar with filter controls
with ui.sidebar(title="Filter Controls"):
    # Creating input slider for mass filter
    ui.input_slider("mass", "Select Mass (g)", 2000, 6000, 6000)
    # Creating input checkbox group for species filter
    ui.input_checkbox_group(
        "species",
        "Select Species",
        ["Adelie", "Gentoo", "Chinstrap"],
        selected=["Adelie", "Gentoo", "Chinstrap"],
    )
    ui.hr()  # Horizontal line
    ui.h6("Links")  # Heading
    # Links to GitHub repositories and PyShiny documentation
    ui.a(
        "GitHub Source",
        href="https://github.com/denisecase/cintel-07-tdash",
        target="_blank",
    )
    ui.a(
        "GitHub App",
        href="https://denisecase.github.io/cintel-07-tdash/",
        target="_blank",
    )
    ui.a(
        "GitHub Issues",
        href="https://github.com/denisecase/cintel-07-tdash/issues",
        target="_blank",
    )
    ui.a("PyShiny", href="https://shiny.posit.co/py/", target="_blank")
    ui.a(
        "Template: Basic Dashboard",
        href="https://shiny.posit.co/py/templates/dashboard/",
        target="_blank",
    )
    ui.a(
        "See also",
        href="https://github.com/denisecase/pyshiny-penguins-dashboard-express",
        target="_blank",
    )

# Creating layout with value boxes to display summary statistics
with ui.layout_column_wrap(fill=False):
    with ui.value_box(showcase=icon_svg("earlybirds")):
        "Total Number of Penguins"

        @render.text
        def count():
            return filtered_df().shape[0]

    with ui.value_box(showcase=icon_svg("ruler-horizontal")):
        "Average Bill Length"

        @render.text
        def bill_length():
            return f"{filtered_df()['bill_length_mm'].mean():.1f} mm"

    with ui.value_box(showcase=icon_svg("ruler-vertical")):
        "Average Bill Depth"

        @render.text
        def bill_depth():
            return f"{filtered_df()['bill_depth_mm'].mean():.1f} mm"

# Creating layout with cards for data visualization
with ui.layout_columns():
    with ui.card(full_screen=True):
        ui.card_header("Bill Length and Depth")

        # Rendering scatter plot for bill length and depth
        @render.plot
        def length_depth():
            return sns.scatterplot(
                data=filtered_df(),
                x="bill_length_mm",
                y="bill_depth_mm",
                hue="species",
            )

    with ui.card(full_screen=True):
        ui.card_header("Penguin Data")

        # Rendering data frame for summary statistics
        @render.data_frame
        def summary_statistics():
            cols = [
                "species",
                "island",
                "bill_length_mm",
                "bill_depth_mm",
                "body_mass_g",
            ]
            return render.DataGrid(filtered_df()[cols], filters=True)

# Defining a reactive calculation to filter the dataset based on input values
@reactive.calc
def filtered_df():
    filt_df = df[df["species"].isin(input.species())]
    filt_df = filt_df.loc[filt_df["body_mass_g"] < input.mass()]
    return filt_df
