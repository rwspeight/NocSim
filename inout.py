from analyze import AnalysisResult

def export_to_csv(sequence, path, mode = "w+"):
	with open(path, mode) as f:

		lines = [e.to_csv(newline=True) for e in sequence]
		f.writelines(lines)

def import_from_csv(path):
	with open(path, "r+") as f:
		line = f.readline().strip()
		while line != "":
			yield AnalysisResult().from_csv(line)
			line = f.readline().strip()
