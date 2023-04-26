RESULT_FILES = qiskit-results.txt qutip-results.txt quest-results.txt

.PHONY: all
all: plot.svg

.PHONY: clean
clean:
	rm -f $(RESULT_FILES) plot.svg

instances.txt: generate_instances.py
	python3 $< > $@

qiskit-results.txt: instances.txt ../qiskit/circuit.py ../qiskit/benchmarks.py
	PYTHONPATH=../.. python3 ../qiskit/benchmarks.py \
	    instances.txt qiskit-results.txt --variables=28 \
	  || ( rm -f iqp_gap/benchmarks/qiskit-results.txt; false )

qutip-results.txt: instances.txt ../qutip/circuit.py ../qutip/benchmarks.py
	PYTHONPATH=../.. python3 ../qutip/benchmarks.py \
	    instances.txt qutip-results.txt --variables=21 \
	  || ( rm -f iqp_gap/benchmarks/qutip-results.txt; false )

quest-results.txt: instances.txt
	../quest/benchmark instances.txt quest-results.txt --variables=28 \
	  || ( rm -f iqp_gap/benchmarks/quest-results.txt; false )

plot.svg: benchmarks.py instances.txt $(RESULT_FILES)
	PYTHONPATH=../.. python3 benchmarks.py -o plot.svg instances.txt \
	  qiskit:qiskit-results.txt \
	  qutip:qutip-results.txt \
	  quest:quest-results.txt
