import webbrowser, os
from reportlab.pdfgen import canvas


def loadFiles():
    images_to_read = os.listdir("input/images")
    images = []

    text_to_read = os.listdir("input/text")
    text = []

    count = 0
    for file in images_to_read:
        images.append("input/images/"+file)

    for file in text_to_read:
        text.append("input/text/"+file)

    return images, text

def readText(num):
    with open("input/text/"+str(num)+".txt") as f:
        content = f.readlines()
        # you may also want to remove whitespace characters like `\n` at the end of each line
        content = [x.strip() for x in content]
        content = " ".join(str(x) for x in content)
    print(content)
    return content

Story = []
images, texts = loadFiles()
c = Canvas('foo.pdf', pagesize=landscape(letter))
frame1 = Frame(0.25*inch, 0.25*inch, 4*inch, 4*inch, showBoundary=1)

styles = getSampleStyleSheet()
s = "foo bar " * 1000
story = [Paragraph(s, styles['Normal'])]
story_inframe = KeepInFrame(4*inch, 8*inch, story)
frame1.addFromList([story_inframe], c)
# c = canvas.Canvas("hello.pdf")
for file in range(0, len(images)):
    for name in images:
        if int(name[13:name.index(".")]) == file:
            c.drawImage(images[file],100,750, width=300, preserveAspectRatio=True, mask='auto')

            c.drawString(100,750,str(readText(file)))
            c.showPage()
c.save()
webbrowser.open_new("file:///Users/allisonbolen/school/fall2018/cis452/projects/deadlock/hello.pdf")
