from enum import Enum
from typing import Any, Optional, Union

from pydantic import ConfigDict, Field

from ..base import SchemaBaseModel
from .base import RootSchemaBaseModelV01


class ColorScale(str, Enum):
    INTERPOLATE_CUBEHELIX_DEFAULT = "interpolateCubehelixDefault"
    INTERPOLATE_RAINBOW = "interpolateRainbow"
    INTERPOLATE_WARM = "interpolateWarm"
    INTERPOLATE_COOL = "interpolateCool"
    INTERPOLATE_VIRIDIS = "interpolateViridis"
    INTERPOLATE_MAGMA = "interpolateMagma"
    INTERPOLATE_INFERNO = "interpolateInferno"
    INTERPOLATE_PLASMA = "interpolatePlasma"
    INTERPOLATE_BLUES = "interpolateBlues"
    INTERPOLATE_BR_BG = "interpolateBrBG"
    INTERPOLATE_BU_GN = "interpolateBuGn"
    INTERPOLATE_BU_PU = "interpolateBuPu"
    INTERPOLATE_CIVIDIS = "interpolateCividis"
    INTERPOLATE_GN_BU = "interpolateGnBu"
    INTERPOLATE_GREENS = "interpolateGreens"
    INTERPOLATE_GREYS = "interpolateGreys"
    INTERPOLATE_OR_RD = "interpolateOrRd"
    INTERPOLATE_ORANGES = "interpolateOranges"
    INTERPOLATE_PR_GN = "interpolatePRGn"
    INTERPOLATE_PI_YG = "interpolatePiYG"
    INTERPOLATE_PU_BU = "interpolatePuBu"
    INTERPOLATE_PU_BU_GN = "interpolatePuBuGn"
    INTERPOLATE_PU_OR = "interpolatePuOr"
    INTERPOLATE_PU_RD = "interpolatePuRd"
    INTERPOLATE_PURPLES = "interpolatePurples"
    INTERPOLATE_RD_BU = "interpolateRdBu"
    INTERPOLATE_RD_GY = "interpolateRdGy"
    INTERPOLATE_RD_PU = "interpolateRdPu"
    INTERPOLATE_RD_YL_BU = "interpolateRdYlBu"
    INTERPOLATE_RD_YL_GN = "interpolateRdYlGn"
    INTERPOLATE_REDS = "interpolateReds"
    INTERPOLATE_SINEBOW = "interpolateSinebow"
    INTERPOLATE_SPECTRAL = "interpolateSpectral"
    INTERPOLATE_TURBO = "interpolateTurbo"
    INTERPOLATE_YL_GN = "interpolateYlGn"
    INTERPOLATE_YL_GN_BU = "interpolateYlGnBu"
    INTERPOLATE_YL_OR_BR = "interpolateYlOrBr"
    INTERPOLATE_YL_OR_RD = "interpolateYlOrRd"


class CompositeMode(str, Enum):
    SOURCE_OVER = "source-over"
    LIGHTER = "lighter"
    DARKEN = "darken"
    SOURCE_ATOP = "source-atop"
    SOURCE_IN = "source-in"
    SOURCE_OUT = "source-out"
    DESTINATION_OVER = "destination-over"
    DESTINATION_ATOP = "destination-atop"
    DESTINATION_IN = "destination-in"
    DESTINATION_OUT = "destination-out"
    COPY = "copy"
    XOR = "xor"
    MULTIPLY = "multiply"
    SCREEN = "screen"
    OVERLAY = "overlay"
    COLOR_DODGE = "color-dodge"
    COLOR_BURN = "color-burn"
    HARD_LIGHT = "hard-light"
    SOFT_LIGHT = "soft-light"
    DIFFERENCE = "difference"
    EXCLUSION = "exclusion"
    HUE = "hue"
    SATURATION = "saturation"
    COLOR = "color"
    LUMINOSITY = "luminosity"


class Filter(str, Enum):
    COLOR = "Color"
    BRIGHTNESS = "Brightness"
    EXPOSURE = "Exposure"
    HUE = "Hue"
    CONTRAST = "Contrast"
    VIBRANCE = "Vibrance"
    NOISE = "Noise"
    SATURATION = "Saturation"
    GAMMA = "Gamma"
    INVERT = "Invert"
    GREYSCALE = "Greyscale"
    THRESHOLD = "Threshold"
    EROSION = "Erosion"
    DILATION = "Dilation"


class Shape(str, Enum):
    CROSS = "cross"
    DIAMOND = "diamond"
    SQUARE = "square"
    TRIANGLE_UP = "triangle up"
    STAR = "star"
    CLOBBER = "clobber"
    DISC = "disc"
    HBAR = "hbar"
    VBAR = "vbar"
    TAILED_ARROW = "tailed arrow"
    TRIANGLE_DOWN = "triangle down"
    RING = "ring"
    X = "x"
    ARROW = "arrow"


class Layer(SchemaBaseModel):
    name: str = Field(description="Name of the image layer")
    tile_source: str = Field(
        alias="tileSource",
        description="Relative path to an image file in a supported format.",
    )
    x: Optional[float] = Field(
        default=None, description="Left coordinate of the image in viewport coordinate."
    )
    y: Optional[float] = Field(
        default=None, description="Top coordinate of the image in viewport coordinate."
    )
    rotation: Optional[float] = Field(
        default=None, description="Rotation of the image in degrees."
    )
    flip: bool = Field(
        default=False,
        description="Flip the image horizontally.",
    )
    scale: Optional[float] = Field(default=None, description="Scale of the image.")


class LayerFilter(SchemaBaseModel):
    name: Filter = Field(description="Filter name.")
    value: str = Field(description="Filter parameter.")


class BoundingBox(SchemaBaseModel):
    x: float = Field(
        description="Left coordinate of the bounding box in viewport coordinate."
    )
    y: float = Field(
        description="Top coordinate of the bounding box in viewport coordinate."
    )
    width: float = Field(
        description="Width of the bounding box in viewport coordinate."
    )
    height: float = Field(
        description="Height of the bounding box in viewport coordinate."
    )


class Setting(SchemaBaseModel):
    module: str = Field(description="Module where the function or property lies.")
    function: str = Field(description="Function or property of the given module.")
    value: Union[int, float]


class ExpectedHeader(SchemaBaseModel):
    x: str = Field(alias="X", description="Name of CSV column to use as X-coordinate.")
    y: str = Field(alias="Y", description="Name of CSV column to use as Y-coordinate.")
    gb_col: Optional[str] = Field(
        default=None,
        description="Name of CSV column to use as key to group markers by.",
    )
    gb_name: Optional[str] = Field(
        default=None,
        description="Name of CSV column to display for groups instead of group key.",
    )
    cb_cmap: Optional[str] = Field(
        default=None,
        description="Name of D3 color scale to be used for color mapping.",
    )
    cb_col: Optional[str] = Field(
        default=None,
        description=(
            "Name of CSV column containing scalar values for color mapping or "
            "hexadecimal RGB colors in format '#ff0000'."
        ),
    )
    cb_gr_dict: str = Field(
        default="",
        description=(
            "JSON string specifying a custom dictionary for mapping group keys to "
            "group colors. Example: "
            "``\"{'key1': '#ff0000', 'key2': '#00ff00', 'key3': '#0000ff'}\"``."
        ),
    )
    scale_col: Optional[str] = Field(
        default=None,
        description=(
            "Name of CSV column containing scalar values for changing the size of "
            "markers."
        ),
    )
    scale_factor: float = Field(
        default=1.0,
        description=(
            "Numerical value for a fixed scale factor to be applied to markers."
        ),
    )
    coord_factor: float = Field(
        default=1.0,
        description=(
            "Numerical value for a fixed scale factor to be applied to marker "
            "coordinates."
        ),
    )
    pie_col: Optional[str] = Field(
        default=None,
        description=(
            "Name of CSV column containing data for pie chart sectors. TissUUmaps "
            "expects labels and numerical values for sectors to be separated by ':' "
            "characters in the CSV column data."
        ),
    )
    pie_dict: str = Field(
        default="",
        description=(
            "JSON string specifying a custom dictionary for mapping pie chart sector "
            "indices to colors. Example: "
            "``\"{0: '#ff0000', 1: '#00ff00', 2: '#0000ff'}\"``. If no dictionary is "
            "specified, TissUUmaps will use a default color palette instead."
        ),
    )
    shape_col: Optional[str] = Field(
        default=None,
        description=(
            "Name of CSV column containing a name or an index for marker shape."
        ),
    )
    shape_fixed: str = Field(
        default="cross",
        description="Name or index of a single fixed shape to be used for all markers.",
    )
    shape_gr_dict: str = Field(
        default="",
        description=(
            "JSON string specifying a custom dictionary for mapping group keys to "
            "group shapes. Example: "
            "``\"{'key1': 'square', 'key2': 'diamond', 'key3': 'triangle up'}\"``."
        ),
    )
    edges_col: Optional[str] = Field(
        default=None,
        description=(
            "Name of CSV column containing a name or an index for marker edges "
            "in Network Diagram mode."
        ),
    )
    collectionItem_col: Optional[str] = Field(
        default=None,
        description=(
            "Name of CSV column containing a name or an index for marker collection "
            "items in Collection mode."
        ),
    )
    collectionItem_fixed: str = Field(
        default="",
        description=(
            "Name or index of a single fixed collection item to be used for all "
            "markers in Collection mode."
        ),
    )
    opacity_col: Optional[str] = Field(
        default=None,
        description="Name of CSV column containing scalar values for opacities.",
    )
    opacity: float = Field(
        default=1.0,
        description=(
            "Numerical value for a fixed opacity factor to be applied to markers."
        ),
    )
    sortby_col: Optional[str] = Field(
        default=None,
        description=(
            "Name of CSV column containing scalar values for sorting markers."
        ),
    )
    z_order: float = Field(
        default=1.0,
        description=("Numerical value of z-order to be used for all markers."),
    )
    tooltip_fmt: str = Field(
        default="",
        description=(
            "Custom formatting string used for displaying metadata about a selected "
            "marker. See https://github.com/TissUUmaps/TissUUmaps/issues/2 for an "
            "overview of the grammer and keywords. If no string is specified, "
            "TissUUmaps will show default metadata depending on the context."
        ),
    )


class ExpectedRadios(SchemaBaseModel):
    cb_col: bool = Field(
        default=False,
        description="If markers should be colored by data in CSV column.",
    )
    cb_gr: bool = Field(
        default=True, description="If markers should be colored by group."
    )
    cb_gr_rand: bool = Field(
        default=False, description="If group color should be generated randomly."
    )
    cb_gr_dict: bool = Field(
        default=False,
        description="If group color should be read from custom dictionary.",
    )
    cb_gr_key: bool = Field(
        default=True, description="If group color should be generated from group key."
    )
    pie_check: bool = Field(
        default=False, description="If markers should be rendered as pie charts."
    )
    scale_check: bool = Field(
        default=False, description="If markers should be scaled by data in CSV column."
    )
    shape_col: bool = Field(
        default=False,
        description="If markers should get their shape from data in CSV column.",
    )
    shape_gr: bool = Field(
        default=True, description="If markers should get their shape from group."
    )
    shape_gr_rand: bool = Field(
        default=True, description="If group shape should be generated randomly."
    )
    shape_gr_dict: bool = Field(
        default=False,
        description="If group shape should be read from custom dictionary.",
    )
    shape_fixed: bool = Field(
        default=False,
        description="If a single fixed shape should be used for all markers.",
    )
    opacity_check: bool = Field(
        default=False,
        description="If markers should get their opacities from data in CSV column.",
    )
    no_outline: bool = Field(
        default=False,
        alias="_no_outline",
        description="If marker shapes should be rendered without outline.",
    )
    collectionItem_col: bool = Field(
        default=False,
        description=(
            "If markers should get their collection item from data in CSV column."
        ),
    )
    collectionItem_fixed: bool = Field(
        default=False,
        description=(
            "If a single fixed collection item should be used for all markers."
        ),
    )
    sortby_check: bool = Field(
        default=False,
        description="If markers should be sorted by data in CSV column.",
    )
    sortby_desc_check: bool = Field(
        default=False,
        description="If markers should be sorted in descending order.",
    )
    edges_check: bool = Field(
        default=False,
        description="If markers should be connected by edges in Network Diagram mode.",
    )


class DropdownOption(SchemaBaseModel):
    # We use extra="allow" here because we want to allow extra keys in the config
    # dictionary. This is because we want to allow the user to add custom keys to the
    # dropdown options, e.g. "expectedHeader.cb_col".
    model_config = ConfigDict(extra="allow")
    optionName: str = Field(description="Name displayed in the dropdown menu.")
    name: str = Field(
        description="Name of the tab to be loaded when the option is selected."
    )


class MarkerFile(SchemaBaseModel):
    title: str = Field(description="Name of marker button.")
    comment: Optional[str] = Field(
        default=None,
        description="Optional description text shown next to marker button.",
    )
    name: Optional[str] = Field(default=None, description="Name of marker tab.")
    auto_load: Union[bool, int] = Field(
        default=False,
        alias="autoLoad",
        description=(
            "If the CSV file for the marker dataset should be automatically loaded "
            "when the TMAP project is opened. If this is false, the user instead has "
            "to click on the marker button in the GUI to load the dataset. "
            "If this is an integer, the n-th marker dataset is automatically loaded."
        ),
    )
    hide_settings: bool = Field(
        default=False,
        alias="hideSettings",
        description="Hide markers' settings and add a toggle button instead.",
    )
    uid: Optional[str] = Field(
        default=None,
        description=(
            "A unique identifier used internally by TissUUmaps to reference the marker "
            "dataset."
        ),
    )
    expected_header: ExpectedHeader = Field(alias="expectedHeader")
    expected_radios: ExpectedRadios = Field(
        default_factory=lambda: ExpectedRadios(), alias="expectedRadios"
    )
    path: Union[str, list[str]] = Field(
        description=(
            "Relative file path to CSV file in which marker data is stored. If array "
            "of string, then a dropdown is created instead of a button."
        ),
    )
    dropdown_options: Optional[list[DropdownOption]] = Field(
        default=None,
        alias="dropdownOptions",
        description=(
            "List of dropdown options. Each option is a dictionary with the keys "
            "'title' and 'path'."
        ),
    )
    settings: list[Setting] = []
    from_button: Optional[int] = Field(
        default=None,
        alias="fromButton",
        description=(
            "If this is an integer, then the marker dataset is loaded from the n-th "
            "marker button."
        ),
    )


class RegionFile(SchemaBaseModel):
    title: str = Field(description="Name of region button.")
    comment: Optional[str] = Field(
        default=None,
        description="Optional description text shown next to region button.",
    )
    auto_load: bool = Field(
        default=False,
        alias="autoLoad",
        description=(
            "If the regions should be automatically loaded when the TMAP project is "
            "opened. If this is false, the user instead has to click on the region "
            "button in the GUI to load the regions."
        ),
    )
    path: Union[str, list[str]] = Field(
        description=(
            "Relative file path to GeoJSON file in which marker data is stored. If "
            "array of string, then a dropdown is created instead of a button."
        ),
    )
    settings: list[Setting] = []


class Project(RootSchemaBaseModelV01):
    filename: Optional[str] = Field(default=None, description="Name of the project.")
    link: Optional[str] = Field(
        default=None,
        description=(
            "Url to a publication or other external resource: a click on the filename "
            "will open this link."
        ),
    )
    layers: list[Layer] = []
    layer_opacities: dict[int, float] = Field(default={}, alias="layerOpacities")
    layer_visibilities: dict[int, bool] = Field(default={}, alias="layerVisibilities")
    layer_filters: dict[int, list[LayerFilter]] = Field(
        default={},
        alias="layerFilters",
        description="Image filters to be applied to pixels in image layers.",
    )
    filters: list[Filter] = Field(
        default=[Filter.SATURATION, Filter.BRIGHTNESS, Filter.CONTRAST],
        description=(
            "List of filters shown as active filters in the GUI under the Image layers "
            "tab."
        ),
    )
    composite_mode: CompositeMode = Field(
        default=CompositeMode.SOURCE_OVER,
        alias="compositeMode",
        description=(
            "Mode defining how image layers will be merged (composited) with each "
            "other. Valid string values are 'source-over' and 'lighter', which "
            "correspond to 'Channels' and 'Composite' in the GUI."
        ),
    )
    mpp: Optional[float] = Field(
        default=None,
        description=(
            "The image scale in Microns Per Pixels. If not null, then adds a scale bar "
            "to the viewer. Set to 0 to display the scale bar in pixels."
        ),
    )
    bounding_box: Optional[BoundingBox] = Field(
        default=None,
        alias="boundingBox",
        description=(
            "Bounding box used to set initial zoom and pan on the view when loading "
            "the project."
        ),
    )
    rotate: int = Field(
        default=0,
        description=(
            "Angle of rotation of the view in degrees. Only multiples of 90 degrees "
            "are supported."
        ),
    )
    marker_files: list[MarkerFile] = Field(default=[], alias="markerFiles")
    regions: dict[str, Any] = Field(default={}, description="GeoJSON object.")
    region_file: Optional[str] = Field(
        default=None,
        alias="regionFile",
        description=(
            "**[Deprecated]** GeoJSON region file loaded on project initialization. "
            "Use regionFiles instead."
        ),
    )
    region_files: list[RegionFile] = Field(default=[], alias="regionFiles")
    plugins: list[str] = Field(
        default=[], description="List of plugins to load with the project."
    )
    hide_tabs: bool = Field(
        default=False,
        alias="hideTabs",
        description=(
            "Hide tabs of markers dataset. Only use when you have a unique marker tab."
        ),
    )
    hide_channel_range: bool = Field(
        default=False,
        alias="hideChannelRange",
        description=(
            "Hide input range of channels. Only use when you have a unique image layer."
        ),
    )
    hide_navigator: bool = Field(
        default=False,
        alias="hideNavigator",
        description="Hide navigator of the viewer.",
    )
    collection_mode: bool = Field(
        default=False,
        alias="collectionMode",
        description=(
            "If true, then the viewer will be in collection mode, which puts "
            "all layers in a grid next to each other."
        ),
    )
    background_color: Optional[str] = Field(
        default=None,
        alias="backgroundColor",
        description="Background color of the viewer.",
    )
    settings: list[Setting] = []
