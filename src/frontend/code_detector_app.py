
import ast
import io
import keyword
import tokenize
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="AI Style Classifier",
    page_icon="💻",
    layout="wide"
)


def extract_features(code):
    """Extract structural and stylistic features from Python code."""

    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        raise ValueError(f"Invalid Python code: {e}")

    lines = [line for line in code.splitlines() if line.strip()]

    functions = [n for n in ast.walk(tree)
                 if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]

    classes = [n for n in ast.walk(tree)
                if isinstance(n, ast.ClassDef)]

    loops = [n for n in ast.walk(tree)
             if isinstance(n, (ast.For, ast.While))]

    conditions = [n for n in ast.walk(tree)
                  if isinstance(n, ast.If)]

    names = [n.id for n in ast.walk(tree)
             if isinstance(n, ast.Name)]

    comments = [
        tok.string for tok in tokenize.generate_tokens(
            io.StringIO(code).readline
        ) if tok.type == tokenize.COMMENT
    ]

    identifiers = [
        n.id for n in ast.walk(tree)
        if isinstance(n, ast.Name)
    ]

    function_lengths = [
        n.end_lineno - n.lineno + 1
        for n in functions if n.end_lineno
    ]

    def get_depth(node, depth=0):
        if not isinstance(node, ast.AST):
            return depth
        children = list(ast.iter_child_nodes(node))
        if not children:
            return depth
        return max(get_depth(child, depth + 1)
                   for child in children)

    return {
        "Lines of Code": len(lines),
        "Functions": len(functions),
        "Classes": len(classes),
        "Loops": len(loops),
        "Conditional Statements": len(conditions),
        "Comments": len(comments),
        "Average Identifier Length":
            round(sum(map(len, identifiers)) /
                  max(len(identifiers), 1), 2),
        "Average Function Length":
            round(sum(function_lengths) /
                  max(len(function_lengths), 1), 2),
        "AST Depth": get_depth(tree),
        "Unique Identifiers": len(set(names)),
        "Comment Ratio": round(
            len(comments) / max(len(lines), 1), 2
        )
    }


def assess_style(features):
    """
    Preliminary heuristic indicator.
    This is NOT a trained ML prediction.
    """

    score = 0
    indicators = []

    if features["Average Function Length"] > 20:
        score += 15
        indicators.append("Longer function structure")

    if features["Average Identifier Length"] > 8:
        score += 10
        indicators.append("Long identifier naming")

    if features["AST Depth"] > 7:
        score += 15
        indicators.append("Deeply nested code structure")

    if features["Comment Ratio"] < 0.03:
        score += 10
        indicators.append("Low comment frequency")

    if features["Functions"] >= 5:
        score += 10
        indicators.append("Highly modular structure")

    if features["Unique Identifiers"] > 15:
        score += 10
        indicators.append("Large identifier vocabulary")

    score = min(score, 100)

    return score, indicators


# ---------------- USER INTERFACE ----------------

st.title("💻 AI Style Classifier")

st.subheader(
    "Analyze Python source code for structural "
    "and stylistic patterns"
)

st.info(
    "This is a preliminary code-style analysis prototype. "
    "Its indicators do not establish whether AI was used."
)

uploaded_file = st.file_uploader(
    "Upload Python source code",
    type=["py"]
)

code = ""

if uploaded_file:
    code = uploaded_file.read().decode("utf-8")
    st.subheader("Code Preview")
    st.code(code, language="python")

if st.button("Analyze Code", type="primary"):

    if not code.strip():
        st.warning("Please upload a Python file.")

    else:
        try:
            with st.spinner("Analyzing code..."):

                features = extract_features(code)
                score, indicators = assess_style(features)

            st.success("Code analysis completed!")

            st.divider()

            st.subheader("Analysis Results")

            col1, col2 = st.columns(2)

            with col1:
                st.metric("AI-style indicator", f"{score}%")

            with col2:
                if score >= 50:
                    result = "Higher AI-style signals"
                else:
                    result = "Lower AI-style signals"

                st.metric("Assessment", result)

            st.progress(score / 100)

            st.caption(
                "This percentage is a heuristic indicator, "
                "NOT a calibrated probability of AI authorship."
            )

            st.subheader("Extracted Code Features")

            df = pd.DataFrame(
                features.items(),
                columns=["Feature", "Value"]
            )

            st.dataframe(df, use_container_width=True)

            st.subheader("Stylistic Indicators")

            if indicators:
                for item in indicators:
                    st.write("•", item)
            else:
                st.write(
                    "No predefined style indicators were triggered."
                )

            st.subheader("Interpretation")

            st.write(
                "The system evaluates code structure, naming, "
                "complexity and comment patterns. These patterns "
                "can occur in both human-written and AI-assisted code."
            )

        except (ValueError, UnicodeDecodeError, tokenize.TokenError) as e:
            st.error(str(e))

        except Exception as e:
            st.error(f"Analysis failed: {e}")

st.divider()

st.caption(
    "AI Style Classifier | Python Mini Project | "
    "Academic Integrity Analysis"
)
