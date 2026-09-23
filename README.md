# Trust Deed Compliance Checker

A Streamlit web app that checks whether a trust deed covers a set of regulatory requirements. It splits the deed into clauses, embeds each clause and each regulation with **LegalBERT**, and uses cosine similarity to find the closest matching clause for every regulation.

## How it works

```
Trust deed PDF ──► pdf_parser.py ──► clauses ──► embedder.py ──► clause embeddings ─┐
                                                                                     ├─► matcher.py ──► Covered / Partially Covered / Missing
Regulations (text) ─────────────────────────────► embedder.py ──► regulation embedding┘
```

1. **Parse** (`pdf_parser.py`): reads the uploaded PDF with PyMuPDF and splits the text into clauses on legal numbering patterns (`1.`, `1.1`, `(a)`, `CLAUSE 1.`). Fragments of 40 characters or fewer are dropped.
2. **Embed** (`embedder.py`): encodes text with [`nlpaueb/legal-bert-base-uncased`](https://huggingface.co/nlpaueb/legal-bert-base-uncased), mean-pooling the last hidden state into a 768-dimensional vector. Input is truncated to 512 tokens.
3. **Match** (`matcher.py`): computes cosine similarity between each regulation and every clause, then keeps the best match:

   | Best similarity score | Status            |
   | --------------------- | ----------------- |
   | ≥ 0.82                | Covered           |
   | ≥ 0.65                | Partially Covered |
   | < 0.65                | Missing           |

4. **Display** (`app.py`): shows one expandable result per regulation with its score and the best-matching clause.

`report.py` contains an `export_report()` helper that writes results to a PDF with fpdf2. It is not yet connected to the UI.

## Project structure

```
.
├── app.py              # Streamlit UI
├── pdf_parser.py       # PDF text extraction and clause splitting
├── embedder.py         # LegalBERT embeddings
├── matcher.py          # Cosine-similarity matching and status thresholds
├── report.py           # PDF report export (fpdf2)
├── statement.txt       # Sample regulation for testing
└── requirements.txt
```

## Getting started

**Requirements:** Python 3.10+. The first run downloads the LegalBERT model (about 440 MB) from Hugging Face.

```bash
git clone https://github.com/<your-username>/trust-deed-compliance-checker.git
cd trust-deed-compliance-checker

python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
```

The app opens at <http://localhost:8501>.

> **Windows note:** if you get `OSError: [WinError 10013]`, port 8501 falls inside a range Windows
> reserves for Hyper-V/WSL on your machine. Run the app on a free port instead:
>
> ```powershell
> streamlit run app.py --server.port 8900
> ```
>
> Do not put that port in a committed `.streamlit/config.toml`: Streamlit Community Cloud
> health-checks the app on 8501 and the deployment will fail. Keep it local (the folder is
> in `.gitignore`) or pass the flag each time.

## Deployment

The app is deployed on [Streamlit Community Cloud](https://streamlit.io/cloud): connect the
repository, set the main module to `app.py`, and let it install `requirements.txt`. Leave the
server port unset so the platform can use its default.

## Usage

1. Upload a trust deed PDF.
2. Paste the regulatory requirements into the text box, one per line. `statement.txt` has an example:
   > The deed must specify that the trustee is to make distribution resolutions to appoint income to beneficiaries prior to midnight 30 June of the relevant financial year.
3. Click **Run Compliance Check**.
4. Expand each result to see the similarity score and the best-matching clause.

## Limitations

- **Semantic similarity is not legal compliance.** A high score means a clause talks about a similar topic, not that it satisfies the requirement. Results need review by a qualified person.
- The thresholds (0.82 / 0.65) were set by hand and are not calibrated against a labelled dataset.
- Clause splitting is regex-based, so unusual numbering or scanned (image-only) PDFs may split poorly or yield no text.
- Clauses longer than 512 tokens are truncated before embedding.
- Only the single best-matching clause is reported per regulation.

## Tech stack

- [Streamlit](https://streamlit.io/): web UI
- [Hugging Face Transformers](https://huggingface.co/docs/transformers) + [PyTorch](https://pytorch.org/): LegalBERT
- [scikit-learn](https://scikit-learn.org/): cosine similarity
- [PyMuPDF](https://pymupdf.readthedocs.io/): PDF parsing
- [fpdf2](https://py-pdf.github.io/fpdf2/): PDF report generation

## Authors

- Prayush Shrestha

## Acknowledgements

LegalBERT: Chalkidis, I., Fergadiotis, M., Malakasiotis, P., Aletras, N., & Androutsopoulos, I. (2020). _LEGAL-BERT: The Muppets straight out of Law School._ Findings of EMNLP 2020.
