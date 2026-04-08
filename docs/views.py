import os
import markdown
from django.conf import settings
from django.shortcuts import render

def hackathon_guidelines(request):
    file_path = os.path.join(settings.BASE_DIR, "HACKATHON_GUIDELINES.md")

    with open(file_path, "r", encoding="utf-8") as f:
        md_content = f.read()

    html_content = markdown.markdown(md_content, extensions=["fenced_code", "tables"])

    return render(request, "hackathon.html", {
        "content": html_content
    })