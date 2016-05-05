from analyze import AnalysisResult

def export_to_csv(sequence, path, mode = "w+"):
	with open(path, mode) as f:

		for element in sequence:
			f.writeline(element.to_csv())

def import_from_csv(file):
	with open(path, "+r") as f:
		yield AnalysisResult().from_csv(f.readline())
