from fpdf import FPDF

ROW_COUNT = 2
COLUMN_COUNT = 5


def make_pdf(list_of_imgs):
    pdf = FPDF(orientation='L')

    height = pdf.fh / ROW_COUNT
    width = pdf.fw / COLUMN_COUNT

    pdf.add_page()
    for i in range(ROW_COUNT):
        for j in range(COLUMN_COUNT):
            pdf.image('../results/diagrams/l_100_it_0.png', j * width, i * height,
                      height, width)

    pdf.output("yourfile3.pdf", "F")


make_pdf([])
