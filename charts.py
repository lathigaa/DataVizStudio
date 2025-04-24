import matplotlib.pyplot as plt
import pandas as pd
from io import BytesIO

# Your style map
def get_style(style_choice):
    valid_styles = {
        'classic': 'classic',
        'modern': 'seaborn',
        'minimal': 'seaborn-white',
        'flat': 'ggplot'
    }
    return valid_styles.get(style_choice, 'classic')

# 🔹 1. Bar Chart
def generate_bar_chart(df, colors, style):
    plt.style.use(get_style(style))
    if df.shape[1] < 2:
        raise ValueError("Need at least 2 columns for a bar chart.")
    fig, ax = plt.subplots(figsize=(10, 6))
    df.iloc[:, :2].plot(kind='bar', ax=ax, color=colors)
    plt.tight_layout()
    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=100)
    buf.seek(0)
    plt.close(fig)
    return buf

# 🔹 2. ✅ Line Chart
def generate_line_chart(df, colors, style):
    plt.style.use(get_style(style))
    if df.shape[1] < 2:
        raise ValueError("Need at least 2 columns for a line chart.")
    fig, ax = plt.subplots(figsize=(10, 6))
    df.iloc[:, :2].plot(kind='line', ax=ax, color=colors)
    plt.tight_layout()
    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=100)
    buf.seek(0)
    plt.close(fig)
    return buf

def generate_pie_chart(df, colors, style):
    try:
        # Apply the selected style
        plt.style.use(get_style(style))

        # Data validation: check if DataFrame has at least one column for the pie chart
        if df.shape[1] < 1:
            raise ValueError("DataFrame must have at least one column for pie chart.")

        # Create the pie chart
        fig, ax = plt.subplots(figsize=(8, 8))

        # Assuming the first column contains categorical data for the pie chart
        df.iloc[:, 0].value_counts().plot(kind='pie', ax=ax, colors=colors, autopct='%1.1f%%', startangle=90)

        # Adjust layout to avoid clipping
        plt.tight_layout()

        # Save the chart to a buffer
        buf = BytesIO()
        plt.savefig(buf, format='png', dpi=100)
        buf.seek(0)
        plt.close(fig)

        return buf

    except Exception as e:
        plt.close('all')  # Clean up any figures
        raise  # Re-raise the exception

# 🔸 Mapping (must come AFTER function definitions)
CHART_FUNCTIONS = {
    'bar_chart': generate_bar_chart,
    'line_chart': generate_line_chart,
    'pie_chart': generate_pie_chart, 
}


def generate_chart(df, chart_type, colors='blue', style='classic'):
    if chart_type not in CHART_FUNCTIONS:
        raise ValueError(f"Chart type '{chart_type}' is not supported.")
    
    return CHART_FUNCTIONS[chart_type](df, colors, style)

    