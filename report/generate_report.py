"""Generate the final CIS6005 WRIT1 academic report as a verified A4 PDF."""

from __future__ import annotations

import re
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import (
    BaseDocTemplate,
    Flowable,
    Frame,
    Image,
    KeepTogether,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.platypus.tableofcontents import TableOfContents

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "report"
PDF_PATH = OUT / "20302367_CIS6005_WRIT1.pdf"
WORD_COUNT_PATH = OUT / "word-count.txt"
REFERENCE_CHECK_PATH = OUT / "reference-check.md"
FIGURE_INVENTORY_PATH = OUT / "figure-inventory.md"

NAVY = colors.HexColor("#133A56")
TEAL = colors.HexColor("#087F8C")
CORAL = colors.HexColor("#D95D5D")
PALE = colors.HexColor("#EAF2F5")
MID = colors.HexColor("#526776")
LIGHT = colors.HexColor("#F5F7F8")
INK = colors.HexColor("#1C2730")

font_candidates = [
    Path("C:/Windows/Fonts/aptos.ttf"),
    Path("C:/Windows/Fonts/calibri.ttf"),
]
bold_candidates = [
    Path("C:/Windows/Fonts/aptos-bold.ttf"),
    Path("C:/Windows/Fonts/calibrib.ttf"),
]
BODY_FONT = "Helvetica"
BOLD_FONT = "Helvetica-Bold"
for normal, bold in zip(font_candidates, bold_candidates):
    if normal.exists() and bold.exists():
        pdfmetrics.registerFont(TTFont("ReportBody", str(normal)))
        pdfmetrics.registerFont(TTFont("ReportBold", str(bold)))
        BODY_FONT, BOLD_FONT = "ReportBody", "ReportBold"
        break

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="BodyAcademic", parent=styles["BodyText"], fontName=BODY_FONT, fontSize=10.4, leading=13.1, alignment=TA_JUSTIFY, textColor=INK, spaceAfter=6.5))
styles.add(ParagraphStyle(name="H1Academic", parent=styles["Heading1"], fontName=BOLD_FONT, fontSize=16, leading=19, textColor=NAVY, spaceBefore=10, spaceAfter=8, keepWithNext=True))
styles.add(ParagraphStyle(name="H2Academic", parent=styles["Heading2"], fontName=BOLD_FONT, fontSize=12.5, leading=15, textColor=TEAL, spaceBefore=8, spaceAfter=5, keepWithNext=True))
styles.add(ParagraphStyle(name="H3Academic", parent=styles["Heading3"], fontName=BOLD_FONT, fontSize=10.7, leading=13, textColor=NAVY, spaceBefore=6, spaceAfter=4, keepWithNext=True))
styles.add(ParagraphStyle(name="Caption", parent=styles["BodyText"], fontName=BODY_FONT, fontSize=8.3, leading=10.2, alignment=TA_CENTER, textColor=MID, spaceBefore=3, spaceAfter=8))
styles.add(ParagraphStyle(name="Small", parent=styles["BodyText"], fontName=BODY_FONT, fontSize=8.2, leading=10.2, textColor=MID, spaceAfter=4))
styles.add(ParagraphStyle(name="TableCell", parent=styles["BodyText"], fontName=BODY_FONT, fontSize=7.2, leading=8.7, textColor=INK))
styles.add(ParagraphStyle(name="TableHead", parent=styles["BodyText"], fontName=BOLD_FONT, fontSize=7.2, leading=8.6, textColor=colors.white, alignment=TA_LEFT))
styles.add(ParagraphStyle(name="Placeholder", parent=styles["BodyText"], fontName=BOLD_FONT, fontSize=9, leading=12, textColor=CORAL, alignment=TA_CENTER))


class AcademicDocTemplate(BaseDocTemplate):
    """A4 template with generated table of contents and PDF outline."""

    def __init__(self, filename: str):
        super().__init__(filename, pagesize=A4, rightMargin=18 * mm, leftMargin=20 * mm, topMargin=19 * mm, bottomMargin=18 * mm, title="Predicting Smartphone Addiction Using Computational Intelligence", author="Sathira Sri Sathsara")
        frame = Frame(self.leftMargin, self.bottomMargin, self.width, self.height, id="normal")
        self.addPageTemplates(PageTemplate(id="academic", frames=frame, onPage=self._decorate))

    def _decorate(self, canvas, doc):
        canvas.saveState()
        if doc.page > 1:
            canvas.setStrokeColor(colors.HexColor("#C8D4DA"))
            canvas.line(self.leftMargin, A4[1] - 13 * mm, A4[0] - self.rightMargin, A4[1] - 13 * mm)
            canvas.setFont(BODY_FONT, 7.5)
            canvas.setFillColor(MID)
            canvas.drawString(self.leftMargin, A4[1] - 10.5 * mm, "CIS6005 Computational Intelligence - WRIT1")
            canvas.drawRightString(A4[0] - self.rightMargin, A4[1] - 10.5 * mm, "Student ID 20302367")
            canvas.line(self.leftMargin, 12 * mm, A4[0] - self.rightMargin, 12 * mm)
            canvas.drawCentredString(A4[0] / 2, 8.5 * mm, str(doc.page))
        canvas.restoreState()

    def afterFlowable(self, flowable):
        if isinstance(flowable, Paragraph):
            style = flowable.style.name
            if style in {"H1Academic", "H2Academic", "H3Academic"}:
                level = {"H1Academic": 0, "H2Academic": 1, "H3Academic": 2}[style]
                text = flowable.getPlainText()
                key = f"heading-{self.seq.nextf('heading')}"
                self.canv.bookmarkPage(key)
                self.canv.addOutlineEntry(text, key, level=level, closed=False)
                self.notify("TOCEntry", (level, text, self.page, key))


class ArchitectureFlow(Flowable):
    """Compact vector architecture diagram."""

    def __init__(self, width=160 * mm, height=53 * mm):
        super().__init__(); self.width = width; self.height = height

    def draw(self):
        c = self.canv
        labels = ["Web form", "FastAPI +\nPydantic", "Feature\nengineering", "Saved\npipeline", "LightGBM", "Risk + local\nfactors"]
        gap = 4 * mm; box_w = (self.width - gap * 5) / 6; box_h = 20 * mm; y = 20 * mm
        for i, label in enumerate(labels):
            x = i * (box_w + gap)
            c.setFillColor(PALE if i not in {1, 4} else colors.HexColor("#D6ECEF"))
            c.setStrokeColor(TEAL); c.roundRect(x, y, box_w, box_h, 2 * mm, fill=1, stroke=1)
            c.setFillColor(INK); c.setFont(BOLD_FONT, 7)
            lines = label.split("\n")
            for j, line in enumerate(lines): c.drawCentredString(x + box_w / 2, y + box_h / 2 + (len(lines) - 1 - 2 * j) * 3, line)
            if i < 5:
                ax = x + box_w; ay = y + box_h / 2
                c.setStrokeColor(NAVY); c.line(ax + 1, ay, ax + gap - 1, ay)
                c.line(ax + gap - 3, ay + 2, ax + gap - 1, ay); c.line(ax + gap - 3, ay - 2, ax + gap - 1, ay)
        c.setFont(BODY_FONT, 7.2); c.setFillColor(MID)
        c.drawCentredString(self.width / 2, 12 * mm, "Validated inference path - the fitted preprocessing is reused, not recreated")


body_strings: list[str] = []
figure_titles: list[str] = []
table_titles: list[str] = []
story: list = []


def p(text: str, count: bool = True):
    story.append(Paragraph(text, styles["BodyAcademic"]))
    if count: body_strings.append(re.sub(r"<[^>]+>", " ", text))


def h1(text: str):
    story.append(Paragraph(text, styles["H1Academic"])); body_strings.append(text)


def h2(text: str):
    story.append(Paragraph(text, styles["H2Academic"])); body_strings.append(text)


def h3(text: str):
    story.append(Paragraph(text, styles["H3Academic"])); body_strings.append(text)


def table(title: str, headers: list[str], rows: list[list[str]], widths=None, count=True):
    table_titles.append(title)
    story.append(Paragraph(title, styles["Small"]))
    data = [[Paragraph(x, styles["TableHead"]) for x in headers]] + [[Paragraph(str(x), styles["TableCell"]) for x in row] for row in rows]
    t = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), NAVY), ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#AEBEC6")), ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4), ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3), ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT])]))
    story.extend([t, Spacer(1, 5)])
    if count:
        body_strings.extend([title, *headers]); body_strings.extend(str(x) for row in rows for x in row)


def figure(path: str, title: str, width=150 * mm, height=None):
    figure_titles.append(title)
    from PIL import Image as PILImage
    source = ROOT / path
    if height is None:
        with PILImage.open(source) as opened:
            height = width * opened.height / opened.width
    img = Image(str(source), width=width, height=height, kind="proportional")
    img.hAlign = "CENTER"
    story.extend([img, Paragraph(title + "<br/><i>Source: Author's analysis.</i>", styles["Caption"])])
    body_strings.append(title)


def placeholder(title: str, message: str):
    figure_titles.append(title)
    box = Table([[Paragraph(message, styles["Placeholder"])]] , colWidths=[155 * mm], rowHeights=[28 * mm])
    box.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 1.2, CORAL), ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#FFF2F2")), ("VALIGN", (0, 0), (-1, -1), "MIDDLE")]))
    story.append(KeepTogether([box, Paragraph(title + "<br/><i>Source: Student evidence required.</i>", styles["Caption"])]))
    body_strings.extend([title, message])


# Title page
story.extend([Spacer(1, 28 * mm), Paragraph("PREDICTING SMARTPHONE ADDICTION", ParagraphStyle(name="TitleMain", fontName=BOLD_FONT, fontSize=25, leading=29, alignment=TA_CENTER, textColor=NAVY)), Paragraph("USING COMPUTATIONAL INTELLIGENCE", ParagraphStyle(name="TitleSub", fontName=BOLD_FONT, fontSize=15, leading=19, alignment=TA_CENTER, textColor=TEAL)), Spacer(1, 16 * mm)])
title_data = [["Module", "CIS6005 Computational Intelligence"], ["Assessment", "WRIT1 - Deep Learning Plus AI Mini Project"], ["Student", "Sathira Sri Sathsara"], ["Student ID", "20302367"], ["Competition", "Predicting Smartphone Addiction - Playground Series S6E8"], ["Submission", "November 2026"]]
t = Table([[Paragraph(f"<b>{a}</b>", styles["BodyAcademic"]), Paragraph(b, styles["BodyAcademic"])] for a, b in title_data], colWidths=[35 * mm, 105 * mm], hAlign="CENTER")
t.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.8, NAVY), ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#B7C7CF")), ("BACKGROUND", (0, 0), (0, -1), PALE), ("VALIGN", (0, 0), (-1, -1), "TOP")]))
story.extend([t, Spacer(1, 16 * mm), Paragraph("Educational machine-learning prototype - not a medical or psychological diagnostic tool", ParagraphStyle(name="TitleNotice", fontName=BOLD_FONT, fontSize=10, leading=13, alignment=TA_CENTER, textColor=CORAL)), PageBreak()])

# TOC and inventories
story.append(Paragraph("Table of Contents", styles["H1Academic"]))
toc = TableOfContents(); toc.levelStyles = [ParagraphStyle(name="TOC0", fontName=BOLD_FONT, fontSize=10, leading=15, leftIndent=0, firstLineIndent=0, textColor=NAVY), ParagraphStyle(name="TOC1", fontName=BODY_FONT, fontSize=9, leading=13, leftIndent=12, firstLineIndent=0, textColor=INK), ParagraphStyle(name="TOC2", fontName=BODY_FONT, fontSize=8.5, leading=12, leftIndent=24, firstLineIndent=0, textColor=MID)]
story.extend([toc, PageBreak(), Paragraph("List of Figures", styles["H1Academic"])])
for item in ["Figure 1. Target class distribution", "Figure 2. Numerical correlation matrix", "Figure 3. Screen-time relationship with target", "Figure 4. Inference architecture", "Figure 5. LightGBM validation confusion matrix", "Figure 6. LightGBM feature importance", "Figure 7. Kaggle submission and leaderboard evidence", "Figure 8. Working application prediction interface"]:
    story.append(Paragraph(item, styles["BodyAcademic"]))
story.append(Spacer(1, 5)); story.append(Paragraph("List of Tables", styles["H1Academic"]))
for item in ["Table 1. Literature comparison", "Table 2. Dataset feature categories", "Table 3. EDA findings and model decisions", "Table 4. Model comparison", "Table 5. Cross-validation results", "Table 6. API endpoints", "Table 7. Limitations and improvements"]:
    story.append(Paragraph(item, styles["BodyAcademic"]))
story.append(PageBreak())

h1("1. Introduction")
p("Smartphone-use data combine behavioural intensity, context and self-reported wellbeing. This project develops a reproducible computational-intelligence (CI) workflow for the Kaggle competition <i>Predicting Smartphone Addiction</i>. Its aim is to compare classical, ensemble and neural models, select the strongest validated pipeline, and expose that model through a responsible web application. The objectives were to audit and preprocess the competition data; engineer defensible behavioural ratios; compare Logistic Regression, Random Forest, LightGBM and a multilayer perceptron (MLP); use stratified holdout and cross-validation; generate a Kaggle submission; serialize the complete pipeline; and implement a validated FastAPI and browser interface.")
p("The scope is prediction of the competition label <i>addicted_label</i>, not clinical assessment. The system is an educational machine-learning prototype and not a medical or psychological diagnostic tool. It minimises requested data, rejects the Kaggle identifier, stores no application records, presents probability as uncertainty, and labels explanations as model influences rather than causes.")

h1("2. Comprehensive Overview of Computational Intelligence (10 marks)")
p("Artificial intelligence is the broad ambition of producing computational behaviour associated with perception, reasoning or action. Traditional symbolic AI encodes explicit rules and representations: it can be auditable when domain rules are stable, but brittle where behaviour is noisy, incomplete and context dependent. Machine learning instead estimates functions from examples. Deep learning is a machine-learning family using layered representation learning, while CI emphasises adaptive, data-driven techniques that tolerate uncertainty and approximate rather than require a complete symbolic world model.")
p("CI is therefore appropriate to smartphone-use prediction because fixed rules such as 'more than x hours equals addiction' cannot capture interactions among screen time, social media, sleep, notifications and context. Logistic Regression offers a transparent linear baseline; Random Forest reduces variance through bagged trees (Breiman, 2001); LightGBM sequentially corrects errors with efficient gradient-boosted trees (Ke <i>et al.</i>, 2017); and the MLP tests learned nonlinear representations. Advantages are adaptability, scalable pattern discovery and probabilistic ranking. Disadvantages include dependence on representative labels, limited causal meaning, distribution shift and less transparent decisions. Unlike a rule engine, the fitted model generalises statistically but can reproduce dataset bias. Responsible CI therefore requires validation, uncertainty communication and human accountability, not performance alone.")

h1("3. Critical Literature Review (20 marks)")
h2("3.1 Construct, measurement and behavioural evidence")
p("Terminology is contested. Harris <i>et al.</i> (2020) reviewed 78 problematic-use scales and found uneven theoretical foundations, internal consistency and test-retest evidence. This weakens direct comparison between studies and supports cautious use of the competition label. Ratan <i>et al.</i> (2021) found consistent health associations across 27 adult studies, but every included study was cross-sectional; association cannot establish that smartphone use caused the outcome. Wacks and Weinstein (2021) similarly synthesised links with sleep, mood and cognition, while emphasising co-occurrence rather than a validated diagnostic pathway.")
p("Objective sensing can reduce recall error. Ryding and Kuss (2020) found passive measures centred on screen time and checking behaviour across 18 studies and argued that short monitoring periods can capture ecologically valid patterns. Lee and Kim (2021) used 29,712 respondents and 27 personal/log variables: Random Forest achieved 82.59% accuracy, exceeding their decision tree, while basic demographics contributed relatively little. By contrast, this project uses competition data with missing behavioural and demographic fields and optimises ROC AUC rather than accuracy. The comparison supports tree ensembles and detailed usage measures but does not make results directly equivalent.")
h2("3.2 Wellbeing, context and predictive modelling")
p("Duan <i>et al.</i> (2021) analysed 3,615 Chinese children and adolescents during COVID-19; a decision tree reached AUC 0.884, with internet use, smartphone hours, anxiety, injury fear and sex selected as factors. Nikolic <i>et al.</i> (2023) studied 761 Serbian medical students and reported associations with more than four hours' daily use, sleep quality, stress, anxiety and depression. Sela, Rozenboim and Ben-Gal (2022), using 215 participants, distinguished aware from concurrent or late-night use and found different quality-of-life associations. These studies disagree on the importance of demographics and operationalise outcomes differently, indicating that context matters and that a single threshold is unsafe.")
p("The repository includes screen time, social-media time, gaming, sleep, stress and work/academic impact, so the literature informed behavioural coverage and the sleep-deficit/ratio features. It also motivated privacy minimisation and non-diagnostic wording. It did not justify causal claims, clinical thresholds or treatment advice. From a methods perspective, benchmark evidence indicates that tree ensembles remain strong on medium-sized tabular problems with irregular decision boundaries (Grinsztajn, Oyallon and Varoquaux, 2022). Gorishniy <i>et al.</i> (2021) show that carefully designed tabular neural baselines can be competitive, so an MLP comparison is appropriate, but superiority should be demonstrated rather than assumed.")
table("Table 1. Literature comparison", ["Study", "Data/method", "Main evidence", "Limitation / design implication"], [["Harris et al. (2020)", "Systematic review; 78 scales", "Measurement quality varies", "Label is not a clinical ground truth"], ["Ryding and Kuss (2020)", "Systematic review; 18 passive-monitoring studies", "Screen/check patterns can be measured objectively", "Instrumentation and privacy challenges"], ["Lee and Kim (2021)", "29,712; DT, RF, XGBoost", "RF accuracy 82.59%", "Different data/metric; supports ensemble comparison"], ["Duan et al. (2021)", "3,615; regression and decision tree", "Decision-tree AUC 0.884", "Cross-sectional, pandemic-specific sample"], ["Ratan et al. (2021)", "Systematic review; 27 studies", "Consistent physical/mental-health associations", "All included studies cross-sectional"], ["Nikolic et al. (2023)", "761 medical students; regression", "Use, sleep and distress associated", "Restricted population; no causality"], ["Grinsztajn et al. (2022)", "Tabular benchmark", "Trees remain strong on typical tabular data", "Benchmark conclusion is task-dependent"]], widths=[30*mm, 38*mm, 48*mm, 55*mm])

h1("4. Dataset and Exploratory Data Analysis (10 marks)")
p("The competition training set contains 691,369 rows and 14 columns; test contains 296,302 rows and 13 columns. Training comprises ID, 12 raw predictors and the binary target. No duplicate rows or IDs were found. Class 1 contains 490,474 records (70.9424%) versus 200,895 class 0 records (29.0576%), making unstratified accuracy potentially misleading.")
table("Table 2. Dataset feature categories", ["Category", "Verified fields"], [["Numeric", "age; daily screen time; social media; gaming; work/study; sleep; notifications; app opens; weekend screen time"], ["Categorical", "gender; stress level; academic/work impact"], ["Engineered", "social-media ratio; gaming ratio; notifications per screen hour; absolute sleep deficit from 8 hours"], ["Excluded", "id (row identifier)"], ["Target", "addicted_label"]], widths=[30*mm, 140*mm])
figure("outputs/figures/target_distribution.png", "Figure 1. Target class distribution", width=118*mm)
p("Figure 1 confirms imbalance. Missingness affects every raw predictor: 4.18% for age up to 19.38% for social-media hours; 422,184 rows contain at least one missing value. Deleting incomplete rows would discard substantial information and may distort the sample. Numeric train/test standardized mean differences are very small (absolute range 0.000035-0.002226), although matching means do not rule out local shift.")
figure("outputs/figures/correlation_matrix.png", "Figure 2. Numerical correlation matrix", width=120*mm)
figure("outputs/figures/daily_screen_time_hours_by_target.png", "Figure 3. Daily screen time by target class", width=105*mm)
p("Figures 2 and 3 show correlated behavioural intensity and marked nonlinear class separation, particularly for daily screen time; social-media, gaming, work/study, app-opening and weekend-use plots show additional differences. This supports comparing boosting and bagging with linear and neural baselines, while avoiding the claim that any feature causes the label.")
table("Table 3. EDA findings and model decisions", ["EDA finding", "Observed evidence", "Implemented decision"], [["Class imbalance", "70.94% class 1", "Stratified split/CV; ROC AUC and balanced metrics"], ["Substantial missingness", "4.18%-19.38% by predictor", "Median numeric and mode categorical imputation inside pipeline"], ["Different scales", "Hours, counts and age", "Scale Logistic Regression/MLP; leave trees unscaled"], ["Categorical inputs", "Three object fields", "One-hot encoding; unknown categories ignored"], ["Nonlinear separation", "Target boxplots and correlations", "Compare RF/LightGBM with linear and MLP baselines"]], widths=[36*mm, 58*mm, 76*mm])

h1("5. System Architecture and ML Methods (10 marks)")
p("Training proceeds from Kaggle CSVs through EDA, deterministic feature engineering, pipeline preprocessing, a stratified holdout, four-model comparison, three-fold cross-validation of the top two models, full-data LightGBM fitting, joblib serialization and probability submission. Leakage is constrained because imputers, encoders and scalers are fitted inside each pipeline fold rather than before splitting.")
story.append(ArchitectureFlow()); story.append(Paragraph("Figure 4. Online inference architecture.<br/><i>Source: Author's design.</i>", styles["Caption"])); figure_titles.append("Figure 4. Online inference architecture"); body_strings.append("Figure 4. Online inference architecture")
p("At inference, the browser obtains the model schema, posts 12 fields, and FastAPI applies Pydantic bounds and category checks. A one-row DataFrame is copied into shared feature engineering, producing 16 ordered columns. The saved `ColumnTransformer` performs fitted preprocessing and LightGBM returns class probabilities. Application thresholds map class-1 probability to Low (<0.35), Moderate (0.35-<0.65) or High (>=0.65). Native LightGBM contribution values are grouped to readable factors; they are directional model influences, not causal percentages.")
p("Logistic Regression provides a regularised linear, scaled baseline but cannot naturally express complex interactions. Random Forest averages decorrelated trees and is robust but trained more slowly here. LightGBM grows boosted trees sequentially, efficiently concentrating capacity on residual errors and nonlinear interactions. The MLP uses two hidden layers to learn nonlinear mappings, but requires scaling and tuning and is less transparent. The application differentiates itself through probability output, a validated API, shared preprocessing, local factor disclosure, privacy wording and reproducible artifacts; these are implementation characteristics, not a claim of research novelty.")

h1("6. Model Evaluation, Implementation and Practical Demonstration (40 marks)")
h2("6.1 Environment and preprocessing")
p("The notebook was executed in Google Colab with Drive paths. Recorded training versions are Python 3.12.13, pandas 2.2.2, NumPy 2.0.2, scikit-learn 1.6.1 and joblib 1.5.3; the original LightGBM version was not recorded. The application pins FastAPI 0.115.9, Uvicorn 0.34.2, pydantic-settings 2.9.1 and LightGBM 4.7.0. Frontend technologies are HTML, CSS and JavaScript; pytest provides automated verification.")
p("After separating `addicted_label` and removing `id`, feature engineering creates social-media/screen-time, gaming/screen-time, notifications/screen-hour and absolute sleep-deficit features. Zero ratio denominators become missing. Numeric median and categorical most-frequent imputers, one-hot encoding and optional scaling live inside the pipeline. Scaling is used for Logistic Regression and MLP, not tree models. This design preserves identical fitted preprocessing when the joblib artifact is loaded for API inference.")
h2("6.2 Validation and model comparison")
p("The 80/20 stratified split produced 553,095 training and 138,274 validation rows. Three-fold shuffled stratified cross-validation with random state 42 was then applied to LightGBM and Random Forest, the two strongest holdout models. ROC AUC is appropriate because Kaggle requires probability ranking and the target is imbalanced; accuracy at one threshold can hide minority-class errors. Precision, recall, balanced accuracy, F1 and log loss provide complementary views.")
table("Table 4. Holdout model comparison", ["Model", "Acc.", "Bal. acc.", "Precision", "Recall", "F1", "ROC AUC", "Log loss", "Seconds"], [["LightGBM", ".8961", ".8691", ".9211", ".9335", ".9272", ".9598", ".2325", "47.06"], ["Random Forest", ".8473", ".8578", ".9456", ".8327", ".8856", ".9391", ".3004", "350.18"], ["MLP", ".8636", ".8192", ".8874", ".9250", ".9058", ".9374", ".2832", "104.61"], ["Logistic Reg.", ".8334", ".8355", ".9271", ".8305", ".8761", ".9147", ".3819", "303.96"]], widths=[27*mm, 16*mm, 18*mm, 19*mm, 16*mm, 16*mm, 18*mm, 18*mm, 18*mm])
table("Table 5. Three-fold ROC AUC", ["Model", "Fold 1", "Fold 2", "Fold 3", "Mean", "SD"], [["LightGBM", "0.959698", "0.960774", "0.960673", "0.960381", "0.000485"], ["Random Forest", "0.939074", "0.940262", "0.940061", "0.939799", "0.000519"]], widths=[35*mm, 27*mm, 27*mm, 27*mm, 27*mm, 27*mm])
p("LightGBM achieved the highest holdout ROC AUC, accuracy, balanced accuracy and F1, the lowest log loss, and a stable three-fold mean. It also trained substantially faster than Random Forest in this run. These results, plus compact tabular inference, justify its selection. The final model used 600 estimators, learning rate 0.04, 31 leaves, minimum child samples 30, subsample and column sample 0.85, L1 0.1 and L2 0.2, then fitted all 691,369 rows in 62.75 seconds.")
figure("outputs/figures/best_model_confusion_matrix.png", "Figure 5. LightGBM holdout confusion matrix", width=102*mm)
p("Figure 5 records 32,330 true negatives, 7,849 false positives, 6,523 false negatives and 91,572 true positives. False predictions matter because a high-risk display can worry a user, while a false negative can create false reassurance. The interface therefore avoids diagnosis and presents both probability and limitations.")
figure("outputs/figures/feature_importance.png", "Figure 6. LightGBM split importance", width=120*mm)
p("Notifications and app opens lead split importance, followed by daily and weekend screen time. Split counts are global model-use indicators, not causal effects. The API's local contribution section is separately labelled and limits output to five factors (Lundberg and Lee, 2017).")
h2("6.3 Kaggle result and serialization")
p("The generated `submission_lightgbm.csv` contains 296,302 test IDs and finite probabilities from 0.000713 to 0.999993. The provided verified public score is <b>0.96189 ROC AUC</b>. This is competition ranking performance, not clinical accuracy. Public rank, competition-date eligibility, selected final/private submission and private score are not evidenced in the repository and are not claimed.")
placeholder("Figure 7. Kaggle submission and leaderboard evidence", "[STUDENT TO INSERT VERIFIED EVIDENCE]\nPublic submission history, score 0.96189, competition dates, and selected final/private submission.")
p("The final pipeline is serialized with joblib alongside metadata, environment versions and model requirements. API startup verifies required files, parses metadata, checks package compatibility, loads only the trusted local artifact, confirms `predict`, `predict_proba`, classes `[0,1]` and exact feature order, then stores one singleton in application state. Exact scikit-learn/joblib compatibility is important because pickle-based artifacts depend on Python class structure.")
h2("6.4 API, frontend and tests")
table("Table 6. Implemented API endpoints", ["Method", "Endpoint", "Function"], [["GET", "/api/health", "Status, environment, version and timestamp"], ["GET", "/api/model/info", "Allow-listed model metadata"], ["GET", "/api/model/schema", "Twelve raw form fields and categories"], ["POST", "/api/predict", "Validation, probability, band, disclaimer and local factors"]], widths=[22*mm, 45*mm, 103*mm])
p("`api/main.py` configures lifespan, CORS, middleware, routes and static serving. `PredictionRequest` in `api/schemas.py` forbids extra fields, NaN, infinity, invalid categories and out-of-range values. `predict_addiction` builds the DataFrame, calls `add_domain_features`, checks order, calls `predict_proba`, resolves positive class 1 from schema, validates probability bounds, assigns the display band and requests a local explanation. Exceptions return safe JSON without paths or traces. Requests receive a UUID, size limit, structured log and defensive headers.")
p("The frontend fetches schema dynamically, renders numeric/select controls with labels and helper/error associations, prevents duplicate submission, calls `/api/predict`, and reveals an accessible SVG gauge only after success. It highlights one band, prints the model message/version/disclaimer, and displays local influences with a fallback. Responsive CSS, visible focus and reduced-motion support improve access. No login or application database is implemented.")
p("The final audit executed 39 pytest tests successfully. Coverage includes feature order and immutability; zero denominators; artifact and version failures; singleton load; health/static routes; missing, extra, categorical, numeric and non-finite validation; low/moderate/high mapping; real-model integration; probability bounds; safe 500 responses; local explanation structure/fallback; request size, IDs, headers and CORS. `compileall` also passed. Docker configuration is present, but its build is not claimed because Docker was unavailable in the verification environment.")
h2("6.5 Practical demonstration")
p("The demonstrable flow is: start Uvicorn; open the landing page; navigate to the prediction form; submit the 12 fields; observe Pydantic validation, feature engineering and singleton pipeline inference; review probability, band, explanation and disclaimer; then submit an invalid value to show HTTP 422 feedback. Swagger, `/api/health` and `/api/model/info` expose the operational contract without local paths. Programmatic HTTP checks passed for these routes and a real prediction, but screenshot evidence remains to be inserted.")
placeholder("Figure 8. Working application prediction interface", "[STUDENT TO INSERT VERIFIED EVIDENCE]\nLanding page, populated form, successful result, validation error, Swagger, health, model info and test output.")

h1("7. Critical Evaluation and Deep-Learning Suitability (10 marks)")
p("Strengths are the large competition sample, stable LightGBM cross-validation, full leakage-aware pipeline, exact inference feature order, safe model lifecycle, usable web/API interface and transparent limitations. The public ROC AUC is strong competition evidence. Nevertheless, the data may be synthetic and is not externally or clinically validated. Self-report and label measurement may embed error; Harris <i>et al.</i> (2020) show that problematic-use scales themselves vary. Demographic fairness was not evaluated, thresholds are arbitrary display choices, and probability calibration was not measured. Distribution shift, false positives, false negatives, privacy and automation bias remain material risks.")
p("Deep learning is not automatically preferable. The MLP underperformed LightGBM here (ROC AUC 0.9374 versus 0.9598), required scaling and trained more slowly. The problem has only 16 engineered tabular columns, where tree-based models efficiently learn thresholds and interactions; benchmark research similarly finds tree ensembles difficult to displace on typical tabular tasks (Grinsztajn, Oyallon and Varoquaux, 2022). Gorishniy <i>et al.</i> (2021) caution that strong neural designs and tuning can narrow the gap, so this result rejects this MLP configuration, not deep learning generally.")
p("Deep architectures become more plausible with longitudinal event sequences, app-level logs, text or sensor streams. Recurrent networks or temporal transformers could model changing behaviour, but require consent, larger storage, stronger privacy controls and temporal/external validation. Priorities are validation on real diverse cohorts; subgroup fairness/error analysis; probability calibration and threshold optimisation; model/drift monitoring; stronger causal-study design; and privacy-preserving or federated learning. SHAP-style local explanations should be user-tested rather than assumed beneficial. NIST's AI Risk Management Framework emphasises governance, measurement and ongoing management (NIST, 2023), aligning with consent, minimisation, transparency and accountable deployment rather than an unsupported claim of legal compliance.")
table("Table 7. Limitations and evidence-based improvements", ["Limitation", "Risk", "Improvement"], [["Competition/possibly synthetic data", "Weak real-world generalisation", "External longitudinal validation"], ["No fairness audit", "Unequal subgroup errors", "Report subgroup ROC AUC, calibration and error rates"], ["Uncalibrated display thresholds", "Misleading risk communication", "Calibration and decision-specific threshold study"], ["Cross-sectional behavioural inputs", "No temporal or causal inference", "Consent-based sequence modelling and causal designs"], ["No deployment monitoring", "Silent drift", "Input/performance monitoring and review triggers"], ["Sensitive behavioural data", "Privacy and stigma", "Minimisation, retention controls, federated learning research"]], widths=[47*mm, 52*mm, 71*mm])

h1("8. Conclusion")
p("This project compared linear, bagged-tree, boosted-tree and neural approaches for competition smartphone-addiction prediction. Leakage-aware preprocessing, four verified engineered features, stratified validation and multiple metrics supported selection of LightGBM. It achieved holdout ROC AUC 0.9598, three-fold mean 0.9604 and the provided public Kaggle score 0.96189, then powered a validated FastAPI and accessible web interface. The principal contribution is a reproducible route from notebook evidence to responsible probability delivery; the principal limitation is the absence of external clinical validation and complete Kaggle final/private evidence. Future work should prioritise real longitudinal data, fairness, calibration, privacy and drift monitoring before considering more complex temporal deep learning. The output remains educational, uncertain and non-diagnostic.")

# References (excluded from word count)
story.append(PageBreak()); story.append(Paragraph("References", styles["H1Academic"]))
references = [
    "Breiman, L. (2001) 'Random forests', <i>Machine Learning</i>, 45, pp. 5-32. doi: 10.1023/A:1010933404324.",
    "Duan, L. et al. (2021) 'Based on a decision tree model for exploring the risk factors of smartphone addiction among children and adolescents in China during the COVID-19 pandemic', <i>Frontiers in Psychiatry</i>, 12, 652356. doi: 10.3389/fpsyt.2021.652356.",
    "Gorishniy, Y., Rubachev, I., Khrulkov, V. and Babenko, A. (2021) 'Revisiting deep learning models for tabular data', <i>Advances in Neural Information Processing Systems</i>, 34. Available at: https://arxiv.org/abs/2106.11959 (Accessed: 4 August 2026).",
    "Grinsztajn, L., Oyallon, E. and Varoquaux, G. (2022) 'Why do tree-based models still outperform deep learning on typical tabular data?', <i>Advances in Neural Information Processing Systems</i>, 35. doi: 10.52202/068431-0037.",
    "Harris, B., Regan, T., Schueler, J. and Fields, S.A. (2020) 'Problematic mobile phone and smartphone use scales: a systematic review', <i>Frontiers in Psychology</i>, 11, 672. doi: 10.3389/fpsyg.2020.00672.",
    "Ke, G. et al. (2017) 'LightGBM: a highly efficient gradient boosting decision tree', <i>Advances in Neural Information Processing Systems</i>, 30.",
    "Lee, J. and Kim, W. (2021) 'Prediction of problematic smartphone use: a machine learning approach', <i>International Journal of Environmental Research and Public Health</i>, 18(12), 6458. doi: 10.3390/ijerph18126458.",
    "Lundberg, S.M. and Lee, S.-I. (2017) 'A unified approach to interpreting model predictions', <i>Advances in Neural Information Processing Systems</i>, 30. doi: 10.48550/arXiv.1705.07874.",
    "National Institute of Standards and Technology (2023) <i>Artificial Intelligence Risk Management Framework (AI RMF 1.0)</i>. NIST AI 100-1. doi: 10.6028/NIST.AI.100-1.",
    "Nikolic, A. et al. (2023) 'Smartphone addiction, sleep quality, depression, anxiety, and stress among medical students', <i>Frontiers in Public Health</i>, 11, 1252371. doi: 10.3389/fpubh.2023.1252371.",
    "Ratan, Z.A. et al. (2021) 'Smartphone addiction and associated health outcomes in adult populations: a systematic review', <i>International Journal of Environmental Research and Public Health</i>, 18(22), 12257. doi: 10.3390/ijerph182212257.",
    "Ryding, F.C. and Kuss, D.J. (2020) 'Passive objective measures in the assessment of problematic smartphone use: a systematic review', <i>Addictive Behaviors Reports</i>, 11, 100257. doi: 10.1016/j.abrep.2020.100257.",
    "Sela, A., Rozenboim, N. and Ben-Gal, H.C. (2022) 'Smartphone use behavior and quality of life: what is the role of awareness?', <i>PLOS ONE</i>, 17(3), e0260637. doi: 10.1371/journal.pone.0260637.",
    "Wacks, Y. and Weinstein, A.M. (2021) 'Excessive smartphone use is associated with health problems in adolescents and young adults', <i>Frontiers in Psychiatry</i>, 12, 669042. doi: 10.3389/fpsyt.2021.669042.",
]
for ref in references: story.append(Paragraph(ref, styles["Small"]))

# Appendices
story.append(PageBreak()); story.append(Paragraph("Appendix A. Evidence gaps requiring student action", styles["H1Academic"]))
for item in ["Competition Overview with verified start/end dates.", "Kaggle Evaluation page confirming ROC AUC.", "Public submission history and leaderboard screenshot linking score 0.96189.", "Selected final/private submission and private result when available.", "Application, API, Swagger and pytest screenshots.", "Moodle deadline and applicable AI-use disclosure requirement."]:
    story.append(Paragraph("- [STUDENT TO INSERT VERIFIED EVIDENCE] " + item, styles["BodyAcademic"]))
story.append(Paragraph("Appendix B. Verified API request fields", styles["H1Academic"]))
story.append(Paragraph("Required raw fields: age; daily_screen_time_hours; social_media_hours; gaming_hours; work_study_hours; sleep_hours; notifications_per_day; app_opens_per_day; weekend_screen_time; gender; stress_level; academic_work_impact. The ID field is excluded.", styles["BodyAcademic"]))
story.append(Paragraph("Appendix C. AI-tool disclosure placeholder", styles["H1Academic"]))
story.append(Paragraph("[STUDENT TO INSERT VERIFIED EVIDENCE] Add the university-approved disclosure of AI assistance after checking the current Moodle and institutional policy. The student must review every claim and citation and remain responsible for the submitted work.", styles["BodyAcademic"]))


def word_count(strings: list[str]) -> int:
    return len(re.findall(r"\b[\w]+(?:[-'][\w]+)*\b", " ".join(strings)))


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    count = word_count(body_strings)
    if count > 4000:
        raise RuntimeError(f"Assessed body word count exceeds limit: {count}")
    doc = AcademicDocTemplate(str(PDF_PATH))
    doc.multiBuild(story)
    WORD_COUNT_PATH.write_text(f"Assessed body word count: {count}\nMethod: headings, body text, table text, and figure captions counted; title pages, contents, references, and appendices excluded.\nMaximum: 4000 words.\n", encoding="utf-8")
    REFERENCE_CHECK_PATH.write_text("# Reference check\n\nAll cited works have matching Harvard-style reference entries. Titles, years and identifiers were checked against Europe PMC, OpenAlex, NIST or publisher/proceedings metadata on 4 August 2026.\n\n" + "\n".join(f"- {re.sub('<[^>]+>', '', ref)}" for ref in references), encoding="utf-8")
    FIGURE_INVENTORY_PATH.write_text("# Figure inventory\n\n" + "\n".join(f"- {x}" for x in figure_titles) + "\n\nFigures 7 and 8 are visible evidence placeholders and must be replaced by the student.\n", encoding="utf-8")
    print(f"PDF={PDF_PATH}")
    print(f"BODY_WORDS={count}")
    print(f"FIGURES={len(figure_titles)} TABLES={len(table_titles)} REFERENCES={len(references)}")


if __name__ == "__main__":
    main()
