"""CSV batch processing for sentiment analysis."""

import csv
import io
from typing import Optional

from app.services.sentiment import analyze_text, SentimentResult


class CSVProcessorError(Exception):
    """Custom exception for CSV processing failures."""
    pass


def _detect_text_column(headers: list[str]) -> Optional[str]:
    """
    Auto-detect the text column from CSV headers.

    Looks for common column names like 'text', 'content', 'review', 'comment', 'message'.
    """
    priority_names = ["text", "content", "review", "comment", "message", "body", "feedback", "description"]

    # Exact match (case-insensitive)
    for name in priority_names:
        for header in headers:
            if header.strip().lower() == name:
                return header

    # Partial match
    for name in priority_names:
        for header in headers:
            if name in header.strip().lower():
                return header

    return None


def process_csv(file_content: bytes, text_column: Optional[str] = None) -> list[dict]:
    """
    Process a CSV file and analyze sentiment for each row.

    Args:
        file_content: Raw bytes of the uploaded CSV file
        text_column: Optional column name containing text to analyze.
                     If None, auto-detects the column.

    Returns:
        List of dicts with original text and sentiment results

    Raises:
        CSVProcessorError: If the CSV cannot be parsed or no text column is found
    """
    try:
        # Decode CSV content
        try:
            content_str = file_content.decode("utf-8")
        except UnicodeDecodeError:
            content_str = file_content.decode("latin-1")

        reader = csv.DictReader(io.StringIO(content_str))

        if not reader.fieldnames:
            raise CSVProcessorError("CSV file has no headers")

        # Determine text column
        if text_column:
            if text_column not in reader.fieldnames:
                raise CSVProcessorError(
                    f"Column '{text_column}' not found. Available: {', '.join(reader.fieldnames)}"
                )
            col = text_column
        else:
            col = _detect_text_column(list(reader.fieldnames))
            if col is None:
                raise CSVProcessorError(
                    f"Could not auto-detect text column. Available columns: {', '.join(reader.fieldnames)}. "
                    f"Please specify the text column name."
                )

        # Process each row
        results = []
        max_rows = 500  # Limit to prevent abuse

        for i, row in enumerate(reader):
            if i >= max_rows:
                break

            text = row.get(col, "").strip()
            if not text:
                continue

            result = analyze_text(text)
            results.append({
                "row_number": i + 1,
                "text": text[:200],  # Truncate for storage
                "full_text": text,
                "polarity": result.polarity,
                "subjectivity": result.subjectivity,
                "vader_compound": result.vader_compound,
                "vader_positive": result.vader_positive,
                "vader_negative": result.vader_negative,
                "vader_neutral": result.vader_neutral,
                "sentiment_label": result.sentiment_label,
                "confidence": result.confidence,
            })

        if not results:
            raise CSVProcessorError("No valid text entries found in the CSV")

        return results

    except CSVProcessorError:
        raise
    except Exception as e:
        raise CSVProcessorError(f"Failed to process CSV: {str(e)}")
