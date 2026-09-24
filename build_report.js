const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, ImageRun, Table, TableRow,
  TableCell, WidthType, ShadingType, BorderStyle, AlignmentType, PageBreak,
  PositionalTab, PositionalTabAlignment, PositionalTabLeader, Header, Footer,
  PageNumber, NumberFormat, LevelFormat, convertInchesToTwip
} = require("docx");

const VIS = "/home/claude/project/visuals/";
const NAVY = "1E3A5F";
const ACCENT = "2563EB";
const ORANGE = "F97316";
const GREEN = "10B981";
const GREY = "6B7280";
const LIGHTBG = "F3F4F6";

function imgBuf(name) { return fs.readFileSync(VIS + name); }
function imgDims(name) {
  const dims = {
    "01_monthly_sales_profit_trend.png": [1517, 747],
    "02_category_sales_profit.png": [1657, 688],
    "03_subcategory_profit.png": [1377, 817],
    "04_region_performance.png": [1237, 747],
    "05_segment_analysis.png": [1608, 677],
    "06_discount_vs_margin.png": [1237, 747],
    "07_correlation_heatmap.png": [997, 817],
    "08_sales_forecast.png": [1517, 747],
    "09_feature_importance.png": [1237, 677],
    "10_actual_vs_predicted.png": [957, 887],
  };
  return dims[name];
}

function chartImage(name, widthIn = 6.3) {
  const [w, h] = imgDims(name);
  const width = widthIn * 96;
  const height = width * (h / w);
  return new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 150, after: 100 },
    children: [
      new ImageRun({ type: "png", data: imgBuf(name), transformation: { width, height } }),
    ],
  });
}

function caption(text) {
  return new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 260 },
    children: [new TextRun({ text, italics: true, size: 18, color: GREY })],
  });
}

function h1(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_1,
    spacing: { before: 420, after: 180 },
    border: { bottom: { color: ACCENT, space: 4, style: BorderStyle.SINGLE, size: 8 } },
    children: [new TextRun({ text, color: NAVY, bold: true })],
  });
}

function h2(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_2,
    spacing: { before: 280, after: 140 },
    children: [new TextRun({ text, color: ACCENT, bold: true })],
  });
}

function body(text, opts = {}) {
  return new Paragraph({
    spacing: { after: 160, line: 300 },
    children: [new TextRun({ text, size: 22, ...opts })],
  });
}

function bullet(text, opts = {}) {
  return new Paragraph({
    numbering: { reference: "bullet-list", level: 0 },
    spacing: { after: 90 },
    children: [new TextRun({ text, size: 22, ...opts })],
  });
}

function numbered(text, ref = "num-list") {
  return new Paragraph({
    numbering: { reference: ref, level: 0 },
    spacing: { after: 90 },
    children: [new TextRun({ text, size: 22 })],
  });
}

function kpiCell(label, value, color) {
  return new TableCell({
    width: { size: 25, type: WidthType.PERCENTAGE },
    shading: { type: ShadingType.CLEAR, fill: LIGHTBG },
    margins: { top: 160, bottom: 160, left: 120, right: 120 },
    children: [
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { after: 40 },
        children: [new TextRun({ text: value, bold: true, size: 30, color })],
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        children: [new TextRun({ text: label, size: 17, color: GREY })],
      }),
    ],
  });
}

const findings = fs.readFileSync("/home/claude/project/report/key_findings.txt", "utf8");
const fmap = {};
findings.split("\n").forEach((line) => {
  const idx = line.indexOf(":");
  if (idx > -1) fmap[line.slice(0, idx).trim()] = line.slice(idx + 1).trim();
});

// ---------- Title Page ----------
const titlePage = [
  new Paragraph({ spacing: { before: 1800 }, children: [] }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    children: [new TextRun({ text: "RETAIL SALES", bold: true, size: 30, color: ACCENT, characterSpacing: 20 })],
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 80, after: 60 },
    children: [new TextRun({ text: "Data Analysis & Predictive Modeling Report", bold: true, size: 56, color: NAVY })],
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 700 },
    border: { bottom: { color: ORANGE, space: 10, style: BorderStyle.SINGLE, size: 18 } },
    children: [new TextRun({ text: "An End-to-End Real-World Data Science Project — Retail Domain", size: 24, color: GREY, italics: true })],
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 900, after: 40 },
    children: [new TextRun({ text: "Prepared for: Applied Data Science Coursework", size: 22, color: NAVY })],
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 40 },
    children: [new TextRun({ text: "Dataset: retail_sales_dataset.csv  |  6,500 Orders  |  2024–2025", size: 22, color: NAVY })],
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 40 },
    children: [new TextRun({ text: `Report Date: ${new Date().toLocaleDateString("en-GB", { day: "numeric", month: "long", year: "numeric" })}`, size: 22, color: NAVY })],
  }),
  new Paragraph({ children: [new PageBreak()] }),
];

// ---------- Executive Summary ----------
const execSummary = [
  h1("Executive Summary"),
  body(
    `This report presents an end-to-end data science analysis of a two-year retail transaction dataset spanning ${fmap["Total Orders"]} orders, ${fmap["Unique Customers"]} unique customers, five regions, and three product categories. The objective was to uncover sales and profitability drivers, identify seasonal patterns, and build predictive models to support inventory, pricing, and marketing decisions.`
  ),
  body(
    `Across the analysis period, the business generated total sales of ${fmap["Total Sales"]} with a total profit of ${fmap["Total Profit"]}, representing an overall margin of ${fmap["Overall Margin"]}. The average order value was ${fmap["Average Order Value"]}. Methodology followed a standard applied data science pipeline: data quality checks, exploratory data analysis, statistical relationship testing, and machine learning-based prediction (Random Forest regression for profit, linear trend regression for sales forecasting).`
  ),
  new Table({
    width: { size: 100, type: WidthType.PERCENTAGE },
    borders: {
      top: { style: BorderStyle.NONE }, bottom: { style: BorderStyle.NONE },
      left: { style: BorderStyle.NONE }, right: { style: BorderStyle.NONE },
      insideHorizontal: { style: BorderStyle.NONE }, insideVertical: { style: BorderStyle.NONE },
    },
    rows: [
      new TableRow({ children: [
        kpiCell("Total Sales", fmap["Total Sales"], ACCENT),
        kpiCell("Total Profit", fmap["Total Profit"], GREEN),
        kpiCell("Overall Margin", fmap["Overall Margin"], ORANGE),
        kpiCell("Avg Order Value", fmap["Average Order Value"], NAVY),
      ]}),
    ],
  }),
  new Paragraph({ spacing: { after: 200 }, children: [] }),
];

// ---------- Methodology ----------
const methodology = [
  h1("1. Methodology"),
  body("This project followed a structured, reproducible data science workflow:"),
  numbered("Data Generation & Quality Assurance — validated for completeness, correct types, and logical ranges (6,500 orders, 0 missing values)."),
  numbered("Exploratory Data Analysis (EDA) — trend analysis, category/regional/segment breakdowns, and outlier review."),
  numbered("Statistical Relationship Analysis — correlation matrix and discount-vs-margin investigation."),
  numbered("Predictive Modeling — a linear trend model for short-term sales forecasting, and a Random Forest Regressor to predict order-level profit from operational features."),
  numbered("Model Evaluation — R\u00B2 and Mean Absolute Error (MAE) on a held-out 20% test set."),
  numbered("Business Recommendations — translated statistical findings into actionable retail strategy."),
  body("Tools used: Python (pandas, NumPy, scikit-learn, matplotlib, seaborn) within a Jupyter notebook environment.", { italics: true, color: GREY, size: 20 }),
];

// ---------- Section builder for charts ----------
function chartSection(num, title, imgName, widthIn, captionText, analysisText) {
  return [
    h1(`${num}. ${title}`),
    chartImage(imgName, widthIn),
    caption(captionText),
    body(analysisText),
  ];
}

const sections = [];

sections.push(...chartSection(
  2, "Monthly Sales & Profit Trend", "01_monthly_sales_profit_trend.png", 6.3,
  "Figure 1. Monthly sales (bars) and profit (line) across 2024–2025.",
  "Sales and profit both exhibit a pronounced seasonal spike in November of each year, consistent with holiday-driven retail demand, before returning to baseline in the following quarter. This pattern should directly inform inventory build-up, staffing, and cash-flow planning ahead of Q4."
));

sections.push(...chartSection(
  3, "Category Performance", "02_category_sales_profit.png", 6.3,
  "Figure 2. Total sales and profit by product category.",
  `${fmap["Top Category by Sales"]} generates the highest total sales value of the three categories. However, sales leadership does not always translate directly into margin leadership — the sub-category breakdown below explores this further.`
));

sections.push(...chartSection(
  4, "Sub-Category Profitability", "03_subcategory_profit.png", 6.0,
  "Figure 3. Profit contribution by sub-category (red indicates a net loss).",
  "Breaking category performance down further reveals meaningful variation in profitability at the sub-category level. Sub-categories with thin or negative margins are strong candidates for pricing review or targeted discount caps."
));

sections.push(...chartSection(
  5, "Regional Performance", "04_region_performance.png", 6.0,
  "Figure 4. Sales versus profit by region.",
  `The ${fmap["Top Region by Sales"]} region leads in total sales. Comparing sales and profit side-by-side highlights regions where high revenue does not proportionally convert to profit — a signal for reviewing regional operating costs, logistics, or discounting practices.`
));

sections.push(...chartSection(
  6, "Customer Segment Analysis", "05_segment_analysis.png", 6.3,
  "Figure 5. Share of sales and average order value by customer segment.",
  `The ${fmap["Best Segment by Sales"]} segment accounts for the largest share of total sales by order volume. Average order value differs meaningfully across segments, suggesting distinct purchasing behavior that could support segment-specific marketing and account strategies.`
));

sections.push(...chartSection(
  7, "Discount vs. Profit Margin", "06_discount_vs_margin.png", 6.0,
  "Figure 6. Relationship between discount level and resulting profit margin, by category.",
  "There is a clear negative relationship between discount depth and profit margin. Orders discounted beyond roughly 30% frequently approach or fall below breakeven, particularly within Technology and Furniture. This is one of the strongest and most actionable patterns in the dataset."
));

sections.push(...chartSection(
  8, "Correlation Analysis", "07_correlation_heatmap.png", 5.3,
  "Figure 7. Correlation matrix across key numeric metrics.",
  "Discount shows the strongest negative correlation with profit margin among the tested variables, reinforcing the discounting pattern observed above. Sales and Profit are positively correlated but far from perfectly so — reflecting the margin variability introduced by discounting and category mix."
));

// ---------- Predictive Modeling ----------
sections.push(h1("9. Predictive Modeling"));
sections.push(h2("9.1 Short-Term Sales Forecast"));
sections.push(chartImage("08_sales_forecast.png", 6.3));
sections.push(caption("Figure 8. Linear trend forecast of total monthly sales for the next 3 months."));
sections.push(body(`A linear trend regression projects continued gradual sales growth over the next quarter: ${fmap["Forecast next 3 months sales"]}. As a trend-only model, it does not capture seasonal effects (e.g., the November spike) — a seasonal model such as SARIMA or Prophet is recommended for operational forecasting.`));

sections.push(h2("9.2 Profit Prediction Model"));
sections.push(body("A Random Forest Regressor was trained to predict order-level profit from operational attributes (quantity, unit price, discount, category, region, segment, and shipping mode). The model was evaluated on a held-out 20% test set:"));

sections.push(new Table({
  width: { size: 60, type: WidthType.PERCENTAGE },
  alignment: AlignmentType.CENTER,
  columnWidths: [4000, 4000],
  rows: [
    new TableRow({ children: [
      new TableCell({ width: { size: 50, type: WidthType.PERCENTAGE }, shading: { type: ShadingType.CLEAR, fill: NAVY },
        children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "Metric", bold: true, color: "FFFFFF", size: 22 })] })] }),
      new TableCell({ width: { size: 50, type: WidthType.PERCENTAGE }, shading: { type: ShadingType.CLEAR, fill: NAVY },
        children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "Value", bold: true, color: "FFFFFF", size: 22 })] })] }),
    ]}),
    new TableRow({ children: [
      new TableCell({ shading: { type: ShadingType.CLEAR, fill: LIGHTBG }, children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "Mean Absolute Error (MAE)", size: 22 })] })] }),
      new TableCell({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: fmap["Profit Model MAE"], size: 22 })] })] }),
    ]}),
    new TableRow({ children: [
      new TableCell({ shading: { type: ShadingType.CLEAR, fill: LIGHTBG }, children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "R\u00B2 Score", size: 22 })] })] }),
      new TableCell({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: fmap["Profit Model R2"], size: 22 })] })] }),
    ]}),
  ],
}));
sections.push(new Paragraph({ spacing: { after: 200 }, children: [] }));

sections.push(chartImage("10_actual_vs_predicted.png", 5.2));
sections.push(caption("Figure 9. Actual vs. predicted profit on the test set."));
sections.push(chartImage("09_feature_importance.png", 6.0));
sections.push(caption("Figure 10. Relative feature importance for predicting order profit."));
sections.push(body("Discount and Unit Price emerge as the dominant predictors of order-level profit, quantitatively confirming the discount-erosion pattern identified in the exploratory analysis. Category and Region contribute secondary explanatory power."));

// ---------- Key Findings ----------
sections.push(h1("10. Key Findings"));
sections.push(numbered("Strong, repeatable seasonality — sales and profit peak sharply every November.", "num-list-2"));
sections.push(numbered(`${fmap["Top Category by Sales"]} leads in revenue, while margin efficiency varies meaningfully by sub-category.`, "num-list-2"));
sections.push(numbered("Discounting beyond ~30% materially erodes profitability, confirmed both visually and by the predictive model's feature importance ranking.", "num-list-2"));
sections.push(numbered(`${fmap["Top Region by Sales"]} leads regional sales, but regional profit efficiency is uneven and merits a cost review.`, "num-list-2"));
sections.push(numbered(`${fmap["Best Segment by Sales"]} drives the largest share of revenue by volume, with distinct average order values across segments.`, "num-list-2"));
sections.push(numbered(`The Random Forest profit model achieves an R\u00B2 of ${fmap["Profit Model R2"]} with an MAE of ${fmap["Profit Model MAE"]}, providing a usable baseline for profit estimation at the point of sale.`, "num-list-2"));

// ---------- Recommendations ----------
sections.push(h1("11. Business Recommendations"));
sections.push(bullet("Cap promotional discounts at approximately 20–25% on Technology and Furniture to protect margin."));
sections.push(bullet("Prioritize marketing investment in Office Supplies, which shows the strongest margin efficiency."));
sections.push(bullet("Build inventory and staffing plans ahead of the November demand peak identified in the trend analysis."));
sections.push(bullet("Conduct a regional cost review to close the profit gap between high-revenue and high-margin regions."));
sections.push(bullet("Adopt a seasonal forecasting model (SARIMA/Prophet) for operational planning beyond this baseline linear trend."));
sections.push(bullet("Integrate the profit prediction model into order-entry workflows to flag low-profit orders before confirmation."));

sections.push(h1("12. Conclusion"));
sections.push(body("This end-to-end analysis demonstrates how applied data science techniques — from exploratory analysis to machine learning-based prediction — can convert raw retail transaction data into concrete, actionable business strategy. The combination of clear seasonal patterns, a quantified discount-profitability relationship, and a working profit prediction model provides a solid foundation for data-driven decision-making across pricing, inventory, and regional operations."));

// ---------- Build Document ----------
const doc = new Document({
  numbering: {
    config: [
      { reference: "bullet-list", levels: [{ level: 0, format: LevelFormat.BULLET, text: "\u2022", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 440, hanging: 260 } } } }] },
      { reference: "num-list", levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 440, hanging: 260 } } } }] },
      { reference: "num-list-2", levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 440, hanging: 260 } } } }] },
    ],
  },
  sections: [
    {
      properties: {
        page: {
          size: { width: 12240, height: 15840 },
          margin: { top: 1080, bottom: 1080, left: 1080, right: 1080 },
        },
      },
      children: titlePage,
    },
    {
      properties: {
        page: {
          size: { width: 12240, height: 15840 },
          margin: { top: 1080, bottom: 1080, left: 1080, right: 1080 },
        },
      },
      headers: {
        default: new Header({
          children: [new Paragraph({
            alignment: AlignmentType.RIGHT,
            border: { bottom: { color: "D1D5DB", space: 4, style: BorderStyle.SINGLE, size: 4 } },
            children: [new TextRun({ text: "Retail Sales Analysis — Real-World Data Project", size: 16, color: GREY, italics: true })],
          })],
        }),
      },
      footers: {
        default: new Footer({
          children: [new Paragraph({
            alignment: AlignmentType.CENTER,
            children: [
              new TextRun({ text: "Page ", size: 16, color: GREY }),
              new TextRun({ children: [PageNumber.CURRENT], size: 16, color: GREY }),
              new TextRun({ text: " of ", size: 16, color: GREY }),
              new TextRun({ children: [PageNumber.TOTAL_PAGES], size: 16, color: GREY }),
            ],
          })],
        }),
      },
      children: [...execSummary, ...methodology, ...sections],
    },
  ],
});

Packer.toBuffer(doc).then((buf) => {
  fs.writeFileSync("/home/claude/project/report/Retail_Sales_Analysis_Report.docx", buf);
  console.log("Report written.");
});
