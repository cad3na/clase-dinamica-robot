TARGET=Practica1
OUTDIR=../PDF's/

all: pdf clean move

pdf:
	@/usr/local/bin/hr #Se necesita descargar el programa con 'brew install hr'
	@echo "Compilando con pdflatex, el archivo:" $(TARGET)
	@/usr/local/bin/hr
	@/usr/texbin/pdflatex -interaction=batchmode $(TARGET).tex
	@/usr/texbin/pdflatex -interaction=batchmode $(TARGET).tex

clean:
	@/usr/local/bin/hr
	@echo "Quitando archivos irrelevantes."
	@rm -rf *.aux *.log *.fdb_latexmk  *.synctex.gz

move:
	@/usr/local/bin/hr
	@echo "Moviendo el archivo a la carpeta de PDF's."
	@mv "$(TARGET).pdf" "$(OUTDIR)$(TARGET).pdf"
