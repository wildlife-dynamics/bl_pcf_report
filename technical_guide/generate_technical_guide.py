"""
Generate the BL PCF Report Technical Guide as a PDF using ReportLab.
Run with: python3 generate_technical_guide.py
Output: bl_pcf_report_technical_guide.pdf
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak,
)
from datetime import date

OUTPUT_FILE = "bl_pcf_report_technical_guide.pdf"

# ── Colour palette ─────────────────────────────────────────────────────────────
GREEN_DARK  = colors.HexColor("#115631")
GREEN_MID   = colors.HexColor("#2d6a4f")
AMBER       = colors.HexColor("#e7a553")
SLATE       = colors.HexColor("#3d3d3d")
LIGHT_GREY  = colors.HexColor("#f5f5f5")
MID_GREY    = colors.HexColor("#cccccc")
WHITE       = colors.white

# ── Styles ─────────────────────────────────────────────────────────────────────
styles = getSampleStyleSheet()

def _style(name, parent="Normal", **kw):
    s = ParagraphStyle(name, parent=styles[parent], **kw)
    styles.add(s)
    return s

TITLE    = _style("DocTitle",    fontSize=26, leading=32, textColor=GREEN_DARK,
                  spaceAfter=6,  alignment=TA_CENTER, fontName="Helvetica-Bold")
SUBTITLE = _style("DocSubtitle", fontSize=13, leading=18, textColor=SLATE,
                  spaceAfter=4,  alignment=TA_CENTER)
META     = _style("Meta",        fontSize=9,  leading=13, textColor=colors.grey,
                  alignment=TA_CENTER, spaceAfter=2)
H1       = _style("H1", fontSize=15, leading=20, textColor=GREEN_DARK,
                  spaceBefore=18, spaceAfter=6, fontName="Helvetica-Bold")
H2       = _style("H2", fontSize=12, leading=16, textColor=GREEN_MID,
                  spaceBefore=12, spaceAfter=4, fontName="Helvetica-Bold")
H3       = _style("H3", fontSize=10, leading=14, textColor=SLATE,
                  spaceBefore=8,  spaceAfter=3, fontName="Helvetica-Bold")
BODY     = _style("Body", fontSize=9, leading=14, textColor=SLATE,
                  spaceAfter=6, alignment=TA_JUSTIFY)
BULLET   = _style("BulletItem", fontSize=9, leading=14, textColor=SLATE,
                  spaceAfter=3, leftIndent=14, firstLineIndent=-10, bulletIndent=4)
CODE     = _style("InlineCode", fontSize=8, leading=12, fontName="Courier",
                  backColor=LIGHT_GREY, textColor=colors.HexColor("#c0392b"),
                  spaceAfter=4, leftIndent=10, rightIndent=10, borderPad=3)
NOTE     = _style("Note", fontSize=8.5, leading=13,
                  textColor=colors.HexColor("#555555"),
                  backColor=colors.HexColor("#fff8e1"),
                  leftIndent=10, rightIndent=10, spaceAfter=6, borderPad=4)


def hr():                return HRFlowable(width="100%", thickness=1, color=MID_GREY, spaceAfter=6)
def p(text, style=BODY): return Paragraph(text, style)
def h1(text):            return Paragraph(text, H1)
def h2(text):            return Paragraph(text, H2)
def h3(text):            return Paragraph(text, H3)
def sp(n=6):             return Spacer(1, n)
def bullet(text):        return Paragraph(f"• {text}", BULLET)
def note(text):          return Paragraph(f"<b>Note:</b> {text}", NOTE)

def c(text):
    return Paragraph(str(text), BODY)

def make_table(data, col_widths, header_row=True):
    wrapped = [[c(cell) if isinstance(cell, str) else cell for cell in row]
               for row in data]
    t = Table(wrapped, colWidths=col_widths, repeatRows=1 if header_row else 0)
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0 if header_row else -1), GREEN_DARK),
        ("TEXTCOLOR",     (0, 0), (-1, 0 if header_row else -1), WHITE),
        ("FONTNAME",      (0, 0), (-1, 0 if header_row else -1), "Helvetica-Bold"),
        ("FONTSIZE",      (0, 0), (-1, -1), 8),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1), [WHITE, LIGHT_GREY]),
        ("GRID",          (0, 0), (-1, -1), 0.4, MID_GREY),
        ("VALIGN",        (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING",    (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING",   (0, 0), (-1, -1), 5),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 5),
    ]))
    return t


def on_page(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.grey)
    canvas.drawCentredString(A4[0] / 2, 1.5 * cm,
                             f"BL PCF Report — Technical Guide  |  Page {doc.page}")
    canvas.restoreState()


# ── Document ───────────────────────────────────────────────────────────────────
doc = SimpleDocTemplate(
    OUTPUT_FILE,
    pagesize=A4,
    leftMargin=2*cm, rightMargin=2*cm,
    topMargin=2.5*cm, bottomMargin=2.5*cm,
)

W = A4[0] - 4*cm   # usable width

story = []

# ══════════════════════════════════════════════════════════════════════════════
# COVER
# ══════════════════════════════════════════════════════════════════════════════
story += [
    sp(60),
    p("BL PCF Report", TITLE),
    p("Technical Guide", SUBTITLE),
    sp(4),
    p("Predator Compensation Fund — Livestock Predation Incident Analysis", SUBTITLE),
    sp(4),
    p(f"Generated {date.today().strftime('%B %d, %Y')}", META),
    p("Workflow id: <b>bl_pcf_report</b>", META),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 1. OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("1. Overview"),
    hr(),
    p("The <b>bl_pcf_report</b> workflow ingests livestock predation events "
      "(event type <b>hwc_lvstprd</b>) from EarthRanger for the Amboseli "
      "ecosystem and produces a comprehensive Predator Compensation Fund (PCF) "
      "incident analysis report. The workflow covers three target ranches — "
      "<b>Eselengei</b>, <b>Mbirikani</b>, and <b>Kimana</b> — and restricts "
      "analysis to <b>valid claims</b> only."),
    sp(4),
    p("For each run the workflow delivers:"),
    bullet("10 charts — pie charts by predator/ranch/location/boma type, stacked "
           "bar charts by claim type and predator, time-of-day bar, multi-line "
           "and multi-bar time-series, and historic comparison charts per ranch"),
    bullet("3 maps — overall predation density grid, boma-attack density grid, "
           "and livestock species scatter map"),
    bullet("Summary tables — overall predation summary, per-ranch summaries, "
           "claim-type breakdown, predator breakdown, location analysis, and "
           "boma incident statistics"),
    bullet("A Word document report — all charts, maps, and tables assembled into "
           "the Big Life PCF report template"),
    sp(6),
    h2("Output summary"),
    make_table(
        [
            ["Output type", "Count", "Description"],
            ["Pie charts", "4", "Livestock killed and compensation value by predator, ranch, and attack location; boma type targeted"],
            ["Stacked bar charts", "3", "Livestock killed and claim count by Type of claim × Ranch; 100% stacked by predator × Ranch"],
            ["Time-of-day bar chart", "1", "Predation incidents by 4-hour time bin"],
            ["Multi-line time series", "3", "Killed over time by ranch, by attack location, and claim count over time by type"],
            ["Multi-bar time series", "1", "Animals killed over time per predator (2-column grid)"],
            ["Historic comparison charts", "3", "Per-ranch current vs. historic mean with 95% CI (one per ranch)"],
            ["Density grid maps", "2", "All predation incidents; boma attacks only"],
            ["Scatter map", "1", "Livestock species scatter map"],
            ["Summary tables (GeoParquet)", "6+", "Overall, per-ranch, claim type, predator, location, boma"],
            ["Word document", "1", "big_life_pcf_report.docx"],
        ],
        [3.5*cm, 2*cm, W - 5.5*cm],
    ),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 2. DEPENDENCIES
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("2. Dependencies"),
    hr(),
    h2("2.1  Python packages"),
    p("The workflow declares seven versioned packages from the Ecoscope "
      "prefix.dev channels:"),
    make_table(
        [
            ["Package", "Version", "Channel"],
            ["ecoscope-workflows-core",       "0.22.17.*", "ecoscope-workflows"],
            ["ecoscope-workflows-ext-ecoscope","0.22.17.*", "ecoscope-workflows"],
            ["ecoscope-workflows-ext-custom",  "0.0.39.*",  "ecoscope-workflows-custom"],
            ["ecoscope-workflows-ext-ste",     "0.0.17.*",  "ecoscope-workflows-custom"],
            ["ecoscope-workflows-ext-mnc",     "0.0.7.*",   "ecoscope-workflows-custom"],
            ["ecoscope-workflows-ext-mep",     "0.12.0.*",  "ecoscope-workflows-custom"],
            ["ecoscope-workflows-ext-big-life","0.0.9.*",   "ecoscope-workflows-custom"],
        ],
        [6.5*cm, 3*cm, W - 9.5*cm],
    ),
    sp(6),
    h2("2.2  External data — static Amboseli layers"),
    p("Three GeoPackage files are downloaded from Dropbox at run time and "
      "cached locally (overwrite_existing: false, 3 retries):"),
    make_table(
        [
            ["File", "Purpose"],
            ["amboseli_ranch_conservancies_layers.gpkg",
             "Land-use styling layer overlaid on all maps"],
            ["amboseli_group_ranch_boundaries_x_electric_fence.gpkg",
             "Ranch boundaries and electric fence overlay"],
            ["amboseli_group_ranch_boundaries.gpkg",
             "Conservancy boundary polygons (used for spatial context)"],
        ],
        [8*cm, W - 8*cm],
    ),
    sp(6),
    h2("2.3  Base map tiles"),
    p("Two ESRI tile layers are composited for every map:"),
    make_table(
        [
            ["Layer", "Opacity", "Role"],
            ["ESRI World Hillshade", "1.0", "Terrain relief base layer"],
            ["ESRI World Street Map", "0.15", "Faint street/label overlay"],
        ],
        [5*cm, 2*cm, W - 7*cm],
    ),
    sp(6),
    h2("2.4  EarthRanger connection"),
    p("A single EarthRanger connection (<b>set_er_connection</b>) is required. "
      "The client is reused to fetch events, look up the current user's name for "
      "report attribution, and retrieve the user's full name via "
      "<b>get_user_full_name</b>."),
    sp(6),
    h2("2.5  Grouper"),
    p("The workflow groups data by the <b>Ranch</b> column. This grouper drives "
      "per-ranch table splits and the ranch-level historic time-series charts."),
    sp(6),
    h2("2.6  Time frequency"),
    p("A user-selectable <b>time_frequency</b> parameter (via "
      "<b>select_time_frequency</b>) controls the temporal aggregation unit "
      "used by all multi-line and multi-bar time-series charts."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 3. DATA INGESTION AND PROCESSING
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("3. Data Ingestion and Processing"),
    hr(),
    h2("3.1  Event fetch"),
    p("Events of type <b>hwc_lvstprd</b> (livestock predation) are fetched from "
      "EarthRanger for the configured time range. Two parallel pipelines process "
      "the same event fetch result — one for the <b>current period</b> and one "
      "for the <b>previous period</b> — each passing through identical "
      "transformation steps."),
    sp(6),
    h2("3.2  Previous period"),
    p("The previous period is computed by <b>shift_previous_period</b> with "
      "<b>periods_back = 5</b>. This shifts the time window back by five periods "
      "relative to the current time range, enabling historic comparison in the "
      "ranch-level time-series charts."),
    sp(6),
    h2("3.3  Field normalisation"),
    p("Each pipeline applies the following transformation sequence:"),
    make_table(
        [
            ["Step", "Task", "Purpose"],
            ["1", "process_events_details",
             "Converts EarthRanger field IDs to display names "
             "(map_to_titles: true, ordered: true)"],
            ["2", "normalize_json_column",
             "Flattens the nested event details JSON column into flat columns"],
            ["3", "drop_column_prefix",
             "Removes redundant column name prefixes introduced by normalisation"],
            ["4", "map_columns",
             "Renames and retains only the required columns; drops 14 unused columns"],
        ],
        [1.5*cm, 4.5*cm, W - 6*cm],
    ),
    sp(6),
    h2("3.4  Filtering"),
    p("After normalisation two filters are applied in sequence:"),
    bullet("<b>Ranch filter</b> — retains only rows where Ranch is one of "
           "Eselengei, Mbirikani, or Kimana"),
    bullet("<b>Validity filter</b> — retains only rows where "
           '"Validity of claim" == "Valid"'),
    sp(6),
    h2("3.5  Missing value handling"),
    p("Two passes of <b>replace_missing_with_label</b> fill blank values with "
      "context-appropriate labels:"),
    make_table(
        [
            ["Pass", "Label applied", "Fields targeted"],
            ["1", "N/A",
             "Adults injured, Adults killed, Compensation value to owner, "
             "Young (<1yr) injured, Young (<1yr) killed, "
             "Number of livestock in boma, Number of livestock in the area"],
            ["2", "Unknown",
             "Animal responsible, Boma type, Crop raided, "
             "Livestock species, Ranch, Time of attack, "
             "Type of claim, Validity of claim, "
             "Where were the livestock when the attack happened"],
        ],
        [1.2*cm, 2.5*cm, W - 3.7*cm],
    ),
    sp(6),
    h2("3.6  Numeric conversion and derived columns"),
    p("Five fields are cast to integer via <b>convert_to_int</b>:"),
    bullet("Adults injured"),
    bullet("Adults killed"),
    bullet("Compensation value to owner"),
    bullet("Young (&lt;1yr) injured"),
    bullet("Young (&lt;1yr) killed"),
    sp(4),
    p("A derived column <b>Total animals killed</b> is then computed by "
      "<b>combine_columns</b> (agg_func: sum) as:"),
    p("<i>Total animals killed = Adults killed + Young (&lt;1yr) killed</i>", CODE),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 4. SUMMARY TABLES
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("4. Summary Tables"),
    hr(),
    h2("4.1  Overall predation summary"),
    p("Three overall crosstab tables are computed from the current-period events "
      "and combined into a single summary via <b>summarize_predation_table</b>:"),
    make_table(
        [
            ["Table id", "Rows", "Columns", "Values"],
            ["current_total_incidents", "Ranch", "—", "Count of events (predation incidents)"],
            ["current_total_killed",    "Ranch", "—", "Sum of Total animals killed"],
            ["current_total_compensation", "Ranch", "—", "Sum of Compensation value to owner"],
        ],
        [4*cm, 2*cm, 2*cm, W - 8*cm],
    ),
    sp(4),
    p("The equivalent three previous-period crosstabs are computed and combined "
      "via a second call to <b>summarize_predation_table</b>, enabling "
      "current vs. previous comparisons in the Word report."),
    sp(6),
    h2("4.2  Per-ranch summaries"),
    p("Events are split by Ranch using <b>mapvalues</b> (task: "
      "<b>split_by_ranch</b> and <b>split_previous_by_ranch</b>). For each "
      "ranch, three crosstabs (incidents, killed, compensation) are computed and "
      "combined via <b>summarize_predation_table</b>, then formatted by "
      "<b>format_ranch_summary</b>."),
    sp(6),
    h2("4.3  Additional breakdown tables"),
    make_table(
        [
            ["Table", "Dimensions", "Notes"],
            ["claim_type_killed",
             "Type of claim × Ranch",
             "Total animals killed crosstab"],
            ["predator_killed",
             "Animal responsible × Ranch",
             "Total animals killed crosstab"],
            ["location_attack",
             "Where were the livestock when the attack happened",
             "Count and percentage of incidents"],
            ["predation_by_predator_and_location",
             "Animal responsible × attack location",
             "Percentage format"],
            ["boma_incidents",
             "Boma type",
             "Count and percentage (Permanent vs. Temporary)"],
        ],
        [4.5*cm, 4*cm, W - 8.5*cm],
    ),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 5. COLOR MAPPING
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("5. Color Mapping"),
    hr(),
    p("Six color maps are built via <b>get_color_map</b> and applied to the "
      "events GeoDataFrame via <b>map_color_column_value</b>. Each map adds a "
      "dedicated color column used by all downstream charts and maps."),
    sp(6),
    h2("5.1  Animal responsible"),
    make_table(
        [
            ["Animal", "Hex color", "Animal", "Hex color"],
            ["Caracal",   "#fd7f6f", "Leopard",  "#ffee65"],
            ["Cheetah",   "#7eb0d5", "Lion",     "#beb9db"],
            ["Elephant",  "#b2e061", "Unknown",  "#cfcfc4"],
            ["Hyena",     "#bd7ebe", "Wild dog", "#4cc9b0"],
            ["Jackal",    "#ffb55a", "—",        "—"],
        ],
        [3.5*cm, 2.8*cm, 3.5*cm, 2.8*cm],
    ),
    sp(6),
    h2("5.2  Other color maps"),
    make_table(
        [
            ["Color map", "Key", "Hex color"],
            ["Boma type",         "Permanent",                      "#fd7f6f"],
            ["Boma type",         "Temporary",                      "#7eb0d5"],
            ["Livestock location","Inside Boma",                    "#fd7f6f"],
            ["Livestock location","Within 200m of Boma",            "#b2e061"],
            ["Livestock location","More than 200m from Boma",       "#7eb0d5"],
            ["Claim type",        "Bad Boma",                       "#beb9db"],
            ["Claim type",        "No Penalty",                     "#b2e061"],
            ["Claim type",        "Lost in the Bush",               "#7eb0d5"],
            ["Ranch",             "Eselengei",                      "#fd7f6f"],
            ["Ranch",             "Kimana",                         "#7eb0d5"],
            ["Ranch",             "Mbirikani",                      "#b2e061"],
            ["Livestock species", "Shoat",                          "#0000ff"],
            ["Livestock species", "Cow",                            "#8b0000"],
            ["Livestock species", "Donkey",                         "#ffff00"],
        ],
        [4*cm, 6*cm, W - 10*cm],
    ),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 6. CHARTS
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("6. Charts"),
    hr(),
    h2("6.1  Pie charts"),
    p("All pie charts use <b>draw_pie_chart</b> with "
      "textinfo: \"percent+label+value\", font_size: 15, showlegend: true. "
      "Screenshots use device_scale_factor 2.0, wait_for_timeout 50 ms."),
    make_table(
        [
            ["Output file", "Value column", "Label / color column"],
            ["livestock_killed_by_predator_pie.html/.png",
             "Total animals killed",
             "Animal responsible / animal_responsible_colors"],
            ["compensation_value_by_predator_pie.html/.png",
             "Compensation value to owner",
             "Animal responsible / animal_responsible_colors"],
            ["compensation_value_by_ranch_pie.html/.png",
             "Compensation value to owner",
             "Ranch / ranch_colors"],
            ["livestock_attack_location_pie.html/.png",
             "Where were the livestock when the attack happened",
             "livestock_location_colors"],
            ["boma_type_targeted_pie.html/.png",
             "Total Incidents (from boma_pred_incidents table)",
             "Boma type / boma_type_colors"],
        ],
        [6*cm, 4*cm, W - 10*cm],
    ),
    sp(6),
    h2("6.2  Stacked bar charts"),
    p("Three stacked bar charts use <b>draw_custom_stacked_bar_chart</b> and "
      "<b>draw_custom_100_stacked_bar_chart</b>. All share plot_bgcolor: #f5f5f5, "
      "bargap: 0.1, font_color: #222222, x-axis: Ranch."),
    make_table(
        [
            ["Output file", "Y axis / agg", "Stack column", "Stack order"],
            ["livestock_killed_by_claim_type_bar.html/.png",
             "Total animals killed / sum",
             "Type of claim",
             "Lost in the Bush → No Penalty → Bad Boma"],
            ["claim_count_by_type_bar.html/.png",
             "id / count",
             "Type of claim",
             "Lost in the Bush → No Penalty → Bad Boma"],
            ["livestock_killed_by_predator_pct_bar.html/.png",
             "Total animals killed / sum (100%)",
             "Animal responsible",
             "Hyena → Jackal → Lion"],
        ],
        [5.5*cm, 3.5*cm, 3*cm, W - 12*cm],
    ),
    sp(6),
    h2("6.3  Time-of-day bar chart"),
    p("Built with <b>draw_custom_bar_chart</b>. Incidents are counted per time "
      "bin in fixed order, with agg_func: count and show_label: true. "
      "plot_bgcolor: #f5f5f5, showlegend: false."),
    make_table(
        [
            ["Time bin", "Hours covered"],
            ["Morning",   "06:00 – 11:59"],
            ["Afternoon", "12:00 – 16:59"],
            ["Evening",   "17:00 – 19:59"],
            ["Night",     "20:00 – 05:59"],
        ],
        [4*cm, W - 4*cm],
    ),
    p("Output: <b>predation_incidents_by_time_of_day_bar.html/.png</b>"),
    sp(6),
    h2("6.4  Multi-line time-series charts"),
    p("Three charts use <b>draw_custom_multi_line_time_series</b>. All use "
      "time_frequency from the user-selectable parameter, hovermode: "
      "\"x unified\", tickangle: 45, plot_bgcolor: #f5f5f5."),
    make_table(
        [
            ["Output file", "Group column", "Y / agg", "Fill", "Group order"],
            ["livestock_killed_over_time_by_ranch_chart.html/.png",
             "Ranch", "Total animals killed / sum", "No",
             "Eselengei → Mbirikani → Kimana"],
            ["livestock_killed_over_time_by_attack_location_chart.html/.png",
             "Attack location", "Total animals killed / sum", "Yes",
             "Inside Boma → Within 200m → More than 200m"],
            ["claim_count_over_time_by_type_chart.html/.png",
             "Type of claim", "id / count", "Yes",
             "Lost in the Bush → No Penalty → Bad Boma"],
        ],
        [5.5*cm, 3*cm, 3*cm, 1.5*cm, W - 13*cm],
    ),
    sp(6),
    h2("6.5  Multi-bar time-series chart"),
    p("Built with <b>draw_custom_multi_bar_time_series</b>. Animals killed are "
      "summed per predator species in a 2-column subplot grid "
      "(ncols: 2, row_height: 350, shared_yaxes: false). "
      "bar_color: <b>#6495ed</b> (cornflower blue). Screenshot dimensions: "
      "1280 × 2000 px."),
    p("Output: <b>livestock_killed_over_time_by_predator_mulit_bar_chart.html/.png</b>"),
    sp(6),
    h2("6.6  Historic comparison charts (per ranch)"),
    p("Built with <b>draw_historic_time_series_chart</b> via "
      "<b>mapvalues</b> — one chart per ranch pairing current and previous "
      "period data. Parameters:"),
    make_table(
        [
            ["Parameter", "Value"],
            ["Group column",          "Animal responsible"],
            ["Y axis",                "Total animals killed"],
            ["Aggregation",           "sum"],
            ["ncols / row_height",    "2 / 350 px"],
            ["Current line color",    "#6495ed (cornflower blue)"],
            ["Historical line color", "#ff7f0e (orange)"],
            ["CI method",             "seasonal (95%, multiplier 1.96)"],
            ["Screenshot size",       "1280 × 2000 px"],
        ],
        [5*cm, W - 5*cm],
    ),
    p("Outputs: <b>ranch_level_historic_time_series_chart_&lt;ranch&gt;.html/.png</b> "
      "(one file per ranch)"),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 7. MAPS
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("7. Maps"),
    hr(),
    p("All maps use the dual base-tile layer stack (Hillshade + Street Map) "
      "and overlay the Amboseli land-use and boundary layers. Map screenshots "
      "use device_scale_factor: 2.0 and wait_for_timeout: <b>40000 ms</b> to "
      "allow tiles to fully render."),
    sp(6),
    h2("7.1  Predation incident density map"),
    p("All valid predation events are converted to a 2000 m hexagonal density "
      "grid. The density column is classified into 5 equal-interval bins, "
      "which are then coloured with a yellow-to-dark-red ramp:"),
    make_table(
        [
            ["Bin rank", "Hex color", "Visual meaning"],
            ["1 (lowest)", "#FFF7BC", "Light yellow"],
            ["2",          "#FD8D3C", "Orange"],
            ["3",          "#F03B20", "Red-orange"],
            ["4",          "#BD0026", "Dark red"],
            ["5 (highest)","#99000D", "Near-black red"],
        ],
        [2.5*cm, 3*cm, W - 5.5*cm],
    ),
    p("Grid cells are rendered as filled GeoJSON polygons (opacity 0.55, "
      "black outline). Output: <b>predation_incident_density_map.html/.png</b>"),
    sp(6),
    h2("7.2  Boma predation density map"),
    p("Identical pipeline to the overall density map, but events are "
      "pre-filtered to only those where "
      "\"Where were the livestock when the attack happened\" == "
      "\"Inside Boma\". Same 2000 m grid, equal-interval k=5, and "
      "yellow-to-dark-red colormap."),
    p("Output: <b>boma_predation_density_map.html/.png</b>"),
    sp(6),
    h2("7.3  Livestock species scatter map"),
    p("Individual predation events are plotted as scatter points. Before "
      "rendering, two cleaning steps are applied:"),
    bullet("<b>exclude_geom_outliers</b> — removes geographic outliers "
           "with z_threshold: 3"),
    bullet("<b>drop_null_geometry</b> — removes rows with invalid or "
           "missing geometry"),
    sp(4),
    p("Layer style: get_fill_color and get_line_color both set to "
      "<b>livestock_species_colors</b>, get_radius: 4, opacity: 0.75. "
      "The legend is sorted ascending by Livestock species name."),
    make_table(
        [
            ["Livestock species", "Color"],
            ["Shoat",   "#0000ff (blue)"],
            ["Cow",     "#8b0000 (dark red)"],
            ["Donkey",  "#ffff00 (yellow)"],
        ],
        [4*cm, W - 4*cm],
    ),
    p("Output: <b>livestock_predation_event_map.html/.png</b>"),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 8. WORD REPORT
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("8. Word Report"),
    hr(),
    p("The final report is generated by <b>generate_pcf_report</b>, which "
      "populates the Big Life PCF Word template with all charts, maps, and "
      "summary tables produced during the workflow run."),
    sp(6),
    h2("8.1  Template"),
    p("The Word template <b>pcf_report_template.docx</b> is downloaded from "
      "Dropbox at run time (overwrite_existing: false, 3 retries) and stored "
      "in the results directory."),
    sp(6),
    h2("8.2  Report fields"),
    make_table(
        [
            ["Field",          "Source"],
            ["template_path",  "Path to pcf_report_template.docx"],
            ["output_dir",     "$ECOSCOPE_WORKFLOWS_RESULTS"],
            ["filename",       "big_life_pcf_report.docx"],
            ["time_period",    "Workflow time range (set_time_range)"],
            ["generated_by",   "Current EarthRanger user's full name (get_user_full_name)"],
            ["validate_images","true — verifies all image paths before populating"],
        ],
        [4*cm, W - 4*cm],
    ),
    sp(6),
    h2("8.3  Dashboard"),
    p("The workflow also calls <b>gather_dashboard</b> with an empty widgets "
      "list (widgets: []), which registers the run in the workflow dashboard "
      "without embedding any interactive widgets."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 9. OUTPUT FILES
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("9. Output Files"),
    hr(),
    p("All outputs are written to <b>$ECOSCOPE_WORKFLOWS_RESULTS</b>:"),
    make_table(
        [
            ["File", "Description"],
            # charts
            ["livestock_killed_by_predator_pie.html/.png",
             "Pie — Total animals killed by Animal responsible"],
            ["compensation_value_by_predator_pie.html/.png",
             "Pie — Compensation value by Animal responsible"],
            ["compensation_value_by_ranch_pie.html/.png",
             "Pie — Compensation value by Ranch"],
            ["livestock_attack_location_pie.html/.png",
             "Pie — Attack location distribution"],
            ["boma_type_targeted_pie.html/.png",
             "Pie — Boma type (Permanent vs Temporary)"],
            ["livestock_killed_by_claim_type_bar.html/.png",
             "Stacked bar — Livestock killed by Type of claim × Ranch"],
            ["claim_count_by_type_bar.html/.png",
             "Stacked bar — Claim count by Type of claim × Ranch"],
            ["livestock_killed_by_predator_pct_bar.html/.png",
             "100% stacked bar — Livestock killed % by Predator × Ranch"],
            ["predation_incidents_by_time_of_day_bar.html/.png",
             "Bar — Incidents by 4-bin time of day"],
            ["livestock_killed_over_time_by_ranch_chart.html/.png",
             "Multi-line — Killed over time by Ranch"],
            ["livestock_killed_over_time_by_attack_location_chart.html/.png",
             "Multi-line — Killed over time by attack location (filled)"],
            ["claim_count_over_time_by_type_chart.html/.png",
             "Multi-line — Claim count over time by Type (filled)"],
            ["livestock_killed_over_time_by_predator_mulit_bar_chart.html/.png",
             "Multi-bar (2-col, 1280×2000) — Killed per predator over time"],
            ["ranch_level_historic_time_series_chart_<ranch>.html/.png",
             "Historic comparison per ranch (one file per ranch, 1280×2000)"],
            # maps
            ["predation_incident_density_map.html/.png",
             "Density grid — all predation incidents (2000 m, equal-interval 5 bins)"],
            ["boma_predation_density_map.html/.png",
             "Density grid — boma attacks only (Inside Boma filter)"],
            ["livestock_predation_event_map.html/.png",
             "Scatter — livestock species coloured points"],
            # word report
            ["big_life_pcf_report.docx",
             "Final populated Word PCF report"],
            # static layers (cached)
            ["amboseli_ranch_conservancies_layers.gpkg",
             "Cached Amboseli land-use layer (from Dropbox)"],
            ["amboseli_group_ranch_boundaries_x_electric_fence.gpkg",
             "Cached ranch boundaries + electric fence (from Dropbox)"],
            ["amboseli_group_ranch_boundaries.gpkg",
             "Cached conservancy boundaries (from Dropbox)"],
            ["pcf_report_template.docx",
             "Cached Big Life PCF Word template (from Dropbox)"],
        ],
        [7.5*cm, W - 7.5*cm],
    ),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 10. WORKFLOW EXECUTION LOGIC
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("10. Workflow Execution Logic"),
    hr(),
    h2("10.1  Global skip conditions"),
    p("The top-level <b>task-instance-defaults</b> block applies two skip "
      "conditions to every task unless overridden:"),
    bullet("<b>any_is_empty_df</b> — skips the task if any upstream DataFrame "
           "dependency is empty"),
    bullet("<b>any_dependency_skipped</b> — skips the task if any upstream "
           "task was itself skipped"),
    p("This propagates gracefully: if no valid events are found for a ranch "
      "or time period, all downstream tasks for that branch are skipped "
      "without raising an error."),
    sp(6),
    h2("10.2  Dual pipeline (current + previous)"),
    p("Event fetch → normalisation → filtering → missing-value replacement → "
      "numeric conversion → column derivation runs twice in parallel: once for "
      "the current period and once for the previous period (shifted by 5 "
      "periods). Both pipelines produce independent GeoDataFrames that flow "
      "into the summary tables and historic comparison charts."),
    sp(6),
    h2("10.3  mapvalues fan-out"),
    p("The <b>mapvalues</b> directive is used to fan out per-ranch processing:"),
    bullet("<b>split_by_ranch</b> and <b>split_previous_by_ranch</b> — "
           "partition the current and previous GeoDataFrames by Ranch value"),
    bullet("<b>zip_groupbykey</b> — zips current and previous ranch partitions "
           "into paired tuples keyed by ranch name"),
    bullet("<b>draw_ranch_level_historic_chart</b> and "
           "<b>persist_ranch_historic_chart</b> — run once per ranch, producing "
           "a separate HTML/PNG file per ranch with the ranch name as filename "
           "suffix"),
    sp(6),
    h2("10.4  Screenshot timing"),
    make_table(
        [
            ["wait_for_timeout", "Applied to"],
            ["50 ms",    "All chart screenshots (fast static Plotly HTML)"],
            ["40000 ms", "All map screenshots (density and scatter maps "
                         "require full tile layer rendering)"],
        ],
        [3*cm, W - 3*cm],
    ),
    sp(6),
    h2("10.5  Geographic outlier removal"),
    p("Before the livestock species scatter map is rendered, "
      "<b>exclude_geom_outliers</b> removes points with a geometry z-score "
      "above 3 (i.e. more than 3 standard deviations from the centroid). "
      "A second pass via <b>drop_null_geometry</b> removes any remaining "
      "rows with null geometry to prevent rendering errors."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 11. SOFTWARE VERSIONS
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("11. Software Versions"),
    hr(),
    make_table(
        [
            ["Package", "Version pinned"],
            ["ecoscope-workflows-core",        "0.22.17.*"],
            ["ecoscope-workflows-ext-ecoscope","0.22.17.*"],
            ["ecoscope-workflows-ext-custom",  "0.0.39.*"],
            ["ecoscope-workflows-ext-ste",     "0.0.17.*"],
            ["ecoscope-workflows-ext-mnc",     "0.0.7.*"],
            ["ecoscope-workflows-ext-mep",     "0.12.0.*"],
            ["ecoscope-workflows-ext-big-life","0.0.9.*"],
        ],
        [8*cm, W - 8*cm],
    ),
    sp(6),
    note("All packages are resolved from the prefix.dev Ecoscope conda channels. "
         "The wildcard patch-version pin (.*) allows bug-fix releases to be "
         "picked up automatically while keeping minor and major versions locked."),
]

# ══════════════════════════════════════════════════════════════════════════════
# BUILD
# ══════════════════════════════════════════════════════════════════════════════
doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
print(f"Written → {OUTPUT_FILE}")
