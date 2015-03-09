OUTPUT_DIR=./out

all: $(OUTPUT_DIR)/main.pdf

clean: 
	rm $(OUTPUT_DIR)/*

$(OUTPUT_DIR)/main.pdf:
	mv $(OUTPUT_DIR)/*.aux $(OUTPUT_DIR)/*.log $(OUTPUT_DIR)/*.toc . 2>/dev/null || true
	pdflatex main.tex
	pdflatex main.tex
	mv *.aux *.log *.toc *.pdf $(OUTPUT_DIR)
