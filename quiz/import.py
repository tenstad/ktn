import json
from quiz.models import Section, Subsection, Question

with open('data.txt', 'r') as f:
    raw = f.read()

data = json.loads(raw)

for a in data:
    section = Section.objects.create(number=a)
    for b in data[a]:
        subsection = Subsection.objects.create(section=section, number=b)
        for c in data[a][b]:
            Question.objects.create(subsection=subsection, number=c, question=data[a][b][c]['q'], true=data[a][b][c]['a'])
