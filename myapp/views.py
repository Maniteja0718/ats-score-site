from django.shortcuts import render
import PyPDF2
import docx

def extract_text_from_docx(file):
    doc = docx.Document(file)
    full_text = [para.text for para in doc.paragraphs]
    return "\n".join(full_text)

def home(request):
    score = None
    message = ""

    if request.method == "POST":
        resume_file = request.FILES["resume"]
        job_desc = request.POST["jobdesc"].lower()

        # Extract resume text
        file_text = ""

        if resume_file.name.endswith(".pdf"):
            pdf_reader = PyPDF2.PdfReader(resume_file)
            for page in pdf_reader.pages:
                file_text += page.extract_text()
        elif resume_file.name.endswith(".docx"):
            file_text = extract_text_from_docx(resume_file)
        else:
            message = "Unsupported file format. Please upload PDF or DOCX."
            return render(request, "myapp/home.html", {"message": message})

        # Compare text
        resume_text = file_text.lower()
        job_words = set(job_desc.split())
        resume_words = set(resume_text.split())
        common_words = job_words.intersection(resume_words)

        score = round((len(common_words) / len(job_words)) * 100, 2)
        message = f"Found {len(common_words)} matching keywords out of {len(job_words)}."

    return render(request, "myapp/home.html", {"score": score, "message": message})
